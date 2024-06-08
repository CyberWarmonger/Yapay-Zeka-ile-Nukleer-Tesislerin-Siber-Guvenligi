import snap7
from snap7.exceptions import Snap7Exception
import time
import os
import csv
import pandas as pd
import datetime

class PLCDataInfo:
    def __init__(self, ip_address, plc_number):
        self.ip_address = ip_address
        self.plc_number = plc_number
        self.client = self.connect_plc()

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

    def close_connection(self):
        if self.client:
            self.client.disconnect()

# Usage example
ip_address = '192.168.0.1'
plc_number = 1
plc_data_Info = PLCDataInfo(ip_address, plc_number)

#RUNN
'''
try:
    plc_data_Info.read_cpu_info()
except KeyboardInterrupt:
    plc_data_Info.close_connection()
'''