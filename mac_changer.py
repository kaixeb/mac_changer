#!usr/bin/env python3
import subprocess, re, optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, _) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC address, use --help for more info.")
    return options

def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    #changing interface state to 'down'
    subprocess.run(["ifconfig", interface, "down"])    
    #writing new value to the 'ether' that is the mac address itself
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
    #changing interface state to 'up'
    subprocess.run(["ifconfig", interface, "up"])
    print("[+] The change of MAC address has completed.")

def get_current_mac(interface):
    #putting the output of ifconfig into the variable as a text
    ifconfig_result = subprocess.check_output(["ifconfig", interface], text=True)
    #using regular expression to find mac address in ifconfig result
    mac_addr = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    #could not find mac address
    if not mac_addr: 
        print("[-] Could not find the MAC address.")
        quit()
    #success in finding the mac address
    #group(0) takes first found occurrence from group of matches
    return mac_addr.group(0)

#main sequence
options = get_arguments()
#showing current mac
print("[!] Current MAC address is: ", get_current_mac(options.interface))
#changing mac
change_mac(options.interface, options.new_mac)
#displaying mac changing results
cur_mac = get_current_mac(options.interface)
#if mac has changed
if cur_mac == options.new_mac:
    #show positive result
    print("[+] MAC address was successfully changed to ", cur_mac)
else:
    #display error
    print("[-] MAC address change error! Maybe you should try using 'sudo' keyword.")
