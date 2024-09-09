import dash
from dash import html,dcc,callback,Output,Input,dash_table
import dash_bootstrap_components as dbc
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
            print(f"Failed to authenticate. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error occurred while making the request: {str(e)}")
        return []
    
def fetch_metrics():
    try:
        response = requests.get("http://localhost:8050/api/v1/transact/num_transaction")
        if response.status_code==200:
            return response.json()['data']
        else:
            print(f"Failed to authenticate. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred while making the request: {str(e)}")


today_date=datetime.now().strftime('%d-%m-%Y')

navbar = html.Div([
    html.Div([
        html.H1("Transact", className="text-black font-bold py-6 text-3xl text-center"),
        html.Div([
            html.A(
                html.H2("Home", className="text-black font-semibold w-full p-2 rounded-md bg-cyan-100 text-lg tracking-wider"),
                href="/app/dashboard", className="w-full"
            ),
            html.A(
                html.H2("Spending Updates", className="text-black font-semibold active:bg-cyan-100 w-full p-2 rounded-md text-lg tracking-wider"),
                href="/app/spending-updates", className="w-full"
            ),
        ], className="flex flex-col gap-2 w-full"),
    ], className="flex flex-col h-full"),
    html.Div(
        dbc.Button("Logout", id="logout-btn",n_clicks=0, color="danger", className="w-full"),
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
        dcc.Location(id="url"),
        navbar,
        dash_screen,
    ],
    className="h-full w-full flex flex-col md:flex-row gap-4 bg-neutral-200 text-black"
)

@callback(
    [
        Output("category-pie-chart", "figure"),
        Output("spending-line-chart", "figure"),
        Output("payment-methods-pie-chart", "figure"),
        Output("location-bar-chart", "figure"),
        Output("monthly-spending-bar-chart", "figure"),
        Output("total-transactions", "children"),
        Output("total-amount-spent", "children"),
        Output("average-transaction-amount", "children"),
        Output("highest-transaction-amount", "children"),
        Output('transaction-table-container', 'children'),
    ],
    [Input('url', 'pathname')]
)
def update_dashboard(pathname):
    data = fetch_data()
    metrics = fetch_metrics()

    if not data or not metrics:
        empty_fig = px.pie(names=[], values=[], title="No Data Available")
        return (
            empty_fig, empty_fig, empty_fig, empty_fig, empty_fig,
            0, 0.0, 0.0, 0.0, html.Div("No data available.")
        )

    total_amount_spent = round(metrics.get('total_amount_spent', 0), 2)
    average_amount = round(metrics.get('average_amount', 0), 2)
    highest_amount = round(metrics.get('highest_amount', 0), 2)
    total_transactions = len(data)


    category_fig = px.pie(
        names=[d['category'] for d in data],
        values=[d['amount'] for d in data],
        title="Transaction Categories Breakdown"
    )

    spending_fig = px.line(
        x=[d['date'] for d in data],
        y=[d['amount'] for d in data],
        title="Spending Over Time",
        labels={"x": "Date", "y": "Amount"}
    )

    payment_method_fig = px.pie(
        names=[d['payment_method'] for d in data],
        values=[d['amount'] for d in data],
        title="Payment Methods Breakdown"
    )

    location_fig = px.bar(
        x=[d['location'] for d in data],
        y=[d['amount'] for d in data],
        title="Location-Based Spending"
    )

    monthly_spending_fig = px.bar(
        x=list(set([datetime.strptime(d['date'], '%Y-%m-%d').strftime('%Y-%m') for d in data])),
        y=[d['amount'] for d in data],
        title="Monthly Spending Breakdown"
    )

    return (
        category_fig, spending_fig, payment_method_fig, location_fig, 
        monthly_spending_fig, total_transactions, total_amount_spent,
        average_amount, highest_amount, update_transaction_table(pathname)
    )


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
    
@callback(
    Output('url', 'pathname'),
    [Input('logout-btn', 'n_clicks')]
)
def logout(n_clicks):
    if n_clicks:
        try:
            response = requests.get("http://localhost:8050/api/v1/auth/logout")
            if response.status_code == 200:
                return "/app/"
            else:
                return "/app/dashboard"
        except Exception as e:
            print(f"Error during logout: {str(e)}")
            return "/app/dashboard"
    return dash.no_update
