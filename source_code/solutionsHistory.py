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
        #{"headerName": "Problem No.", "field": "ProblemID", "filter": "agNumberColumnFilter"},
        #{"headerName": "Selection Type", "field": "SelectionType", "filter": "agTextColumnFilter"},
        {"headerName": "Crossover Prob", "field": "CrossoverProb", "filter": "agNumberColumnFilter"},
        {"headerName": "Distance", "field": "Distance", "filter": "agNumberColumnFilter"},
        {"headerName": "Date", "field": "Date", "filter": "agDateColumnFilter"},
        {"headerName": "Time", "field": "Time", "filter": "agTextColumnFilter"}
    ]

    # Create AgGrid table using solutions data
    #global solutionsHistory 
    solutionsHistory = dag.AgGrid(
        # Reference id of the table
        id="solutions_history", 
        style={
            # Add space below the table
            "margin-bottom": "20px", 
            # Fixed height
            "height": "250px" 
        }, 
        # Create row data for future solutions
        rowData = [],  
         # Use the defined columnDefs to structure the grid
        columnDefs=columnDefs, # (Remove later Problem No column) !!!!!
        # Enable filtering for all columns 
        defaultColDef={"filter": True},
        # Adjust columns automatically to fit titles
        columnSize="autoSize",
         # Disable row animation for better performance
        dashGridOptions={"animateRows": False} 
    )
    return solutionsHistory

def updateSolutionsHistory(DB, problemIndex):
    # Get solutions DataFrame from the DB
    newSolutions = (DB.returnSolutions(problemIndex)).to_dict("records")  
    return newSolutions