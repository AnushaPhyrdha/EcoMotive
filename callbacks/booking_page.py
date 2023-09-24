import dash.dependencies
from app import app

@app.callback(
    dash.dependencies.Output('url', 'pathname'),
    [dash.dependencies.Input('navigate-btn', 'n_clicks')]
)
def navigate_to_page(n_clicks):
    if n_clicks:
        return "/new_page_path"  # Change this to your desired page path
    return dash.no_update