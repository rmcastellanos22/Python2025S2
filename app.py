# incluir los paquetes

import plotly as pl
import numpy as np
import pathlib

from dash import Dash, dcc, html, dash_table, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# paso 1
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#Github linea de server
server = app.server()

app.title = "Dashboard Financiero Github"

# dataset
df = pd.read_csv("empresas.csv")

sales_list = [
    "Total Revenues", "Cost of Revenues", "Gross Profit", "Total Operating Expenses",
    "Operating Income", "Net Income", "Shares Outstanding", "Close Stock Price",
    "Market Cap", "Multiple of Revenue"
]

# paso 2
app.layout = html.Div([
    html.Div([
        # Dropdown para empresas (multi)
        html.Div(
            dcc.Dropdown(
                id="empresa-dropdown",
                value=["Apple", "Tesla", "Microsoft", "Google"],  # sin duplicados
                options=[{"label": x, "value": x} for x in sorted(df["Company"].unique())],
                clearable=False,
                multi=True,                  # ⬅️ IMPORTANTE
                style={"width": "100%"}
            ),
            className="six columns"
        ),

        # Dropdown variable numérica
        html.Div(
            dcc.Dropdown(
                id="numericdropdown",
                value="Total Revenues",
                options=[{"label": x, "value": x} for x in sales_list],
                clearable=False,
                style={"width": "100%"}
            ),
            className="six columns"
        ),
    ], className="custom-dropdown"),

    # Gráficas
    html.Div([dcc.Graph(id="bar", figure={})]),
    html.Div([dcc.Graph(id="boxplot", figure={})]),

    # Tabla
    html.Div(
        html.Div(id="table-container_1"),
        style={"marginBottom": "15px", "marginTop": "15px"}
    ),
])

# paso 3
@app.callback(
    [Output("bar", "figure"),
     Output("boxplot", "figure"),
     Output("table-container_1", "children")],
    [Input("empresa-dropdown", "value"),
     Input("numericdropdown", "value")]
)
# paso 4
def display_value(selected_stock, selected_numeric):
    if not selected_stock:
        selected_stock = ["Apple", "Tesla", "Microsoft", "Google"]

    dfv_filtered = df[df["Company"].isin(selected_stock)]

    # Línea
    fig = px.line(
        dfv_filtered, x="Quarter", y=selected_numeric, markers=True, color="Company",
        width=1000, height=500
    )
    fig.update_layout(
        title=f"{selected_numeric} de {', '.join(selected_stock)}",
        xaxis_title="Quarter", yaxis_title=selected_numeric, template="plotly_dark"
    )
    fig.update_traces(line=dict(width=2))

    # Boxplot
    fig2 = px.box(
        dfv_filtered, x="Company", y=selected_numeric, color="Company",
        width=800, height=500
    )
    fig2.update_layout(
        title=f"Distribución de {selected_numeric} de {', '.join(selected_stock)}",
        xaxis_title="Company", yaxis_title=selected_numeric, template="plotly_dark"
    )

    # Tabla
    df_reshaped = dfv_filtered.pivot(index="Company", columns="Quarter", values=selected_numeric)
    df_reshaped2 = df_reshaped.reset_index()  # ⬅️ SIN inplace

    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_reshaped2.columns],
        data=df_reshaped2.to_dict("records"),
        export_format="csv",
        fill_width=True,
        style_table={"backgroundColor": "Blue", "color": "white"},
        style_cell={"textAlign": "left", "minWidth": "100px", "width": "100px", "maxWidth": "100px"},
        style_header={"backgroundColor": "rgb(30,30,30)", "fontWeight": "bold", "color": "white"},
        style_data={"backgroundColor": "white", "color": "black"}  # ⬅️ en lugar de style_data_conditional
    )

    return fig, fig2, table

# Correr la app

# Para git agregar host

if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=10000)
