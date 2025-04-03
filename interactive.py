# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 12:13:51 2025

@author: Roh Jun Seok

인터랙티브 시각화: html 파일로 저장 후 web에서 실행
"""

import pandas as pd
mpg = pd.read_csv('./data/mpg.csv')

import plotly.express as px

# 산점도
fig = px.scatter(mpg, x='cty', y='hwy', color='drv')
fig.write_html('scatter_plot.html')

import webbrowser as webb
webb.open_new('scatter_plot.html')

# 막대 그래프
df = mpg.groupby('category', as_index=False).agg(total=('category', 'count'))

fig = px.bar(df, x='category', y='total', color='category')

fig.write_html('bar_plot.html')
webb.open_new('bar_plot.html')

# 선 그래프
eco = pd.read_csv('./data/economics.csv')

fig = px.line(eco, x='date', y='psavert')
fig.write_html('line_plot.html')
webb.open_new('line_plot.html')

# boxplot()
fig = px.box(mpg, x='drv', y='hwy', color='drv')
fig.write_html('box_plot.html')
webb.open_new('box_plot.html')

fig = px.scatter(mpg, x='hwy', y='cty', color='drv', width=600, height=400)
fig.write_html('size_scatter.html')
webb.open_new('size_scatter.html')
