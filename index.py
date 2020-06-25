import dash_core_components as dcc
import dash_html_components as html

from layouts import navbar
from app import app
import callbacks

server = app.server

content = html.Div(id="page-content")

location = dcc.Location(id="url")

app.layout = html.Div([navbar, location, content])

if __name__ == "__main__":
    app.run_server(debug=True)