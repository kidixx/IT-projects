#!/usr/bin/env python3
"""
Subnet Calculator
------------------
Given an IP address with a prefix length or subnet mask (CIDR notation,
e.g. 192.168.1.10/24 or 192.168.1.10/255.255.255.0), prints:
- Network address
- Broadcast address
- Netmask / Wildcard mask
- First and last usable host
- Total and usable host counts
- Binary representation

Also supports subnetting a network into N smaller subnets, or into
subnets that each fit at least H hosts.

Usage:
    python subnet_calculator.py 192.168.1.10/24
    python subnet_calculator.py 10.0.0.0/255.255.255.0
    python subnet_calculator.py 192.168.1.0/24 --split 4
    python subnet_calculator.py 192.168.1.0/24 --hosts 50
"""

import argparse
import ipaddress
import sys


def format_binary(ip_int, bits=32):
    return '.'.join(
        format((ip_int >> (24 - 8 * i)) & 0xFF, '08b')
        for i in range(4)
    )


def describe_network(net_input: str):
    """Parse an address/prefix or address/mask string and print details."""
    try:
        # ipaddress handles both CIDR (/24) and dotted mask (/255.255.255.0)
        interface = ipaddress.ip_interface(net_input)
        network = interface.network
    except ValueError as e:
        print(f"Error: could not parse '{net_input}' — {e}")
        sys.exit(1)

    if network.version != 4:
        print("Note: only IPv4 is fully supported for host/broadcast breakdown.")

    print(f"\nInput:              {net_input}")
    print(f"Network address:    {network.network_address}")
    print(f"Broadcast address:  {network.broadcast_address}")
    print(f"Netmask:            {network.netmask}  (/{network.prefixlen})")
    print(f"Wildcard mask:      {network.hostmask}")
    print(f"Total addresses:    {network.num_addresses}")

    hosts = list(network.hosts())
    if hosts:
        print(f"Usable hosts:       {len(hosts)}")
        print(f"First usable host:  {hosts[0]}")
        print(f"Last usable host:   {hosts[-1]}")
    else:
        print("Usable hosts:       0 (network too small for host range)")

    if network.version == 4:
        print(f"Network (binary):   {format_binary(int(network.network_address))}")
        print(f"Netmask (binary):   {format_binary(int(network.netmask))}")

    print(f"Is private:         {network.is_private}")
    return network


def split_network(network, count=None, min_hosts=None):
    """Split a network into `count` equal subnets, or subnets holding
    at least `min_hosts` usable hosts each."""
    if count is not None:
        import math
        new_prefix = network.prefixlen + math.ceil(math.log2(count))
    elif min_hosts is not None:
        import math
        # +2 for network/broadcast addresses
        needed_bits = math.ceil(math.log2(min_hosts + 2))
        new_prefix = 32 - needed_bits
    else:
        return

    if new_prefix > 32 or new_prefix < network.prefixlen:
        print("Error: requested split is not possible within this network.")
        return

    subnets = list(network.subnets(new_prefix=new_prefix))
    print(f"\nSplit into {len(subnets)} subnet(s) of /{new_prefix}:")
    for i, sn in enumerate(subnets):
        hosts = list(sn.hosts())
        host_range = f"{hosts[0]} - {hosts[-1]}" if hosts else "n/a"
        print(f"  [{i}] {sn}  (hosts: {host_range}, usable: {len(hosts)})")


def main():
    parser = argparse.ArgumentParser(description="IPv4/IPv6 subnet calculator")
    parser.add_argument("network", help="e.g. 192.168.1.10/24 or 10.0.0.0/255.255.255.0")
    parser.add_argument("--split", type=int, metavar="N", help="split into N equal subnets")
    parser.add_argument("--hosts", type=int, metavar="H", help="split into subnets fitting at least H hosts each")
    args = parser.parse_args()

    network = describe_network(args.network)

    if args.split:
        split_network(network, count=args.split)
    elif args.hosts:
        split_network(network, min_hosts=args.hosts)


if __name__ == "__main__":
    main()