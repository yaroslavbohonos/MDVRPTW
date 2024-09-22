from numpy import ma
from ReportsDB import DataBase
from dash import Dash, dcc, html, Input, Output, State
from GeneticAlgorithm import GeneticAlgorithm
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import dash_ag_grid as dag
import pandas

# Initialise Dash app with Bootstrap theme for easier styling
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

DB = DataBase() # Initialise DB as DataBase object

# Add empty-coordinate objects as a visual for the legend of map
def add_legend_only_entry(fig, name, symbol, color, size, mode='markers', line_color=None):
    """Adds a legend-only entry (no actual data points) to the figure."""
    fig.add_trace(go.Scatter(
        x=[None], y=[None],  # No actual data point plotted
        mode=mode,
        # Passing shape inputs as icons to the legend visual
        marker=dict(size=size, symbol=symbol, color=color) if mode == 'markers' else None,
        # If a icon represent a line
        line=dict(color=line_color) if mode == 'lines' else None,
        name=f"<b>{name}</b>",
        showlegend=True
    ))

# Returning a problem map figure 
def create_vrp_map():
    # Experimental data with routes for customers and depots(including time windows):
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

    # Initialise map's object
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
            text=f"<b>[{customer['start_time']}, {customer['end_time']}]</b>"
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
            text=f"<b>[{depot['start_time']}, {depot['end_time']}]</b>"
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
    # Add a legend-only time window with "text" shape as bold text
    add_legend_only_entry(fig, name="[Start, End] - Time Window", symbol=None, color=None, size=None, mode='text')

    # Properties of map's axes
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
            yanchor="bottom",  # Anchor legend to the bottom
            y=-0.09,  # Position legend below the plot
            xanchor="center",
            x=0.5  # Center legend horizontally
        ),
        margin=dict(l=10, r=10, t=30, b=80)  # Adjust margins to fit the legend
    )
    
    return fig

# Create solutions history table
def create_solutions_history(problemIndex=1):
    # Fetch problem data based on index
    solutions = DB.returnSolutions(problemIndex)  # Get solutions DataFrame from the DB

    # Define the column titles and make them sortable
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
        id="solutions_history", # Reference id of the table
        style={"margin-bottom": "20px"}, # Add space below the table
        rowData=solutions.to_dict("records"),  # Pass the solutions DataFrame as row data
        columnDefs=columnDefs,  # Use the defined columnDefs to structure the grid
        # (include later except of the Problem No column)
        defaultColDef={"filter": True},  # Enable filtering for all columns 
        columnSize="autoSize",  # Adjust columns automatically to fit titles
        dashGridOptions={"animateRows": False}  # Disable row animation for better performance
    )

# Initialising the GeneticAlgorithm object as "ga"
GA = GeneticAlgorithm()

