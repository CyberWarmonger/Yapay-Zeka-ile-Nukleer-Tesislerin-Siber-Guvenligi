import plotly.graph_objs as go
from datetime import datetime
import dash
from dash import dcc, html, Input, Output
from dash.dash_table import DataTable
import plotly.express as px
import pandas as pd
import os
from flask import Flask
import dash_bootstrap_components as dbc

# Convert row with date and time components into a datetime object
def convert_to_datetime(row):
    return datetime(
        year=row['Year'],
        month=row['Month'],
        day=row['Day'],
        hour=row['Hour'],
        minute=row['Minute'],
        second=row['Second'],
        microsecond=int(row['Millisecond'] * 1000)  # Convert millisecond to microsecond
    )

def create_heatmap(df):
    # Convert 'Arrival Time' to datetime if it's not already, and sort
    df['Arrival Time'] = pd.to_datetime(df['Arrival Time'])
    df.sort_values('Arrival Time', inplace=True)

    # Define a custom colorscale for gradient representation
    custom_colorscale = [
        [0.0, 'green'],  # Normal traffic
        [0.5, 'white'],  # Midpoint - can represent average/uncertain
        [1.0, 'red']     # High level of anomalies
    ]

    # Ensure GB_Predictions are normalized between 0 and 1 for the gradient scale
    df['GB_Predictions_Normalized'] = df['GB_Predictions'].apply(lambda x: 1 if x > 0 else 0)

    # Creating the heatmap
    heatmap_fig = go.Figure(data=go.Heatmap(
        x=df['Arrival Time'], 
        y=[0]*len(df),  # Create a dummy y-axis with zeros, as we only want to use the x-axis and color
        z=df['GB_Predictions_Normalized'],  # Use the normalized predictions for color
        colorscale=custom_colorscale,  # Apply the custom colorscale
        showscale=True  # Show the colorscale for reference
    ))
    
    # Update layout for the figure
    heatmap_fig.update_layout(
        title="Anomalies Over Time",
        xaxis_title="Arrival Time",
        yaxis=dict(tickvals=[], ticktext=[]),  # Hide y-axis ticks as we are not using y-axis
        yaxis_visible=False,  # Hide y-axis completely
        height=200,  # Height of the heatmap
        margin=dict(l=20, r=20, t=40, b=20)  # Adjust margins as needed
    )
    
    return heatmap_fig




# Initialize the Flask server and Dash app
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Function to create smaller figures for the bar and pie charts
def create_small_fig(fig):
    fig.update_layout(height=400, width=400, margin=dict(l=20, r=20, t=40, b=20))
    return fig

# App layout
app.layout = dbc.Container(fluid=True, children=[
    html.H1("Network Traffic Anomaly Detection", className="mb-4"),
    dbc.Row(id="summary-row", children=[
        dbc.Col(html.Div(id="total-packets"), width=3),
        dbc.Col(html.Div(id="normal-packets"), width=3),
        dbc.Col(html.Div(id="anomaly-packets"), width=3),
        dbc.Col(html.Div(id="current-time"), width=3),
    ], className="mb-4"),
    dbc.Button("Scroll Down", id="scroll-button", className="mb-3", n_clicks=0),
    dbc.Row([
        dbc.Col(width=6, children=[
            dcc.Graph(id='prediction-bar-chart')
        ]),
        dbc.Col(width=6, children=[
            dcc.Graph(id='prediction-pie-chart')
        ]),
    ], justify="around"),
    html.Div(id="tables-container", children=[
        dbc.Row([
            dbc.Col(width=6, children=[
                html.H2("All Packets"),
                DataTable(
                    id='table-all-packets',
                    columns=[],
                    data=[],
                    filter_action='native',
                    sort_action='native',
                    page_action='native',
                    page_size=5,
                    style_table={'overflowY': 'scroll', 'maxHeight': '300px'},
                )
            ]),
            dbc.Col(width=6, children=[
                html.H2("Anomalies"),
                DataTable(
                    id='table-anomalies',
                    columns=[],
                    data=[],
                    filter_action='native',
                    sort_action='native',
                    page_action='native',
                    page_size=5,
                    style_table={'overflowY': 'scroll', 'maxHeight': '300px'},
                )
            ]),
        ]),
        dbc.Row([
            dbc.Col(width=12, children=[
                html.H2("Heatmap"),
                dcc.Graph(id='heatmap')
            ]),
        ]),
    ]),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # in milliseconds
        n_intervals=0
    ),
])

# Callback to update the content of the page
@app.callback(
    [Output('table-all-packets', 'data'), 
     Output('table-all-packets', 'columns'),
     Output('table-anomalies', 'data'), 
     Output('table-anomalies', 'columns'),
     Output('prediction-bar-chart', 'figure'), 
     Output('prediction-pie-chart', 'figure'),
     Output('total-packets', 'children'),
          Output('normal-packets', 'children'),
     Output('anomaly-packets', 'children'),
     Output('current-time', 'children'),
     Output('heatmap', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_content(n):
    # Check if the CSV file exists
    if os.path.exists('network_output_model.csv'):
        df = pd.read_csv('network_output_model.csv')
        
        # Convert time components to a datetime object and sort by this datetime
        df['Arrival Time'] = df.apply(convert_to_datetime, axis=1)
        df.sort_values('Arrival Time', inplace=True)
        
        # Processing for GB_Predictions to text for pie chart
        df['GB_Predictions_Text'] = df['GB_Predictions'].replace({0: 'Normal', 1: 'Anomaly'})
        
        # Calculating summary statistics
        total_packets = len(df)
        normal_packets = len(df[df['GB_Predictions'] == 0])
        anomaly_packets = len(df[df['GB_Predictions'] == 1])
        
        # Current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Anomaly counts for bar chart
        anomaly_counts = df['GB_Predictions_Text'].value_counts().reset_index()
        anomaly_counts.columns = ['GB_Predictions', 'Count']
        
        # Generating figures for the bar and pie charts
        bar_fig = px.bar(anomaly_counts, x='GB_Predictions', y='Count', title='Anomaly Counts')
        bar_fig = create_small_fig(bar_fig)
        
        pie_fig = px.pie(anomaly_counts, names='GB_Predictions', values='Count', title='Anomaly Distribution')
        pie_fig = create_small_fig(pie_fig)
        
        # Column names for the data tables
        columns = [{"name": i, "id": i} for i in df.columns]
        anomalies_df = df[df['GB_Predictions'] == 1]
        anomalies_columns = [{"name": i, "id": i} for i in anomalies_df.columns]
        
        # Create the heatmap figure
        heatmap_fig = create_heatmap(df)
        
        # Return all outputs
        return (df.to_dict('records'), columns, anomalies_df.to_dict('records'), anomalies_columns, 
                bar_fig, pie_fig, f"Total Packets: {total_packets}", f"Normal: {normal_packets}",
                f"Anomalies: {anomaly_packets}", f"Current Time: {current_time}", heatmap_fig)
    else:
        # If the CSV file doesn't exist, return empty data and placeholders
        return ([], [], [], [], {}, {}, "Total Packets: N/A", "Normal: N/A", 
                "Anomalies: N/A", "Current Time: N/A", go.Figure())

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)

