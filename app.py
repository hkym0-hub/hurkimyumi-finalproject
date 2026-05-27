import streamlit as st
import random
import json
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="오늘 뭐 먹지? 🍽️",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 데이터
MENU_DATA = {
    "상황별": {
        "저녁 메뉴": [
            {"name": "삼겹살", "cal": 700, "emoji": "🥓"},
            {"name": "치킨", "cal": 850, "emoji": "🍗"},
            {"name": "피자", "cal": 900, "emoji": "🍕"},
            {"name": "파스타", "cal": 650, "emoji": "🍝"},
            {"name": "스테이크", "cal": 800, "emoji": "🥩"},
            {"name": "초밥", "cal": 500, "emoji": "🍣"},
            {"name": "된장찌개", "cal": 350, "emoji": "🍲"},
        ],
        "배달 메뉴": [
            {"name": "치킨", "cal": 850, "emoji": "🍗"},
            {"name": "피자", "cal": 900, "emoji": "🍕"},
            {"name": "짜장면", "cal": 650, "emoji": "🍜"},
            {"name": "짬뽕", "cal": 700, "emoji": "🍜"},
            {"name": "떡볶이", "cal": 500, "emoji": "🌶️"},
            {"name": "족발", "cal": 750, "emoji": "🦷"},
            {"name": "보쌈", "cal": 700, "emoji": "🥬"},
            {"name": "버거", "cal": 650, "emoji": "🍔"},
        ],
        "데이트 메뉴": [
            {"name": "파스타", "cal": 650, "emoji": "🍝"},
            {"name": "스테이크", "cal": 800, "emoji": "🥩"},
            {"name": "초밥", "cal": 500, "emoji": "🍣"},
            {"name": "샤브샤브", "cal": 450, "emoji": "🍲"},
            {"name": "오마카세", "cal": 700, "emoji": "🍱"},
            {"name": "와인 파스타", "cal": 680, "emoji": "🍷"},
        ],
        "캠핑 메뉴": [
            {"name": "삼겹살 구이", "cal": 700, "emoji": "🔥"},
            {"name": "라면", "cal": 500, "emoji": "🍜"},
            {"name": "핫도그", "cal": 400, "emoji": "🌭"},
            {"name": "불고기", "cal": 550, "emoji": "🥩"},
            {"name": "감자 구이", "cal": 200, "emoji": "🥔"},
            {"name": "옥수수 구이", "cal": 180, "emoji": "🌽"},
        ],
        "파티 메뉴": [
            {"name": "피자", "cal": 900, "emoji": "🍕"},
            {"name": "치킨", "cal": 850, "emoji": "🍗"},
            {"name": "샌드위치 플래터", "cal": 600, "emoji": "🥪"},
            {"name": "파스타", "cal": 650, "emoji": "🍝"},
            {"name": "타코", "cal": 550, "emoji": "🌮"},
            {"name": "뷔페", "cal": 800, "emoji": "🍽️"},
        ],
        "혼밥 메뉴": [
            {"name": "편의점 도시락", "cal": 550, "emoji": "🍱"},
            {"name": "라면", "cal": 500, "emoji": "🍜"},
            {"name": "김밥", "cal": 400, "emoji": "🍙"},
            {"name": "덮밥", "cal": 600, "emoji": "🍚"},
            {"name": "순대국밥", "cal": 550, "emoji": "🍲"},
            {"name": "우동", "cal": 450, "emoji": "🍜"},
        ],
        "술안주 메뉴": [
            {"name": "치킨", "cal": 850, "emoji": "🍗"},
            {"name": "족발", "cal": 750, "emoji": "🦷"},
            {"name": "마른안주", "cal": 300, "emoji": "🦑"},
            {"name": "감자전", "cal": 400, "emoji": "🥞"},
            {"name": "두부김치", "cal": 350, "emoji": "🥬"},
            {"name": "골뱅이소면", "cal": 450, "emoji": "🍜"},
        ],
    },
    "선호도별": {
        "다이어트 메뉴": [
            {"name": "샐러드", "cal": 150, "emoji": "🥗"},
            {"name": "닭가슴살 도시락", "cal": 300, "emoji": "🍱"},
            {"name": "두부 스테이크", "cal": 200, "emoji": "🥩"},
            {"name": "곤약 비빔밥", "cal": 250, "emoji": "🍚"},
            {"name": "그릭 요거트 볼", "cal": 200, "emoji": "🥣"},
            {"name": "채소 스무디", "cal": 120, "emoji": "🥤"},
        ],
        "매운 메뉴": [
            {"name": "불닭볶음면", "cal": 530, "emoji": "🔥"},
            {"name": "마라탕", "cal": 700, "emoji": "🌶️"},
            {"name": "엽기 떡볶이", "cal": 600, "emoji": "🌶️"},
            {"name": "불닭 피자", "cal": 850, "emoji": "🍕"},
            {"name": "매운 김치찌개", "cal": 400, "emoji": "🍲"},
            {"name": "화끈한 육개장", "cal": 350, "emoji": "🍲"},
        ],
        "가성비 메뉴": [
            {"name": "편의점 도시락", "cal": 550, "emoji": "🏪"},
            {"name": "김밥", "cal": 400, "emoji": "🍙"},
            {"name": "순대국밥", "cal": 550, "emoji": "🍲"},
            {"name": "라면", "cal": 500, "emoji": "🍜"},
            {"name": "분식 세트", "cal": 600, "emoji": "🍱"},
            {"name": "백반", "cal": 650, "emoji": "🍚"},
        ],
    },
    "음식 종류별": {
        "한식": [
            {"name": "비빔밥", "cal": 550, "emoji": "🍚"},
            {"name": "된장찌개", "cal": 350, "emoji": "🍲"},
            {"name": "삼겹살", "cal": 700, "emoji": "🥓"},
            {"name": "불고기", "cal": 550, "emoji": "🥩"},
            {"name": "갈비탕", "cal": 600, "emoji": "🍲"},
            {"name": "냉면", "cal": 500, "emoji": "🍜"},
            {"name": "순두부찌개", "cal": 300, "emoji": "🍲"},
        ],
        "일식": [
            {"name": "초밥", "cal": 500, "emoji": "🍣"},
            {"name": "라멘", "cal": 700, "emoji": "🍜"},
            {"name": "우동", "cal": 450, "emoji": "🍜"},
            {"name": "돈카츠", "cal": 750, "emoji": "🥩"},
            {"name": "오야코동", "cal": 600, "emoji": "🍚"},
            {"name": "타코야키", "cal": 400, "emoji": "🐙"},
        ],
        "양식": [
            {"name": "파스타", "cal": 650, "emoji": "🍝"},
            {"name": "피자", "cal": 900, "emoji": "🍕"},
            {"name": "스테이크", "cal": 800, "emoji": "🥩"},
            {"name": "리조또", "cal": 600, "emoji": "🍚"},
            {"name": "버거", "cal": 650, "emoji": "🍔"},
            {"name": "샐러드", "cal": 250, "emoji": "🥗"},
        ],
        "중식": [
            {"name": "짜장면", "cal": 650, "emoji": "🍜"},
            {"name": "짬뽕", "cal": 700, "emoji": "🍜"},
            {"name": "탕수육", "cal": 800, "emoji": "🥩"},
            {"name": "마파두부", "cal": 400, "emoji": "🌶️"},
            {"name": "마라탕", "cal": 700, "emoji": "🫕"},
            {"name": "딤섬", "cal": 500, "emoji": "🥟"},
        ],
    },
}

