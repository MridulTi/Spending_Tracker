import dash
import requests
from dash import html, dcc, Output, Input, callback, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/Signup")
ALLOWED_TYPES = [
    ("text", "First Name", "firstname"),
    ("text", "Last Name", "lastname"),
    ("email", "Email Address", "email"),
    ("text", "Username", "username"),
    ("password", "Password", "password"),
]

layout = html.Div([
    dcc.Location(id='redirect-location', refresh=True),
    html.Div([
        html.Div([
            
            html.H1("TRANSACT", className="w-full text-center font-bold text-2xl md:text-3xl"),
            html.H1("Sign up to create an account!", className="w-full text-center font-medium text-xl py-2 md:text-2xl"),

            
            html.Form([
                html.Div([
                    dbc.Label(name, color="black", className="px-2 font-semibold"),
                    dbc.Input(id=f"input-{id}", placeholder=name, type=input_type, className="rounded-xl w-full p-2 border"),
                ], className="my-3") for input_type, name, id in ALLOWED_TYPES
            ]),

            
            dbc.Button("Signup", id="signup-btn", color="info", className="text-white font-bold w-full py-2", n_clicks=0),

            
            html.Div([
                dbc.Label(
                    "Already have an account?",
                    className="w-full text-center font-medium text-md my-4",
                ),
                dcc.Link(
                    "Login!",
                    href="/",
                    className="text-blue-500 text-center w-full font-medium text-md underline hover:text-blue-700"
                )
            ], className="w-full flex flex-col items-center gap-2")
        ], className="bg-white text-black rounded-xl px-6 py-6 w-full max-w-md") 
    ], className="grid place-items-center h-full px-4")
], className="h-screen w-full bg-gradient-to-t from-violet-500 to-fuchsia-500 text-white")


@callback(
    Output('redirect-location', "href"),
    Input('signup-btn', 'n_clicks'),
    State("input-firstname", 'value'),
    State("input-lastname", 'value'),
    State("input-email", 'value'),
    State('input-username', 'value'),
    State('input-password', 'value'),
    prevent_initial_call=True
)
def signup_user(n_clicks, firstname, lastname, email, username, password):
    if n_clicks:
        # Collect input data
        data = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "username": username,
            "password": password
        }
        print(data)
        try:
            response = requests.post("http://localhost:8050/api/v1/auth/register", json=data)
            if response.status_code == 200:
                return "/"
            else:
                print(f"Failed to sign up. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error occurred while making the request: {str(e)}")
    return None
