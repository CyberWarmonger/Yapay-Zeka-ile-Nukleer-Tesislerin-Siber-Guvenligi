import snap7
from snap7.exceptions import Snap7Exception
import time
import os
import csv
import pandas as pd
import datetime
import snap7


class PLCDataWriter:
    def __init__(self, ip_address,db_number):
        self.ip_address = ip_address
        self.plc_number = plc_number
        self.db_number = db_number
        self.client = self.connect_plc()

    def connect_plc(self):
        client = snap7.client.Client()
        try:
            client.connect(self.ip_address, 0, 1, 102)
            return client
        except Snap7Exception as e:
            return None

    def writeBool(self, db_number, start_offset,bit_offset,value):
        try:
            reading = self.client.db_read(db_number, start_offset, 1)  # Read 1 byte
            snap7.util.set_bool(reading, 0, bit_offset, value)  # Set the boolean value
            self.client.db_write(db_number, start_offset, reading)  # Write back the updated bytearray
            print(f"DB 1 Offset {start_offset}.{bit_offset}: {plc_data_writer.readBool(db_number, start_offset,bit_offset)}")
            return True  # Indicate success
        except Snap7Exception as e:
            print(f"Error writing Data Block {db_number}, Offset {start_offset}.{bit_offset}: {str(e)}")
            return False  # Indicate failure

    def readBool(self, db_number, start_offset,bit_offset):
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


# Usage example
ip_address = '192.168.0.1'
plc_number = 1
db_number = 1


plc_data_writer = PLCDataWriter(ip_address,db_number)

try:
    # Write boolean values
    plc_data_writer.writeBool(1, 346, 1,0)
except ValueError:
    print("Please enter a valid integer.")
