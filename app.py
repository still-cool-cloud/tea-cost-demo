# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 16:09:37 2026

@author: 徐冉
"""

# streamlit完整交互demo：增加物流模式选择 + 回本周期
import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="茶叶跨境成本测算系统", layout="wide")
st.title("茶叶跨境成本测算工具【Demo】")

st.sidebar.header("参数调节面板")

# =========新增：物流模式下拉选择========
logi_mode = st.sidebar.selectbox("选择物流模式",["空运","海运","陆运"])
# 不同模式预设基础单价
if logi_mode == "空运":
    default_log = 45
elif logi_mode == "海运":
    default_log = 22
else:
    default_log = 32

month_sale = st.sidebar.number_input("月销售数量(kg)", min_value=100, max_value=5000, value=1000, step=100)
buy_price = st.sidebar.number_input("采购单价(元/kg)", min_value=20, max_value=200, value=120)
log_price = st.sidebar.number_input("跨境物流单价(元/kg)", min_value=10, max_value=80, value=default_log)
tariff_rate = st.sidebar.slider("关税税率 %", min_value=0, max_value=30, value=10)
commission_rate = st.sidebar.slider("电商平台佣金 %", min_value=0, max_value=20, value=5)
sell_price = st.sidebar.number_input("对外销售单价(元/kg)", min_value=100, max_value=400, value=180)

# --------计算各项成本与利润--------
total_buy = month_sale * buy_price
total_log = month_sale * log_price
total_tariff = total_buy * tariff_rate / 100
total_commission = month_sale * sell_price * commission_rate /100
total_revenue = month_sale * sell_price
total_cost = total_buy + total_log + total_tariff + total_commission
profit = total_revenue - total_cost

# 计算回本周期（月），防止利润为0除错
if profit > 0:
    payback_month = total_cost / profit
else:
    payback_month = 999

# --------输出计算结果--------
st.subheader("📊计算结果")
st.markdown(f"**当前选择物流模式：{logi_mode}**")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("月度总营收", f"{total_revenue:,.2f} 元")
    st.metric("产品采购成本", f"{total_buy:,.2f} 元")
with col2:
    st.metric("跨境物流成本", f"{total_log:,.2f} 元")
    st.metric("关税费用", f"{total_tariff:,.2f} 元")
with col3:
    st.metric("平台佣金", f"{total_commission:,.2f} 元")
    st.metric("✅月度净利润", f"{profit:,.2f} 元")

st.info(f"💡测算回本周期：{payback_month:.2f} 个月（净利润为负时无实际回本意义）")

# --------饼图：成本结构可视化--------
pie_data = pd.DataFrame({
    "成本项目":["产品采购","跨境物流","关税费用","平台佣金"],
    "金额":[total_buy, total_log, total_tariff, total_commission]
})
fig_pie = px.pie(pie_data, values="金额", names="成本项目", title="月度成本结构占比饼图")
st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("""
> **使用说明：**
> 在左侧侧边栏可选择物流模式（空运/海运/陆运），模式切换自动填充对应默认物流单价，也可手动修改全部业务参数；
> 参数改动后，营收、成本、净利润、回本周期与成本占比饼图实时更新，模拟不同物流方案下经营效果。
""")