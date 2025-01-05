# Classes 
from GeneticAlgorithm import GeneticAlgorithm
from Database import Database 
# Visual components 
from problemMap import getProblemMap, updateProblemMap
from solutionsHistory import getSolutionsHistory, updateSolutionsHistory
from parameterSettings import getParameterSettings
from description import getDescription
from instructions import getInstructions
from fitnessGraph import getFitnessGraph, getFig, updateFitnessGraph
# Dash and logic
from dash import Dash, dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import dash_ag_grid as dag
import pandas
import time
import os




# Initialise Dash app with Bootstrap theme for easier styling
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
DB = Database() # Initialise DB as DataBase object
DB.loadTables() # Create and/or clear up Solutions entity

# Initialising the GeneticAlgorithm object
GA = GeneticAlgorithm()

# Define app layout
app.layout = dbc.Container(
    [
        # Row for web-application title
        dbc.Row([
            dbc.Col(
                html.H4(
                    "Visualisation of Solving Multi-Depot Vehicle Routing Problem with Time Windows",
                    className="text-center" # Centre the title
                ),
                
                width=12 # Set max width size
            )],
            # Pin the to center
            justify="center", 
            # Styling for the main title
            # Title colour - white, padding top is added to make equal distances from top and bottom
            style={"padding-top": "5px","margin-bottom": "10px", "background-color": "#7d858c", "color": "white"}
        ),  
        
        #html.Hr(style={"margin-top": "0px"}),  # Horizontal line separator
    
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
                
                # Trigger needed for live updates of fitness graph and problem map
                # n_intervals represent a current position in bestSolutions
                dcc.Interval(id="speed-update", interval=1000, n_intervals=0, disabled=True),  # Initially disabled
                
                # Center section with problem map and description
                dbc.Col(
                    [
                        html.H5("Visualised Problem Map"), # Section title
                        getProblemMap(DB, 1),
                        #html.H5("Problem Description"), # Section title
                        getDescription()
                    ], width=5 # Set 5 out of 12 for the map and description section
                ),
                
        
                # Right section with fitness graph and solutions history
                dbc.Col(
                    [
                        # Fitness graph section
                        html.Div(
                            [
                                html.H5("Fitness Graph"), # Title
                                getFitnessGraph()            
                            ]
                        ),
            
                        # Solutions History
                        html.H5("Solutions History"),  # Section title  
                        getSolutionsHistory()
                    ], 
                 width=4), # Set 4 out of 12 for the graph and solutions section
            ], align="start" # Align content to the top
        ),  
    ], 
fluid=True)  # Use fluid layout for full-width display




# CALLBACKS(instant web updates) for interactivity between components in Dash

bestSolutions=[]
iterationLabels=[]

startTime = 0
endSolvingTime = 0
startDisplayingTime = 0

# Callback: Updates the displaying speed 
@app.callback(
    Output("speed-update", "interval"),
    # Current speed value (0 or 0.5 or 1)
    Input("speed-slider", "value"),
    # Triggers when interval is changed
    Input("speed-update", "disabled"),
    prevent_initial_call=True
)
def updateSpeed(speed, _):
    if speed == 0:
        return 5000
    elif speed == 0.5:
        return 1000
    else:
        return 250


# Callback: Update Problem Map and Fitness Graph Dynamically
@app.callback(
    Output("problem-map", "figure"),
    Output("speed-update", "disabled"),
    Output("fitness-graph", "figure"),
    # Triggers when a new problem is selected on dropdown
    Input("problems-dropdown", "value"), 
    # Represent a position in bestSolutions
    # Triggers when interval is changed
    Input("speed-update", "n_intervals"),
    prevent_initial_call=True
)
def updateMapAndFitness(problemIndex, pos):
    global startDisplayingTime
    #Determines what input triggered the callback
    triggeredId = ctx.triggered_id
    mapFig=None
    fitnessFig=None
    isDisabled = None

    if triggeredId == "problems-dropdown":
        mapFig = updateProblemMap(DB, None, problemIndex)
        isDisabled = True
        fitnessFig = getFig()
    else:
        if startDisplayingTime == 0:
            startDisplayingTime = time.time()
            print(f"Time taken to display after start of the solving {startDisplayingTime-startTime} sec.")
        mapFig, isDisabled = drawMap(problemIndex, pos)
        fitnessFig = updateFitnessGraph(pos, bestSolutions, iterationLabels)
    
    return mapFig, isDisabled, fitnessFig

def drawMap(problemIndex, pos):
    #global bestSolutions
    # Check if position is reached 2nd element from the end
    if pos > len(bestSolutions)-2 and bestSolutions:
        # 2nd sol from the end because last solution is duplicated 
        # This makes fitness graph obvious to interpret and continious
        return updateProblemMap(DB, bestSolutions[-1], problemIndex), True 
    else:
        # Generate figure that based on position in bestSolutions
        return updateProblemMap(DB, bestSolutions[pos], problemIndex), False


# Callback to run GA to record GA parameters and problem index
@app.callback(
    #Output("ga-completion-status", "data"),
    Output("speed-update", "disabled", allow_duplicate=True),
    Output("speed-update", "n_intervals"),
    Input("run-btn", "n_clicks"),              # Trigger the callback by pressing the button
    State("problems-dropdown", "value"),       # State: each current input on given element
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
def runVisualisation(n_clicks, problemIndex, initPopSize, numGenerations, crossoverRate, selectionType, speedRate):
    global startTime, endSolvingTime,startDisplayingTime
    startDisplayingTime=0
    startTime = time.time()
    # Record parameters and get the returned params
    GA.recordParameters(problemIndex, initPopSize, numGenerations, 0, crossoverRate, selectionType)
    GA.recordProblemData(DB)
    GA.evolvePopulation()
    DB.recordSolution(GA)
    
    global bestSolutions, iterationLabels
    # Create best solution list for easier access of the dictinary within GA
    bestSolutions = list(GA.bestSolutions.values())
    iterationLabels = list(GA.bestSolutions.keys())
    #print(f"number of best solutions  {len(bestSolutions)}")
    #print("Min. distances")
    for sol in bestSolutions:
        print(sol.fitness)
    #print(f"number of iteration labels {len(iterationLabels)}")
    #print(f"iteration labels {iterationLabels}")
 
    endSolvingTime = time.time()
    print(f"Time taken to solve a problem: {endSolvingTime - startTime} sec.")
    # Activate and reset the live updates trigger 
    return False, 0


# Callback to udpate Solutions History after each new solution
@app.callback(
    Output("solutions_history", "rowData"),
    # Triggers when GA finishes or a new problem is plotted
    Input("speed-update", "disabled"),
    # Triggers when a new problem is selected on dropdown
    State("problems-dropdown", "value"),
    prevent_initial_call=True 
)
def updateSolutions(_, problemIndex):
    return updateSolutionsHistory(DB, problemIndex)




# Run web appplication
if __name__ == "__main__":
    app.run_server()