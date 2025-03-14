from dash import html

def getInstructions():
    return html.Div(
        [
            html.H5("Instructions"),  # Title for instructions section 
            #html.P("Follow steps to run the visualisation:"),
            html.Ul(
                [
                    html.Li("Select a problem from the dropdown "),
                    html.Li("Tune the genetic parameters below"),
                    html.Li("Press the run button to start solving"),
                    html.Li("Visuals are updated with solving data"),
                ]
            ),
        ],
        # Styling for the instructions section
        style={"background-color": "#dbdee1", "padding": "15px", "border-radius": "15px", "margin-bottom": "15px"}   
    )
