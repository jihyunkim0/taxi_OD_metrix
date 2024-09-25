import streamlit as st
import pandas as pd

# 엑셀 파일 읽어오기
input_file = 'C:\\callTaxi\\totalList_OD.xlsx'

@st.cache_data
def load_data(file_path):
    return pd.read_excel(file_path, sheet_name='list6', header=0, usecols=['목적', '출발지', '목적지'])

df = load_data(input_file)

st.title("교통약자 특별 교통수단 OD 매트릭스2")

# 모든 '목적' 값을 가져오기
all_purposes = df['목적'].unique()

# 세션 상태로 현재 선택된 항목을 저장
if 'selected_purpose' not in st.session_state:
    st.session_state.selected_purpose = []

# 모두 선택/해제 버튼 만들기
col1, col2 = st.columns(2)
if col1.button("모두 선택"):
    st.session_state.selected_purpose = list(all_purposes)
if col2.button("모두 해제"):
    st.session_state.selected_purpose = []

# 필터 선택 (다중 선택 가능) - 세션 상태에 따라 업데이트
selected_purpose = st.multiselect("목적 선택", all_purposes, default=st.session_state.selected_purpose)

# 총 개수 표시
st.write(f"선택된 목적의 총 개수: {len(selected_purpose)}")

# '적용' 버튼 추가
if st.button("필터 적용"):
    # 필터가 선택된 경우에만 필터링을 적용
    filtered_df = df[
        (df['목적'].isin(selected_purpose))
    ]

    # OD 매트릭스 계산
    od_matrix = filtered_df.groupby(['출발지', '목적지']).size().unstack(fill_value=0)

    # 모든 출발지와 도착지 목록 정의
    all_locations = ['가평군','고양시', '과천시','광명시','광주시','구리시','군포시','김포시','남양주시','동두천시','부천시','성남시',
                     '수원시','시흥시','안산시','안성시','안양시','양주시','양평군','여주시','연천군','오산시','용인시','의왕시',
                     '의정부시','이천시','파주시','평택시','포천시','하남시','화성시','서울특별시','인천광역시']

    # reindex 사용
    od_matrix = od_matrix.reindex(index=all_locations, columns=all_locations, fill_value=0)

    # 서울특별시와 인천광역시를 맨 뒤로 재배열
    cols = [col for col in od_matrix.columns if col not in ['서울특별시', '인천광역시']]
    cols += ['서울특별시', '인천광역시']
    od_matrix = od_matrix.reindex(cols, fill_value=0)

    rows = [row for row in od_matrix.index if row not in ['서울특별시', '인천광역시']]
    rows += ['서울특별시', '인천광역시']
    od_matrix = od_matrix.reindex(rows)

    # OD 매트릭스 출력
    st.write("OD 매트릭스:")
    st.dataframe(od_matrix)

    # OD 매트릭스의 총 이동 건수 표시
    total_count = od_matrix.values.sum()
    st.write(f"OD 매트릭스의 총 이동 건수: {total_count}")