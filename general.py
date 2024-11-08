import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import json
st.markdown(
    "<p style='text-align: center; font-size: 36px; font-weight: bold;'>入网信息概览</p>",
    unsafe_allow_html=True
)
st.divider()
column_data = pd.read_excel("citys.xlsx")
c1, c2= st.columns([4,1])
with c1:
    with open('china.json', 'r',encoding='utf-8') as file:
        geojson_data = json.load(file)
    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=35,
                longitude=103,
                zoom=2.8,
                pitch=40,
            ),
            layers=[
                pdk.Layer(
                    'ColumnLayer',
                    data=column_data,
                    get_position="[lon, lat]",
                    get_elevation='hei',
                    get_color="[255, 255-hei*2, 0]",  # 固定颜色
                    elevation_scale=10000,  # 控制柱状图的高度缩放
                    radius=20000,
                    pickable=True,
                    onClick=True,
                    extruded=True,
                ),
                pdk.Layer(
                    'GeoJsonLayer',
                    geojson_data,  # GeoJson数据源
                    opacity=0.8,
                    stroked=False,
                    filled=True,
                    extruded=True,
                    wireframe=True,
                    get_elevation=100,  # 根据属性计算高度
                    get_fill_color=[40, 40, 233],  # 根据属性计算填充颜色
                    get_line_color=[255, 255, 255],
                    pickable=True,
                    get_text='properties.name',
                    get_text_size=24,
                ),
            ],
        )
    )
# table=column_data[['name','hei']].copy()
# table.rename(columns={'name': '城市','hei':'车辆数'}, inplace=True)
c2.dataframe(column_data[['name','hei']],hide_index=True,column_config={
    'name':{'label':'城市','width':'small'},
    'hei':{'label':'车辆数','width':None}
})
st.divider()
date = pd.date_range(start='2022-01-01', end='2024-10-31', freq='MS')
num1=[]
num2=[]
for idx,month in enumerate(date):
    num1.append(idx*10+np.random.randint(0, 20))
    num2.append(idx*10+np.random.randint(0, 18))
df1 = pd.DataFrame({'时间':date,'入网数量':num1})
df2 = pd.DataFrame({'时间':date,'入网数量':num2})
tab1,tab2=st.tabs(["米时捷","保时泰"])
with tab1:
    col1, col2= st.columns([2,3])
    with col1:
        st.image("missj.png")
    with col2:
        fig = px.line(df1, x='时间', y='入网数量', title='米时捷入网数量')
        st.plotly_chart(fig, use_container_width=True)
with tab2:
    col1, col2= st.columns([2,3])
    with col1:
        st.image("BullShitTai.png")
    with col2:
        fig = px.line(df2, x='时间', y='入网数量', title='保时泰入网数量')
        st.plotly_chart(fig, use_container_width=True)