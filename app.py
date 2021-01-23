import pandas as pd
import plotly.graph_objects as go
from math import floor
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)
server = app.server
app.title = "Test"

test_df = pd.read_excel("testdata.xlsx")
print(test_df.to_dict("records"))


time = [f"{i}:00" for i in range(12)]
z = [i**2 for i in range(12)]

app.layout = html.Div(
    [
        html.H1("Blood Alcohol Predictor"),

        html.Label("Select your sex", style={"margin": "5px"}),
        html.Br(),

        dcc.Dropdown(
            id="sex", options=[
                {
                    "label": "Male", "value": "Male"}, {
                    "label": "Female", "value": "Female"},

            ], multi=False, value="ALL", style={
                "background": "black"}),
        html.Br(),
        html.Label("Select your age", style={"margin": "5px"}, id="AGE"),
        dcc.Slider(
            id="age",
            min=18,
            max=60,
            step=1,
            value=18,
            marks={2 * i: str(2 * i) for i in range(36)},


        ),

        html.Br(),
        html.Label("Height", style={"margin": "5px"}, id="HEIGHT"),
        dcc.Slider(
            id="height",
            min=140,
            max=230,
            step=1,
            value=170,
            marks={10 * i: str(10 * i) for i in range(24)},
        ),
        html.Br(),
        html.Label("Weight", style={"margin": "5px"}, id="WEIGHT"),
        dcc.Slider(
            id="weight",
            min=20,
            max=200,
            step=1,
            value=70,
            marks={10 * i: str(10 * i) for i in range(21)},
        ),
        html.Br(),
        dcc.Input(
            id='adding-rows-name',
            placeholder='Enter a column name...',
            value='',
            style={'padding': 10}
        ),
        html.Button('Add Column', id='adding-rows-button', n_clicks=0),
        html.Br(),
        dash_table.DataTable(
            id='adding-rows-table',
            columns=[

                {
                    'name': "Drink",
                    'id': "Drink",
                    'deletable': False,
                    'renamable': False
                },

                {
                    'name': "Volume (mL)",
                    'id': "Volume (mL)",
                    'deletable': False,
                    'renamable': False
                },
                {
                    'name': "Time",
                    'id': "Time",
                    'deletable': False,
                    'renamable': False
                }



            ],
            data=test_df.to_dict("records"),

            editable=False,
            row_deletable=True,
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={'textAlign': 'left',
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white'},
            style_cell_conditional=[
                {
                    'if': {'column_id': 'Region'},
                    'textAlign': 'left'
                }]



        ),

        html.Button('Add Row', id='editing-rows-button', n_clicks=0),






        dcc.Graph(
            id="graph", figure={

            },

        ),
















    ], id="container",)


@app.callback(
    Output('adding-rows-table', 'data'),
    Input('editing-rows-button', 'n_clicks'),
    State('adding-rows-table', 'data'),
    State('adding-rows-table', 'columns'))
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


@app.callback(
    [Output(component_id="AGE", component_property="children"),
     Output(component_id="HEIGHT", component_property="children"),
     Output(component_id="WEIGHT", component_property="children"),
     Output(component_id="graph", component_property="figure")

     ],
    [Input(component_id="age", component_property="value"),
     Input(component_id="height", component_property="value"),
     Input(component_id="weight", component_property="value"),


     ]

)
def update(age, height, weight):
    age_txt = f"Age selected: {age} years"

    ft = 0.0328 * height
    number_dec = str(ft - int(ft))[1:]

    height_ft_inch = f"{floor(ft)}ft {round(float(number_dec)*12,1)}in"

    height_txt = f"Height selected: {height} cm == {height_ft_inch}"
    weight_txt = f"Weight: {weight}kg"

    figure = go.Figure(data=go.Scatter(
        x=time,
        y=z,

    ))

    figure.update_traces(line_color="white", textfont_color="white", selector=dict(type='scatter'), marker_colorbar_tickcolor="white"
                         )

    figure.update_xaxes(showgrid=False, zeroline=False, tickcolor='white',
                        tickfont=dict(color='white'))

    figure.update_yaxes(showgrid=False, zeroline=False, tickcolor='white',
                        tickfont=dict(color='white'))

    figure.update_layout(
        plot_bgcolor="#1f1f1f",
        paper_bgcolor="#2c2c2c",

    )

    return age_txt, height_txt, weight_txt, figure


if __name__ == "__main__":
    app.run_server(debug=True)
