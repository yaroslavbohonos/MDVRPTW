import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
import pandas as pd

df = pd.DataFrame(columns=['Iteration', 'Distance'])
#fig = px.line(df, x='Iteration', y='Distance', markers=True)
fig = go.Figure()        

def getFitnessGraph():
    global fig
    fig.add_trace(
        go.Scatter( 
            mode='lines+markers', 
            name='Fitness'
        )
    )

    # Update of map's axes 
    fig.update_xaxes(
        title = 'Iteration',
        range = [-5, 503],
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey',
        zeroline=True,  # Makes y=0 line is visible
        zerolinecolor='black',  # Makes the line black
        zerolinewidth=2  # Makes the line thicker
    )    
    
    fig.update_yaxes(
        title='Min. Distance', 
        range=[0, 1000],
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey',
        zeroline=True,  # Makes x=0 line is visible
        zerolinecolor='black',  # Makes the line black
        zerolinewidth=2  # Makes the line thicker
    )
    
    fig.update_layout(
        plot_bgcolor='white',
        margin=dict(l=0, r=0, t=5, b=50)
    )
        
    return dcc.Graph(
        id="fitness-graph",              # Reference id of the section
        style={"margin-bottom": "20px"}, # Add space below the map
        figure=fig                       # Placeholder for figure
    )

def getFig():
    fig.data[0].x = ()
    fig.data[0].y = ()
    return fig

def updateFitnessGraph(pos, solutions, iterations):
    #global problemIndex
    # Select only needed data incrementally
    # Created for live updates
    currentSolutions = solutions[:pos + 1]
    currentIterations = iterations[:pos + 1]
    xData = currentIterations
    yData = [row.fitness for row in currentSolutions]
    # Update existing trace data
    fig.data[0].x = xData
    fig.data[0].y = yData
    return fig