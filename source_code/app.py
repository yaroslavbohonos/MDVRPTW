from ReportsDB import DataBase
from dash import Dash, dcc, Input, Output, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import dash_ag_grid as dag
import pandas


DB = DataBase()

def add_legend_only_entry(fig, name, symbol, color, size, mode='markers', line_color=None):
    """Adds a legend-only entry (no actual data points) to the figure."""
    fig.add_trace(go.Scatter(
        x=[None], y=[None],  # No actual data point plotted
        mode=mode,
        marker=dict(size=size, symbol=symbol, color=color) if mode == 'markers' else None,
        line=dict(color=line_color) if mode == 'lines' else None,
        name=name,
        showlegend=True
    ))

def create_vrp_map():
    # Experimental data for with routes, customers and depots(including time windows):
    customers = [
        {"id": 1, "x": 5, "y": 10, "start_time": 9, "end_time": 16},
        {"id": 2, "x": 15, "y": 20, "start_time": 9, "end_time": 17},
        {"id": 3, "x": 25, "y": 15, "start_time": 10, "end_time": 18},
        {"id": 4, "x": 25, "y": 5, "start_time": 16, "end_time": 17},
    ]

    depots = [
        {"id": 1, "x": 0, "y": 0, "start_time": 9, "end_time": 18},
        {"id": 2, "x": 10, "y": 0, "start_time": 9, "end_time": 19},
    ]

    routes = [
        {"start_x": 0, "start_y": 0, "end_x": 5, "end_y": 10},  
        {"start_x": 5, "start_y": 10, "end_x": 15, "end_y": 20}, 
        {"start_x": 15, "start_y": 20, "end_x": 0, "end_y": 0},
        {"start_x": 10, "start_y": 0, "end_x": 25, "end_y": 15},
        {"start_x": 25, "start_y": 15, "end_x": 25, "end_y": 5},
        {"start_x": 25, "start_y": 5, "end_x": 10, "end_y": 0}
    ]

    # Initialise the map
    fig = go.Figure()
    
    # Change from standard blue to white background
    fig.update_layout(
        plot_bgcolor='white'
    )

    # Plot customers with time windows
    for customer in customers:
        fig.add_trace(go.Scatter(
            x=[customer['x']],
            y=[customer['y']],
            mode='markers+text', # Allows displaying not only icons but also contents of "text" next to icons
            textposition='top center',
            showlegend=False,  # Not displaying each customer in legend
            marker=dict(size=10, symbol='circle', color='blue'), # An icon for each customer
            text=f"[{customer['start_time']}, {customer['end_time']}]"
        ))

    # Plot depots with time windows
    for depot in depots:
        fig.add_trace(go.Scatter(
            x=[depot['x']],
            y=[depot['y']],
            mode='markers+text',
            textposition='top center',
            showlegend=False, 
            marker=dict(size=15, symbol='square', color='green'),
            text=f"[{depot['start_time']}, {depot['end_time']}]"
        ))

    # Plot route connection between a depot and customer(-s)
    for route in routes:
        fig.add_trace(go.Scatter(
            x=[route['start_x'], route['end_x']],
            y=[route['start_y'], route['end_y']],
            mode='lines',
            showlegend=False,
            line=dict(color='blue'),
            name="Route",
        ))

    # Add legend-only entries using the multi-figure function
    add_legend_only_entry(fig, name="Depot", symbol='square', color='green', size=15)
    add_legend_only_entry(fig, name="Customer", symbol='circle', color='blue', size=10)
    add_legend_only_entry(fig, name="Route", symbol=None, color=None, size=None, mode='lines', line_color='blue')

    # Axes properties for map
    axis_properties = dict(
        showgrid=False,
        showticklabels=False,
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black'
    )

    # Update layout with legend and map style
    fig.update_layout(
        xaxis = axis_properties,
        yaxis = axis_properties,
        showlegend=True,
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",  # Anchor it to the bottom
            y=-0.09,  # Position below the plot
            xanchor="center",
            x=0.5  # Center it horizontally
        ),
        margin=dict(l=10, r=10, t=30, b=80)  # Adjust margins to fit the legend
    )
    
    return fig

# Create solutions history table
def create_solutions_history(problemIndex=0):
    # Fetch problem data based on index
    solutions = DB.returnSolutions(problemIndex)  # Get solutions DataFrame from the DB

    # Define the column definitions
    columnDefs = [
        {"headerName": "Problem No.", "field": "ProblemID", "filter": "agNumberColumnFilter"},
        {"headerName": "Selection Type", "field": "SelectionType", "filter": "agTextColumnFilter"},
        {"headerName": "Mutation Prob", "field": "MutationProb", "filter": "agNumberColumnFilter"},
        {"headerName": "Distance", "field": "Distance", "filter": "agNumberColumnFilter"},
        {"headerName": "Date", "field": "Date", "filter": "agDateColumnFilter"},
        {"headerName": "Time", "field": "Time", "filter": "agTextColumnFilter"}
    ]
    
    # Create AgGrid table using solutions data
    return dag.AgGrid(
        id="solutions_history",
        rowData=solutions.to_dict("records"),  # Pass the solutions DataFrame as row data
        columnDefs=columnDefs,  # Use the defined columnDefs to structure the grid
        defaultColDef={"filter": True},  # Enable filtering for all columns
        columnSize="sizeToFit",  # Adjust columns to fit the content
        dashGridOptions={"animateRows": False}  # Disable row animation for performance
    )


