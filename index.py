import dash
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd 
import plotly.express as px
import plotly.graph_objs as go

# Importing csv as a Dataframe
covid_deaths = pd.read_csv('./data/fallecidos_covid.csv', delimiter=';')
# Formatting date column as datetime type
covid_deaths['FECHA_FALLECIMIENTO'] = pd.to_datetime(covid_deaths['FECHA_FALLECIMIENTO'], format='%Y%m%d')
covid_deaths.set_index('FECHA_FALLECIMIENTO', inplace=True)
# print(covid_deaths)

# quit()

# Formatting departments in list for further use in dropdowns.
depts = covid_deaths['DEPARTAMENTO'].unique().tolist()
depts_options = [{'label': dept,'value':dept} for dept in depts]

# Grouping by state
deaths_by_state = covid_deaths.groupby(['FECHA_FALLECIMIENTO', 'DEPARTAMENTO']).DEPARTAMENTO.agg('count').to_frame('TOTAL').reset_index()
# print(deaths_by_state)

# Linking an external CSS stylesheet 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initializing the dash application
app = dash.Dash(__name__)

# Structuring the layout of the web app
app.layout = html.Div([
    html.H1('COVID-19 Deaths in Peru', style={'textAlign':'center'}),

    html.Div([
        html.H2('Deaths by Department (State)'),
        html.P('Note: Single-Click in any department to remove it from the graph, double-click any department to isolate it (single-click after that to add other departments).'),
        dcc.Graph(
            id='deaths_by_department',
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
    ]),

    html.Div([
        html.H2('Visualize by Month and Department (State)'),
        dcc.Dropdown(
            id='year_dropdown',
            options=[
                {'label':'2020', 'value': '2020'},
                {'label':'2021', 'value': '2021'}
            ],
            value='2021',
            className='two columns'
        ),
        dcc.Dropdown(
            id='month_dropdown',
            options=[
                {'label':'Jan', 'value':'01'},
                {'label':'Feb', 'value':'02'},
                {'label':'Mar', 'value':'03'},
                {'label':'Apr', 'value':'04'},
                {'label':'May', 'value':'05'},
                {'label':'Jun', 'value':'06'},
                {'label':'Jul', 'value':'07'},
                {'label':'Aug', 'value':'08'},
                {'label':'Sep', 'value':'09'},
                {'label':'Oct', 'value':'10'},
                {'label':'Nov', 'value':'11'},
                {'label':'Dec', 'value':'12'}, 
            ],
            value='03',
            className='two columns'
        ),
        dcc.Dropdown(
            id='dept_dropdown',
            options=depts_options,
            value=['AREQUIPA', 'LA LIBERTAD'],
            multi=True,
            className='eight columns'
        ) 
    ]),

    html.Div(),

    html.Div([
        dcc.Graph(id='deaths_by_month')
    ])

], className='covid_dash')

@app.callback(Output('deaths_by_month', 'figure'),
            [Input('year_dropdown', 'value'),
            Input('month_dropdown', 'value'),
            Input('dept_dropdown', 'value')])
def monthly_figure(year, month, dept):
    filtered_date = year + '-' + month
    monthly_df = covid_deaths.loc[filtered_date].reset_index()
    monthly_df = monthly_df[monthly_df['DEPARTAMENTO'].isin(dept)]
    monthly_df = monthly_df[['FECHA_FALLECIMIENTO','DEPARTAMENTO']].value_counts().rename('TOTAL')
    monthly_df = monthly_df.reset_index().sort_values(by='FECHA_FALLECIMIENTO')

    fig = px.line(
        monthly_df,
        x='FECHA_FALLECIMIENTO',
        y='TOTAL',
        color='DEPARTAMENTO',
        labels={
            'FECHA_FALLECIMIENTO':'Date of Decease',
            'TOTAL':'Number of Deaths',
            'DEPARTEMENTO':'Department/State'
        }
    )

    return fig

if __name__ == '__main__':
    app.run_server()