# Define app layout
app.layout = dbc.Container([

    # Row for web-application title
    dbc.Row([
        dbc.Col(
            html.H1(
                "Visualisation of Multi-Depot Vehicle Routing Problem with Time Windows",
                className="text-center" # Centre the title
            ), 
            width=12 # Set max width size
        )                       
    ], justify="center", style={"padding-top": "15px"}),  # Center title and add padding from top
    
    html.Hr(),  # Horizontal line separator
    
    # Row for main content, divided into 3 sections 
    # (left: parameters, center: map and description, right: fitness and history)
    dbc.Row([
        # Left column for parameter settings section
        dbc.Col([
            html.Div([
                html.H5("Parameter Settings"),  # Section title              

                # Label for dropdown and add space above
                html.Label("Problem to be solved and displayed", style={"margin-top": "20px"}), 
                # Dropdown for choosing problem
                dcc.Dropdown(
                    id='problems-dropdown', # Reference id of the dropdown
                    options=[ # Options with titles and reference values
                        {'label': 'Problem 1 (n customers, n depots)', 'value': 1},
                        {'label': 'Problem 2 (n customers, n depots)', 'value': 2},
                        {'label': 'Problem 3 (n customers, n depots)', 'value': 3},
                        {'label': 'Problem 4 (n customers, n depots)', 'value': 4},  
                        {'label': 'Problem 5 (n customers, n depots)', 'value': 5}],
                    value=1,  # Default to 'Problem 1'
                    searchable=False, # Restrict user text input,
                    clearable=False  # Disable the clear option (no "x" icon)
                ),  

                # Label for slider and add space above
                html.Label( "Initial Population Size", style={"margin-top": "20px"}),
                # Slider for start population size    
                dcc.Slider(
                    id='population-slider', # Reference id of the slider
                    # Range from 5 to 50, step size of 5
                    min=5, max=50, step=5,
                    value=10, # Default to 10
                    # Custom marks on slider allows navigate users on slider's limit
                    marks={5: '5', 50: '50'},
                    tooltip={"placement": "bottom", "always_visible": True} # current value constant displaying
                ),

                # Label for slider and add space above
                html.Label("Number of Iterations", style={"margin-top": "20px"}),
                # Slider for number of iterations
                dcc.Slider(
                    id='iterations-slider', # Reference id of the slider
                    # Range from 10 to 500
                    min=10, max=500, step=10,
                    value=200, # Default to 200
                    # Custom marks on slider allows navigate users on inputs and slider's limit
                    marks={10: '10', 50: '50', 100: '100', 200: '200', 300: '300', 400: '400', 500: '500'},  
                    tooltip={"placement": "bottom", "always_visible": True} # current value constant displaying
                ),
                
                # Label for slider and add space above
                html.Label("Mutation Rate", style={"margin-top": "20px"}),
                # Slider for mutation rate
                dcc.Slider(
                    id='mutation-slider', # Reference id of the slider
                    # Range from 0.1 to 1.0, step size of 0.1
                    min=0, max=1, step=0.1,
                    value=0.5, # Default to 0.5
                    # Custom marks on slider allows navigate users on inputs and slider's limit
                    marks= {0: '0', 1: '1'},
                    tooltip={"placement": "bottom", "always_visible": True, } # current value constant displaying
                ),

                # Label for slider and add space above 
                html.Label("Crossover Rate", style={"margin-top": "20px"}),
                # Slider for Crossover Rate
                dcc.Slider(
                    id='crossover-slider',  # Reference id of the slider
                    # Range from 0.1 to 1.0, step size of 0.1
                    min=0, max=1, step=0.1,
                    value=0.4, # Default to 0.4
                    # Custom marks on slider allows navigate users on inputs and slider's limit
                    marks={0: '0', 1: '1'},
                    tooltip={"placement": "bottom", "always_visible": True} # current value constant displaying
                ),
            
                # Label for dropdown and add space above 
                html.Label("Selection Method", style={"margin-top": "20px"}),  
                # Dropdown for Selection Method
                dcc.Dropdown(
                    id='selection-dropdown', # Reference id of the dropdown
                    options=[                # Options with titles and reference values
                        {'label': 'Tournament', 'value': 'Tournament'}, 
                        {'label': 'Roulette', 'value': 'Roulette'}
                    ],
                    value='Tournament', # Default to Tournament
                    searchable=False,   # Disable search option
                    clearable=False     # Disable the clear option (no "x" icon)
                ),

                # Button to trigger the visualisation (Centered)
                html.Div(
                    html.Button('Run Visualisation',        # Label
                                id='run-btn',               # Reference ID of the button 
                                # It triggers a callback and use the value of n_clicks in your callback logic
                                n_clicks=0,                 # Counter determines if button was pressed
                                className="btn btn-primary" # Primary action in a set of buttons
                    ), 
                    # Flexbox to center the button
                    style={"display": "flex", "justify-content": "center", "margin-top": "20px"}  
                )
            # Parameter settings styling
            ], style={"background-color": "#F8F9FA", "padding": "20px", "border-radius": "10px"})  
        ], width=3), # Adjust width for the left column
        
        # Center section of problem map and description
        dbc.Col([
            html.H5("Visualised Problem Map"),   # Title 
            dcc.Graph(
                id="problem-map",                # Reference id of the section
                style={"margin-bottom": "20px"}, # Add space below the map
                figure=create_vrp_map()),        # Creating the graph of visualised problem
            
            # Title
            html.H5("Problem Description"),  
            html.Div(
                id="problem-description", # Reference id of the section
                # Description styling
                style={"background-color": "#F8F9FA", "padding": "20px", "border-radius": "10px"})
            ], width=4                    # Set 4 out of 12 for the map and description section
        ),
        
        # Right section of fitness graph and solutions history
        dbc.Col([
            # Fitness graph section
            html.Div([
                html.H5("Fitness Graph"),            # Title
                dcc.Graph(
                    id="fitness-graph",              # Reference id of the graph
                    style={"margin-bottom": "20px"}, # Add space below
                    figure={})                       # Placeholder for fitness graph
            ]),
            
            # Solutions History
            create_solutions_history(1)
            ], width=5), # Set 5 out of 12 for the graph and solutions section
        ], align="start" # Align content to the top
    ),  

], fluid=True)  # Use fluid layout for full-width display



# CALLBACKS for interactivity between components in Dash

# Callback to run GA to record GA parameters and problem index
@app.callback(
    Input("run-btn", "n_clicks"),              # Trigger the callback by pressing the button
    State("problems-dropdown", "value"),       # State: each input from the callback to a function
    State("population-slider", "value"),
    State("iterations-slider", "value"),
    State("mutation-slider", "value"),
    State("crossover-slider", "value"),
    State("selection-dropdown", "value"),
    prevent_initial_call=True                  # Don't run the callback when the app loads
)
def run_visualisation(n_clicks, problem_index, init_pop_size, num_generations,
                      mutation_rate, crossover_rate, selection_type):
    # Call record_parameters and get the returned params
    params = GA.record_parameters(
        problem_index, init_pop_size, num_generations, mutation_rate, crossover_rate, selection_type
    )

# Run web appplication
if __name__ == "__main__":
    app.run_server()