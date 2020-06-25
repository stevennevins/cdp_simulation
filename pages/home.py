import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go

from cdp import cdp_sim, bt, ccxt_datahandler
from analyzers import coll_ratio, amt_eth

pairs = 'BTC/USDT','ETH/USDT'
def run_sim(strat, pair, exchange, tf):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(strat,verbose=False)
    cerebro.broker.setcash(1000000000000000000000000000000)
    cerebro.adddata(bt.feeds.PandasData(dataname=ccxt_datahandler(pair, exchange, tf)))
    cerebro.addanalyzer(amt_eth, _name='amt_eth')
    cerebro.addanalyzer(coll_ratio,_name='coll_ratio')
    strat = cerebro.run()[0]
    return strat

def return_go(sim):
    amt = sim.analyzers.amt_eth.get_analysis()['amt_eth']
    col_rat = sim.analyzers.coll_ratio.get_analysis()['coll_ratios']
    trace1 = go.Scatter(
        x=amt[0],
        y=amt[1],
        name='Amount of ETH',
        mode='lines+markers',
        yaxis='y1'
    )
    trace2 = go.Scatter(
        x=col_rat[0],
        y=col_rat[1],
        name='Collateralization Ratio',
        mode='lines+markers',
        yaxis='y2'
    )
    data = [trace1,trace2]
    layout= go.Layout(
        title='CDP Simulation',
        yaxis = dict(title='Amount of Asset'),
        yaxis2 = dict(title='Collateralization Ratio',overlaying='y',side='right')
        )
    fig = go.Figure(data=data,layout=layout)
    return dcc.Graph(id='sim_results',figure=fig)

home_page = dbc.Jumbotron(
    [
        dbc.Container(
            children=[
                html.H1("CDP Simulator", className="strong"),
                dcc.Dropdown(
                    id='pairs-dd',
                    options=[{'label': i, 'value': i} for i in pairs],
                    value='ETH/USDT',
                    style={'display':'inline-block','width':'7.5rem'}
                ),
                dcc.Loading(id='graph-content')
            ],
            fluid=True,
        )
    ],
)