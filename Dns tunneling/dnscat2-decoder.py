# Sample usage: 
#   python3 dnscat2-decoder.py sample.pcap mydomain.org

from scapy.all import *
import sys
import binascii


PCAP_FILE = sys.argv[1]
OUTPUT_FILE = 'output.txt'
DOMAIN = sys.argv[2]
DOMAIN = f".{DOMAIN}".encode('utf-8')

c = b""

try:
    r = rdpcap(PCAP_FILE)

except FileNotFoundError:
    print("Error: Packet capture file not found at ",PCAP_FILE)
    sys.exit(1)

except Exception as e:
    print("Error reading pcap file:",e)
    sys.exit(1)



with open(OUTPUT_FILE, "w") as myfile:

    for packet in r:
        
        # Check if the packet has a DNS query record
        if packet.haslayer(DNSQR):
            
            try:
                a = packet[DNSQR].qname
                
                # slice a[18:] is very specific. Check common patterns in pcap and change this value if necessary
                no9 = a[18:] 
                
                b = no9.replace(DOMAIN, b'')
                
                if b == c:
                    continue # Skip duplicates
                c = b
                
                modified_str = b.replace(b".", b"").decode("utf-8", errors="ignore") # Removed dots and decode hexa
                
                ascii_str = bytes.fromhex(modified_str).decode("utf-8", errors="ignore") # Make it ASCII string
                
                print(ascii_str, end="")
                myfile.write(ascii_str)

            except (binascii.Error, Exception) as e:
                pass

print("\nDone. Output saved to", OUTPUT_FILE)
