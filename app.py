import pandas as pd
import plotly.graph_objects as go
from math import floor
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from time import strptime
from calculations import r, alcohol_ingested, main_calculate
import numpy as np
from operator import itemgetter
empty_stomach_half_life_hour = 0.1066
full_stomach_half_life_hour = 0.3009


def isTimeFormat(input):
    try:
        strptime(input, '%H:%M')
        return True
    except ValueError:
        return False


app = dash.Dash(__name__)
server = app.server
app.title = "EtOH"

test_df = pd.DataFrame()

alcohol_dictionary = {
    "Custom": None,
    "Cider": 6,
    "Beer": 6,
    "Lager": 4,
    "Red Wine": 12.5,
    "White Wine": 11,
    "Vodka": 40,
    "Whiskey": 40,
    "Rum": 40}
alc_labels = []

for key, val in alcohol_dictionary.items():
    tempd = {}
    tempd["label"] = key
    tempd["value"] = key
    alc_labels.append(tempd)


time = [f"{i}:00" for i in range(12)]
z = [i**2 for i in range(12)]

app.layout = html.Div(
    [
        html.Div([
            html.H1("EtOH - The Blood Alcohol Level Predictor"),

            html.Label("Select your sex", style={"margin": "5px"}),
            html.Br(),

            dcc.Dropdown(
                id="sex", options=[
                    {
                        "label": "Male", "value": "male"}, {
                        "label": "Female", "value": "female"},

                ], multi=False, value="male", style={
                    "background": "black"}),
            html.Br(),
            html.Label("Select your age", style={"margin": "5px"}, id="AGE"),

            html.Br(),
            dcc.Input(
                id="age",
                type="number",
                min=0,
                max=100,
                value=18,
            ),



            html.Br(),
            html.Br(),
            html.Label("Height", style={"margin": "5px"}, id="HEIGHT"),
            html.Br(),

            dcc.Input(
                id="height",
                type="number",
                min=0,
                max=230,
                value=170,

            ),
            html.Br(),
            html.Br(),
            html.Label("Weight", style={"margin": "5px"}, id="WEIGHT"),
            html.Br(),
            dcc.Input(
                id="weight",
                type="number",
                min=0,
                max=200,
                value=70,

            ),
            html.Br(),
            html.Br(),
            html.Div(
                html.H1("Have you eaten?"), style={'width': '32%', 'display': 'inline-block'}),

            html.Div(
                dcc.Dropdown(
                    id="hungry_inp",

                    options=[
                        {"label": "Yes", "value": "Yes"},
                        {"label": "No", "value": "No"},
                    ],
                    value="Yes",
                    multi=False,
                ), style={'width': '32%', "height": "100px", "text-align": "center", "font-size": 13}, id="drop2"),


            html.Hr(),
            html.Br(),

            html.Div(
                html.H1("Select Drink"), style={'width': '32%', 'display': 'inline-block'}),

            html.Div(
                dcc.Dropdown(
                    id="drink_inp",
                    options=alc_labels,
                    value="Custom",
                ), style={'width': '32%', "height": "100px", "text-align": "center", "font-size": 13}, id="drop"),





        ], id="container"),


        html.Div([
            html.Div(
                html.H1("Enter the ABV of drink in % (if custom was selected)"), style={'width': '32%', 'display': 'inline-block'}),

            html.Div(
                html.H1("Enter Volume of that drink in mL"), style={'width': '32%', 'display': 'inline-block'}),
            html.Div(
                html.H1("Enter the time you drunk it (HH:MM)"),
                style={'width': '32%', 'display': 'inline-block'}),
        ]),

        html.Div([
            html.Div(
                dcc.Input(
                    id="ABV_inp",
                    placeholder="Enter ABV if necessary",
                    type="number",
                    min=0,
                    max=100,
                ), style={'width': '32%', 'display': 'inline-block', "text-align": "center", "height": "30%"}),
            html.Div(
                dcc.Input(
                    id="volume_inp",
                    placeholder="Enter Volume (mL)",
                    type="number",
                    min=0,
                ), style={'width': '32%', 'display': 'inline-block', "text-align": "center", "height": "30%"}),
            html.Div(
                dcc.Input(
                    id="time_inp",
                    placeholder="Enter Time",

                ),
                style={'width': '32%', 'display': 'inline-block', "text-align": "center"}),



        ], id="vol_time_inp"),


        html.Br(),
        html.Button('ADD DRINK', id='editing-rows-button', n_clicks=0),
        html.Br(),
        html.Div(id='output_div'),

        html.Br(),
        dash_table.DataTable(
            id='table',
            columns=[

                {
                    'name': "Drink",
                    'id': "Drink",
                    'deletable': False,
                    'renamable': False
                },
                {
                    'name': "ABV (%)",
                    'id': "ABV",
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
        html.Br(),
        html.Br(),


        html.Button('Update Graph', id='update_graph', n_clicks=0),



        dcc.Graph(
            id="graph", figure={

            },

        ),

    ], id="data",

)


@app.callback(
    Output("table", "data"),
    Input('editing-rows-button', 'n_clicks'),
  
    State(component_id="drink_inp", component_property="value"),
    State(component_id="ABV_inp", component_property="value"),
    State(component_id="volume_inp", component_property="value"),
    State(component_id="time_inp", component_property="value"),
    State(component_id="table", component_property="data")

)
def add(c, d, abv, v, t, og_data):
    if (c > 0) and abv is not None and v is not None and isTimeFormat(t) is True:

        global test_df
        ss = pd.DataFrame(
            og_data,
            columns=[
                "Drink",
                "ABV",
                "Volume (mL)",
                "Time"])
        test_df = ss

        test_df.loc[-1] = [d, abv, v, t]
        test_df.index = test_df.index + 1
        test_df = test_df.sort_index()
        data = test_df.to_dict("records")
        # print(test_df)
        df2 = test_df.copy()
        del df2["Drink"]
        cols = list(df2.columns)
        a, b = cols.index('Volume (mL)'), cols.index('Time')
        cols[b], cols[a] = cols[a], cols[b]
        df2 = df2[cols]
        global drinks_list
        df2["Time"] = pd.to_timedelta(df2.Time + ":00")
        
        df2.sort_values(by="Time", ascending=True)
        

        drinks_list = df2.values.tolist()
        drinks_list = sorted(drinks_list, key=itemgetter(1))

        for i in drinks_list:
            i[1] = str(i[1])[7:12]

        

        return data

    if abv is None or t is None or isTimeFormat(t) is False or v is None:
        ss = pd.DataFrame(
            og_data,
            columns=[
                "Drink",
                "ABV",
                "Volume (mL)",
                "Time"])
        return ss.to_dict("records")


@app.callback(
    Output("output_div", "children"),
    [Input('table', 'data_previous')],
    [State('table', 'data')]
)
def update(d0, d1):
    if d1 != d0:
        global test_df
        ss = pd.DataFrame(d1, columns=["Drink", "ABV", "Volume (mL)", "Time"])
        test_df = ss
        df2 = test_df.copy()
        del df2["Drink"]
        cols = list(df2.columns)
        a, b = cols.index('Volume (mL)'), cols.index('Time')
        cols[b], cols[a] = cols[a], cols[b]
        df2 = df2[cols]
        global drinks_list
        df2["Time"] = pd.to_timedelta(df2.Time + ":00")
        
        df2.sort_values(by="Time", ascending=True)
        

        drinks_list = df2.values.tolist()
        drinks_list = sorted(drinks_list, key=itemgetter(1))

        for i in drinks_list:
            i[1] = str(i[1])[7:12]

    print(test_df)


@app.callback(
    Output("ABV_inp", "value"),
    Input("drink_inp", "value"),
)
def update_ABV(drink):
    if drink != "Custom" and drink is not None:
        return alcohol_dictionary[drink]


@app.callback(
    [Output(component_id="AGE", component_property="children"),
     Output(component_id="HEIGHT", component_property="children"),
     Output(component_id="WEIGHT", component_property="children"),
     Output(component_id="graph", component_property="figure")

     ],
    [Input(component_id="age", component_property="value"),
     Input(component_id="height", component_property="value"),
     Input(component_id="weight", component_property="value"),
     Input(component_id="sex", component_property="value"),
     Input(component_id="hungry_inp", component_property="value"),
     Input(component_id="update_graph", component_property="n_clicks"),


     ]

)
def update(age, height, weight, sex, eaten, c):
    
    age_txt = f"Age selected: {age} years"
    
    global user
    user = [sex, age, weight, height / 100, eaten]
    # r_value = r(sex, height/100,weight,age)
    print(user)

    ft = 0.0328 * height
    number_dec = str(ft - int(ft))[1:]

    height_ft_inch = f"{floor(ft)}ft {round(float(number_dec)*12,1)}in"

    height_txt = f"Height selected: {height} cm = {height_ft_inch}"
    weight_txt = f"Weight: {weight}kg"

    figure = go.Figure(data=go.Scatter(
        x=[0],
        y=[0],
    ))

    if c > 0:
        t, c = main_calculate(user, drinks_list)
        figure = go.Figure(data=go.Scatter(
            x=t / 3600,
            y=c,

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
        xaxis_title = "Time after first drink (hr)",
        yaxis_title = "Blood Alcohol Level (g%)",
        font=dict(
            size=10,
            color="white"
        )

    )

    return age_txt, height_txt, weight_txt, figure


if __name__ == "__main__":
    app.run_server(debug=True)
