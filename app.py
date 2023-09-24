import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output  # <-- Ensure this line is present
from layouts import main_layout, booking_layout
from flask import send_from_directory
from dash import dcc, html
import os
import booking_code


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = booking_layout.booking_page
server = app.server

@server.route('/assets/<path:path>')
def serve_static(path):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, 'assets'), path)

# Callbacks can be defined here referencing the main app instance.
# Example:

@app.callback(
    [Output('output-fare', 'children'),
     Output('total-message', 'children'),
     Output('coupon-message', 'children'),
     Output('payment-message', 'children'),
     Output('booking-confirmation', 'children')
     ],
    [Input('from-city', 'value'),
     Input('to-city', 'value'),
     Input('submit-btn', 'n_clicks')]
)

def update_output(from_city, to_city, n_clicks):
    # Initialize the fare message
    fare_message = ""
    coupon_message = ""
    payment_message = ""
    total_message = ""
    if from_city and to_city:
        fare = booking_code.get_fare(from_city, to_city)
        coupon_value = (main_layout.user_data['points'])/100
        fare_message = f"The fare from {from_city} to {to_city} is ${fare}."
        total_message= f"Total:       ${fare}"
        coupon_message = f"{coupon_value}"
        Net_Payable = round(fare - coupon_value, 2)
        if Net_Payable > 0:
            payment_message = f"Net Payable:     ${Net_Payable}"
        else:
            payment_message = f"$0"
    
    booking_message = ""
    # Check for booking button click
    ctx = dash.callback_context
    if n_clicks and ctx.triggered and ctx.triggered[0]['prop_id'] == 'submit-btn.n_clicks':
        booking_message = "Booking confirmed!"

    return fare_message, total_message, coupon_message, payment_message, booking_message


if __name__ == "__main__":
    app.run_server(debug=True)