SAMPLE_RESTAURANTS = {
    "강남구": [
        {"name": "맛있는 식당", "rating": 4.5, "address": "강남구 테헤란로 123", "reviews": 342},
        {"name": "행복한 밥상", "rating": 4.3, "address": "강남구 역삼동 456", "reviews": 218},
        {"name": "맛나라", "rating": 4.1, "address": "강남구 논현동 789", "reviews": 156},
    ],
    "마포구": [
        {"name": "홍대 맛집", "rating": 4.6, "address": "마포구 홍익로 100", "reviews": 521},
        {"name": "합정 식당", "rating": 4.2, "address": "마포구 합정동 200", "reviews": 189},
    ],
    "종로구": [
        {"name": "광화문 밥집", "rating": 4.4, "address": "종로구 세종로 50", "reviews": 298},
        {"name": "인사동 식당", "rating": 4.3, "address": "종로구 인사동 30", "reviews": 167},
    ],
    "서초구": [
        {"name": "반포 맛집", "rating": 4.5, "address": "서초구 반포대로 77", "reviews": 403},
        {"name": "교대 식당", "rating": 4.1, "address": "서초구 서초동 12", "reviews": 134},
    ],
    "성동구": [
        {"name": "성수 핫플", "rating": 4.7, "address": "성동구 성수동 88", "reviews": 672},
        {"name": "뚝섬 밥상", "rating": 4.2, "address": "성동구 뚝섬로 45", "reviews": 201},
    ],
}

