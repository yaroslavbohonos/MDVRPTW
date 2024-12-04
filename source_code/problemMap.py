from dash import dcc
import plotly.graph_objects as go
import time

problemIndex = 1 # Initial plotted problem #1
fig = go.Figure() # Initialise map's object
isSolutionPlotted = False



# Add empty-coordinate objects as a visual for the legend of map
def addLegendOnlyEntry(fig, name, symbol, color, size, mode='markers', line_color=None):
    """Adds a legend-only entry (no actual data points) to the figure."""
    fig.add_trace( 
        go.Scatter(
            x=[None], y=[None],  # No actual data point plotted
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
                mode='markers+text', # Allows displaying not only icons but also contents of "text" next to icons
                textposition='top center',
                showlegend=False,  # Not displaying each customer in legend
                marker=dict(size=10, symbol='circle', color='blue'), # An icon for each customer
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

def plotRoutes(solution):
    # Plot a route connection between a depot and customer(-s)
    for route in solution.routes:
        for i in range(len(route) - 1):
            start=route[i]
            end=route[i+1]
            try:
                fig.add_annotation(
                    x=end.X,
                    y=end.Y,
                    ax=start.X,
                    ay=start.Y,
                    xref="x",
                    yref="y",
                    axref="x",
                    ayref="y",
                    showarrow=True,
                    arrowhead=3,      
                    arrowsize=2,      
                    arrowwidth=1,   
                    arrowcolor="black",
                    name = "Route"
                )
            except:
                invalidValues= [end.X,
                                end.Y,
                                start.X,
                                start.Y ]
                print()
                print("Invalid values error: printing values caused this:", invalidValues)
                print()


def clearRoutes():
    #fig.update_annotations(showarrow = False, visible = False)
    #temp = list(fig.layout.annotations)
    #temp.clear()
    #fig.layout.annotations = tuple(temp)
    fig.layout.annotations = ()


def clearProblemMap():
    fig.data = []
    addLegendOnlyEntries()
   

def updateProblemMap(DB, sol, index):
    global problemIndex
    if problemIndex != index:
        clearProblemMap()
        problemIndex = index
    clearRoutes()
    if sol != None: # Avoid plotting an empty Solutions list
        plotRoutes(sol)
        #sol.clear() # Avoid reploting after changing problem, plot only a new solution
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
            orientation="h",  # Horizontal legend
            yanchor="bottom",  # Anchor legend to the bottom
            y=-0.09,  # Position legend below the plot
            xanchor="center",
            x=0.5  # Center legend horizontally
        ),
        margin=dict(l=0, r=0, t=5, b=50)  # Adjust margins to fit the legend
    )

    return dcc.Graph(
        id="problem-map",                # Reference id of the section
        style={"margin-bottom": "20px"}, # Add space below the map
        figure=fig
    )