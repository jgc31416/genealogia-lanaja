# DASH attempt, cannot cope with the network size
"""
from typing import List, Dict
from dash import dash
from dash import html
import visdcc

def initialize_app(nodes, edges):
    app = dash.Dash()
    node_list = [{"id": node[0], "label": node[1], "shape": "dot", "size": 7} for node in nodes]
    edge_list = [{'id': f"{edge[0][0]}--{edge[1][0]}", 'from': edge[0][0], 'to':edge[1][0], 'width':2} for edge in edges]
    app.layout = html.Div(
        [
            visdcc.Network(id='net',
                           data={'nodes': node_list, 'edges': edge_list},
                           options={'height': '800px', 'width':'100%'})
        ]
    )
    return app
"""
