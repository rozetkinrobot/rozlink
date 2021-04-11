import netaddr


def ip2int(ip: str):
    return int(netaddr.IPAddress(ip))


def int2ip(ip: int):
    return str(netaddr.IPAddress(ip))
