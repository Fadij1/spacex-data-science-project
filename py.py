from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

spacex_df = pd.read_csv("dataset_part_2.csv")
max_payload = spacex_df["PayloadMass"].max()
min_payload = spacex_df["PayloadMass"].min()

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1("SpaceX Launch Records Dashboard",
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': site, 'value': site} for site in spacex_df['LaunchSite'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    html.Br(),

    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=max_payload,
        step=1000,
        marks={0: '0', int(max_payload/2): str(int(max_payload/2)), int(max_payload): str(int(max_payload))},
        value=[min_payload, max_payload]
    ),

    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df,
            values='Class',
            names='LaunchSite',
            title='Total Success Launches by Site'
        )
        return fig
    else:
        filtered_df = spacex_df[spacex_df['LaunchSite'] == entered_site]
        success_counts = filtered_df['Class'].value_counts().reset_index()
        success_counts.columns = ['Class', 'count']
        success_counts['Class'] = success_counts['Class'].map({1: 'Success', 0: 'Failure'})

        fig = px.pie(
            success_counts,
            values='count',
            names='Class',
            title=f'Total Success Launches for site {entered_site}'
        )
        return fig

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['PayloadMass'] >= low) & (spacex_df['PayloadMass'] <= high)]

    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='PayloadMass',
            y='Class',
            color='Orbit',
            title='Payload vs. Launch Outcome for All Sites'
        )
        return fig
    else:
        site_df = filtered_df[filtered_df['LaunchSite'] == entered_site]
        fig = px.scatter(
            site_df,
            x='PayloadMass',
            y='Class',
            color='Orbit',
            title=f'Payload vs. Launch Outcome for {entered_site}'
        )
        return fig

if __name__ == '__main__':
    app.run(debug=True)