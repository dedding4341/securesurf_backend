import ipinfo
from .settings import IPINFO_ACCESS_TOKEN

handler = ipinfo.getHandler(IPINFO_ACCESS_TOKEN)

def location_check(offending_ip, trusted_ip):
    in_details = handler.getDetails(offending_ip)
    trusted_details = handler.getDetails(trusted_ip)

    if in_details.region == trusted_details.region:
        return True