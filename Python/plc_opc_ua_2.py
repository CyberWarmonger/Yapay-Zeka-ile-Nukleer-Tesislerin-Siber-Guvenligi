from opcua import Client
from opcua import ua
import time
import os
import csv
import pandas as pd
import numpy as np
from datetime import datetime

def connect_to_opc_server(server_address):
    try:
        client = Client(server_address)
        client.connect()
        return client
    except Exception as e:
        print(f"Failed to connect to OPC server: {e}")
        return None


def read_opc_value(client, node_id):
    try:
        client_node = client.get_node(node_id)
        value = client_node.get_value()
        return value
    except Exception as e:
        print(f"Failed to read value from node {node_id}: {e}")
        return None


def divide_datetime(dt):
    year, month, day, hour, minute, second, millisecond = 0, 0, 0, 0, 0, 0, 0
    if dt:
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour
        hour = int(hour) + 8
        minute = dt.minute
        second = dt.second
        millisecond = dt.microsecond // 1000  # Convert microseconds to milliseconds
    return year, month, day, hour, minute, second, millisecond


data_list = []  # To store collected data
iter = 50000 #iter count
def main():
    server_address = "opc.tcp://192.168.0.1:4840"
    client = connect_to_opc_server(server_address)

    if client is None:
        return
    try:
        root = client.get_root_node()
        print("Objects root node is: ", root)
        count = 0

        while count <= iter:  # Limit the number of iterations
            try:
                if root:
                    current_cycle = read_opc_value(client, 'ns=3;s="Data_block_1"."infoData_current_Dint"')
                    shortest_cycle = read_opc_value(client, 'ns=3;s="Data_block_1"."infoData_shortest_Dint"')
                    longest_cycle = read_opc_value(client, 'ns=3;s="Data_block_1"."infoData_Longest_Dint"')
                    min_runtime = read_opc_value(client, 'ns=3;s="Data_block_1"."infoData_min_runtime_Dint"')
                    max_runtime = read_opc_value(client, 'ns=3;s="Data_block_1"."infoData_max_runtime_Dint"')
                    status_plc = read_opc_value(client, 'ns=3;s="Data_block_1"."HMIStart"')
                    server_current_time = read_opc_value(client, 'i=2258')
                    pid_output_pump_speed = read_opc_value(client, 'ns=3;s="Data_block_OPCUA"."OPCUA_PID_Control"')
                    pid_input_sg_lvl = read_opc_value(client, 'ns=3;s="Data_block_OPCUA"."OPCUA_PID_PV"')

                    #io_module_status = read_opc_value(client, 'ns=3;s="Data_block_1"."retVal_device"')

                    year, month, day, hour, minute, second, millisecond = divide_datetime(server_current_time)
                    print(f'Iteration : {count}\n')
                    data = {
                        "PLC Current cycle time": current_cycle or 0,
                        "PLC The shortest cycle time": shortest_cycle or 0,
                        "PLC The longest cycle time": longest_cycle or 0,
                        "PLC Min runtime": min_runtime or 0,
                        "PLC Max runtime": max_runtime or 0,
                        "PLC Running Status": status_plc,
                        "Server_current_time": server_current_time or 0,
                        "Pump Speed" : pid_output_pump_speed or 0,
                        "SG lEVEL" : pid_input_sg_lvl or 0,
                        "Year": year,
                        "Month": month,
                        "Day": day,
                        "Hour": hour,
                        "Minute": minute,
                        "Second": second,
                        "Millisecond": millisecond,
                    }
                    data_list.append(data)
                    print(data)
                    count += 1
                else:
                    # Add a placeholder entry for inactive PLCs
                    data = {
                        "PLC Current cycle time": 0,
                        "PLC The shortest cycle time": 0,
                        "PLC The longest cycle time": 0,
                        "PLC Min runtime": 0,
                        "PLC Max runtime": 0,
                        "PLC Running Status": "Not active",
                        "Server_current_time": 0,
                        "Pump Speed": 0,
                        "SG lEVEL": 0,
                        "Year": 0,
                        "Month": 0,
                        "Day": 0,
                        "Hour": 0,
                        "Minute": 0,
                        "Second": 0,
                        "Millisecond": 0,
                    }
                    data_list.append(data)
            except Exception as e:
                print(f"An error occurred while reading OPC values: {e}")
                break

    finally:
        try:
            client.disconnect()
        except Exception as e:
            print(f"An error occurred while disconnecting from OPC server: {e}")
if __name__ == "__main__":
    main()



# Write collected data to a CSV file
csv_file = "plc_data_cpu.csv"
with open(csv_file, mode='w', newline='') as file:
    fieldnames = ["PLC Current cycle time", "PLC The shortest cycle time",
                  "PLC The longest cycle time", "PLC Min runtime", "PLC Max runtime",
                  "PLC Running Status", "Server_current_time","Pump Speed","SG lEVEL",
                  "Year","Month","Day","Hour","Minute","Second","Millisecond"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data_list)


