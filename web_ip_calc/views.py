from flask import render_template, request, Blueprint
from .functions import check_address, check_class, check_mask,\
    convert_to_binary, convert_to_decimal, calculate_subnet,\
    calculate_broadcast, calculate_hosts, calculate_minhost, calculate_maxhost
view = Blueprint('calc', __name__)


@view.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@view.route('/send', methods=['POST'])
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
        binaddress = convert_to_binary(address)
        binSubnetMask = convert_to_binary(subnetMask)
        classOfAddress = check_class(address)
        binNetworkAddress = calculate_subnet(address, subnetMask)
        if binNetworkAddress == "It's not a subnet, it's a host.":
            networkAddress = "It's not a subnet, it's a host."
            binNetworkAddress = "."
            binHosts = "."
            minhost = "."
            binMinHost = "."
            maxhost = "."
            binMaxHost = "."
            binBroadcastAddress = "."
            broadcastAddress = "."
            hosts = "."
        else:
            networkAddress = convert_to_decimal(binNetworkAddress)
            minhost = calculate_minhost(address, subnetMask)
            binMinHost = convert_to_binary(minhost)
            maxhost = calculate_maxhost(address, subnetMask)
            binMaxHost = convert_to_binary(maxhost)
            binBroadcastAddress = calculate_broadcast(address, subnetMask)
            broadcastAddress = convert_to_decimal(binBroadcastAddress)
            hosts = calculate_hosts(subnetMask)
            binHosts = str(format(int(hosts), "08b"))

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
