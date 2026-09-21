import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor

# List of IP addresses to check
ip_addresses = [
    "8.8.8.8",
    "1.1.1.1",
    "192.168.1.1",
    "192.168.1.100"
]

TIMEOUT_SECONDS = 1
system = platform.system().lower()

if system == "windows":
    count_flag, count_val = "-n", "1"
    timeout_flag, timeout_val = "-w", str(TIMEOUT_SECONDS * 1000)  # ms
else:
    count_flag, count_val = "-c", "1"
    timeout_flag, timeout_val = "-W", str(TIMEOUT_SECONDS)  # seconds


def ping_host(ip):
    try:
        result = subprocess.run(
            ["ping", count_flag, count_val, timeout_flag, timeout_val, ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=TIMEOUT_SECONDS + 2  # safety net in case ping itself hangs
        )
        return ip, result.returncode == 0
    except subprocess.TimeoutExpired:
        return ip, False


print("Network Ping Utility")
print("-" * 30)

with ThreadPoolExecutor(max_workers=len(ip_addresses)) as executor:
    results = executor.map(ping_host, ip_addresses)

for ip, is_online in results:
    status = "ONLINE" if is_online else "OFFLINE"
    print(f"{ip} → {status}")