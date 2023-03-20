from dash import dash, html, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
from vega_datasets import data

alt.data_transformers.enable('data_server')

cars = data.cars()
data = pd.read_csv("data/raw/owid-covid-data.csv", parse_dates=['date'])
selected_cols = ["iso_code",
                 "location",
                 "date",
                 "continent",
                 "new_cases_smoothed",
                 "stringency_index",
                 "population",
                 "gdp_per_capita"]

data = data[selected_cols]

data = data[~data["iso_code"].str.contains("OWID")]
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
print(app.server)
server = app.server
date_labels = pd.date_range(data['date'].min(), data['date'].max(), freq="3M")
date_marks = {int(d.timestamp()):d.strftime('%Y-%m-%d') for d in date_labels}

countries = [{"label": "Worldwide", "value": "Worldwide"}]
countries.extend([{"label": l, "value": l} for l in list(data['location'].unique())])

app.layout = dbc.Container(
    # dbc.Row([
    #     dbc.Col([
        html.Div([
            html.H1('Covid Visualisation'),
            dbc.Row([
                dbc.Col(width = 4, 
                        children=[
                    dbc.Card([
                        dbc.CardHeader('Parameters', style={'fontWeight': 'bold'}),
                        html.Label("Select Country"),
                        html.Br(),
                        dcc.Dropdown(
                            id='country-dropdown',
                            options=countries,
                            value='Worldwide'
                        ),
                        html.Br(),
                        html.Br(),
                        html.Label("Set a filter based on the population"),
                        html.Br(),
                        dbc.CardBody(
                            dcc.RangeSlider(
                                data['population'].min(),
                                data['population'].max(),
                                step=None,
                                value=[120_000_000, 400_000_000],
                                id='population_slider',
                        )),
                        html.Br(),
                        html.Br(),
                        html.Label("Set a filter based on the GDP"),
                        html.Br(),
                        dbc.CardBody(
                            dcc.RangeSlider(
                                data['gdp_per_capita'].min(),
                                data['gdp_per_capita'].max(),
                                step=None,
                                value=[2000, 12000],
                                # marks={i:str(i) for i in range(10)},
                                id='gdp_slider',
                        )),
                        html.Br(),
                        html.Br(),
                        html.Label("Select the time period"),
                        html.Br(),
                        dbc.CardBody(
                            dcc.DatePickerRange(
                                id='date-range',
                                min_date_allowed=data['date'].min(),
                                max_date_allowed=data['date'].max(),
                                initial_visible_month=data['date'].max(),
                                start_date=data['date'].min(),
                                end_date=data['date'].max()
                            ),
                        ),
                    ]),
                ]),                     
                dbc.Col(width=8, 
                        children=[
                            dbc.Row([
                                dbc.Card([
                                dbc.CardHeader('Stringency Index', style={'fontWeight': 'bold'}),
                                dbc.CardBody(
                                    [   html.H6(id="stringency-subtitle"),
                                        html.Iframe(
                                        id='stringency-index-plot',
                                        style={'border-width': '0', 'width': '100%', 'height': '400px'}
                                    )],
                                )
                                ])            
                            ]),
                            dbc.Row([
                                dbc.Card([
                                dbc.CardHeader('New Cases', style={'fontWeight': 'bold'}),
                                dbc.CardBody(
                                    [   html.H6(id="new-cases-subtitle"),
                                        html.Iframe(
                                        id='new-cases-plot',
                                        style={'border-width': '0', 'width': '100%', 'height': '400px'}
                                    )],
                                )
                            ])
                            ])
                        ]),
            ])
    ]),
        style={"border-width": "1px", "padding": "1px"}#     ])
    # ])
)



@app.callback(
    Output('stringency-index-plot', "srcDoc"),
    Output('stringency-subtitle', "children"),
    Input('country-dropdown', "value"),
    Input('population_slider', "value"),
    Input('gdp_slider', "value"),
    Input('date-range', "start_date"),
    Input('date-range', "end_date"))
def update_stringency_plot(country, 
                     population,
                     gdp_per_capita, 
                     start_date,
                     end_date):
    
    subtitle_text = ""
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    if country != "Worldwide":
        country_data = data[data['location'] == country]
        country_data = country_data[(country_data['date'] >= start_date) &
                                    (country_data['date'] <= end_date)]
        fig = alt.Chart(country_data, title=f'Stringency Index in {country}').mark_line().encode(
            x=alt.X("date", title="Date"),
            y=alt.Y("stringency_index", title="Stringency index")
        ).properties(
            width=600,
            height=250
        )
    else:
        population_filter = (data['population'] >= population[0]) & (data['population'] <= population[1])
        gdp_filter = (data['gdp_per_capita'] >= gdp_per_capita[0]) & (data['gdp_per_capita'] <= gdp_per_capita[1])

        countries_data = data[gdp_filter & population_filter]
        countries_data = countries_data[(countries_data['date'] >= start_date) &
                                    (countries_data['date'] <= end_date)]
        if len(countries_data) == 0:
            subtitle_text = "No countries match your filters."
            
        fig = alt.Chart(countries_data, title='Stringency Index in the filtered countries').mark_line().encode(
            x=alt.X("date", title="Date"),
            y=alt.Y("stringency_index", title="Stringency index"),
            color=alt.Color("location")
        ).properties(
            width=600,
            height=400
        )
    
    return fig.to_html(), subtitle_text

@app.callback(
    Output('new-cases-plot', "srcDoc"),
    Output('new-cases-subtitle', "children"),
    Input('country-dropdown', "value"),
    Input('population_slider', "value"),
    Input('gdp_slider', "value"),
    Input('date-range', "start_date"),
    Input('date-range', "end_date"))
def update_cases_plot( country, 
                        population,
                        gdp_per_capita, 
                        start_date,
                        end_date):
    subtitle_text = ""
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    if country != "Worldwide":
        country_data = data[data['location'] == country]
        country_data = country_data[country_data['date'] == end_date]
        fig = alt.Chart(country_data, title=f'Daily new cases in {country}').mark_bar().encode(
            x=alt.X("new_cases_smoothed", title="Daily Cases"),
            y=alt.Y("location", title="Country", sort="-x"),
            color=alt.Color("location")
        ).properties(
            width=600,
            height=250
        )

    else:
        population_filter = (data['population'] >= population[0]) & (data['population'] <= population[1])
        gdp_filter = (data['gdp_per_capita'] >= gdp_per_capita[0]) & (data['gdp_per_capita'] <= gdp_per_capita[1])

        countries_data = data[gdp_filter & population_filter]
        countries_data = countries_data[countries_data['date'] == end_date]
        if len(countries_data) == 0:
            subtitle_text = "No countries match your filters."        
        fig = alt.Chart(countries_data, title='Top Daily new cases in the filtered countries').mark_bar().encode(
            x=alt.X("new_cases_smoothed", title="Daily Cases"),
            y=alt.Y("location", title="Countries", sort="-x"),
            color=alt.Color("location")
        ).properties(
            width=600,
            height=250
        )
    
    return fig.to_html(), subtitle_text


if __name__ == '__main__':
    app.run_server(debug=True)