DISTRICTS = ["선택 안 함"] + sorted(SAMPLE_RESTAURANTS.keys()) + ["기타 지역"]

# 세션 상태 초기화
def init_session():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "excluded" not in st.session_state:
        st.session_state.excluded = set()
    if "custom_menus" not in st.session_state:
        st.session_state.custom_menus = []
    if "tournament_state" not in st.session_state:
        st.session_state.tournament_state = None
    if "scratch_revealed" not in st.session_state:
        st.session_state.scratch_revealed = False
    if "scratch_menu" not in st.session_state:
        st.session_state.scratch_menu = None
    if "last_result" not in st.session_state:
        st.session_state.last_result = None

init_session()

# 유틸리티 함수
def get_all_menus_flat(category_type=None, subcategory=None):
    menus = []
    if category_type and subcategory:
        source = MENU_DATA.get(category_type, {}).get(subcategory, [])
        menus = [m for m in source if m["name"] not in st.session_state.excluded]
    else:
        for cat in MENU_DATA.values():
            for items in cat.values():
                menus.extend([m for m in items if m["name"] not in st.session_state.excluded])
        menus += [m for m in st.session_state.custom_menus if m["name"] not in st.session_state.excluded]
    return menus

def add_to_history(menu, method, category=""):
    entry = {
        "menu": menu["name"],
        "emoji": menu.get("emoji", "🍽️"),
        "cal": menu.get("cal", 0),
        "method": method,
        "category": category,
        "time": datetime.now().strftime("%m/%d %H:%M"),
    }
    st.session_state.history.insert(0, entry)
    if len(st.session_state.history) > 20:
        st.session_state.history = st.session_state.history[:20]
    st.session_state.last_result = entry

def show_result_card(menu, method=""):
    st.markdown(f"""
    <div style="text-align:center; padding:20px; border:1px solid #ddd; border-radius:10px;">
        <div style="font-size:3rem">{menu.get('emoji','🍽️')}</div>
        <h3>{menu['name']}</h3>
        <p>🔥 약 {menu.get('cal',0)} kcal</p>
        <p>추천 방식: {method}</p>
    </div>
    """, unsafe_allow_html=True)

# UI 구성
with st.sidebar:
    st.markdown("## 🍽️ 오늘 뭐 먹지?")
    cat_type = st.selectbox("대분류", ["전체"] + list(MENU_DATA.keys()), key="cat_type")
    cat_sub = None
    if cat_type != "전체":
        cat_sub = st.selectbox("소분류", list(MENU_DATA[cat_type].keys()), key="cat_sub")

    if st.button("🗑️ 이력 초기화"):
        st.session_state.history = []
        st.rerun()

tab1, tab2, tab3, tab4 = st.tabs(["🎯 추천받기", "🔧 메뉴 관리", "📍 맛집 찾기", "📜 전체 이력"])

with tab1:
    menus = get_all_menus_flat(cat_type if cat_type != "전체" else None, cat_sub)
    col1, col2, col3, col4, col5 = st.columns(5)
    if col1.button("⚡ 빠른 추천"):
        pick = random.choice(menus)
        show_result_card(pick, "빠른 추천")
        add_to_history(pick, "빠른 추천", cat_sub or "전체")

with tab2:
    st.write("메뉴 관리 탭입니다.")
    new_name = st.text_input("새 메뉴 이름")
    if st.button("추가"):
        st.session_state.custom_menus.append({"name": new_name, "cal": 500, "emoji": "🍽️"})
        st.rerun()

with tab3:
    st.write("맛집 찾기 탭입니다.")
    
with tab4:
    st.write("추천 이력:")
    st.write(st.session_state.history)
