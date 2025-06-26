import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import time

st.set_page_config(layout="wide")
st.title("🚦 SUMO OSM 路网轨迹可视化 Demo")

uploaded = st.file_uploader("上传 fcd_output.csv", type="csv")
if uploaded:
    df = pd.read_csv(uploaded)
    st.success(f"已加载 {len(df)} 条轨迹")

    min_t, max_t = float(df.time.min()), float(df.time.max())

    # 播放控制区
    st.sidebar.header("🎬 动画播放控制")
    if "playing" not in st.session_state:
        st.session_state.playing = False

    if st.sidebar.button("▶️ 播放"):
        st.session_state.playing = True
    if st.sidebar.button("⏸ 暂停"):
        st.session_state.playing = False

    speed = st.sidebar.slider("播放速度（秒/帧）", 0.05, 1.0, 0.2, 0.05)
    current_time = st.sidebar.slider("当前时间", min_t, max_t, min_t, step=1.0)

    # 坐标转换（模拟地理位置：以乌鲁木齐农大东路为中心）
    def sim2geo(x, y):
        return 43.8250 + y * 0.00001, 87.6000 + x * 0.00001

    df["lat"], df["lon"] = zip(*df.apply(lambda row: sim2geo(row["x"], row["y"]), axis=1))

    chart_col, map_col = st.columns([1, 1])

    chart_area = chart_col.empty()
    map_area = map_col.empty()

    while st.session_state.playing and current_time <= max_t:
        df_t = df[df.time == current_time]

        # 普通 matplotlib 动画
        fig, ax = plt.subplots()
        ax.scatter(df_t.x, df_t.y, c="red")
        ax.set_title(f"Time = {current_time:.1f} s")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        chart_area.pyplot(fig)

        # 地图轨迹展示
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_t,
            get_position='[lon, lat]',
            get_fill_color='[200, 30, 0, 160]',
            get_radius=6,
            pickable=True,
        )
        view_state = pdk.ViewState(
            latitude=df_t["lat"].mean(),
            longitude=df_t["lon"].mean(),
            zoom=14,
            pitch=0,
        )
        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "ID: {id}, Speed: {speed}"}
        )
        map_area.pydeck_chart(deck)

        time.sleep(speed)
        current_time += 1

    # 静态查看帧（若未播放）
    if not st.session_state.playing:
        df_t = df[df.time == current_time]

        fig, ax = plt.subplots()
        ax.scatter(df_t.x, df_t.y, c="red")
        ax.set_title(f"Time = {current_time:.1f} s")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        chart_area.pyplot(fig)

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_t,
            get_position='[lon, lat]',
            get_fill_color='[200, 30, 0, 160]',
            get_radius=6,
        )
        view_state = pdk.ViewState(
            latitude=df_t["lat"].mean(),
            longitude=df_t["lon"].mean(),
            zoom=14,
        )
        map_area.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
