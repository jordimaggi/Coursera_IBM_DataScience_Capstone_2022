# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
sites = spacex_df['Launch Site'].tolist()
sites = list(dict.fromkeys(sites))

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': sites[0], 'value': sites[0]},
                                        {'label': sites[1], 'value': sites[1]},
                                        {'label': sites[2], 'value': sites[2]},
                                        {'label': sites[3], 'value': sites[3]},
                                    ],
                                    value='ALL',
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 1000: '1000',
                                                2000: '2000', 3000: '3000',
                                                4000: '4000', 5000: '5000',
                                                6000: '6000', 7000: '7000',
                                                8000: '8000', 9000: '9000',
                                                10000: '10000'},
                                                value=[min_payload, max_payload]),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'))


def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df.groupby(['Launch Site'], as_index=False).sum()
        fig = px.pie(filtered_df, values='class',
                names='Launch Site',
                title='All sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        final_df = filtered_df.groupby(['Launch Site','class'], as_index=False).count()
        print(final_df)
        fig = px.pie(final_df, values='Unnamed: 0', names='class', title='Total success launches for site {}'.format(entered_site))
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site, payload):
    range_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload[0]) & ((spacex_df['Payload Mass (kg)'] <= payload[1]))]
    if entered_site == 'ALL':
        fig = px.scatter(x=range_df['Payload Mass (kg)'], y=range_df['class'],
                color=range_df['Booster Version Category'],
                title='Coorelation between Payload and Success for all Sites')
    
    else:
        filtered_df = range_df[range_df['Launch Site'] == entered_site]
        fig = px.scatter(x=filtered_df['Payload Mass (kg)'], y=filtered_df['class'],
                color=filtered_df['Booster Version Category'],
                title='Coorelation between Payload and Success for all {}'.format(entered_site))
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
