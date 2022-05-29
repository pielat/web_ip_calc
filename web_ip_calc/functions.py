import re

def check_address(ip: str) -> bool:
    is_correct = re.match(r"(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])$",ip)
    return is_correct


def check_class(ip: str) -> str:
    octets = ip.split(".")
    if octets[0] == "127":
        return "This is loopback address."
    elif 1 <= int(octets[0]) <= 126:
        return "This is class A."
    elif 128 <= int(octets[0]) <= 191:
        return "This is class B."
    elif 192 <= int(octets[0]) <= 223:
        return "This is class C"
    elif 224 <= int(octets[0]) <= 239:
        return "This is class D"
    elif 240 <= int(octets[0]) <= 254:
        return "This is class E"


def calculate_cidr(mask: str) -> int:
    return mask.count('1')


def check_mask(mask: str):
    if check_address(mask):
        octets = mask.split(".")
        maskbits = ""
        for x in octets:
            maskbits = maskbits + str(format(int(x), "08b"))
        end_of_ones = False
        i = 0
        while i < 32:
            if end_of_ones and int(maskbits[i]) == 1:
                return False
                quit()
            elif int(maskbits[i]) == 0:
                end_of_ones = True
            i += 1
    else:
        return False
    return True



def convert_to_binary(address: str) -> str:
    octets = address.split(".")
    binary = ""
    for x in octets[:-1]:
        binary += str(format(int(x), "08b")) + "."
    binary += str(format(int(octets[-1]), "08b"))
    return binary


def convert_to_decimal(binary: str) -> str:
    octets = binary.split(".")
    decimal = ""
    for x in octets[:-1]:
        decimal += str(int(x, 2)) + "."
    decimal += str(int(octets[-1], 2))
    return decimal


def calculate_subnet(ip: str, mask: str) -> str:
    binary_ip = convert_to_binary(ip)
    binary_mask = convert_to_binary(mask)
    subnet_binary_address = ""
    i = 0
    cidr = calculate_cidr(binary_mask)
    while i < 35:
        if i <= cidr-1:
            if binary_ip[i] == ".":
                cidr += 1
            subnet_binary_address += binary_ip[i]
        else:
            if i == 8 or i == 17 or i == 26:
                subnet_binary_address += "."
            else:
                subnet_binary_address += "0"
        i += 1
    return subnet_binary_address


def calculate_broadcast(ip: str, mask: str) -> str:
    binary_ip = convert_to_binary(ip)
    binary_mask = convert_to_binary(mask)
    broadcast_address = ""
    i = 0
    cidr = calculate_cidr(binary_mask)
    while i < 35:
        if i <= cidr-1:
            if binary_ip[i] == ".":
                cidr += 1
            broadcast_address += binary_ip[i]
        else:
            if i == 8 or i == 17 or i == 26:
                broadcast_address += "."
            else:
                broadcast_address += "1"
        i += 1
    return broadcast_address


def calculate_hosts(mask: str) -> int:
    # how many hosts block
    cidr = calculate_cidr(convert_to_binary(mask))
    max_addresses = pow(2, 32-cidr) - 2
    return max_addresses


def calculate_minhost(ip: str, mask: str) -> int:
    # first host block
    min_host = convert_to_decimal(calculate_subnet(ip, mask))
    octets_min_host = min_host.split(".")
    octets_min_host[-1] = int(octets_min_host[-1]) + 1
    new_min_hosts = ""
    for x in octets_min_host[:-1]:
        new_min_hosts += str(x) + "."
    new_min_hosts = new_min_hosts + str(octets_min_host[-1])
    return new_min_hosts


def calculate_maxhost(ip: str, mask: str) -> int:
    # last host block
    max_host = convert_to_decimal(calculate_broadcast(ip, mask))
    octets_max_host = max_host.split(".")
    octets_max_host[-1] = int(octets_max_host[-1]) - 1
    new_max_hosts = ""
    for x in octets_max_host[:-1]:
        new_max_hosts += str(x) + "."
    new_max_hosts = new_max_hosts + str(octets_max_host[-1])
    return new_max_hosts