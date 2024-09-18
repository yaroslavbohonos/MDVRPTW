from dash import Dash, dcc, Input, Output, html
import dash_bootstrap_components as dbc
import plotly.express as px

# Initialise Dash app with Bootstrap theme for easier styling
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define app layout
app.layout = dbc.Container([

    # Row for title
    dbc.Row([
        dbc.Col(html.H1("Visualisation of Multi-Depot Vehicle Routing Problem with Time Windows",
                        className="text-center"), width=12)                       
    ], justify="center", style={"padding-top": "15px"}),  # Center title and add distance from top
    
    html.Hr(),  # Horizontal line separator
    
    # Row for main content, divided into 3 sections (left: parameters, center: map and description, right: fitness and history)
    # A page has max width of 12 inclusively 
    dbc.Row([

        # Left column for parameter settings
        dbc.Col([
            html.Div([
                html.H5("Parameter Settings"),  # Section title
                
                # Slider for start population size
                html.Label("Start Population Size"),
                # Validating input allowing only the given range
                dcc.Slider(10, 50, 5, marks=None,  # Range from 10 to 50, step size of 5
                    tooltip={"placement": "bottom", "always_visible": True}),
                
                html.Br(),  # Line break for spacing
                
                # Slider for mutation rate
                html.Label("Mutation Rate"),
                # Validating input allowing only the given range
                dcc.Slider(0.1, 1.0, 0.1, marks=None,  # Range from 0.1 to 1.0, step size of 0.1
                    tooltip={"placement": "bottom", "always_visible": True}),
                
                html.Br(),  # Line break for spacing

                # Slider for Crossover Rate
                html.Label("Crossover Rate"),
                # Validating input allowing only the given range
                dcc.Slider(0.1, 1.0, 0.1, marks=None,  # Range from 0.1 to 1.0, step size of 0.1
                    tooltip={"placement": "bottom", "always_visible": True}),
                
                html.Br(),  # Line break for spacing

                # Dropdown for Selection Method
                html.Label("Selection Method"),
                # Validating input allowing given options and restricting user text input
                dcc.Dropdown(['Tournament', 'Roulette'], 'Tournament', searchable=False),  # Default to 'Tournament'

                html.Br(),  # Line break for spacing
                
                # Button to trigger the visualisation
                html.Button('Run Visualization', id='run-btn', n_clicks=0, className="btn btn-primary")
            ], style={"background-color": "#F8F9FA", "padding": "20px", "border-radius": "10px"})  # Styling for parameter section
        ], width=4),  # Adjust width for the left column 
        
        # Center column for the problem visualisation and description
        dbc.Col([
            html.H5("Visualised Problem (Map)"),  # Section title for the problem map
            dcc.Graph(id="problem-map", figure={}),  # Mock-up problem map used for estimating layout size
            
            html.Br(),  # Line break for spacing
            
            # Problem description section
            html.H5("Problem Description"),  
            # Mock-up problem description used for estimating layout size
            html.Div(id="problem-description", style={"background-color": "#F8F9FA", "padding": "20px", "border-radius": "10px"})  
        ], width=4),  # Adjust width for the center column
        
        # Right column for fitness graph and solutions history
        dbc.Col([
            # Fitness graph section
            html.Div([
                html.H5("Fitness Graph"),  # Section title for fitness graph
                dcc.Graph(id="fitness-graph", figure={})  # Mock-up fitness graph used for estimating layout size
            ]),
            
            html.Br(),  # Line break for spacing
                         
            # Solutions history section
            html.Div([
                html.H5("Solutions History"),  # Section title for solutions history
                dcc.Graph(id="solution-history", figure={})  # Mock-up solutions history used for estimating layout size
            ])
        ], width=5),  # Adjust width for the right column
    ], align="start"),  # Align content to the top
    
    html.Br(),  # Line break for spacing

], fluid=True)  # Use fluid layout for full-width displaying

# Callbacks for interactive elements (e.g., updating graphs based on user input) will be added here

# Run the app
if __name__ == "__main__":
    app.run_server()

"""
The following code block interacts with the 'Reports' class to load depot and customer data for visualization:

DB = Reports()

# Load data from the tables in the database
DB.loadTables()

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