import subprocess
import platform

#list of Ip address to check
ip_addresses = [
    "8.8.8.8",
    "1.1.1.1",
    "192.168.1.1",
    "192.168.1.100"
]

#Choose the correct option for the operating system
system = platform.system().lower()

if system == "windows":
    ping_option = "-n"
else:
    ping_option = '-c'

def ping_host(ip):
    result = subprocess.run