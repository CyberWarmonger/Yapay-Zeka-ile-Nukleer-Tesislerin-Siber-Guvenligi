import pyshark
import pandas as pd
from datetime import datetime
import pickle
from sklearn.preprocessing import LabelEncoder

def split_datetime(dt_str):
    # First, parse the string to a datetime object to handle potential parsing issues
    dt_obj = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S.%f')
    
    # Now, we can format the datetime object into the desired string formats
    year = dt_obj.strftime('%Y')
    month = dt_obj.strftime('%m')
    day = dt_obj.strftime('%d')
    hour = dt_obj.strftime('%H')
    minute = dt_obj.strftime('%M')
    second = dt_obj.strftime('%S')
    microsecond = dt_obj.strftime('%f')  # This gives microsecond precision
    
    # If you want milliseconds, you can divide the microseconds by 1000
    millisecond = int(dt_obj.microsecond / 1000)
    
    # Create a dictionary to return
    datetime_components = {
        'Year': int(year),
        'Month': int(month),
        'Day': int(day),
        'Hour': int(hour),
        'Minute': int(minute),
        'Second': int(second),
        'Millisecond': millisecond
    }
    
    return datetime_components

def df_preprocess(packet_info_list):
    # Convert the list of packet info to a pandas DataFrame
    df = pd.DataFrame(packet_info_list)
    print(df)
    df.to_csv('df.csv', index=False)
    df = pd.read_csv("df.csv", encoding='ISO-8859-1')
    # Assuming you have a DataFrame called df
    missing_values = df.isnull()  # or df.isnull()
    # Count the number of missing values in each column
    missing_count = missing_values.sum()
    return df

def preprocessing(df):
    # Drop non-numeric columns and convert IP columns to numerical form (using dummy variables)
    numeric_columns = ['Source', 'Destination', 'Protocol', 'Length',
       'Source Port',
       'Destination Port', 
       'Time to Live', 'Byte Address']
    
    #copy of dataframe
    data = df.copy()
    
    # Replace NaN values with 0
    data.fillna(0, inplace=True)
    # Convert labels to numeric form using label encoding
    label_encoder = LabelEncoder()
    
    data['Source'] = data['Source'].apply(lambda x: 0 if x in ['192.168.0.1', '192.168.0.2'] else 1)
    data['Destination'] = data['Destination'].apply(lambda x: 0 if x in ['192.168.0.1', '192.168.0.2'] else 1)
    
    data['Byte Address'] = data['Byte Address'].apply(lambda x: 0 if x in [int('0')] else 1)
   
    # Assuming 'data' is your DataFrame and 'Protocol' column needs encoding
    data['Protocol'] = data['Protocol'].fillna('Unknown')  # Fill NaN values with 'Unknown'

    known_protocols = ['ARP', 'BROWSER', 'COTP', 'ICMPv6', 'IGMPv3', 'IPv4', 'LLDP', 'LLMNR',
                       'MDNS', 'NBNS', 'NTP', 'OpcUa', 'S7COMM', 'SSDP', 'TCP','TPKT','ICMP']

    # Create a label encoder
    label_encoder = LabelEncoder()

    # Fit and transform the 'Protocol' column
    data['Protocol'] = label_encoder.fit_transform(data['Protocol'])

    # Handling unknown protocols
    if 'Unknown' not in label_encoder.classes_:
        # Assign a unique value for 'Unknown' protocol
        unknown_label = max(data['Protocol']) + 1
        #print(f"Assigning 'Unknown' protocol label as: {unknown_label}")
        data.loc[data['Protocol'] == 'Unknown', 'Protocol'] = unknown_label

    # Define a function to encode protocols or assign a default value for unknown ones
    def encode_protocol(protocol):
        if protocol in known_protocols:
            return label_encoder.transform([protocol])[0]
        else:
            return unknown_label  # Assign the value you previously determined for unknown protocols

    # Apply the encode_protocol function to the 'Protocol' column
    data['Protocol'] = data['Protocol'].apply(encode_protocol)

    data= data[numeric_columns]
    dataframe = data.copy()
    raw_data = data.values
    # Get values not last column which is target column
    data = raw_data[:, 0:-1]
    #normalization of data
    data = ((data - data.min()) / (data.max() - data.min()))*2
    return data

