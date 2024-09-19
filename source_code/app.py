from dash import Dash, dcc, Input, Output, html
import dash_bootstrap_components as dbc
import plotly.express as px

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
                    {'label': 'Problem 1 (n customers, n depots)', 'value': 0}, 
                    {'label': 'Problem 2 (n customers, n depots)', 'value': 1},
                    {'label': 'Problem 3 (n customers, n depots)', 'value': 2},
                    {'label': 'Problem 4 (n customers, n depots)', 'value': 3},
                    {'label': 'Problem 5 (n customers, n depots)', 'value': 4}
                ], 
                value=0,  # Default to 'Problem 1'
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
            html.H5("Visualised Problem (Map)"),  # Section title for the problem map
            dcc.Graph(id="problem-map", figure={}),  # Placeholder for the problem map
            
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
                         
            # Solutions history section
            html.Div([
                html.H5("Solutions History"),  # Section title for solutions history
                dcc.Graph(id="solution-history", figure={})  # Placeholder for solutions history
            ])
        ], width=5),  # Adjust width for the right column
    ], align="start"),  # Align content to the top
    
    html.Br(),  # Line break for spacing

], fluid=True)  # Use fluid layout for full-width display

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