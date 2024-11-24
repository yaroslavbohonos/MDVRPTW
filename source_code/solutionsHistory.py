from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import dash_ag_grid as dag
import pandas

# Create solutions history table
def getSolutionsHistory(problemIndex=1):
    # Fetch problem data based on index
    # solutions = DB.returnSolutions(problemIndex)  # Get solutions DataFrame from the DB

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
    #global solutionsHistory 
    solutionsHistory = dag.AgGrid(
        id="solutions_history", # Reference id of the table
        style={"margin-bottom": "20px"}, # Add space below the table
        rowData = [],  # Create row data for future solutions
        columnDefs=columnDefs,  # Use the defined columnDefs to structure the grid
        # (include later except of the Problem No column)
        defaultColDef={"filter": True},  # Enable filtering for all columns 
        columnSize="autoSize",  # Adjust columns automatically to fit titles
        dashGridOptions={"animateRows": False}  # Disable row animation for better performance
    )

    return solutionsHistory

def updateSolutionsHistory(DB, problemIndex):
    #global solutionsHistory
    newSolutions = (DB.returnSolutions(problemIndex)).to_dict("records")  # Get solutions DataFrame from the DB
    return newSolutions