#run the network traffic model
def run_network_model(data):
    #new data 
    X_new = data
    with open('gradient_boosting_model.pk', 'rb') as file:
        model = pickle.load(file)
        gb_predictions = model.predict(X_new)
        print(gb_predictions)
    return gb_predictions


def realtime_packet(packet_count):
    # Define the network interface to capture packets from
    interface_name = 'Ethernet 3'  # Replace with your actual interface name

    # Set up the BPF filter to exclude OPC UA packets on ports 4840 and 4841
    bpf_filter = 'not (port 4840 or port 4841)'

    # Create a live capture object with the BPF filter applied
    capture = pyshark.LiveCapture(interface=interface_name, bpf_filter=bpf_filter)

    # List to store packet information
    packet_info_list = []

    # Capture packets
    for packet in capture.sniff_continuously(packet_count):
        try:
            # Initialize packet_info with default values
            packet_info = {
                'Time': packet.sniff_timestamp,
                'Length': packet.length,
                'Protocol': packet.highest_layer,
                'Source': '',
                'Destination': '',
                'Source Port': '',
                'Destination Port': '',
                'Sequence Number': '',
                'Acknowledgment Number': '',
                'Time to Live': '',
                'Arrival Time': '',
                'S7 Communication': '',
                'Data length': '',
                'Function': '',
                'Length': '',
                'Byte Address': '',
                'Info': ''
            }

            # Check if the packet has an IP layer and extract fields if present
            if hasattr(packet, 'ip'):
                packet_info['Source'] = packet.ip.src
                packet_info['Destination'] = packet.ip.dst
                packet_info['Time to Live'] = packet.ip.ttl

            # Check if the packet has a TCP layer and extract fields if present
            if hasattr(packet, 'tcp'):
                packet_info['Source Port'] = packet.tcp.srcport
                packet_info['Destination Port'] = packet.tcp.dstport
                packet_info['Sequence Number'] = packet.tcp.seq
                packet_info['Acknowledgment Number'] = packet.tcp.ack
                if hasattr(packet.tcp, 'time_delta'):
                    packet_info['Time since previous frame in this TCP stream'] = packet.tcp.time_delta

            # Add protocol-specific information, such as S7COMM, if present
            if 'S7COMM' in packet:
                # Extract S7COMM-specific fields
                # Note: Replace 's7comm_field' with actual field names from the packet
                # packet_info['S7 Communication'] = packet.s7comm.s7comm_field
                pass  # Replace with actual field extraction for S7COMM

            # Convert timestamp to a readable format if necessary
            packet_info['Arrival Time'] = datetime.fromtimestamp(
                float(packet_info['Time'])
            ).strftime('%Y-%m-%d %H:%M:%S.%f')
            components = split_datetime(packet_info['Arrival Time'])

            # Add the split components to the packet_info dictionary
            packet_info.update(components)

            # Add the packet_info dictionary to our list
            packet_info_list.append(packet_info)

        except Exception as e:
            print(f"An error occurred while processing a packet: {e}")

    return packet_info_list

import os

def data_save(df, predictions_df, filename):
    if os.path.exists(filename):
        # If file exists, load the old data and append new data
        old_df = pd.read_csv(filename)
        updated_df = pd.concat([old_df, predictions_df], axis=0, ignore_index=True)
    else:
        # If file does not exist, start a new file with the current predictions
        updated_df = predictions_df
    
    # Save the updated DataFrame to a CSV file
    updated_df.to_csv(filename, index=False)

# Set a base file name
base_filename = 'network_output_model.csv'

# Here's the loop that would generate predictions and save them
for i in range(7000):  # Adjust the range as needed
    packet_info_list = realtime_packet(100)
    df = df_preprocess(packet_info_list)
    data = preprocessing(df)
    gb_predictions = run_network_model(data)
    
    # Create a DataFrame for predictions
    predictions_df = pd.DataFrame({
        'GB_Predictions': gb_predictions,
    })
    
    # Concatenate the predictions DataFrame with your new dataset
    result_df = pd.concat([df, predictions_df], axis=1)
    result_df = result_df[result_df['Protocol'] != 'LLDP']
    result_df = result_df[result_df['Protocol'] != 'SSDP']
    # Save the combined results to a CSV file
    data_save(df, result_df, base_filename)
    
    print(f"Batch {i} predictions saved.")


