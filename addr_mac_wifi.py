import netifaces as ni

def get_wifi_mac_address(interface='wlan0'):
  
        interface_info = ni.ifaddresses(interface)
        mac_address = interface_info[ni.AF_LINK][0]['addr']
        return mac_address

wifi_mac_address = get_wifi_mac_address()
print(wifi_mac_address)
