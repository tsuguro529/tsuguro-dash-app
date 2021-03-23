
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

from assets.database_dash import db_session
from assets.models_dash import Data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

data = db_session.query(Data.no, Data.talent, Data.url, Data.magazine, Data.magazine_kana, Data.year, Data.month).all()

talent_dict = {}

for datum in data:
    talent_dict[datum.talent] = 0
for datum in data:
    talent_dict[datum.talent] += 1


talent_name = list(talent_dict.keys())
talent_num = list(talent_dict.values())

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H2(children='雑誌表紙掲載回数'),
    html.Div(children=[

        dcc.Graph(
            id='subscriber_graph',
            figure={
                'data':[
                    go.Bar(
                        x=talent_num,
                        y=talent_name,
                        name='掲載回数',
                        yaxis='y1',
                        orientation='h',
                    )
                ],
                'layout': go.Layout(
                    title='anan',
                    xaxis=dict(title='掲載回数', showgrid=True, range=[0, max(talent_num)+1]),
                    yaxis1=dict(title='タレント', showgrid=False, categoryorder='total ascending'),
                    height = 1720,
                    width = 1180,
                    margin=dict(l=200, r=200, b=100, t=100)
                )
            }),
    ])
],style={
    'textAlign': 'center',
    'width': '1200px',
    'margin': '0 auto'
})

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
