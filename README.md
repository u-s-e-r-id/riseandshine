# riseAndShine
A simple Wake-on-Lan / Wake-on-Wan tool made in python.
It lets you remotely wake up machines that are sleeping, deep sleeping,
hibernating or (in some cases) powered off entirely.


# Pre-requisites
You must have python installed on the machine on which you run the tool.
A remote machine to be awaken doesn't need to have python installed but it must
support Wak-on-Lan. 
Waking up machines on the same network you're on (Wake-on-Lan) usually doesn't
require any network configuration. To wake up a machine that resides on another
network (Wake-on-Wan), you may need to configure port redirections on the
outside-facing network device you use (your router). Router firewalls may also
require attention.

To enable Wake-on-Lan on a machine you wish to awake remotely, see:
Windows:
https://docs.microsoft.com/en-gb/troubleshoot/windows-client/deployment/wake-on-lan-feature

MacOS:
https://www.microcenter.com/tech_center/article/7596/how-to-enable-or-disable-wake-on-lan-in-mac-os-x

Linux (Ubuntu):
https://help.ubuntu.com/community/WakeOnLan

Debian:
https://wiki.debian.org/WakeOnLan


# Installation
There is no installation process to use riseAndShine. Juste download the folder
and place it in a directory of your liking (for example in the "Program Files"
folder of Windows, or the "/Applications" folder of your Mac).


# Configuration
Open the machines.json file. Two default machines are listed as examples.
Replace the values to match your real machine(s) (the one(s) that you want to
awake, not the one you're running riseAndShine from).

"NAME"  >   The name you want to list this machine under.
"IP"    >   The public IP address of the network that the machine sits on.
            If you provide a private/local IP, you will only be able to awake
            this machine from the same network (Wake-on-LAN). You won't be able
            to awake it from a remote network (Wake-on-WAN)
"MAC"   >   The MAC address / hardware address of the machine
"PORT"  >   The port on which to send the wake-up signal. The default is 9.


# Usage
Double click "riseandshine.bat" (Windows) or "riseandshine.sh" (Mac/Linux/Debian).
You may also open "riseandshine.py" with your python interpreter. Then simply
follow the instructions on screen.