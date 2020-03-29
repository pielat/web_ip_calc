from flask import Flask, render_template, request
import re

app = Flask(__name__)


def check_address(ip):
    is_correct = re.match(r"(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])$",ip)
    return is_correct


def check_class(ip):
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


def calculate_cidr(mask):
    return mask.count('1')


def check_mask(mask):
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



def convert_to_binary(address):
    octets = address.split(".")
    binary = ""
    for x in octets[:-1]:
        binary += str(format(int(x), "08b")) + "."
    binary += str(format(int(octets[-1]), "08b"))
    return binary


def convert_to_decimal(binary):
    octets = binary.split(".")
    decimal = ""
    for x in octets[:-1]:
        decimal += str(int(x, 2)) + "."
    decimal += str(int(octets[-1], 2))
    return decimal


def calculate_subnet(ip, mask):
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


def calculate_broadcast(ip, mask):
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


def calculate_hosts(ip, mask):
    # how many hosts block
    cidr = calculate_cidr(convert_to_binary(mask))
    max_addresses = pow(2, 32-cidr) - 2
    return max_addresses


def calculate_minhost(ip, mask):
    # first host block
    min_host = convert_to_decimal(calculate_subnet(ip, mask))
    octets_min_host = min_host.split(".")
    octets_min_host[-1] = int(octets_min_host[-1]) + 1
    new_min_hosts = ""
    for x in octets_min_host[:-1]:
        new_min_hosts += str(x) + "."
    new_min_hosts = new_min_hosts + str(octets_min_host[-1])
    return new_min_hosts


def calculate_maxhost(ip, mask):
    # last host block
    max_host = convert_to_decimal(calculate_broadcast(ip, mask))
    octets_max_host = max_host.split(".")
    octets_max_host[-1] = int(octets_max_host[-1]) - 1
    new_max_hosts = ""
    for x in octets_max_host[:-1]:
        new_max_hosts += str(x) + "."
    new_max_hosts = new_max_hosts + str(octets_max_host[-1])
    return new_max_hosts

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def send(
            address=None,
            subnetMask=None,
            binaddress=None,
            binSubnetMask=None,
            badAddress=None,
            badMask=None,
            classOfAddress=None,
            binNetworkAddress=None,
            networkAddress=None,
            binBroadcastAddress=None,
            broadcastAddress=None,
            hosts=None,
            binHosts=None,
            binMinHost=None,
            minhost=None,
            binMaxHost=None,
            maxhost=None
        ):
    if request.method == 'POST':
        address = request.form['ipAddress']
        subnetMask = request.form['subnetMask']
        if not(check_address(address)):
            badAddress = "IP address is bad"
            return render_template('index.html', badAddress=badAddress)
        if not(check_mask(subnetMask)):
            badMask = "Subnet mask is bad"
            return render_template('index.html', badMask=badMask)
        binaddress=convert_to_binary(address)
        binSubnetMask=convert_to_binary(subnetMask)
        classOfAddress = check_class(address)
        binNetworkAddress = calculate_subnet(address, subnetMask)
        networkAddress = convert_to_decimal(binNetworkAddress)
        binBroadcastAddress = calculate_broadcast(address, subnetMask)
        broadcastAddress = convert_to_decimal(binBroadcastAddress)
        hosts = calculate_hosts(address, subnetMask)
        binHosts = str(format(int(hosts), "08b"))
        minhost = calculate_minhost(address, subnetMask)
        binMinHost = convert_to_binary(minhost)
        maxhost = calculate_maxhost(address, subnetMask)
        binMaxHost = convert_to_binary(maxhost)

        return render_template(
            'index.html',
            binaddress=binaddress,
            address=address,
            subnetMask=subnetMask,
            binSubnetMask=binSubnetMask,
            classOfAddress=classOfAddress,
            binNetworkAddress=binNetworkAddress,
            networkAddress=networkAddress,
            binBroadcastAddress=binBroadcastAddress,
            broadcastAddress=broadcastAddress,
            binHosts=binHosts,
            hosts=hosts,
            minhost=minhost,
            binMinHost=binMinHost,
            maxhost=maxhost,
            binMaxHost=binMaxHost,
        )


if __name__ == '__main__':
    app.run()