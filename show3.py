import streamlit as st
import numpy as np
import datetime
import pandas as pd
from plotly.graph_objs import *
import plotly.figure_factory as ff


st.markdown(
    "<p style='text-align: center; font-size: 36px; font-weight: bold;'>用户行为分析</p>",
    unsafe_allow_html=True
)
st.divider()
st.subheader("用户踏板深度分布")
col1, col2= st.columns(2)
with col1:
    option = st.selectbox(
        "用户VIN",
        ("xxxxxxx", "yyyyyyy", "zzzzzzz"),
        index=None,
        placeholder="请选择车架号",
    )
with col2:
    today = datetime.datetime.now()
    last_year = today.year - 1
    last_year_today = datetime.date(last_year, today.month, today.day)

    # 设置日期输入的最小值和最大值
    min_date = last_year_today
    max_date = today

    # 创建日期选择器
    d = st.date_input(
        "选择数据区间",
        (min_date,max_date),
        min_date,
        max_date,
        format="YYYY.MM.DD",
    )
if option!=None:
    c1, c2= st.columns([4,1])
    with c2:
        tb = st.selectbox(
        "踏板选择",
        ("加速", "制动"),
    )
        show_hist = st.checkbox("显示直方图",True)
        show_curve= st.checkbox("显示曲线",True)
        show_rug=st.checkbox("显示地毯图",True)
    with c1:
        if not option in st.session_state:
            x1 = np.random.rand(200)
            x2 = 0.8*np.random.rand(200)
            st.session_state[option] = [x1, x2]
        hist_data=st.session_state[option]
        group_labels = ['同车型踏板分布', '用户踏板分布']
        # Create distplot with custom bin_size
        fig = ff.create_distplot(
                hist_data, group_labels, bin_size=[.01, .01],
                show_hist=show_hist,
                show_curve=show_curve,
                show_rug=show_rug
                )
        # Plot!
        st.plotly_chart(fig, use_container_width=True)
