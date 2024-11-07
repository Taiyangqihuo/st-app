import streamlit as st
import datetime
import plotly.express as px
import plotly.graph_objects as go

st.markdown(
    "<p style='text-align: center; font-size: 36px; font-weight: bold;'>用户能耗分析</p>",
    unsafe_allow_html=True
)
st.divider()
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
    c1, c2= st.columns(2)
    with c1:
        st.image("missj.png")
    with c2:
        data = dict(
            character=["总能耗","热管理","压缩机","鼓风机","驱动损失","电机效率损失","传动效率损失","制动耗散","电池内阻损失","低压损失"],
            parent=["", "总能耗", "热管理", "热管理", "总能耗", "驱动损失", "驱动损失", "驱动损失","总能耗","总能耗" ],
            value=[100, 25, 20,5, 75, 10, 5, 60, 1, 2])

        fig = px.sunburst(
            data,
            names='character',
            parents='parent',
            values='value',
        )
        st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure(go.Sankey(
        arrangement='snap',
        node=dict(
            label=["交流充电", "直流充电", "动力电池", "电机", "高压电器", "低压电器"],
            align="right",
        ),
        link=dict(
            arrowlen=15,
            source=[0, 1, 2, 2, 2],
            target=[2, 2, 3, 4, 5],
            value=[32, 68, 85, 10, 5]  
        )
    ))
    st.plotly_chart(fig, use_container_width=True)