from dash import dcc, html


def getProblemDropdown():
    info = [[None,None],[50,4],[10,2],["n","n"], ["n","n"], ["n","n"]]
    return dcc.Dropdown(
        id='problems-dropdown', # Reference id of the dropdown
        options=[ # Options with titles and reference values
            {'label': f'Problem {i} ({info[i][0]} customers, {info[i][1]} depots)', 'value': i}
            for i in range(1, 6)
        ],
        value=1,  # Default to 'Problem 1'
        searchable=False, # Restrict user text input,
        clearable=False  # Disable the clear option (no "x" icon)
    )

def getPopulationSlider():
    return dcc.Slider(
        id='population-slider', # Reference id of the slider
        # Range from 5 to 50, step size of 5
        min=5, max=50, step=5,
        value=10, # Default to 10
        # Custom marks on slider allows navigate users on slider's limit
        marks={5: '5', 50: '50'},
        tooltip={"placement": "bottom", "always_visible": True} # current value constant displaying
    )

def getIterationsSlider():
    return dcc.Slider(
        id='iterations-slider', # Reference id of the slider
        # Range from 10 to 500
        min=10, max=500, step=10,
        value=200, # Default to 200
        # Custom marks on slider allows navigate users on inputs and slider's limit
        marks={10: '10', 50: '50', 100: '100', 200: '200', 300: '300', 400: '400', 500: '500'},  
        tooltip={"placement": "bottom", "always_visible": True} # current value constant displaying
    )

def getMutationSlider():
    return dcc.Slider(
        id='mutation-slider', # Reference id of the slider
        # Range from 0.1 to 1.0, step size of 0.1
        min=0, max=1, step=0.1,
        value=0.5, # Default to 0.5
        # Custom marks on slider allows navigate users on inputs and slider's limit
        marks= {0: '0', 1: '1'},
        tooltip={"placement": "bottom", "always_visible": True, } # current value constant displaying
    )

def getCrossoverSlider():
    return dcc.Slider(
        id='crossover-slider',  # Reference id of the slider
        # Range from 0.1 to 1.0, step size of 0.1
        min=0, max=1, step=0.1,
        value=0.4, # Default to 0.4
        # Custom marks on slider allows navigate users on inputs and slider's limit
        marks={0: '0', 1: '1'},
        tooltip={"placement": "bottom", "always_visible": True} # current value constant displaying
    )


def getSpeedSlider():
    return dcc.Slider(
        id='speed-slider', # Reference id of the slider
        # Range from 5 to 50, step size of 5
        min=0, max=1, step=0.5,
        value=0.5, # Default to 0.5 or Normal
        # Custom marks on slider
        marks={0: 'Slow', 0.5: 'Normal', 1: 'Fast'},
    )


def getSelectionDropdown():
    return dcc.Dropdown(
        id='selection-dropdown', # Reference id of the dropdown
        options=[                # Options with titles and reference values
            {'label': 'Tournament', 'value': 'Tournament'}, 
            {'label': 'Roulette', 'value': 'Roulette'}
        ],
        value='Tournament', # Default to Tournament
        searchable=False,   # Disable search option
        clearable=False     # Disable the clear option (no "x" icon)
    )

def getRunButton():
    return html.Div(
        html.Button(
            'Run Visualisation',
            id='run-btn',
            n_clicks=0,
            className="btn btn-primary"
        ),
        style={"display": "flex", "justify-content": "center", "margin-top": "20px"}
    )
    

def getParameterSettings():
    return html.Div(
        [
            html.H5("Parameter Settings"),  # Section title              

            # Label for dropdown and add space above
            html.Label("Problem to be solved and displayed", style={"margin-top": "10px"}), 
            # Dropdown for choosing problem
            getProblemDropdown(),  

            # Label for slider and add space above
            html.Label( "Initial Population Size", style={"margin-top": "20px"}),
            # Slider for start population size    
            getPopulationSlider(),

            # Label for slider and add space above
            html.Label("Number of Iterations", style={"margin-top": "20px"}),
            # Slider for number of iterations
            getIterationsSlider(),
            
            # Label for slider and add space above
            # html.Label("Visualisation Speed", style={"margin-top": "20px"}),
            # Slider for mutation rate
            # getMutationSlider(),             

            # Label for slider and add space above 
            html.Label("Crossover Rate", style={"margin-top": "20px"}),
            # Slider for Crossover Rate
            getCrossoverSlider(),       
            
            # Label for dropdown and add space above 
            html.Label("Selection Method", style={"margin-top": "20px"}),  
            # Dropdown for Selection Method
            getSelectionDropdown(),

            # Label for slider and add space above
            html.Label("Visualisation Speed", style={"margin-top": "20px"}),
            # Slider for mutation rate
            getSpeedSlider(),     

            # Button to trigger the visualisation (Centered)
            getRunButton()
        # Parameter settings styling
        ], style={"background-color": "#F8F9FA", "padding": "15px", "border-radius": "15px"}
    )