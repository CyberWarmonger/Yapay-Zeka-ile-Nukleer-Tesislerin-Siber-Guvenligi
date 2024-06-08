import snap7
from snap7.exceptions import Snap7Exception
import time
import random

class PLCDataWriter:
    def __init__(self, ip_address, db_number):
        self.ip_address = ip_address
        self.db_number = db_number
        self.client = self.connect_plc()

    def connect_plc(self):
        client = snap7.client.Client()
        try:
            client.connect(self.ip_address, 0, 1, 102)
            return client
        except Snap7Exception as e:
            return None

    def writeBool(self, db_number, start_offset, bit_offset, value):
        try:
            reading = self.client.db_read(db_number, start_offset, 1)  # Read 1 byte
            snap7.util.set_bool(reading, 0, bit_offset, value)  # Set the boolean value
            self.client.db_write(db_number, start_offset, reading)  # Write back the updated bytearray
            print("------------------------------------")
            print(f"DB 1 Offset {start_offset}.{bit_offset}: {self.readBool(db_number, start_offset, bit_offset)} \n-----Successfully changed------------")
            print("------------------------------------")
            return True  # Indicate success
        except Snap7Exception as e:
            print(f"Error writing Data Block {db_number}, Offset {start_offset}.{bit_offset}: {str(e)}")
            return False  # Indicate failure

    def readBool(self, db_number, start_offset, bit_offset):
        try:
            reading = self.client.db_read(db_number, start_offset, 1)  # Read 1 byte
            value = snap7.util.get_bool(reading, 0, bit_offset)
            return value
        except Snap7Exception as e:
            print(f"Error reading Data Block {db_number}, Offset {start_offset}.{bit_offset}: {str(e)}")
            return None

    def close_connection(self):
        if self.client:
            self.client.disconnect()

    @staticmethod
    def get_user_input(prompt):
        while True:
            try:
                value = int(input(prompt))
                return value
            except ValueError:
                print("Please enter a valid integer.")

    def run_all_code(self):
            print("PLC Data Writer")
            ip_address = input("Enter the PLC IP address: ")
            db_number = self.get_user_input("Enter the DB number: ")
            start_offset = self.get_user_input("Enter the start offset: ")
            bit_offset = self.get_user_input("Enter the bit offset: ")
            time_running = self.get_user_input("Enter the running time: ")
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
                    while time.time() - start_time < time_running:  # Run for the specified time
                        plc_data_writer.writeBool(db_number, start_offset, bit_offset, int(value_to_set))
                        time.sleep(1)  # Toggle every second

                    user_choice = input("Do you want to change the value again? (Y/N): ")
                    if user_choice.lower() != 'y':
                        break  # Exit the loop if the user chooses not to continue

                plc_data_writer.close_connection()

            except KeyboardInterrupt:
                plc_data_writer.close_connection()


