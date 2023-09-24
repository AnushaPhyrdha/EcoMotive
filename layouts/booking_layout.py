# Necessary imports
from dash import dcc, html
from dash.dependencies import Input, Output
import booking_code

# Available cities (expand as needed)
cities = booking_code.stops
#["NYC", "Boston", "Chicago", "LA"]

# Dummy data for buses
dummy_data = {
    "NYC_to_Boston": [{"bus": "Bus A", "time": "10:00 AM", "fare": "$50"},
                     {"bus": "Bus B", "time": "2:00 PM", "fare": "$55"}],
    "Boston_to_NYC": [{"bus": "Bus C", "time": "1:00 PM", "fare": "$52"},
                     {"bus": "Bus D", "time": "4:00 PM", "fare": "$58"}],
    # Add more routes and dummy data as necessary
}

booking_page = html.Div([
    html.H1("Bus Booking Page"),
    dcc.Dropdown(
        id='from-city',
        options=[{'label': city, 'value': city} for city in cities],
        placeholder='Select starting city...'
    ),
    dcc.Dropdown(
        id='to-city',
        options=[{'label': city, 'value': city} for city in cities],
        placeholder='Select destination city...'
    ),
    html.Div(id='output-fare'),
    html.Button("Book Now", id='submit-btn'),
    html.Div(id='booking-confirmation')
], id='booking-container')



# Callbacks can be defined here, but they will need to reference the main app's instance
# For cleaner organization, consider placing callbacks in a separate file or directly in app.py
