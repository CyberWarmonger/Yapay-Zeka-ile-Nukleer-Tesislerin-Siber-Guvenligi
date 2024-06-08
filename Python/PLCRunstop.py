
import snap7
from snap7.exceptions import Snap7Exception
import time
import random

class PLCRunstop:
    def __init__(self, ip_address, plc_number):
        self.ip_address = ip_address
        self.client = self.connect_plc()


    def connect_plc(self):
        client = snap7.client.Client()
        try:
            client.connect(self.ip_address, 0, 1, 102)
            return client
        except Snap7Exception as e:
            return None

    def start_plc(self):
        try:
            self.client.plc_hot_start()
            print("PLC started")
        except Snap7Exception as e:
            print(f"Error starting PLC: {str(e)}")

    def stop_plc(self):
        try:
            self.client.plc_stop()
            print("PLC stopped")
            self.client.plc_cold_start()
            print("PLC cold started")
            all_data = self.client.upload(db_number)


        except Snap7Exception as e:
            print(f"Error stopping PLC: {str(e)}")

    def cpu_state_plc(self):
        try:
            status = self.client.get_cpu_state()
            print(f"PLC {status}")
        except Snap7Exception as e:
            print(f"Error stopping PLC: {str(e)}")



ip_address = '192.168.0.1'
plc_number = 1

plc_controller = PLCRunstop(ip_address, plc_number)

plc_controller.stop_plc()


