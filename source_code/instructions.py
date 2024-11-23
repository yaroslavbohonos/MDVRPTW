from dash import html

def getInstructions():
    return html.Div(
        [
            html.H5("Instructions"),  # Title for instructions section 
            html.P("Follow steps to run the visualisation:"),
            html.Ul(
                [
                    html.Li("Select a problem from the dropdown list"),
                    html.Li("Adjust the genetic parameters"),
                    html.Li("Click 'Run Visualisation' to start the visualisation"),
                    html.Li("Graphs will be updated with current solving data"),
                ]
            ),
        ],
        style={"background-color": "#F8F9FA", "padding": "20px", "border-radius": "10px", "margin-bottom": "20px"}  # Styling for the instructions section
    )
