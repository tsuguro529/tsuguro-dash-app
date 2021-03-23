
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': 'black',
    'text':'white'
}
app.layout = html.Div([
    html.Label('Dropdown'),
    dcc.Dropdown(
        options=[
            {'label': '佐藤', 'value': 'sato'},
            {'label': '鈴木', 'value': 'suzuki'},
            {'label': '田中', 'value': 'tanaka'},
            {'label': '吉田', 'value': 'yoshida'},
        ],
        value='suzuki'
    ),

    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(
        options=[
            {'label': '佐藤', 'value': 'sato'},
            {'label': '鈴木', 'value': 'suzuki'},
            {'label': '田中', 'value': 'tanaka'},
            {'label': '吉田', 'value': 'yoshida'},
        ],
        value=['sato','suzuki'],
        multi=True
    ),

    html.Label('Radio Items'),
    dcc.RadioItems(
        options=[
            {'label': '佐藤', 'value': 'sato'},
            {'label': '鈴木', 'value': 'suzuki'},
            {'label': '田中', 'value': 'tanaka'},
            {'label': '吉田', 'value': 'yoshida'},
        ],
        value='suzuki'
    ),

    html.Label('Checkboxes'),
    dcc.Checklist(
        options=[
            {'label': '佐藤', 'value': 'sato'},
            {'label': '鈴木', 'value': 'suzuki'},
            {'label': '田中', 'value': 'tanaka'},
            {'label': '吉田', 'value': 'yoshida'},
        ],
        value=['yoshida','suzuki'],
    ),

    html.Label('Text Input'),
    dcc.Input(value='佐藤', type='text'),

    html.Label('Slider'),
    dcc.Slider(
        min=0,
        max=5,
        marks={i:str(i) for i in range(1,6)},
        value=3
    )

], style={'columnCount':2})

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
