import dash
from dash import html,dcc,callback,Output,Input,dash_table
import dash_bootstrap_components as dbc
from flask import jsonify
from datetime import datetime
import requests
import plotly.express as px

dash.register_page(__name__,path="/dashboard")

def fetch_data():
    try:
        response = requests.get("http://localhost:8050/api/v1/transact/")
        if response.status_code==200:
            return response.json()
        else:
            print(f"Failed to authenticate. Status code: {response.status}")
            return []
    except Exception as e:
        print(f"Error occurred while making the request: {str(e)}")
        return []
    
def fetch_metrics():
    try:
        response = requests.get("http://localhost:8050/api/v1/transact/num_transaction")
        print(response.json()['status'])
        print(response)
        if response.status_code==200:
            return response.json()['data']
        else:
            print(f"Failed to authenticate. Status code: {response.status}")
    except Exception as e:
        print(f"Error occurred while making the request: {str(e)}")


today_date=datetime.now().strftime('%d-%m-%Y')

navbar = html.Div([
    html.Div([
        html.H1("Transact", className="text-black font-bold py-6 text-3xl text-center"),
        html.Div([
            html.A(
                html.H2("Home", className="text-black font-semibold w-full p-2 rounded-md bg-cyan-100 text-lg tracking-wider"),
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


dash_screen = html.Div([
    html.Div([
        html.H1("Analytics", className="font-bold text-4xl tracking-wider text-black"),
        dbc.Badge(today_date, className="p-1 bg-white text-black")
    ], className="flex items-center gap-4 mb-4"),

    html.Div([
        html.Div([
            html.Div([
                html.P("Total Transactions", className="font-semibold tracking-tight text-xl"),
                html.H1(id="total-transactions", className="font-bold text-6xl"),
                html.P("Total transactions recorded", className="font-extralight text-sm py-2"),
            ], className="p-4 bg-white text-black rounded-xl shadow-md"),

            html.Div([
                html.P("Total Amount Spent", className="font-semibold tracking-tight text-xl"),
                html.H1(id="total-amount-spent", className="font-bold text-6xl"),
                html.P("Total amount spent", className="font-extralight text-sm py-2"),
            ], className="p-4 bg-white text-black rounded-xl shadow-md"),

            html.Div([
                html.P("Average Transaction Amount", className="font-semibold tracking-tight text-xl"),
                html.H1(id="average-transaction-amount", className="font-bold text-6xl"),
                html.P("Average amount spent per transaction", className="font-extralight text-sm py-2"),
            ], className="p-4 bg-white text-black rounded-xl shadow-md"),

            html.Div([
                html.P("Highest Transaction Amount", className="font-semibold tracking-tight text-xl"),
                html.H1(id="highest-transaction-amount", className="font-bold text-6xl"),
                html.P("Highest amount spent in a single transaction", className="font-extralight text-sm py-2"),
            ], className="p-4 bg-white text-black rounded-xl shadow-md"),
        ], className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6"),

        html.Div([
            html.Div([
                html.P("Monthly Spending Breakdown", className="font-semibold tracking-tight text-xl"),
                dcc.Graph(id="monthly-spending-bar-chart"),
            ], className="p-4 bg-white text-black rounded-xl shadow-md"),
        ], className="grid grid-cols-1 gap-4"),
    ], className="w-full grid grid-cols-1 lg:grid-cols-2 gap-4"),

    html.Div([
        html.Div([
            html.Div([
                html.P("Transaction Categories", className="font-semibold tracking-tight text-xl"),
                dcc.Graph(id="category-pie-chart"),
            ], className="p-4 bg-white text-black rounded-xl shadow-md"),

            html.Div([
                html.P("Spending Over Time", className="font-semibold tracking-tight text-xl"),
                dcc.Graph(id="spending-line-chart"),
            ], className="p-4 bg-white text-black rounded-xl shadow-md"),
        ], className="flex flex-col gap-4"),

        html.Div([
            html.Div([
                html.P("Payment Methods Breakdown", className="font-semibold tracking-tight text-xl"),
                dcc.Graph(id="payment-methods-pie-chart"),
            ], className="p-4 bg-white text-black rounded-xl shadow-md"),
            html.Div([
                html.P("Location-Based Spending", className="font-semibold tracking-tight text-xl"),
                dcc.Graph(id="location-bar-chart"),
            ], className="p-4 bg-white text-black rounded-xl shadow-md")
        ], className="flex flex-col gap-4 py-6"),
    ], className="grid grid-cols-1 pt-4 lg:grid-cols-2 gap-4"),

    html.Div([
        html.H1("Transaction Table", className="text-4xl py-2 font-bold text-black text-center"),
        html.Div(id="transaction-table-container", className="text-black p-4")
    ], className="w-full p-4 bg-white rounded-xl")
], className="w-full md:w-10/12 h-full rounded-xl p-6 mx-auto md:pl-48")

layout = html.Div(
    children=[
        dcc.Location(id="url", refresh=True),
        navbar,
        dash_screen,
    ],
    className="h-full w-full flex flex-col md:flex-row gap-4 bg-neutral-200 text-black"
)

@callback(
    [Output("category-pie-chart", "figure"),
     Output("spending-line-chart", "figure"),
     Output("payment-methods-pie-chart", "figure"),
     Output("location-bar-chart", "figure"),
     Output("monthly-spending-bar-chart", "figure"),
     Output("total-transactions", "children"),
     Output("total-amount-spent", "children"),
     Output("average-transaction-amount", "children"),
     Output('transaction-table-container', 'children'),
     Output("highest-transaction-amount", "children")],
    Input('url', 'pathname')
)
def update_dashboard(_):
    data = fetch_data()
    metrics = fetch_metrics()

    if not data or not metrics:
        empty_fig = px.pie(names=[], values=[], title="No Data Available")
        return (empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, 0, 0.0, 0.0, html.Div("No data available."), 0.0)

    total_amount_spent = metrics.get('total_amount_spent', 0)
    average_amount = metrics.get('average_amount', 0)
    highest_amount = metrics.get('highest_amount', 0)

    total_amount_spent = round(total_amount_spent, 2)
    average_amount = round(average_amount, 2)
    highest_amount = round(highest_amount, 2)

    total_transactions = len(data)

    category_df = {"Category": [d['category'] for d in data],
                   "Amount": [d['amount'] for d in data]}
    
    category_fig = px.pie(
        names=category_df['Category'],
        values=category_df['Amount'],
        title="Transaction Categories Breakdown"
    )

    date_df = {"Date": [d['date'] for d in data],
               "Amount": [d['amount'] for d in data]}

    date_df['Date'] = [datetime.strptime(d, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%d') for d in date_df['Date']]
    
    spending_fig = px.line(
        x=date_df['Date'],
        y=date_df['Amount'],
        title="Spending Over Time",
        labels={"x": "Date", "y": "Amount"}
    )
    
    payment_method_df = {"Payment Method": [d["payment_method"] for d in data],
                         "Amount": [d["amount"] for d in data]}
    
    payment_method_fig = px.pie(
        names=payment_method_df["Payment Method"],
        values=payment_method_df["Amount"],
        title="Payment Methods Breakdown"
    )

    location_df = {"Location": [d["location"] for d in data],
                   "Amount": [d["amount"] for d in data]}
    
    location_fig = px.bar(
        x=location_df["Location"],
        y=location_df["Amount"],
        title="Location-Based Spending",
        labels={"x": "Location", "y": "Amount"}
    )

    date_df['Month'] = [datetime.strptime(d, '%Y-%m-%d').strftime('%Y-%m') for d in date_df['Date']]
    monthly_spending_df = {"Month": list(set(date_df['Month'])),
                            "Amount": [sum(date_df['Amount'][i] for i in range(len(date_df['Month'])) if date_df['Month'][i] == month) for month in set(date_df['Month'])]}
    
    monthly_spending_fig = px.bar(
        x=monthly_spending_df["Month"],
        y=monthly_spending_df["Amount"],
        title="Monthly Spending Breakdown",
        labels={"x": "Month", "y": "Amount"}
    )


    table = update_transaction_table(_)

    return (category_fig, spending_fig, payment_method_fig, location_fig, monthly_spending_fig, total_transactions, total_amount_spent, average_amount, table, highest_amount)


def update_transaction_table(_):
    try:
        response = requests.get("http://localhost:8050/api/v1/transact/")
        if response.status_code == 200:
            transactions = response.json()
            if transactions:
                table = dash_table.DataTable(
                    columns=[{"name": col, "id": col} for col in transactions[0].keys()],
                    data=transactions,
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'left'},
                )
                return table
            else:
                return html.Div("No transactions found.")
        else:
            return html.Div(f"Error: {response.status_code}")
    except Exception as e:
        return html.Div(f"Error: {str(e)}")