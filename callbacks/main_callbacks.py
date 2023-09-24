from dash.dependencies import Input, Output
from app import app

@app.callback(
    Output('download-link', 'href'),
    [Input('emission-comparison', 'relayoutData')]
)
def update_link(relayoutData):
    # For simplicity, we're assuming a static image
    # In real-world applications, you might want to generate this image dynamically or update its URL dynamically
    return "/path/to/image.png"
