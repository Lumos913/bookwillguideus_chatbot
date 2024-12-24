import streamlit as st
import pandas as pd
from openai import OpenAI
pip install streamlit langchain-openai

# 데이터프레임 생성 (CSV 파일을 불러오는 부분)
def load_books():
    df_loaded = pd.read_csv("yes24_bestsellers.csv", encoding="utf-8-sig")
    return df_loaded

# 사용자 입력을 카테고리로 매칭하는 함수
def categorize_response(user_input, categories):
    # 간단한 키워드 매칭 (LLM을 사용한 분석으로 교체 가능)
    if "기술" in user_input:
        return "기술"
    elif "문학" in user_input:
        return "문학"
    elif "성공" in user_input or "자기계발" in user_input:
        return "자기계발"
    else:
        return "기타"

# 책 추천에 사용된 핵심 함수
def recommend_books(category, df):
    # 해당 카테고리의 책 필터링
    filtered_books = df[df['category'] == category]

    # 필터링된 책 리스트 생성
    books_list = "\n".join(
        [
            f"- {row['제목']} by {row['저자']} (₩{row['가격']}): {row['서평']}\n"
            f"  책 설명: {row['서평']}\n"
            f"  구매 링크: {row['Link']}"
            for _, row in filtered_books.iterrows()
        ]
    )

    # LLM에 전달할 프롬프트 생성
    prompt = f"""
    다음은 '{category}' 카테고리에 속하는 추천 도서 목록입니다:
    {books_list}

    사용자가 이 카테고리에 흥미를 보였습니다. 이 목록에 있는 책만을 사용해서 사용자에게 책을 추천해 주세요.

    답변의 형식은 이처럼 해주세요

    "


    지금 ~~~~한 고민을 안고 있군요. 핵심적인 원인은 ~~같아요

    당신의 고민을 해결해줄 수 있는 최근 베스트셀러 책은  이와 같아요
    1 (책의 제목) (책의 저자) (책의 가격)
    => 추천 이유 (추천 이유는 해결책 위주로 작성해주세요)
    => 책의 소개: (책의 소개문은 3줄 이상)
    2 (책의 제목) (책의 저자) (책의 가격) (책의 소개문)
    => 추천 이유
    3 (책의 제목) (책의 저자) (책의 가격) (책의 소개문)
    => 추천 이유"
    """

    return prompt

# Show title and description.
st.title("💬 책 속에 답이 있다")
st.write(
    "각자 고민의 무게를 견디며 살아가는 현대인들. 친구나 동료에게 자신의 고민을 말해보아도, 해결되는 것 같지 않을 때. 같은 고민을 하는 사람들은 어떤 책에서 해결의 실마리를 얻고 있을까?"
    "고민을 말하면 최근 베스트셀러 529권 중에서 얻을 수 있는 지혜를 알아서 나눠주는 챗봇이 있다면?! 당장 사용해보자. "
    "아래 대화창을 통해 대화를 시도해보세요."
)

# OpenAI API 설정
client = OpenAI(api_key="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")

# 메시지 리스트 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사용자 입력 받기
user_input = st.chat_input("당신의 고민이나 현재 상황을 입력해주세요:")

if user_input:
    # 데이터 로드
    df = load_books()
    categories = df["category"].unique()

    # 카테고리 분석
    matched_category = categorize_response(user_input, categories)

    if matched_category == "기타":
        st.chat_message("assistant").markdown(
            "당신의 고민에 대해 더 구체적인 정보를 알려주시면, 적합한 추천을 드릴 수 있습니다."
        )
    else:
        # 책 추천
        recommendation = recommend_books(matched_category, df)
        st.chat_message("assistant").markdown(recommendation)

    # 메시지 기록
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
