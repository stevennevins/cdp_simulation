import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go

from cdp import cdp_sim, bt, ccxt_datahandler, cdp_sim_ma
from analyzers import coll_ratio, amt_eth

pairs = 'BTC/USDT','ETH/USDT'
strats = {'CDP':cdp_sim,
'CDP MA':cdp_sim_ma}
timeframes = {'1d':'1d'}
def run_sim(strat, pair, exchange, tf,args):
    cerebro = bt.Cerebro()
    print(args)
    if strat == 'CDP':
        cerebro.addstrategy(strats[strat],verbose=False,a_upper=args[3]/100,a_lower=args[1]/100,a_target=args[2]/100)
    elif strat == 'CDP MA':
        cerebro.addstrategy(strats[strat],verbose=False,a_upper=args[3]/100,a_lower=args[1]/100,a_target=args[2]/100,period=args[0],na_lower=args[4]/100,na_target=args[5]/100,na_upper=args[6]/100)
        #,period=args[],a_upper=,a_lower=,a_target=
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
        name='#Asset',
        mode='lines',
        yaxis='y1'
    )
    trace2 = go.Scatter(
        x=col_rat[0],
        y=col_rat[1],
        name='Collateralization Ratio',
        mode='markers',
        yaxis='y2',
    )
    data = [trace1,trace2]
    layout= go.Layout(
        title='CDP Simulation',
        yaxis = dict(title='Amount of Asset',type='log'),
        yaxis2 = dict(title='Collateralization Ratio',overlaying='y',side='right',range=[col_rat[1].nsmallest(2).iloc[-1]*.9,max(col_rat[1])*1.1])
        )
    fig = go.Figure(data=data,layout=layout)
    return dcc.Graph(id='sim_results',figure=fig)

home_page = dbc.Jumbotron(
    [
        dbc.Container(
            children=[
                html.H1("CDP Simulator", className="strong"),
                html.P('Pairs:',style={'display':'inline-block'}),
                dcc.Dropdown(
                    id='pairs-dd',
                    options=[{'label': i, 'value': i} for i in pairs],
                    value='ETH/USDT',
                    style={'display':'inline-block','width':'7.5rem'}
                ),
                html.P('Strategies:',style={'display':'inline-block'}),
                dcc.Dropdown(
                    id='strat-dd',
                    options = [{'label': i, 'value': i} for i,v in strats.items()],
                    value='CDP MA',
                    style={'display':'inline-block','width':'7.5rem'}
                ),
                html.P('Timeframe:',style={'display':'inline-block'}),
                dcc.Dropdown(
                    id='tf-dd',
                    options = [{'label': i, 'value': i} for i,v in timeframes.items()],
                    value='1d',
                    style={'display':'inline-block','width':'7.5rem'}
                ),
                html.P(id='period-text',children='Period: ',style={'display':'inline-block'}),
                dcc.Input(id='period-input',type='number',value=20,style={'display':'inline-block','width':'4rem'}),
                html.P(id='R_L-text',children='Risky Lower: ',style={'display':'inline-block'}),
                dcc.Input(id='R_L-input',type='number',value=180,style={'display':'inline-block','width':'4rem'}),
                html.P(id='R_T-text',children='Riksy Target: ',style={'display':'inline-block'}),
                dcc.Input(id='R_T-input',type='number',value=200,style={'display':'inline-block','width':'4rem'}),
                html.P(id='R_U-text',children='Risky Upper: ',style={'display':'inline-block'}),
                dcc.Input(id='R_U-input',type='number',value=220,style={'display':'inline-block','width':'4rem'}),
                html.P(id='NR_L-text',children='Less Risky Lower: ',style={'display':'inline-block'}),
                dcc.Input(id='NR_L-input',type='number',value=250,style={'display':'inline-block','width':'4rem'}),
                html.P(id='NR_T-text',children='Less Risky Target: ',style={'display':'inline-block'}),
                dcc.Input(id='NR_T-input',type='number',value=300,style={'display':'inline-block','width':'4rem'}),
                html.P(id = 'NR_U-text',children='Less Risky Upper: ',style={'display':'inline-block'}),
                dcc.Input(id='NR_U-input',type='number',value=350,style={'display':'inline-block','width':'4rem'}),
                dcc.Loading(id='graph-content')
            ],
            fluid=True,
        )
    ],
)
input_ids = ['period-text','period-input','R_L-text','R_L-input','R_T-text','R_T-input','R_U-text','R_U-input','NR_L-text','NR_L-input','NR_T-text','NR_T-input','NR_U-text','NR_U-input']