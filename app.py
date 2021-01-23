import pandas as pd
import plotly.graph_objects as go
from math import floor
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server
app.title = "Test"

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






        dcc.Graph(
            id="graph", figure={

            },

        ),
















    ], id="container",)


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
