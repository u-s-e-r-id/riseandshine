###############################################################################
# riseAndShine.py: a simple Wake-on-LAN / Wake-on-WAN utility.
###############################################################################
# Copyright (C) 2022 noDesk software.
# 
# Author: Edouard-Hugo Conte <edouard.conte@nodesk.fr>.
#
# This program is free software. You can redistribute it and/or modify it under
# the terms of the GNU General Public License v3.0
# published by the Free Software Foundation.
###############################################################################

from ipaddress import ip_address
import urllib.request
import textwrap
import struct
import socket
import json
import sys


def awake(target):
    # Check MAC address format and splits it into its component bytes
    if len(target["MAC"]) == 17:
        target_MAC_oct = target["MAC"].split(target["MAC"][2])
    elif len(target["MAC"]) == 12:
        target_MAC_oct = []
        for i in range(0, len(target["MAC"]), 2):
            target_MAC_oct.append(target["MAC"][i:i+2])
    else:
        print(textwrap.dedent(f'''
            Invalid MAC address for the machine "{target["NAME"]}" ({target["MAC"]}).
            The MAC address has {len(target["MAC"])} characters.
            It should have 17 characters with separators or 12 without, such as:
            01:02:03:AA:BB:CC (17 chars)
            or
            010203AABBCC      (12 chars)

            Check and correct the MAC address of "{target["NAME"]}" in the 'machines.js' file.

        '''))
        sys.exit()
 
    # Pack the MAC adress bytes with base 16
    try:
        target_MAC_hex = struct.pack('BBBBBB',
            int(target_MAC_oct[0], 16),
            int(target_MAC_oct[1], 16),
            int(target_MAC_oct[2], 16),
            int(target_MAC_oct[3], 16),
            int(target_MAC_oct[4], 16),
            int(target_MAC_oct[5], 16)
        )
    except ValueError:
        print(textwrap.dedent(f'''
            Invalid MAC address for the machine "{target["NAME"]}" ({target["MAC"]}).
            The address was probably provided with multiple different separators.
            The separators should all be the same (if any), such as:
            01:02:03:AA:BB:CC
            or
            010203AABBCC

            Check and correct the MAC address of "{target["NAME"]}" in the 'machines.js' file.

        '''))
        sys.exit()

    # Create the "magic paquet" following the standard created by AMD/HP
    # https://www.amd.com/system/files/TechDocs/20213.pdf
    payload = b'\xff' * 6 + target_MAC_hex * 16

    # Check if target IP is a private or public.
    # If public, check whether we are on the same network.
    # If on the same network, broadcast directly there to avoid
    # unnecessary data transmission to the outside world.
    try:
        target_IP_is_private = ip_address(target["IP"]).is_private
    except ValueError:
        print(textwrap.dedent(f'''
            Invalid IP address for the machine "{target["NAME"]}" ({target["IP"]}).
            The IP should be provided in a valid format such as:
            216.58.213.164 (a public IP, for a machine that can be awoken from anywhere)
            or
            192.168.1.1 (a private IP, for a machine that can only be awoken from the same network)
        
            Check and correct the IP address of "{target["NAME"]}" in the 'machines.js' file.

        '''))
        sys.exit()
    
    same_network = False
    if not target_IP_is_private:
        try:
            this_public_IP = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8')
            same_network = True if this_public_IP == target["IP"] else False
        except:
            prompt = (f'''
                Are you on the same network as "{target["NAME"]}" ?
                y: yes
                n: no
            ''')
            while True:
                same_network = input(textwrap.dedent(prompt))
                if same_network.lower() == 'y':
                    same_network = True
                    break
                elif same_network.lower() == 'n':
                    same_network = False
                    break
                else:
                    print('<!> Invalid choice. Use "y" or "n".\n')

    if target_IP_is_private or same_network:
        destination = '255.255.255.255'
    else:
        destination = target["IP"]
    
    # Send the paquet
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
        sock.sendto(payload, (destination, target["PORT"]))
        sock.close()
        print(f'The wake-up signal has been sent to "{target["NAME"]}".\n')
        log = f'''
            ### Log ###
            Target:
            {target}

            Same network:
            {same_network}

            Paquet sent to:
            {destination}

            Payload content:
            {payload}
        '''
        return(log)
    except Exception as e:
        print('\nAn error has occured.\n')
        raise(e)
        sys.exit(1)


if __name__ == '__main__':
    # Load config files
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    machines_file = 'machines.dev.json' if config["ENVIRONMENT"] == "dev" else 'machines.json'
    with open(machines_file, 'r') as f:
        machines = json.load(f)

    # Splash
    print(textwrap.dedent(f'''
        # {config["NAME"]} v{config["VERSION"]}

    '''))

    # List available machines and prompt for choice
    prompt = 'Which machine do you want to wake up ? Type its number and press Enter.\n'
    for index, machine in enumerate(machines):
        prompt += f'{index}: {machine["NAME"]}\n'
    
    while True:
        try:
            target = machines[int(input(prompt))]
            break
        except IndexError:
            print('<!> Invalid choice: not in the list.\n')
        except ValueError as e:
            print('<!> Invalid choice: not an integer.\n')

    wake_attempt_result = awake(target)
    if config["VERBOSE"]:
        print(textwrap.dedent(f'{wake_attempt_result}\n'))

    input('Press Enter to exit.\n')
    sys.exit()