# Initialise Dash app with Bootstrap theme for easier styling
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define app layout
app.layout = dbc.Container([

    # Row for title
    dbc.Row([
        dbc.Col(
            html.H1(
                "Visualisation of Multi-Depot Vehicle Routing Problem with Time Windows",
                className="text-center"
            ), 
            width=12
        )                       
    ], justify="center", style={"padding-top": "15px"}),  # Center title and add padding from top
    
    html.Hr(),  # Horizontal line separator
    
    # Row for main content, divided into 3 sections (left: parameters, center: map and description, right: fitness and history)
    dbc.Row([

        # Left column for parameter settings
        dbc.Col([
            html.Div([
                html.H5("Parameter Settings"),  # Section title              

                # Dropdown for choosing problem
                html.Label("Problem to be solved and displayed", style={"margin-top": "20px"}),
                dcc.Dropdown([ 
                    {'label': 'Problem 1 (n customers, n depots)', 'value': 1}, 
                    {'label': 'Problem 2 (n customers, n depots)', 'value': 2},
                    {'label': 'Problem 3 (n customers, n depots)', 'value': 3},
                    {'label': 'Problem 4 (n customers, n depots)', 'value': 4},
                    {'label': 'Problem 5 (n customers, n depots)', 'value': 5}
                ], 
                value=1,  # Default to 'Problem 1'
                searchable=False),  # Restrict user text input

                # Slider for start population size
                html.Label("Initial Population Size", style={"margin-top": "20px"}),
                dcc.Slider(
                    5, 50, 5,  # Range from 5 to 50, step size of 5
                    marks=None,
                    tooltip={"placement": "bottom", "always_visible": True}
                ),

                # Slider for number of iterations
                html.Label("Number of Iterations", style={"margin-top": "20px"}),
                dcc.Slider(
                    10, 500,  # Range from 10 to 500, custom marks on slider
                    marks={10: '10', 50: '50', 100: '100', 200: '200', 300: '300', 400: '400', 500: '500'},  
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                
                # Slider for mutation rate
                html.Label("Mutation Rate", style={"margin-top": "20px"}),
                dcc.Slider(
                    0.1, 1.0, 0.1,  # Range from 0.1 to 1.0, step size of 0.1
                    marks=None,
                    tooltip={"placement": "bottom", "always_visible": True}
                ),

                # Slider for Crossover Rate
                html.Label("Crossover Rate", style={"margin-top": "20px"}),
                dcc.Slider(
                    0.1, 1.0, 0.1,  # Range from 0.1 to 1.0, step size of 0.1
                    marks=None,
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            
                # Dropdown for Selection Method
                html.Label("Selection Method", style={"margin-top": "20px", "margin-bottom": "20px"}),  
                dcc.Dropdown(['Tournament', 'Roulette'], 'Tournament', searchable=False),  # Default to 'Tournament'

                # Button to trigger the visualization (Centered)
                html.Div(
                    html.Button('Run Visualization', id='run-btn', n_clicks=0, className="btn btn-primary"),
                    style={"display": "flex", "justify-content": "center", "margin-top": "20px"}  # Flexbox to center the button
                )
            ], style={"background-color": "#F8F9FA", "padding": "20px", "border-radius": "10px"})  # Styling for parameter section
        ], width=3),  # Adjust width for the left column
        
        # Center column for the problem visualization and description
        dbc.Col([
            html.H5("Visualised Problem Map"),  # Section title for the problem map
            dcc.Graph(id="problem-map", figure=create_vrp_map()),  # Placeholder for the problem map
            
            html.Br(),  # Line break for spacing
            
            # Problem description section
            html.H5("Problem Description"),  
            html.Div(id="problem-description", style={"background-color": "#F8F9FA", "padding": "20px", "border-radius": "10px"})  # Placeholder for problem description
        ], width=4),  # Adjust width for the center column
        
        # Right column for fitness graph and solutions history
        dbc.Col([
            # Fitness graph section
            html.Div([
                html.H5("Fitness Graph"),  # Section title for fitness graph
                dcc.Graph(id="fitness-graph", figure={})  # Placeholder for fitness graph
            ]),
            
            html.Br(),  # Line break for spacing
                    
            # Solutions History
            create_solutions_history(1)
        ], width=5),  # Adjust width for the right column
    ], align="start"),  # Align content to the top
    
    html.Br(),  # Line break for spacing

], fluid=True)  # Use fluid layout for full-width display


# Run the app
if __name__ == "__main__":
    app.run_server()


"""
The following code block interacts with the 'Reports' class to load depot and customer data for visualization:

DB = DataBase()

# Retrieve data for the first depot and customer sets
DepotData = DB.returnDepotData(0)
CustomerData = DB.returnCustomerData(0)

# Example of printing depot and customer data for debugging
print("Depots: ")
for row in DepotData:
    print(row)

print("Customers: ")
for row in CustomerData:
    print(row)
"""