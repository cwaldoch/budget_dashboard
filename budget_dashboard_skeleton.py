# -*- coding: utf-8 -*-
"""
Created on Thu May  9 11:35:52 2019

@author: cwaldoch
"""

import dash, webbrowser, pdb, pyodbc
import pandas as pd
import dash_table

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
from datetime import datetime as dt

locPath = ''

app = dash.Dash(__name__)

# default values
#app.css.config.serve_locally = True
#app.scripts.config.serve_locally = True
#app.config.assets_folder = 'assets'     # The path to the assets folder.
#app.config.include_asset_files = True   # Include the files in the asset folder
#app.config.assets_external_path = ""    # The external prefix if serve_locally == False
#app.config.assets_url_path = '/assets'  # the local url prefix ie `/assets/*.js`
colorRef = pd.read_csv(locPath+'small_color_list.csv', low_memory=False)
        
app.config['suppress_callback_exceptions'] = True

dfData = pd.read_csv(locPath+'dfspend_extend.csv', low_memory=False)
dfData['Tx-dt'] = pd.to_datetime(dfData['Transaction Date'])

dfData['yr'] = dfData['Tx-dt'].dt.year
dfData['m'] = dfData['Tx-dt'].dt.month
dfData['m-yr'] = [str(x)+'-'+str(y) for x,y in zip(dfData['m'].values, dfData['yr'].values)]

dfData['Amount'] = np.round(dfData['Amount'],0)

app.layout = html.Div([html.Div([
        dcc.DatePickerRange(id='data-date-picker', 
                            min_date_allowed=min(dfData['Tx-dt']),
                            max_date_allowed=max(dfData['Tx-dt']),
                            initial_visible_month=max(dfData['Tx-dt'])-pd.Timedelta('30 days'),
                            end_date=max(dfData['Tx-dt'])),
        ]),
    dcc.Tabs(id="tabs", value='tab-0', children=[
        dcc.Tab(label='Overview', value='tab-0'),
        dcc.Tab(label='Monthly Spend', value='tab-1'),
        dcc.Tab(label='Transactions Table', value='tab-2'),
    ]),
    dcc.Loading(id='loading-1', children=[html.Div(id='tabs-content')],type='cube')
])
 
finalTags = list(set(dfData['Final Tags']))
tagOptions = []
for tag in finalTags:
    tagOptions.append({'label':tag,'value':tag})

tagColors = list(colorRef['colors'].values)[:len(finalTags)]
dictColors = dict(zip(finalTags, tagColors))
dfData['tagColors'] = [dictColors[x] for x in dfData['Final Tags'].values]

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value'),
               Input('data-date-picker', 'start_date'),
               Input('data-date-picker', 'end_date')])
def render_content(tab, startDate, endDate):
    
    yAxis = {'tickformat':'$:,.2r'}
    if tab == 'tab-0':
        graphs = []
        
        graphingAll = dfData[(dfData['Tx-dt'] >= startDate) & (dfData['Tx-dt'] <= endDate)]
        
        allSpend = graphingAll.groupby(['Final Tags'])['Amount'].sum()
        #pdb.set_trace()
        outlineDict = {'color':'black', 'width':1.5}
        barColor = {'color':[dictColors[x] for x in allSpend.index], 'line':outlineDict}
        data1 = [{'x':allSpend.index, 'y': allSpend.values, 'type':'bar',
                  'marker':barColor}]
        graphObj =  dcc.Graph(id='allSpend-graph',  figure={
                        'data': data1,
                        'layout': {'yaxis':yAxis,
                            'title': 'All Profit'}})           
        graphs.append(graphObj)
        
#        barColor = {'color':[dictColors[x] for x in graphingAll['Final Tags'].values], 'line':outlineDict}
#        data2 = [{'x':graphingAll['Tx-dt'], 'y': graphingAll['Amount'], 'type':'bar',
#                  'marker':barColor}]
#        graphObj =  dcc.Graph(id='dailySpend-graph',  figure={
#                        'data': data2,
#                        'layout': {'yaxis':yAxis,
#                            'title': 'Daily Stacked Spend','barmode':'stack',
#                            'showlegend':True}})           
#        graphs.append(graphObj)
        tagChoices = list(set(dfData['Final Tags']))
        data2 = []
        for tag in tagChoices:

            dfTag = graphingAll[graphingAll['Final Tags'] == tag]
            
            if len(dfTag) > 0:
                tagSum = dfTag.groupby(['Tx-dt'])['Amount'].sum()

                barColor = {'color':dictColors[tag], 'line':outlineDict}
                hoverInfo = [str(np.round(x,2)) +' '+tag for x in tagSum.values]
                trace = {'x':tagSum.index, 'y': tagSum.values,
                             'type': 'bar', 'name':tag, 'marker':barColor,
                             'text':hoverInfo}
                data2.append(trace)
                
        graphObj =  dcc.Graph(id='dailySpend-graph',  figure={
                        'data': data2,
                        'layout': {'yaxis':yAxis,
                            'title': 'Daily Stacked Spend','barmode':'stack',
                            'showlegend':True}})           
        graphs.append(graphObj)
        
        return html.Div(graphs)
    
    if tab == 'tab-1':
        graphs = []
                #pdb.set_trace()
        outlineDict = {'color':'black', 'width':1.5}
        
        graphingAll = dfData[(dfData['Tx-dt'] >= startDate) & (dfData['Tx-dt'] <= endDate)]
        tagChoices = list(set(dfData['Final Tags']))
        data2 = []
        for tag in tagChoices:

            dfTag = graphingAll[graphingAll['Final Tags'] == tag]
        
            if len(dfTag) > 0:
                tagSum = dfTag.groupby(['m-yr'])['Amount'].sum()

                barColor = {'color':dictColors[tag], 'line':outlineDict}
                #hoverInfo = [tag for x in tagSum.values]
                trace = {'x':tagSum.index, 'y': tagSum.values,
                             'type': 'bar', 'name':tag, 'marker':barColor}
                             #'text':hoverInfo}
                data2.append(trace)
                
        graphObj =  dcc.Graph(id='monthlySpend-graph',  figure={
                        'data': data2,
                        'layout': {'yaxis':yAxis,
                            'title': 'Monthly Stacked Spend','barmode':'stack',
                            'showlegend':True}})           
        graphs.append(graphObj)
        return html.Div(graphs)

    elif tab == 'tab-2':
        graphs = []
        
        graphingAll = dfData[(dfData['Tx-dt'] >= startDate) & (dfData['Tx-dt'] <= endDate)]
        
        #pdb.set_trace() 
        tableObj = dash_table.DataTable(id='tx_datatable', data=graphingAll.to_dict('records'),
        columns = [{"name":i,"id":i} for i in graphingAll.columns],
                  style_cell={'textAlign':'left',
                              'minWidth': '60px', 'width': '60px', 'maxWidth': '150px',
                              'whiteSpace':'no-wrap',
                              'overflow':'hidden',
                              'textOverflow':'ellipsis'},
                  style_cell_conditional=[
                          {
                              'if':{'row_index':'odd'},
                               'minWidth': '60px', 'width': '60px', 'maxWidth': '150px',
                              'backgroundColor':'rgb(248,248,248)',
                              'textAlign':'left',
                              'whiteSpace':'no-wrap',
                              'overflow':'hidden',
                              'textOverflow':'ellipsis' }])
        graphs.append(tableObj)
        return html.Div(graphs)
        

webbrowser.open_new('http://127.0.0.1:9999/')
if __name__ == '__main__':
    app.run_server(port=9999)