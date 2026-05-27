import streamlit as st
import time

# 1. 페이지 기본 설정 및 스타일 (코드 입력창처럼 보이도록 스타일링)
st.set_page_config(page_title="코딩 타자 연습 앱", layout="centered")
st.markdown("""
    <style>
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace !important;
        background-color: #1e1e1e !important;
        color: #d4d4d4 !important;
        font-size: 16px !important;
    }
    .example-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 5px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 15px;
        white-space: pre-wrap;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💻 코딩 타자 연습 웹앱")
st.write("스트림릿 클라우드에서 즐기는 타자 연습 프로그램입니다.")

# 2. 사용자 이름 입력
user_name = st.text_input("플레이어 이름을 입력하세요:", value="개발자_지망생")

# 3. 난이도별 예제 문장 (Python 코드 위주)
sentences = {
    "하 (기초)": [
        "print('Hello, World!')",
        "x = 10",
        "import streamlit as st",
        "my_list = [1, 2, 3]"
    ],
    "중 (심화)": [
        "def calculate_wpm(words, time_taken):",
        "for index, value in enumerate(data):",
        "return [x for x in range(10) if x % 2 == 0]",
        "items = {'apple': 2, 'banana': 5}"
    ],
    "상 (고수)": [
        "@st.cache_data\ndef fetch_api_data(url, timeout=5):",
        "try:\n    result = lambda a, b : a if a > b else b\nexcept Exception as e:",
        "class TypingTest(BaseModel):\n    id: int\n    accuracy: float",
        "with open('requirements.txt', 'r') as f:\n    lines = f.readlines()"
    ]
}

# 난이도 선택
level = st.selectbox("난이도를 선택하세요:", list(sentences.keys()))

# 세션 상태 초기화 (단어 변경 시 시간 및 텍스트 리셋을 위함)
if "current_sentence" not in st.session_state or st.button("새 문장 가져오기"):
    import random
    st.session_state.current_sentence = random.choice(sentences[level])
    st.session_state.start_time = None
    st.session_state.user_input = ""

target_text = st.session_state.current_sentence

# 4. 제시어 보여주기
st.write("### 📝 제시된 코드:")
st.markdown(f'<div class="example-box">{target_text}</div>', unsafe_allow_html=True)

# 최초 타이핑 시작 시간 기록을 위한 트릭
if st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# 5. 코드 입력창 (TextArea 이용)
user_input = st.text_area(
    "여기에 코드를 타이핑하세요 (Ctrl + Enter로 제출 가능):", 
    key="typing_area",
    height=100
)

# 6. 결과 확인 버튼 클릭 시 로직
if st.button("결과 확인"):
    end_time = time.time()
    time_taken = end_time - st.session_state.start_time
    
    if not user_input:
        st.warning("입력창이 비어 있습니다. 코드를 입력해 주세요!")
    else:
        # 정확도 계산 (글자 단위 비교)
        correct_chars = 0
        min_len = min(len(target_text), len(user_input))
        
        for i in range(min_len):
            if target_text[i] == user_input[i]:
                correct_chars += 1
                
        accuracy = (correct_chars / max(len(target_text), 1)) * 100
        
        # 타수(CPM) 및 단어수(WPM) 계산 
        # (통상 5글자를 1단어로 취급하나, 여기서는 실제 타이핑한 글자 수 기반 계산)
        cpm = (len(user_input) / time_taken) * 60
        wpm = cpm / 5
        
        # 결과 화면 출력
        st.success(f"🎉 {user_name}님의 연습 결과입니다!")
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="정확도", value=f"{accuracy:.1f} %")
        col2.metric(label="타수 (CPM)", value=f"{int(cpm)} 타/분")
        col3.metric(label="소요 시간", value=f"{time_taken:.2f} 초")
        
        # 피드백 메시지
        if accuracy == 100:
            st.balloons()
            st.info("오타 없는 완벽한 코딩이었습니다! 👍")
        elif accuracy > 80:
            st.info("훌륭합니다! 조금만 더 신중하게 입력해 보세요.")
        else:
            st.error("오타가 조금 많네요. 천천히 다시 연습해 볼까요?")