st.divider()
st.subheader("用户速度/加速度分布")
if option!=None:
    show_on = st.toggle("显示散点",True)
    df=pd.read_excel('wltc.xlsx',header=None)
    df.columns = ['t','v']
    v=df['v'].values
    a=np.diff(v)/3.6
    a=np.append(a,0)
    idx=(v!= 0) | (a!= 0)
    v0=v[idx]
    a0=a[idx]
    trace1 = {
    "type": "histogram2d", 
    "x": v0,
    "y": a0, 
    "xbins": {
        "end": 140, 
        "size": 5, 
        "start": 0
    }, 
    "ybins": {
        "end": 2, 
        "size": 0.1, 
        "start": -2
    }, 
    "zsmooth": "best", 
    "colorbar": {
        "x": 0.99, 
        "y": 0.35, 
        "len": 0.7, 
        "ticks": "outside", 
        "title": "加速度分布", 
        "thickness": 20, 
        "titleside": "right"
    }, 
    "colorscale": "Portland"
    #   "colorscale": [[0, 'rgb(12,51,131)'], [0.02, 'rgb(10,136,186)'], [0.04, 'rgb(242,211,56)'], [0.08, 'rgb(242,143,56)'], [1, 'rgb(217,30,30)']]
    }
    trace2 = {
    "mode": "markers", 
    "name": "", 
    "type": "scatter", 
    "x": v0,
    "y": a0,
    "marker": {
        "size": 2, 
        "color": "#e0e0e0"
    }, 
    #   "text": [0:1:1800]
    }
    trace3 = {
    "name": "", 
    "type": "histogram", 
    "x":v0,
    "xaxis": "x1", 
    "xbins": {
        "end": 140, 
        "size": 5, 
        "start": 0
    }, 
    "yaxis": "y2", 
    "marker": {"color": "rgb(242,211,56)"}
    }
    trace4 = {
    "name": "", 
    "type": "histogram", 
    "y": a0,
    "xaxis": "x2", 
    "yaxis": "y1", 
    "ybins": {
        "end": 2, 
        "size": 0.1, 
        "start": -2
    }, 
    "marker": {"color": "rgb(242,211,56)"}
    }
    if show_on==True:
        data = Data([trace1, trace2, trace3, trace4])
    else:
        data = Data([trace1, trace3, trace4])
    layout = {
    "font": {
        "size": 13, 
        "family": "PT Sans Narrow, sans-serif"
    }, 
    "title": "速度分布", 
    "width": 650, 
    "xaxis": {
        "range": [0, 150], 
        "title": "v", 
        "domain": [0, 0.7], 
        "zeroline": False
    }, 
    "yaxis": {
        "range": [-2, 2], 
        "title": "a", 
        "domain": [0, 0.7], 
        "showgrid": False, 
        "zeroline": False
    }, 
    "height": 520, 
    "xaxis2": {
        "domain": [0.75, 1], 
        "showgrid": True, 
        "zeroline": False
    }, 
    "yaxis2": {
        "domain": [0.75, 1], 
        "showgrid": True, 
        "zeroline": False
    }, 
    "autosize": False, 
    "showlegend": False, 
    "annotations": [
        {
        "x": 1, 
        "y": 1, 
        "text": "WLTC循环工况", 
        "xref": "paper", 
        "yref": "paper", 
        "xanchor": "right", 
        "yanchor": "bottom", 
        "showarrow": False
        }
    ]
    }
    fig = Figure(data=data, layout=layout)
    st.plotly_chart(fig, use_container_width=True)

    #后面是用户工况
    df=pd.read_excel('user.xlsx',header=None)
    df.columns = ['t','v']
    v=df['v'].values
    a=np.diff(v)/3.6
    a=np.append(a,0)
    idx=(v!= 0) | (a!= 0)
    v0=v[idx]
    a0=a[idx]
    trace1 = {
    "type": "histogram2d", 
    "x": v0,
    "y": a0, 
    "xbins": {
        "end": 140, 
        "size": 5, 
        "start": 0
    }, 
    "ybins": {
        "end": 2, 
        "size": 0.1, 
        "start": -2
    }, 
    "zsmooth": "best", 
    "colorbar": {
        "x": 0.99, 
        "y": 0.35, 
        "len": 0.7, 
        "ticks": "outside", 
        "title": "加速度分布", 
        "thickness": 20, 
        "titleside": "right"
    }, 
    "colorscale": "Portland"
    #   "colorscale": [[0, 'rgb(12,51,131)'], [0.02, 'rgb(10,136,186)'], [0.04, 'rgb(242,211,56)'], [0.08, 'rgb(242,143,56)'], [1, 'rgb(217,30,30)']]
    }
    trace2 = {
    "mode": "markers", 
    "name": "", 
    "type": "scatter", 
    "x": v0,
    "y": a0,
    "marker": {
        "size": 2, 
        "color": "#e0e0e0"
    }, 
    #   "text": [0:1:1800]
    }
    trace3 = {
    "name": "", 
    "type": "histogram", 
    "x":v0,
    "xaxis": "x1", 
    "xbins": {
        "end": 140, 
        "size": 5, 
        "start": 0
    }, 
    "yaxis": "y2", 
    "marker": {"color": "rgb(242,211,56)"}
    }
    trace4 = {
    "name": "", 
    "type": "histogram", 
    "y": a0,
    "xaxis": "x2", 
    "yaxis": "y1", 
    "ybins": {
        "end": 2, 
        "size": 0.1, 
        "start": -2
    }, 
    "marker": {"color": "rgb(242,211,56)"}
    }
    if show_on==True:
        data = Data([trace1, trace2, trace3, trace4])
    else:
        data = Data([trace1, trace3, trace4])
    layout = {
    "font": {
        "size": 13, 
        "family": "PT Sans Narrow, sans-serif"
    }, 
    "title": "速度分布", 
    "width": 650, 
    "xaxis": {
        "range": [0, 150], 
        "title": "v", 
        "domain": [0, 0.7], 
        "zeroline": False
    }, 
    "yaxis": {
        "range": [-2, 2], 
        "title": "a", 
        "domain": [0, 0.7], 
        "showgrid": False, 
        "zeroline": False
    }, 
    "height": 520, 
    "xaxis2": {
        "domain": [0.75, 1], 
        "showgrid": True, 
        "zeroline": False
    }, 
    "yaxis2": {
        "domain": [0.75, 1], 
        "showgrid": True, 
        "zeroline": False
    }, 
    "autosize": False, 
    "showlegend": False, 
    "annotations": [
        {
        "x": 1, 
        "y": 1, 
        "text": "用户工况", 
        "xref": "paper", 
        "yref": "paper", 
        "xanchor": "right", 
        "yanchor": "bottom", 
        "showarrow": False
        }
    ]
    }
    fig = Figure(data=data, layout=layout)
    st.plotly_chart(fig, use_container_width=True)

