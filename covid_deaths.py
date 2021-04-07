import dash
import dash_core_components as dcc 
import dash_html_components as html 
import pandas as pd 
import plotly.express as px

# Importing csv as a Dataframe
covid_deaths = pd.read_csv('./fallecidos_covid.csv', delimiter=';')
# Formatting date column as datetime type
covid_deaths['FECHA_FALLECIMIENTO'] = pd.to_datetime(covid_deaths['FECHA_FALLECIMIENTO'], format='%Y%m%d')
# print(covid_deaths)

# Grouping by state
deaths_by_state = covid_deaths.groupby(['FECHA_FALLECIMIENTO', 'DEPARTAMENTO']).DEPARTAMENTO.agg('count').to_frame('TOTAL').reset_index()
# print(deaths_by_state)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('COVID-19 Deaths in Peru', style={'textAlign':'center'}),

    html.Div([
        html.H2('Deaths by Department (State)'),
        html.P('Note: Single-Click in any department to remove it from the graph, double-click any department to isolate it (single-click after that to add other departments).'),
        dcc.Graph(
            id='deaths by department/state',
            figure=px.area(
                deaths_by_state,
                x='FECHA_FALLECIMIENTO',
                y='TOTAL',
                color='DEPARTAMENTO',
                labels={
                    'FECHA_FALLECIMIENTO':'Date of Decease',
                    'TOTAL':'Number of Deaths',
                    'DEPARTEMENTO':'Department/State'
                })
        )
    ])
], className='covid_dash')

if __name__ == '__main__':
    app.run_server()