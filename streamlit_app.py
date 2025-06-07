# app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import matplotlib.font_manager as fm
import os

# 업로드한 한글 폰트 경로 (루트 경로에 업로드됨)
font_path = "NotoSansKR-Regular.ttf"  # 또는 NotoSansKR-Regular.ttf

# 폰트 적용
font_prop = fm.FontProperties(fname=font_path)
plt.rc('font', family=font_prop.get_name())
plt.rcParams['axes.unicode_minus'] = False


st.set_page_config(layout="wide")
st.title("🚕 서울시 장애인 택시 운행량 수요 예측 및 분석 대시보드")

# 1. 파일 업로드
uploaded_file = st.file_uploader("📂 CSV 파일 업로드 (예: Seoul_2024_real.csv)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='cp949')
    df.columns = df.columns.str.strip()

    st.subheader("📋 데이터 미리보기")
    st.dataframe(df.head())

    # 2. 정규화 수행
    if 'precipitation' in df.columns:
        scaler = MinMaxScaler()
        df['precipitation_minmax'] = scaler.fit_transform(df[['precipitation']])

    if 'temperature' in df.columns:
        df['temperature_zscore'] = StandardScaler().fit_transform(df[['temperature']])

    if 'num_boardings' in df.columns:
        df['num_boardings_zscore'] = StandardScaler().fit_transform(df[['num_boardings']])

    # 3. 시각화
    tab1, tab2, tab3 = st.tabs(["📊 요일별 수요량", "📊 자치구별 수요량", "📈 정규화 분포 시각화"])

    with tab1:
        st.subheader("📊 요일별 평균 탑승량")
        order = ['월', '화', '수', '목', '금', '토', '일']
        fig, ax = plt.subplots()(figsize=(6, 4))
        sns.barplot(data=df, x='day_of_week', y='num_boardings', order=order, ax=ax)
        ax.set_title("요일별 수요량", fontsize=11)  # 💡 제목 글씨 크기
        ax.tick_params(labelsize=9)  # 💡 축 글씨 크기
        st.pyplot(fig)

    with tab2:
        st.subheader("📊 자치구별 평균 탑승량")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        district_avg = df.groupby("district")["num_boardings"].mean().sort_values()
        sns.barplot(x=district_avg.values, y=district_avg.index, ax=ax2)
        st.pyplot(fig2)

    with tab3:
        st.subheader("📈 정규화 전/후 분포 비교")
        col1, col2 = st.columns(2)

        with col1:
            st.write("정규화 전")
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            sns.histplot(df['precipitation'], kde=True, ax=ax3)
            ax3.set_title("강수량 원본", fontsize=11)
            st.pyplot(fig3)

        with col2:
            st.write("Min-Max 정규화")
            fig4, ax4 = plt.subplots(figsize=(6, 4))
            sns.histplot(df['precipitation_minmax'], kde=True, color='green', ax=ax4)
            ax4.set_title("강수량 정규화", fontsize=11)
            st.pyplot(fig4)
