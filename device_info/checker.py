# Network Device information system

network_devices = []  #The program uses a list to store devices


def add_device():
    print("\n--- Add Network device ---")
    
    device_name = input("Device name: ")
    device_type = input("Device type (PC/Router/Switch/Server):")
    ip_address = input("IP address: ")
    mac_address = input("MAC address: ")
    location = input("Location: ")
    
    device = {      #each device is stored as a dictionary
        "name": device_name,
        "type": device_type,
        "ip": ip_address,
        "mac": mac_address,
        "location": location
    } 
    
    network_devices.append(device)
    
    print("\nDevice added successfully")
    
def display_devices():
    print("\n Network Devices ")
    
    if len(network_devices) == 0:
        print("No device stored.")
        return
    
    for number, device in enumerate(network_devices, start=1):
        print(f"\nDevice {number}")
        print(f"Name: {device['name']}")
        print(f"Type: {device['type']}")
        print(f"IP Address: {device['ip']}")
        print(f"MAC Address: {device['mac']}")
        print(f"Location: {device['location']}")
        
        
while True:
    print("\n NETWORK DEVICES SYSTEM")
    print("1. Add device")
    print("2. Display devices")
    print("3. Exit")
    
    choice = input("Choose an option: ")
    
    if choice == "1":
        add_device()
    elif choice == "2":
        display_devices()
    elif choice == "3":
        print("Program closed.")
        break
    else:
        print("Invalid option. Please try again")