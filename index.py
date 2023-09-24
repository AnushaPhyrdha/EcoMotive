from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from layouts import main_layout
from layouts import booking_layout

from flask import send_from_directory
import os

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/booking':
        return booking_layout.booking_page
    # ... other routes
    else:
        main_layout.layout
server = app.server

@server.route('/assets/<path:path>')
def serve_static(path):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, 'assets'), path)

if __name__ == '__main__':
    app.run_server(debug=True)
