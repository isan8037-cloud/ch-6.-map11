import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import math

# 앱 제목 설정
st.title("부산 지하철 역별 이용객 지도 분석 앱")

# 1. CSV 파일 업로드 화면 만들기
uploaded_file = st.file_uploader("busan_subway.csv 파일을 업로드해주세요", type=['csv'])

# 파일이 업로드 되었을 때만 아래 코드 실행
if uploaded_file is not None:

    # pandas를 이용해 업로드된 CSV 파일 읽기
    df = pd.read_csv(uploaded_file)

    # 화면에 데이터 표로 보여주기
    st.subheader("데이터 미리보기")
    st.dataframe(df)

    # 2. folium 지도 생성 (부산시청 근처 좌표를 중심으로 설정)
    # location: [위도, 경도], zoom_start: 초기 확대 정도
    m = folium.Map(location=[35.1795, 129.0756], zoom_start=11)

    # 데이터의 각 줄(역)을 하나씩 반복하면서 지도에 마커 찍기
    for index, row in df.iterrows():
        # 원의 면적이 이용객수에 비례하도록 반지름을 제곱근으로 계산
        # (숫자가 너무 클 수 있으므로 적당히 나누어 크기를 조절합니다)
        radius_size = math.sqrt(row['이용객수']) / 10

        # 3. 지도에 CircleMarker(원 마커) 추가하기
        folium.CircleMarker(
            location=[row['위도'], row['경도']],  # 마커 위치 설정
            radius=radius_size,  # 원의 반지름 크기
            color='blue',  # 테두리 색상
            fill=True,  # 원 내부 색칠하기
            fill_color='blue',  # 내부 색상
            tooltip=row['역명'],  # 마우스를 올렸을 때 보여줄 글자
            popup=f"{row['이용객수']}명"  # 클릭했을 때 보여줄 글자
        ).add_to(m)

    # 완성된 지도를 스트림릿 화면에 출력하기
    st.subheader("이용객수 비례 지도")
    st_folium(m, width=700, height=500)