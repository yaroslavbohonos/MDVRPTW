from dash import html

def getDescription():
    return html.Div(        
        id="problem-description", # Reference id of the section
        # Description styling
        children = "This application visualises solving the vehicle problem. It uses genetic algorithm to optimise vehicle routes based on genetic parameters. That is a practical and challenging problem in logistics and supply chain management of service vehicles used for delivery",
        style={"background-color": "#F8F9FA", "padding": "20px", "border-radius": "10px"}
    )