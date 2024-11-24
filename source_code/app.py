# Classes 
import dash
from GeneticAlgorithm import GeneticAlgorithm
from Database import Database 
# Visual components 
from problemMap import getProblemMap, updateProblemMap
from solutionsHistory import getSolutionsHistory, updateSolutionsHistory
from parameterSettings import getParameterSettings
from description import getDescription
from instructions import getInstructions
# Dash and logic
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import dash_ag_grid as dag
import pandas
import time




# Initialise Dash app with Bootstrap theme for easier styling
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
DB = Database() # Initialise DB as DataBase object
DB.loadTables() # Create and/or clear up Solutions entity

# Initialising the GeneticAlgorithm object
GA = GeneticAlgorithm()
isSolvedProblem = False

# Define app layout
app.layout = dbc.Container(
    [
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
        # (left: instructions and parameters, center: map and description, right: fitness and history)
        dbc.Row(
            [
                # Left column for instructions and parameter settings section
                dbc.Col(
                    [
                        getInstructions(),
                        getParameterSettings()
                    ], width=3                    # Set 4 out of 12 for the map and description section
                ),
                
                # Center section with problem map and description
                dbc.Col(
                    [
                        html.H5("Visualised Problem Map"),  # Section title
                        getProblemMap(DB, 1),
                        dcc.Store(id="solution-state", data=0), # Store to track solution number within bestSolutions
                        dcc.Store(id="ga-completion-status", data="unsolved"),
                        html.H5("Problem Description"),  # Section title
                        getDescription()
                    ], width=4                    # Set 4 out of 12 for the map and description section
                ),
                
        
                # Right section with fitness graph and solutions history
                dbc.Col(
                    [
                        # Fitness graph section
                        html.Div(
                            [
                                html.H5("Fitness Graph"),            # Title
                                dcc.Graph(
                                    id="fitness-graph",              # Reference id of the graph
                                    style={"margin-bottom": "20px"}, # Add space below
                                    figure={}
                                )                       # Placeholder for fitness graph
                            ]
                        ),
            
                        # Solutions History
                        html.H5("Solutions History"),  # Section title  
                        getSolutionsHistory()
                    ], 
                 width=5), # Set 5 out of 12 for the graph and solutions section
            ], align="start" # Align content to the top
        ),  
    ], 
fluid=True)  # Use fluid layout for full-width display




# CALLBACKS(instant web updates) for interactivity between components in Dash


bestSolutions = []
# Callback to run GA to record GA parameters and problem index
@app.callback(
    Output("ga-completion-status", "data"),
    Input("run-btn", "n_clicks"),              # Trigger the callback by pressing the button
    State("problems-dropdown", "value"),       # State: each input from the callback to a function
    State("population-slider", "value"),
    State("iterations-slider", "value"),
    State("crossover-slider", "value"),
    State("selection-dropdown", "value"),
    State("speed-slider", "value"),
    running=[                                  # Disable the run button while the callback is running
        (Output("run-btn", "disabled"), True, False)
    ],
    prevent_initial_call=True                  # Don't run the callback when the app loads
)
def runVisualisation(nClicks, problemIndex, initPopSize, numGenerations,
                     crossoverRate, selectionType, speedRate):
    global bestSolutions
    print("solving is started")
    # Call record_parameters and get the returned params
    params = GA.recordParameters(problemIndex, initPopSize, numGenerations, 
                                 0, crossoverRate, selectionType)
    GA.recordProblemData(DB)
    GA.evolvePopulation()
    DB.recordSolution(GA)
    bestSolutions = list(GA.bestSolutions.values())
    print("solving is done")
    return "solved"
    # Return change the ga status


# Callback to update the Problem Map when the problem no. dropdown is changed and after each new solution
@app.callback(
    Output("problem-map", "figure"),
    Input("run-btn", "n_clicks"), 
    Input("ga-completion-status", "data"), # Triggers after the GA generates a solution
    Input("problems-dropdown", "value"),   # Triggers after a prolbem index is changed
    Input("solution-state", "data"),
    prevent_initial_call = True 
)
def updateMap(nClicks, data, problemIndex, state):
    print("updateMap callback was called") 
    return updateProblemMap(DB, GA.bestSolution, problemIndex)
    """
    if state >= len(bestSolutions):
        fig = updateProblemMap(DB, None, problemIndex)
        return fig, state
    else:
        solutionToPlot = bestSolutions[state]
        time.sleep(5)
        fig = updateProblemMap(DB, solutionToPlot, problemIndex)
        return fig, state + 1
    """



# Callback to udpate Fitness Graph after each new solution



# Callback to udpate Solutions History after each new solution
@app.callback(
    Output("solutions_history", "rowData"),
    Input("ga-completion-status", "data"),    # Triggers after the GA generates a solution
    State("problems-dropdown", "value"),
    prevent_initial_call=True 
)
def updateSolutions(nClicks, problemIndex):
    return updateSolutionsHistory(DB, problemIndex)




# Run web appplication
if __name__ == "__main__":
    app.run_server()