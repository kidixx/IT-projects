# Subnet Calculator

A command-line IPv4 subnet calculator built with Python's standard `ipaddress` module. Given an IP address and a prefix length or subnet mask, it computes the network address, broadcast address, usable host range, and more — and can split a network into smaller subnets.

## Features

- Accepts CIDR notation (`192.168.1.10/24`) or dotted-decimal masks (`10.0.0.0/255.255.255.0`)
- Reports:
  - Network address
  - Broadcast address
  - Netmask and wildcard mask
  - Total addresses and usable host count
  - First and last usable host
  - Binary representation of network address and mask
  - Whether the address is private
- Splits a network into:
  - A fixed number of equal-sized subnets (`--split`)
  - Subnets sized to fit at least a given number of hosts each (`--hosts`)

## Requirements

- Python 3.3 or later (uses only the standard library — no dependencies to install)

## Usage

```bash
python subnet_calculator.py <ip_address>/<prefix_or_mask> [options]
```

### Basic lookup

```bash
python subnet_calculator.py 192.168.1.10/24
```

```
Input:              192.168.1.10/24
Network address:    192.168.1.0
Broadcast address:  192.168.1.255
Netmask:            255.255.255.0  (/24)
Wildcard mask:      0.0.0.255
Total addresses:    256
Usable hosts:       254
First usable host:  192.168.1.1
Last usable host:   192.168.1.254
Network (binary):   11000000.10101000.00000001.00000000
Netmask (binary):   11111111.11111111.11111111.00000000
Is private:         True
```

### Using a dotted-decimal mask instead of CIDR

```bash
python subnet_calculator.py 10.0.0.0/255.255.255.0
```

### Splitting into N equal subnets

```bash
python subnet_calculator.py 192.168.1.0/24 --split 4
```

```
Split into 4 subnet(s) of /26:
  [0] 192.168.1.0/26    (hosts: 192.168.1.1 - 192.168.1.62, usable: 62)
  [1] 192.168.1.64/26   (hosts: 192.168.1.65 - 192.168.1.126, usable: 62)
  [2] 192.168.1.128/26  (hosts: 192.168.1.129 - 192.168.1.190, usable: 62)
  [3] 192.168.1.192/26  (hosts: 192.168.1.193 - 192.168.1.254, usable: 62)
```

### Splitting to fit a minimum number of hosts per subnet

```bash
python subnet_calculator.py 192.168.1.0/24 --hosts 50
```

Calculates the smallest subnet size that fits at least 50 usable hosts, then divides the network into that many subnets.

## Options

| Flag | Description |
|------|-------------|
| `network` | Required. IP address with prefix length or subnet mask, e.g. `192.168.1.10/24` |
| `--split N` | Split the network into `N` equal-sized subnets |
| `--hosts H` | Split the network into subnets that each fit at least `H` usable hosts |

`--split` and `--hosts` are mutually exclusive in effect — if both are given, `--split` takes priority.

## Notes

- IPv6 addresses are parsed but host/broadcast breakdown is IPv4-specific; IPv6 support is limited to basic network info.
- `/31` and `/32` networks have no usable host range (per RFC 3021 / single-host conventions), and the tool reports `0` usable hosts in that case.

## License

Free to use, modify, and distribute.