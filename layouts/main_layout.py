import dash_bootstrap_components as dbc
from dash import dcc, html
import sys

# Modify the sys.path first
sys.path.insert(0, 'F:/MLHTransportHack')

# Now, attempt the import
from database import db_connection

def calculate_savings_per_mile(gasoline_price, mpg, electricity_cost, ev_efficiency):
    fuel_cost_per_mile = gasoline_price / mpg
    ev_cost_per_mile = electricity_cost / ev_efficiency 
    return fuel_cost_per_mile - ev_cost_per_mile

gasoline_price = 15.00  
mpg = 25  
electricity_cost = 10.12  
ev_efficiency = 0.3  

savings_per_mile = calculate_savings_per_mile(gasoline_price, mpg, electricity_cost, ev_efficiency)
fuel_cost_per_mile = gasoline_price / mpg
ev_cost_per_mile = electricity_cost / ev_efficiency

url = dcc.Location(id='url', refresh=False)

header = dbc.Row([
    dbc.Col(html.H1("Emission Comparison Dashboard", className="text-center my-4"), width=8),
    dbc.Col(html.Img(src="/assets/your_animated_image.gif", height="60px"), width=2),
    dbc.Col(html.A(
        dbc.Button("Book EV Vehicles", id="booking-button", href="/book-ev-vehicles", color="primary"),
        href="https://www.example.com",  # Change this to your desired external link or internal link
        target="_blank"  # Opens in a new tab. Remove if you want it in the same tab.
    ), width=2)
], className="mb-4")

left_nav = dbc.Col(
    [
        html.H3("Navigation", className="text-center my-4"),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="#", active="exact"),
                dbc.NavLink("Emission Data", href="#", active="exact"),
                dbc.NavLink("Settings", href="#", active="exact"),
                dbc.NavLink("About", href="#", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    width=3,
    className="border-right"
)


footer = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P("Make Earth Green Again! Drive responsibly.", className="footer-message text-center mt-4"),
        )
    )
)

my_button = dbc.Button("Book EV Vehicles", id="booking-button", href="/book-ev-vehicles", color="primary")

all_data = db_connection.get_data_from_db()

# Filter data for vehicle_id = 1
data = [entry for entry in all_data if entry.get("vehicle_id") == 1]
data_entry = data[0]

# Calculate the percentage values
total_emission = data_entry["distance_vs_ev_emission"] + data_entry["distance_vs_fuel_emission"]
ev_percentage = (data_entry["distance_vs_ev_emission"] / total_emission) * 100
fuel_percentage = (data_entry["distance_vs_fuel_emission"] / total_emission) * 100

total_cost = ev_cost_per_mile + fuel_cost_per_mile
ev_cost_percentage = (ev_cost_per_mile / total_cost) * 100
fuel_cost_percentage = (fuel_cost_per_mile / total_cost) * 100
# Define a conversion factor: number of points per unit of emission saved
POINTS_PER_UNIT_SAVED = 10  # Adjust as per your preference

# If data exists for vehicle_id = 1, we'll use the first entry, else we'll create a default entry
if data:
    vehicle_data = data[0]
else:
    vehicle_data = {
        "distance_vs_ev_emission": 0,
        "distance_vs_fuel_emission": 0
    }

user_data = {
    "name": "John Doe",
    "user_id": "JD123",
    "ev_emissions": sum(i.get("distance_vs_ev_emission", 0) for i in data),
    "fuel_emissions": sum(i.get("distance_vs_fuel_emission", 0) for i in data)
}

# Determining which emoji to display
if user_data["ev_emissions"] < user_data["fuel_emissions"]:
    emoji = "😊"  # Happy emoji
    message = "Great job using EVs and contributing to a greener environment!"
else:
    emoji = "😞"  # Sad emoji
    message = "Consider using EVs more for a greener footprint."

# Calculate potential savings: difference between fuel emissions and EV emissions
potential_savings = user_data["fuel_emissions"] - user_data["ev_emissions"]

# Convert savings to points
user_data["points"] = potential_savings * POINTS_PER_UNIT_SAVED


