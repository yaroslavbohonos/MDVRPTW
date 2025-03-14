from dash import html

def getDescription():
    return html.Div(
        [   # Title
            html.H5("Description"), 
            # Text
            html.P("What is the visualisation about?"),
            html.P("It's a live solving of a delivery problem by the genetic algorithm. All results are shown on the delivery map and fitness graph that shows any changes in the solutions over iterations."),
            html.P("What is the problem being used?"),
            html.P("The problem involves delivery of goods from depots to customers. We assume that each customer must be visited once and within their time window, and each transport have limited weight capacity. The main goal is to reduce the total distance of travelling and meet all used constraints. The problem is formally known as multi-depot vehicle routing problem with time windows."),
            html.P("How is the problem being solved?"),
            html.P("It is solved using a genetic algorithm that works like evolution in nature. First, it creates a population with both valid and invalid solutions. Then, they are improved step by step using methods like selection and crossover. This process is repeated many times that is called iterations. In the end, it picks a valid solution based on shortest distance. This is a heuristic approach so it focuses to find a good enough solution"),
            html.P("Why is the problem solved this way?"),
            html.P("The genetic algorithm performs great with many constraints. It explores a big range of solutions. And it can balance between validity of solutions and efficiency. That is why it is very effective for the logistic challenges."),                    
        ],
        # Styling for description section
        style={
            "background-color": "#dbdee1",
            "padding": "15px",
            "border-radius": "15px",
            "margin-bottom": "10px",
            "height": "285px",  # Fixed height
            "overflow-y": "auto",  # Enable vertical scrolling
        }
    )    