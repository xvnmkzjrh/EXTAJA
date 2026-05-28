import streamlit as st
import time
import random
import difflib

# 1. 페이지 기본 설정 및 스타일 (순정 text_area를 다크모드 IDE 스타일로 완벽 튜닝)
st.set_page_config(page_title="코딩 타자 연습 앱", layout="centered")
st.markdown("""
    <style>
    /* 입력창을 완전한 개발자 다크모드 코딩창으로 스타일링 */
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace !important;
        background-color: #1e1e1e !important;
        color: #d4d4d4 !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
        tab-size: 4 !important;
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
    .diff-box {
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 15px;
        border-radius: 5px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 15px;
        white-space: pre-wrap;
        line-height: 1.5;
    }
    .correct { color: #4CAF50; font-weight: bold; }       
    .incorrect { color: #FF5252; background-color: #3e1f1f; font-weight: bold; text-decoration: underline; } 
    .missing { color: #FF9800; font-weight: bold; }         
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
        "@st.cache_data\ndef fetch_api_data(url, timeout=5):\n    return data",
        "try:\n    result = lambda a, b : a if a > b else b\nexcept Exception as e:\n    print(e)",
        "class TypingTest(BaseModel):\n    id: int\n    accuracy: float",
        "with open('requirements.txt', 'r') as f:\n    lines = f.readlines()"
    ]
}

# 난이도 선택
level = st.selectbox("난이도를 선택하세요:", list(sentences.keys()))

# 세션 상태 초기화 (단어 변경 시 시간 및 텍스트 리셋을 위함)
if "current_sentence" not in st.session_state or st.button("새 문장 가져오기"):
    st.session_state.current_sentence = random.choice(sentences[level])
    st.session_state.start_time = None

target_text = st.session_state.current_sentence

# 4. 제시어 보여주기
st.write("### 📝 제시된 코드:")
st.markdown(f'<div class="example-box">{target_text}</div>', unsafe_allow_html=True)

# 최초 타이핑 시작 시간 기록을 위한 트릭
if st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# 5. 순정 코드 입력창 (버그 확률 0%)
user_input = st.text_area(
    "여기에 코드를 타이핑하세요 (작성 후 Ctrl + Enter를 누르면 값이 고정됩니다):", 
    value="",
    height=150,
    key="typing_area"
)

# 6. 결과 확인 버튼 클릭 시 로직
if st.button("결과 확인"):
    end_time = time.time()
    time_taken = end_time - st.session_state.start_time
    
    # 공백 및 인코딩 정규화
    user_input_clean = user_input.replace("\r\n", "\n").rstrip()
    target_text_clean = target_text.rstrip()
    
    if not user_input_clean:
        st.warning("입력창이 비어 있습니다. 코드를 입력한 후 Ctrl+Enter를 누르거나 창 바깥을 클릭하고 버튼을 눌러주세요!")
    else:
        # 글자 단위 오타 하이라이팅 로직 생성
        diff_html = ""
        correct_chars = 0
        
        diff = list(difflib.ndiff(target_text_clean, user_input_clean))
        
        for token in diff:
            flag = token[0]
            char = token[2:]
            
            display_char = char
            if char == "\n":
                display_char = "↵\n"
            elif char == " ":
                display_char = "·"  

            if flag == " ":    
                diff_html += f'<span class="correct">{display_char}</span>'
                if char != "\n": 
                    correct_chars += 1
            elif flag == "-":  
                diff_html += f'<span class="missing">{display_char}</span>'
            elif flag == "+":  
                diff_html += f'<span class="incorrect">{display_char}</span>'

        # 정확도 산출
        accuracy = (correct_chars / max(len(target_text_clean), 1)) * 100
        # 타수(CPM) 계산
        cpm = (len(user_input_clean) / time_taken) * 60
        
        # 결과 화면 출력
        st.success(f"🎉 {user_name}님의 연습 결과입니다!")
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="정확도", value=f"{accuracy:.1f} %")
        col2.metric(label="타수 (CPM)", value=f"{int(cpm)} 타/분")
        col3.metric(label="소요 시간", value=f"{time_taken:.2f} 초")
        
        # 7. 오타 분석 결과 창 보여주기
        st.write("### 🔍 오타 분석 결과:")
        st.caption("💡 도움말: 점(·)은 공백, ↵은 줄바꿈 문자입니다. [ 초록: 일치 | 빨강: 오타/초과 입력 | 주황: 누락 ]")
        st.markdown(f'<div class="diff-box">{diff_html}</div>', unsafe_allow_html=True)
        
        # 피드백 메시지
        if accuracy == 100:
            st.balloons()
            st.info("오타 없는 완벽한 코딩이었습니다! 👍")
        elif accuracy > 80:
            st.info("훌륭합니다! 조금만 더 신중하게 입력해 보세요.")
        else:
            st.error("오타가 조금 많네요. 천천히 다시 연습해 볼까요?")
