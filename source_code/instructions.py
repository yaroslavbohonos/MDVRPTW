from dash import html

def getInstructions():
    return html.Div(
        [
            html.H5("Instructions"),  # Title for instructions section 
            #html.P("Follow steps to run the visualisation:"),
            html.Ul(
                [
                    html.Li("Select a problem from the dropdown "),
                    html.Li("Adjust the genetic parameters below"),
                    html.Li("Press Run button to visualise solving"),
                    html.Li("Visuals are updated with current data"),
                ]
            ),
        ],
        # Styling for the instructions section
        style={"background-color": "#dbdee1", "padding": "15px", "border-radius": "15px", "margin-bottom": "15px"}   
    )