layout = dbc.Container([
    url,
    html.Link(rel="stylesheet", href="/assets/custom_header.html"),
    header,
    dbc.Row([
        dbc.Col([
            html.H1("Emission Comparison Dashboard", className="text-center my-4"),
            html.H3(f"Welcome, {user_data['name']} (ID: {user_data['user_id']})"),
            html.H5(f"Your carbon footprint message: {message} {emoji}", className="my-4"),

        dcc.Graph(
            id="emission-comparison",
            figure={
                "data": [
                    {
                        "x": ["EV", "Fuel"],
                        "y": [data_entry["distance_vs_ev_emission"], data_entry["distance_vs_fuel_emission"]],
                        "type": "bar",
                        "name": "Emissions",
                        "marker": {"color": ["green", "red"]},
                        "text": [f"{ev_percentage:.2f}%", f"{fuel_percentage:.2f}%"],  # Display the calculated percentage
                        "textposition": "outside",
                        "textfont": {
                                "color": "black",
                                "size": 15
                        },
                        "width": 0.35  # making the bar narrower
                    },
                    {
                        "x": ["EV", "Fuel"],
                        "y": [ev_cost_per_mile, fuel_cost_per_mile],
                        "type": "bar",
                        "name": "Cost ($ per mile)",
                        "marker": {"color": ["blue", "orange"]},
                        "text": [f"{ev_cost_percentage:.2f}%", f"{fuel_cost_percentage:.2f}%"],  
                        "width": 0.35,  # making the bar narrower
                        "offset": 0.35  # This offsets the position of this bar for the grouped mode
                    }
                ],
                        "layout": {
                                "title": {
                                    "text": "Emission & Cost Comparison",
                                    "font": {
                                        "size": 24,
                                        "color": "#333",
                                        "family": "Arial, sans-serif"
                                    }
                                },
                                "height": 400,
                                "width": 600,
                                "barmode": 'group',
                                "bargap": 0.1,  # gap between bars of adjacent location coordinates
                                "xaxis": {
                                    "title": "Vehicle Type",
                                    "titlefont": {
                                        "size": 16,
                                        "color": "#333",
                                        "family": "Arial, sans-serif"
                                    },
                                    "tickfont": {
                                        "size": 14,
                                        "color": "#666"
                                    },
                                },
                                "yaxis": {
                                    "title": "Value",
                                    "titlefont": {
                                        "size": 16,
                                        "color": "#333",
                                        "family": "Arial, sans-serif"
                                    },
                                    "tickfont": {
                                        "size": 14,
                                        "color": "#666"
                                    },
                                    "gridcolor": "#e1e1e1"
                                },
                                "legend": {
                                    "font": {
                                        "size": 14
                                    }
                                },
                                "paper_bgcolor": "#f4f4f4",
                                "plot_bgcolor": "#f7f7f7",
                            }
                        }
                    ),

          html.A(
                "📥 Download Graph as Image",
                id="download-link",
                download="emission_comparison.png",
                href="",
                target="_blank",
                className="btn btn-primary mt-3"
            )
        ], width=8),

        dbc.Col([
            # Eco-Points section
          
            html.Div(style={"height": "100px"}),
            html.Div(style={"height": "50px"}),
            html.Div([
                #html.I(className="fas fa-leaf", style={"color": "green", "font-size": "48px"}),
                html.I(className="fas fa-seedling", style={"color": "green", "font-size": "60px"}),
                html.Div("Your Eco-Points", className="points-label text-center"),
                html.Div(f"{user_data['points']}", className="points-value text-center")
            ], className="points-container", style={"background-color": "#e6ffe6", "padding": "25px","margin-bottom": "100px", "margin-bottom": "20px", "border-radius": "10px", "box-shadow": "0px 0px 10px rgba(0,0,0,0.1)"}),  # added margin-top

            # Cost Savings section
            html.Div([
                html.I(className="fas fa-coins", style={"color": "gold", "font-size": "48px"}),
                html.Div("Cost Savings", className="savings-label text-center"),
                html.Div(f"${savings_per_mile:.2f} per mile", className="savings-value text-center")
            ], className="savings-container", style={"background-color": "#fff0b3", "padding": "25px", "border-radius": "10px", "box-shadow": "0px 0px 10px rgba(0,0,0,0.1)"})
            ], width=4)
    ]),
    footer,
],  className="center-content", fluid=True, style={"background-color": "#f7f7f7"})
