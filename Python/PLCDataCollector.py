import snap7
from snap7.exceptions import Snap7Exception
import time
import os
import csv
import pandas as pd
import datetime
import snap7


class PLCDataCollector:
    def __init__(self, ip_address, plc_number, db_number, start_offset, bit_offset):
        self.ip_address = ip_address
        self.plc_number = plc_number
        self.db_number = db_number
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

    def read_cpu_info(self):
        if self.client:
            try:
                timestamp = datetime.datetime.now()
                cpu_state = "Running" if self.client.get_cpu_state() == "S7CpuStatusRun" else "Not Running"
                cpu_info = self.client.get_cpu_info()
                pdu_length = self.client.get_pdu_length()
                data = [timestamp, cpu_info, cpu_state, pdu_length]
                # Print values
                print(timestamp)
                print(f"PLC {self.plc_number} CPU Info: {cpu_info}")
                print(f"PLC {self.plc_number} CPU State: {cpu_state}")
                print(f"PLC {self.plc_number} PDU Length: {pdu_length}")
            except snap7.snap7exceptions.Snap7Exception as e:
                print(f"Error reading CPU info from PLC {self.plc_number}: {str(e)}")
        else:
            print(f"Skipping PLC {self.plc_number} due to connection failure")


    def read_variables(self, db_number, num_items, data_types):
        data_values = {}
        bool_store = {}
        if self.client:
            try:
                for offset, data_type in zip(range(0, num_items * 2, 2), data_types):
                    try:
                        data = self.client.db_read(db_number, offset, 4)  # Read 4 bytes for DInt by default
                        if data_type == 'UInt':
                            value = snap7.util.get_uint(data, 0)
                        elif data_type == 'DInt':
                            value = snap7.util.get_dint(data, 0)
                        elif data_type == 'Bool':
                            value = snap7.util.get_bool(data, 0, 0)  # Read as Bool
                        elif data_type == 'Byte':
                            value = snap7.util.get_byte(data, 0)
                        elif data_type == 'Word':
                            value = snap7.util.get_word(data, 0)


                        if value is not None:
                            data_values[f'Offset_{offset}'] = value
                            print(f'DB Number: {db_number} Offset: {offset} Value: {value} ')
                            if  data_type == 'Bool':
                                bool_store [f'Offset_{offset}'] = value

                        else:
                            pass
                    except Snap7Exception as e:
                        print(f"Error reading Data Block {db_number}, Offset {offset}: {str(e)}")
            except Snap7Exception as e:
                print(f"Error reading Data Block {db_number}: {str(e)}")
        return data_values,bool_store

    def read_boolean_variables(self, db_number, num_items):
        bool_store = {}
        True_store = []
        if self.client:
            try:
                for offset in range(0, num_items * 2, 2):
                    try:
                        data = self.client.db_read(db_number, offset, 2)  # Read 2 bytes for each variable
                        value = snap7.util.get_bool(data, 0, 0)  # Read as Bool

                        bool_store[f'Offset_{offset}'] = value
                        value_bool = bool_store[f'Offset_{offset}']
                        print(f'DB Number: {db_number} Offset: {offset} Value: {value}')
                        if value == True:
                            true_info = f'DB Number: {db_number} Offset: {offset} Value: {value}'
                            True_store.append(true_info)
                    except Snap7Exception as e:
                        if "Address out of range" in str(e):
                            print(f"Address out of range error: {str(e)}")
                        else:
                            print(f"Error reading Data Block {db_number}: {str(e)}")
            except Snap7Exception as e:
                print(f"Error reading Data Block {db_number}: {str(e)}")
        #print(True_store)
        #print TRUE BOOLEAN Values in data block
        print("----------------------------------")
        print("--------Offset numbers------------")
        print("---------TRUE BOOLEAN-------------")
        for i in True_store:
            print(i)
        return bool_store,True_store

    def close_connection(self):
        if self.client:
            self.client.disconnect()

    def run_all_code_collector(self):
        # Usage example
        ip_address = '192.168.0.1' ; plc_number = 1 ;db_number = 1 ; start_offset = 72
        bit_offset = 0 ; value = 1  # 1 = true | 0 = false
        num_items = 17
        # Define the data types based on your knowledge
        # Define data types for each item in the data block
        data_types = [
            'UInt',  # Data Type 1
            'UInt',  # Data Type 2
            'Bool',  # Data Type 3
            'Word',  # Data Type 4
            'LTime',  # Data Type 5
            # ... Repeat this pattern as needed
        ]

        plc_data_get = PLCDataCollector(ip_address, plc_number, db_number, start_offset, bit_offset)

        #RUN

        try:
            plc_data_get.read_cpu_info()
            data_values = plc_data_get.read_variables(1, len(data_types), data_types)
            plc_data_get.read_boolean_variables(1,num_items)
        except KeyboardInterrupt:
            plc_data_get.close_connection()

