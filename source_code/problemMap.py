from dash import dcc
import plotly.graph_objects as go
import time
import plotly.express as px


problemIndex = 1 # Initial plotted problem #1
fig = go.Figure() # Initialise map's object


# Add empty-coordinate objects as a visual for the legend of map
def addLegendOnlyEntry(fig, name, symbol, color, size, mode='markers', line_color=None):
    """Adds a legend-only entry (no actual data points) to the figure."""
    fig.add_trace( 
        go.Scatter(
            # Nothing is plotted on the map
            x=[None], y=[None],  
            mode=mode,
            # Passing shape inputs as icons to the legend visual
            marker=dict(size=size, symbol=symbol, color=color) if mode == 'markers' else None,
            # If a icon represent a line
            line=dict(color=line_color) if mode == 'lines' else None,
            name=f"<b>{name}</b>",
            showlegend=True
        )
    )

def addLegendOnlyEntries():
    # Add legend-only entries using the multi-figure function 
    addLegendOnlyEntry(fig, name="Depot", symbol='square', color='green', size=15)
    addLegendOnlyEntry(fig, name="Customer", symbol='circle', color='blue', size=10)
    addLegendOnlyEntry(fig, name="Route", symbol=None, color=None, size=None, mode='lines', line_color='blue')
    # Add a legend-only time window with "text" shape as bold text
    addLegendOnlyEntry(fig, name="[Start, End]  Time Window", symbol=None, color=None, size=None, mode='text')


def plotCustomers(customers):
    # Plot customers with time windows
    for customer in customers:
        fig.add_trace(
            go.Scatter(
                x=[customer[1]],
                y=[customer[2]],
                # Allows displaying not only icons but also contents of "text" next to icons
                mode='markers+text',
                textposition='top center',
                # Not displaying each customer in legend
                showlegend=False,
                # An icon for each customer
                marker=dict(size=10, symbol='circle', color='blue'), 
                text=f"<b>[{customer[4]}, {customer[5]}]</b>",
                name="Customer",
            )
        )


def plotDepots(depots):
    # Plot depots with time windows
    for depot in depots:
        fig.add_trace(
            go.Scatter(
                x=[depot[1]],
                y=[depot[2]],
                mode='markers+text',
                textposition='top center',
                showlegend=False, 
                marker=dict(size=15, symbol='square', color='green'),
                text=f"<b>[{depot[4]}, {depot[5]}]</b>",
                name="Depot",
            )
        )  

            
# Colourblind-friendly colours
routeColors = px.colors.qualitative.Safe               

def plotRoutes(solution):
    # Plot a route connection between a depot and customer(-s)
    # Counter for uniqueness of colours
    counter = 0
    for route in solution.routes:
        # Set a different colour for each route
        colour = routeColors[ counter % len(routeColors)]
        for i in range(len(route) - 1):
            start=route[i]
            end=route[i+1]
            fig.add_trace(
                go.Scatter(
                    x=[start.X, end.X],
                    y=[start.Y, end.Y],
                    mode="lines+markers",
                    line=dict(color=colour, width=2),
                    marker=dict(size=12, symbol="arrow-bar-up", angleref="previous", color=colour),
                    showlegend=False,
                    name="Route"
                )
            )
        counter+=1    
    return fig
    

def clearProblemMap():
    fig.data=()
    addLegendOnlyEntries()
   

def updateProblemMap(DB, sol, index):
    global problemIndex
    problemIndex = index
    clearProblemMap()
    # Avoid plotting an empty list of solutions
    if sol != None:
        plotRoutes(sol)
    depots = DB.returnDepotData(problemIndex)
    customers = DB.returnCustomerData(problemIndex)
    plotDepots(depots)
    plotCustomers(customers)
    return fig
    

def getProblemMap(DB, problemIndex):    
    # Change from standard blue to white background
    fig.update_layout(plot_bgcolor='white')

    depots = DB.returnDepotData(problemIndex)
    customers = DB.returnCustomerData(problemIndex)
    plotDepots(depots)
    plotCustomers(customers)

    addLegendOnlyEntries()
    
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
            # Horizontal legend
            orientation="h",  
            # Anchor legend to the bottom
            yanchor="bottom",  
            # Position legend below the plot
            y=-0.09,  
            xanchor="center",
            # Center legend horizontally
            x=0.5  
        ),
        # Adjust margins to fit the legend
        margin=dict(l=0, r=0, t=5, b=50)  
    )

    return dcc.Graph(
        # Reference id of the section
        id="problem-map",                
        # Add space below the map
        style={"margin-bottom": "20px"}, 
        figure=fig
    )