import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_tree_select import tree_select

# python 모듈 경로에 프로젝트 루트 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moneybook.config import Headers
from moneybook.data_reader.data_reader import read_moneybook_data


def main():
    st.set_page_config(layout="wide")
    st.title("가계부 대시보드")

    df = read_moneybook_data()
    st.write(df)

    # 필터링 기능 sidebar에 추가
    st.sidebar.header("필터링 옵션")

    df[Headers.DATE] = pd.to_datetime(df[Headers.DATE], format="%Y년%m월%d일")

    # 날짜 범위 필터링
    selected_date = st.sidebar.date_input(
        "날짜 범위",
        value=[df[Headers.DATE].min().date(), df[Headers.DATE].max().date()],
        min_value=df[Headers.DATE].min().date(),
        max_value=df[Headers.DATE].max().date(),
    )
    if isinstance(selected_date, tuple) and len(selected_date) == 2:
        start_date, end_date = selected_date
        filtered_df = df[
            (df[Headers.DATE] >= pd.to_datetime(start_date)) & (df[Headers.DATE] <= pd.to_datetime(end_date))
        ]
    else:
        filtered_df = df

    # 사용내역 필터링
    excluded_details = st.sidebar.multiselect("사용내역 제외", df[Headers.DETAILS].unique())
    if excluded_details:
        filtered_df = filtered_df[~filtered_df[Headers.DETAILS].isin(excluded_details)]

    # 카테고리 필터링
    st.sidebar.write("카테고리 포함")
    filtered_df[[Headers.CATEGORY_L, Headers.CATEGORY_S]] = filtered_df[Headers.CATEGORY].str.split(
        ">", expand=True, n=1
    )
    tree_data = convert_df_to_tree_data(filtered_df)
    # `container()`를 사용해서 사이드바에서 실행
    with st.sidebar.container():
        selected = tree_select(tree_data)
    filtered_df = filtered_df[filtered_df[Headers.CATEGORY].isin(selected["checked"])]

    # 그래프 그림
    date_cash_df = filtered_df.groupby(Headers.DATE)[Headers.CASH].sum().reset_index()
    date_cash_chart = px.bar(
        date_cash_df, x=Headers.DATE, y=Headers.CASH, title="날짜별 지출 금액", labels={Headers.CASH: "원", Headers.DATE: "날짜"}
    )
    st.plotly_chart(date_cash_chart, use_container_width=True)

    date_cumulative_cash_df = filtered_df.groupby(Headers.DATE)[Headers.CASH].sum().cumsum().reset_index()
    date_cash_cumulative_chart = px.line(
        date_cumulative_cash_df,
        x=Headers.DATE,
        y=Headers.CASH,
        title="날짜별 지출 금액",
        labels={Headers.CASH: "원", Headers.DATE: "날짜"},
    )
    st.plotly_chart(date_cash_cumulative_chart, use_container_width=True)


def convert_df_to_tree_data(df: pd.DataFrame) -> list:
    tree = dict()

    for _, row in df.iterrows():
        category_l = row[Headers.CATEGORY_L]
        category_s = row[Headers.CATEGORY_S]

        if category_l not in tree:
            tree[category_l] = set()
        tree[category_l].add(category_s)

    tree_data = [
        {
            "label": category_l,
            "value": category_l,
            "children": [{"label": category_s, "value": f"{category_l}>{category_s}"} for category_s in categories_m],
        }
        for category_l, categories_m in tree.items()
    ]
    return tree_data


if __name__ == "__main__":
    main()
