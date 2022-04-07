import ipaddress

def ip2int(ip: str):
    return str(int(ipaddress.ip_address(ip)))


def int2ip(ip: int):
    return str(ipaddress.ip_address(int(ip)))
