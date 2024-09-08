import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import requests
from datetime import datetime

dash.register_page(__name__, path="/spending-updates")

today_date = datetime.now().strftime('%d-%m-%Y')

navbar = html.Div([
    html.Div([
        html.H1("Transact", className="text-black font-bold py-6 text-3xl text-center"),
        html.Div([
            html.A(
                html.H2("Home", className="text-black w-full p-2 font-semibold rounded-md bg-cyan-100 text-lg tracking-wider"),
                href="/home", className="w-full"
            ),
            html.A(
                html.H2("Spending Updates", className="text-black font-semibold active:bg-cyan-100 w-full p-2 rounded-md text-lg tracking-wider"),
                href="/spending-updates", className="w-full"
            ),
        ], className="flex flex-col gap-2 w-full"),
    ], className="flex flex-col h-full"),
    html.Div(
        html.A(
            html.H2("Logout",id="logout-btn", className="text-black w-full p-2 text-lg bg-red-800 text-white hover:bg-red-600 tracking-wider"),
            href="/", className="w-full"
        ),
        className="mt-auto"
    ),
], className="w-52 lg:w-64 h-screen bg-white flex fixed left-0 flex-col")


amount_input = dbc.Row([
    dbc.Label("Amount", width={"size": 12, "sm": 2}), 
    dbc.Col(dbc.Input(required=True, type="text", id="amount", placeholder="Enter Amount"), width={"size": 12, "sm": 10})
], className="mb-3 text-black font-semibold")

location_input = dbc.Row([
    dbc.Label("Location", width={"size": 12, "sm": 2}),
    dbc.Col(dbc.Input(type="text", id="location", placeholder="Enter location"), width={"size": 12, "sm": 10})
], className="mb-3 text-black font-semibold")

date_input = dbc.Row([
    dbc.Label("Date", width={"size": 12, "sm": 2}),
    dbc.Col(dbc.Input(required=True, type="date", id="date", placeholder="Enter Date"), width={"size": 12, "sm": 10})
], className="mb-3 text-black font-semibold")

payment_input = dbc.Row([
    dbc.Label("Payment Method", html_for="example-radios-row", width={"size": 12, "sm": 2}),
    dbc.Col(dbc.RadioItems(id="example-radios-row", options=[
        {"label": "Cash", "value": "Cash"},
        {"label": "Card", "value": "Card"},
        {"label": "UPI", "value": "UPI"},
        {"label": "NetBanking", "value": "NetBanking"}
    ]), width={"size": 12, "sm": 10})
], className="mb-3 text-black font-semibold")

boolean_input = dbc.Row([
    dbc.Label("Is this a recurring event?", html_for="example-radios-row", width={"size": 12, "sm": 4}),
    dbc.Col(dbc.RadioItems(id="question", options=[
        {"label": "Yes", "value": 1},
        {"label": "No", "value": 0}
    ]), width={"size": 12, "sm": 6})
], className="mb-3 w-full text-black font-semibold")

category_input = dbc.Row([
    dbc.Label("Category", html_for="category-select-row", width={"size": 12, "sm": 2}),
    dbc.Col(dbc.Select(required=True, id="category-select-row", placeholder="Select Category", options=[
        {"label": "Groceries", "value": "Groceries"},
        {"label": "Rent/Mortgage", "value": "Rent/Mortgage"},
        {"label": "Utilities", "value": "Utilities"},
        {"label": "Travel", "value": "Travel"},
        {"label": "Entertainment", "value": "Entertainment"},
        {"label": "Dining Out", "value": "Dining Out"},
        {"label": "Healthcare", "value": "Healthcare"},
        {"label": "Shopping", "value": "Shopping"},
        {"label": "Debt", "value": "Debt"},
        {"label": "Personal", "value": "Personal"}
    ]), width={"size": 12, "sm": 10})
], className="mb-3 text-black font-semibold")

frequency_input = dbc.Row([
    dbc.Label("Frequency", html_for="frequency-select-row", width={"size": 12, "sm": 2}),
    dbc.Col(dbc.Select(id="frequency-select-row", placeholder="Select Frequency", options=[
        {"label": "Weekly", "value": 1},
        {"label": "Monthly", "value": 2},
        {"label": "Yearly", "value": 3}
    ]), width={"size": 12, "sm": 10}),
    dbc.FormText("If Yes, then how frequent?")
], className="mb-3 text-black font-semibold")

description_input = dbc.Row([
    dbc.Label("Description", width={"size": 12, "sm": 2}),
    dbc.Col(dbc.Input(type="text", id="Description", placeholder="Enter Details", className="pb-12"), width={"size": 12, "sm": 10})
], className="mb-3 text-black font-semibold")

checkbox_input = dbc.Row([
    dbc.Col(dbc.Checkbox(id="checkbox-true-entries", label="All entries mentioned here are true", className="text-black font-semibold"), width={"size": 12, "sm": 10})
], className="mb-3")


form = dbc.Form([
    amount_input, date_input, category_input, payment_input, description_input, boolean_input, frequency_input, location_input, checkbox_input, 
    html.Button("Submit Info", id="transaction-submit-btn", n_clicks=0, className="w-full bg-cyan-500 py-2 font-semibold text-lg rounded-md text-white")
], className="py-6 px-4 md:py-14 md:px-32")  # Adjust padding for mobile and larger screens


form_screen = html.Div([
    html.Div([
        html.H1("Transaction Details!", className="font-bold text-2xl md:text-4xl text-center py-2 text-black"), 
        form
    ], className="w-full md:w-5/6 min-h-full bg-white rounded-xl py-2")
], className="w-full md:w-10/12 py-12 h-auto md:h-screen rounded-xl p-6 mx-auto md:pl-48 grid place-items-center")


layout = html.Div(
    children=[
        dcc.Location(id='relocation', refresh=True),
        navbar, form_screen
    ], 
    className="min-h-screen w-full flex flex-col md:flex-row gap-4 bg-neutral-200 text-white"
)



@callback(
    Output('relocation', 'href'),
    Input('transaction-submit-btn', 'n_clicks'),
    State('amount', 'value'),
    State('location', 'value'),
    State('date', 'value'),
    State('example-radios-row', 'value'),
    State('question', 'value'),
    State('category-select-row', 'value'),
    State('frequency-select-row', 'value'),
    State('Description', 'value'),
    State('checkbox-true-entries', 'value')
)
def handle_transaction_submission(n_clicks, amount, location, date, payment_method, is_recurring, category, frequency, description, checkbox):
    if n_clicks > 0:
        data = {
            "amount": amount,
            "location": location or "",
            "date": date or None,
            "payment_method": payment_method,
            "is_recurring": is_recurring,
            "category": category,
            "frequency": frequency or None,
            "description": description or None,
            "checkbox": checkbox
        }
        try:
            response = requests.post("http://localhost:8050/api/v1/transact/create-transaction", json=data)
            if response.status_code == 200:
                return '/dashboard'
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error: {e}")
    return dash.no_update
