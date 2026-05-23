import streamlit as st
import random
from datetime import datetime

st.set_page_config(
    page_title="오늘 뭐 먹지?",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.stApp { background: #0f0f1a; }
.block-container { padding: 1.5rem 2rem 2rem 2rem !important; max-width: 1300px; }

/* ── 제목 pill ── */
.title-pill-wrap { display:flex; justify-content:center; margin-bottom:1.2rem; }
.title-pill {
    background: linear-gradient(135deg, #9b7fe8, #7c5cbf);
    color: white; font-size: 1.35rem; font-weight: 900;
    padding: 0.6rem 3rem; border-radius: 999px;
    letter-spacing: 0.05em; box-shadow: 0 4px 20px rgba(124,92,191,0.35);
}

/* ── 카테고리 탭 바 ── */
.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.08) !important;
    border: 2px solid rgba(255,255,255,0.2) !important;
    color: #ccc !important;
}

/* ── 2×2 메서드 카드 ── */
.method-card {
    background: #1e1e32; border-radius: 18px; min-height: 190px;
    padding: 1.8rem 1.5rem 1.5rem; cursor: pointer;
    transition: transform 0.15s, box-shadow 0.15s;
    display: flex; flex-direction: column; justify-content: space-between;
    position: relative; overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}
.method-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.4); }
.method-card-title { font-size: 1.55rem; font-weight: 900; color: white; text-shadow: 0 2px 8px rgba(0,0,0,0.4); }
.method-card-desc  { font-size: 0.82rem; color: rgba(255,255,255,0.6); margin-top:0.4rem; font-weight:600; }
.method-card-emoji { position:absolute; bottom:1rem; right:1.2rem; font-size:3rem; opacity:0.2; }

/* ── 결과 카드 ── */
.result-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px; padding: 2.5rem; text-align: center;
    color: white; margin: 1rem 0; box-shadow: 0 10px 40px rgba(102,126,234,0.4);
}
.result-emoji { font-size: 4rem; line-height:1; margin-bottom:0.5rem; }
.result-name  { font-size: 2.4rem; font-weight:900; margin-bottom:0.5rem; }
.result-cal   {
    display:inline-block; background:rgba(255,255,255,0.25);
    border-radius:999px; padding:0.3rem 1.2rem; font-size:0.95rem; font-weight:600;
}

/* ── 룰렛 스핀 ── */
@keyframes spin-slow {
    0%   { transform: rotate(0deg) scale(1); }
    60%  { transform: rotate(1080deg) scale(1.2); }
    100% { transform: rotate(1440deg) scale(1); }
}
.spin-emoji { display:inline-block; font-size:5rem; animation:spin-slow 2s cubic-bezier(0.25,0.46,0.45,0.94) forwards; }

/* ── 월드컵 ── */
.wc-option {
    background:#1e1e32; border:3px solid #333; border-radius:16px;
    padding:1.8rem 1.2rem; text-align:center;
    transition:all 0.18s;
}
.wc-option:hover { border-color:#667eea; background:#252540; }
.wc-emoji { font-size:2.5rem; }
.wc-name  { font-size:1.3rem; font-weight:800; margin:0.5rem 0; color:#f0f0ff; }
.wc-cal   { font-size:0.85rem; color:#666; }

/* ── 이력 아이템 ── */
.hist-item {
    background:#1a1a2e; border-radius:10px; padding:0.7rem 1rem; margin:0.3rem 0;
    border-left:4px solid #667eea; display:flex; justify-content:space-between;
    align-items:center; box-shadow:0 2px 6px rgba(0,0,0,0.3); font-size:0.88rem;
    color:#ccc;
}

/* ── 맛집 카드 ── */
.rest-card {
    background:#1a1a2e; border-radius:14px; padding:1rem 1.3rem; margin:0.5rem 0;
    box-shadow:0 4px 14px rgba(0,0,0,0.3); border-left:5px solid #f5576c;
    color:#ccc;
}

/* 다크 모드 텍스트 보정 */
.stMarkdown, .stMarkdown p, label, .stMetric, .stSelectbox label,
.stNumberInput label, .stTextInput label, .stCheckbox label,
[data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
    color: #ccc !important;
}
[data-testid="stMetricValue"] { color: #fff !important; }
.stTabs [data-baseweb="tab-panel"] { background: transparent; }
[data-baseweb="tab-list"] { background: #1a1a2e !important; border-radius: 12px; }
[data-baseweb="tab"] { color: #aaa !important; }
[aria-selected="true"][data-baseweb="tab"] { color: #fff !important; }
.stSelectbox > div > div, .stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #1e1e32 !important; color: #eee !important;
    border-color: #333 !important;
}
hr { border-color: #333 !important; }
.stAlert { background: #1e1e32 !important; color: #ccc !important; }

/* Streamlit 기본 요소 */
#MainMenu, footer, header { visibility:hidden; }
.stButton > button {
    border-radius:12px !important; font-weight:700 !important;
    font-family:'Noto Sans KR',sans-serif !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius:10px !important; font-weight:600 !important;
    font-family:'Noto Sans KR',sans-serif !important;
}

/* ── 스크래치 캔버스 래퍼 ── */
.scratch-wrapper {
    display: flex; flex-direction: column; align-items: center; gap: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── 데이터 ────────────────────────────────────────────────────
CATEGORY_EMOJI = {
    "저녁 메뉴":      "🌙",
    "배달 메뉴":      "🛵",
    "데이트 메뉴":    "💑",
    "다이어트 메뉴":  "🥗",
    "가성비 메뉴":    "💰",
    "캠핑 메뉴":      "⛺",
    "매운 메뉴":      "🌶️",
    "파티 메뉴":      "🎉",
    "한식 메뉴":      "🍚",
    "일식 메뉴":      "🍣",
    "양식 메뉴":      "🍝",
    "중식 메뉴":      "🥢",
    "안주 메뉴":      "🍺",
    "혼자 먹는 메뉴": "🙋",
}

MENU_DATA = {
    "저녁 메뉴": [
        {"name": "삼겹살",        "cal": 700, "emoji": "🥓"},
        {"name": "치킨",          "cal": 850, "emoji": "🍗"},
        {"name": "피자",          "cal": 900, "emoji": "🍕"},
        {"name": "파스타",        "cal": 650, "emoji": "🍝"},
        {"name": "스테이크",      "cal": 800, "emoji": "🥩"},
        {"name": "초밥",          "cal": 500, "emoji": "🍣"},
        {"name": "된장찌개",      "cal": 350, "emoji": "🍲"},
        {"name": "갈비탕",        "cal": 600, "emoji": "🍖"},
        {"name": "불고기",        "cal": 550, "emoji": "🔥"},
        {"name": "쭈꾸미볶음",    "cal": 450, "emoji": "🐙"},
        {"name": "순두부찌개",    "cal": 300, "emoji": "🫕"},
        {"name": "부대찌개",      "cal": 650, "emoji": "🍲"},
        {"name": "곱창전골",      "cal": 700, "emoji": "🫕"},
        {"name": "닭갈비",        "cal": 580, "emoji": "🍗"},
    ],
    "배달 메뉴": [
        {"name": "치킨",          "cal": 850, "emoji": "🍗"},
        {"name": "피자",          "cal": 900, "emoji": "🍕"},
        {"name": "짜장면",        "cal": 650, "emoji": "🍜"},
        {"name": "짬뽕",          "cal": 700, "emoji": "🍜"},
        {"name": "떡볶이",        "cal": 500, "emoji": "🌶️"},
        {"name": "족발",          "cal": 750, "emoji": "🍖"},
        {"name": "버거",          "cal": 650, "emoji": "🍔"},
        {"name": "마라탕",        "cal": 700, "emoji": "🥢"},
        {"name": "초밥 세트",     "cal": 520, "emoji": "🍣"},
        {"name": "국밥",          "cal": 550, "emoji": "🍲"},
        {"name": "쌀국수",        "cal": 480, "emoji": "🍜"},
        {"name": "보쌈",          "cal": 680, "emoji": "🥬"},
        {"name": "감자탕",        "cal": 620, "emoji": "🍲"},
        {"name": "샌드위치",      "cal": 450, "emoji": "🥪"},
    ],
    "데이트 메뉴": [
        {"name": "파스타",        "cal": 650, "emoji": "🍝"},
        {"name": "스테이크",      "cal": 800, "emoji": "🥩"},
        {"name": "초밥 / 오마카세","cal": 600, "emoji": "🍣"},
        {"name": "샤브샤브",      "cal": 450, "emoji": "🍲"},
        {"name": "와인 파스타",   "cal": 700, "emoji": "🍷"},
        {"name": "리조또",        "cal": 620, "emoji": "🍚"},
        {"name": "프렌치 코스",   "cal": 900, "emoji": "🥂"},
        {"name": "타파스",        "cal": 500, "emoji": "🫒"},
        {"name": "훠궈",          "cal": 750, "emoji": "🫕"},
        {"name": "브런치 카페",   "cal": 550, "emoji": "☕"},
        {"name": "이탈리안 뷔페", "cal": 850, "emoji": "🍽️"},
        {"name": "스시 오마카세", "cal": 700, "emoji": "🍱"},
    ],
    "다이어트 메뉴": [
        {"name": "닭가슴살 샐러드","cal": 280, "emoji": "🥗"},
        {"name": "두부 스테이크", "cal": 200, "emoji": "🥩"},
        {"name": "곤약 비빔밥",   "cal": 250, "emoji": "🍚"},
        {"name": "그릭 요거트 볼","cal": 180, "emoji": "🥣"},
        {"name": "채소 스프",     "cal": 120, "emoji": "🥦"},
        {"name": "연어 포케",     "cal": 380, "emoji": "🐟"},
        {"name": "닭가슴살 도시락","cal": 300, "emoji": "🍱"},
        {"name": "오트밀 볼",     "cal": 220, "emoji": "🌾"},
        {"name": "현미 잡곡밥 정식","cal": 420, "emoji": "🍚"},
        {"name": "저칼로리 김밥", "cal": 320, "emoji": "🍙"},
        {"name": "채소 쌈밥",    "cal": 350, "emoji": "🥬"},
        {"name": "토마토 달걀볶음","cal": 200, "emoji": "🍳"},
        {"name": "닭가슴살 볶음밥","cal": 380, "emoji": "🍳"},
    ],
    "가성비 메뉴": [
        {"name": "김밥",          "cal": 400, "emoji": "🍙"},
        {"name": "순대국밥",      "cal": 550, "emoji": "🍲"},
        {"name": "라면",          "cal": 500, "emoji": "🍜"},
        {"name": "백반",          "cal": 650, "emoji": "🍚"},
        {"name": "편의점 도시락", "cal": 550, "emoji": "🏪"},
        {"name": "분식 세트",     "cal": 600, "emoji": "🌶️"},
        {"name": "컵라면 + 삼각김밥","cal": 450, "emoji": "🍙"},
        {"name": "뼈다귀해장국",  "cal": 500, "emoji": "🍲"},
        {"name": "돈까스 정식",   "cal": 700, "emoji": "🥩"},
        {"name": "제육볶음 백반", "cal": 650, "emoji": "🍳"},
        {"name": "칼국수",        "cal": 520, "emoji": "🍜"},
        {"name": "콩나물국밥",    "cal": 400, "emoji": "🍲"},
        {"name": "떡볶이 + 순대", "cal": 580, "emoji": "🌶️"},
    ],
    "캠핑 메뉴": [
        {"name": "삼겹살 구이",   "cal": 700, "emoji": "🔥"},
        {"name": "라면",          "cal": 500, "emoji": "🍜"},
        {"name": "핫도그",        "cal": 380, "emoji": "🌭"},
        {"name": "불고기",        "cal": 550, "emoji": "🥩"},
        {"name": "옥수수 구이",   "cal": 180, "emoji": "🌽"},
        {"name": "감자 구이",     "cal": 200, "emoji": "🥔"},
        {"name": "부대찌개",      "cal": 650, "emoji": "🍲"},
        {"name": "닭꼬치",        "cal": 350, "emoji": "🍢"},
        {"name": "소시지 구이",   "cal": 400, "emoji": "🌭"},
        {"name": "묵은지 삼겹",   "cal": 720, "emoji": "🥓"},
        {"name": "즉석 떡볶이",   "cal": 480, "emoji": "🌶️"},
        {"name": "어묵탕",        "cal": 300, "emoji": "🍢"},
        {"name": "스팸 구이",     "cal": 450, "emoji": "🥫"},
    ],
    "매운 메뉴": [
        {"name": "불닭볶음면",    "cal": 530, "emoji": "🔥"},
        {"name": "마라탕",        "cal": 700, "emoji": "🌶️"},
        {"name": "엽기 떡볶이",   "cal": 600, "emoji": "🌶️"},
        {"name": "매운 김치찌개", "cal": 400, "emoji": "🍲"},
        {"name": "육개장",        "cal": 350, "emoji": "🍲"},
        {"name": "마라샹궈",      "cal": 800, "emoji": "🥢"},
        {"name": "불닭 피자",     "cal": 950, "emoji": "🍕"},
        {"name": "매운 갈비찜",   "cal": 750, "emoji": "🍖"},
        {"name": "낙지볶음",      "cal": 380, "emoji": "🐙"},
        {"name": "쭈꾸미볶음",    "cal": 420, "emoji": "🦑"},
        {"name": "매운 해물탕",   "cal": 500, "emoji": "🦀"},
        {"name": "불족발",        "cal": 780, "emoji": "🔥"},
        {"name": "청양 닭볶음탕", "cal": 600, "emoji": "🍗"},
    ],
    "파티 메뉴": [
        {"name": "피자",          "cal": 900, "emoji": "🍕"},
        {"name": "치킨",          "cal": 850, "emoji": "🍗"},
        {"name": "파스타 플래터", "cal": 700, "emoji": "🍝"},
        {"name": "타코",          "cal": 550, "emoji": "🌮"},
        {"name": "샌드위치 플래터","cal": 600, "emoji": "🥪"},
        {"name": "뷔페",          "cal": 900, "emoji": "🍽️"},
        {"name": "초밥 세트",     "cal": 560, "emoji": "🍣"},
        {"name": "바비큐 플래터", "cal": 850, "emoji": "🔥"},
        {"name": "케이터링 도시락","cal": 700, "emoji": "🍱"},
        {"name": "나초 + 딥",     "cal": 500, "emoji": "🫔"},
        {"name": "핑거푸드 세트", "cal": 450, "emoji": "🍢"},
        {"name": "떡 케이크",     "cal": 400, "emoji": "🎂"},
    ],
    "한식 메뉴": [
        {"name": "비빔밥",        "cal": 550, "emoji": "🍚"},
        {"name": "된장찌개",      "cal": 350, "emoji": "🍲"},
        {"name": "삼겹살",        "cal": 700, "emoji": "🥓"},
        {"name": "불고기",        "cal": 550, "emoji": "🥩"},
        {"name": "냉면",          "cal": 500, "emoji": "🍜"},
        {"name": "갈비탕",        "cal": 600, "emoji": "🍖"},
        {"name": "삼계탕",        "cal": 580, "emoji": "🐔"},
        {"name": "순대국밥",      "cal": 550, "emoji": "🍲"},
        {"name": "해물파전",      "cal": 480, "emoji": "🥞"},
        {"name": "잡채",          "cal": 420, "emoji": "🍜"},
        {"name": "감자탕",        "cal": 620, "emoji": "🍲"},
        {"name": "보쌈",          "cal": 680, "emoji": "🥬"},
        {"name": "닭갈비",        "cal": 580, "emoji": "🍗"},
        {"name": "낙지볶음",      "cal": 380, "emoji": "🐙"},
        {"name": "떡국",          "cal": 450, "emoji": "🍲"},
    ],
    "일식 메뉴": [
        {"name": "초밥",          "cal": 500, "emoji": "🍣"},
        {"name": "라멘",          "cal": 700, "emoji": "🍜"},
        {"name": "우동",          "cal": 450, "emoji": "🍜"},
        {"name": "돈카츠",        "cal": 750, "emoji": "🥩"},
        {"name": "오야코동",      "cal": 600, "emoji": "🍚"},
        {"name": "타코야키",      "cal": 380, "emoji": "🐙"},
        {"name": "규동",          "cal": 620, "emoji": "🍚"},
        {"name": "나가사키 짬뽕", "cal": 680, "emoji": "🍜"},
        {"name": "오마카세",      "cal": 700, "emoji": "🍱"},
        {"name": "야키토리",      "cal": 400, "emoji": "🍢"},
        {"name": "카레라이스",    "cal": 650, "emoji": "🍛"},
        {"name": "소바",          "cal": 400, "emoji": "🍜"},
        {"name": "이자카야 세트", "cal": 750, "emoji": "🍶"},
    ],
    "양식 메뉴": [
        {"name": "파스타",        "cal": 650, "emoji": "🍝"},
        {"name": "피자",          "cal": 900, "emoji": "🍕"},
        {"name": "스테이크",      "cal": 800, "emoji": "🥩"},
        {"name": "버거",          "cal": 650, "emoji": "🍔"},
        {"name": "리조또",        "cal": 620, "emoji": "🍚"},
        {"name": "샐러드",        "cal": 250, "emoji": "🥗"},
        {"name": "그라탱",        "cal": 700, "emoji": "🧀"},
        {"name": "크림 수프",     "cal": 350, "emoji": "🍵"},
        {"name": "연어 스테이크", "cal": 550, "emoji": "🐟"},
        {"name": "브런치 플레이트","cal": 600, "emoji": "🥞"},
        {"name": "함박스테이크",  "cal": 680, "emoji": "🥩"},
        {"name": "치킨 알프레도", "cal": 720, "emoji": "🍝"},
        {"name": "클램 차우더",   "cal": 380, "emoji": "🍵"},
    ],
    "중식 메뉴": [
        {"name": "짜장면",        "cal": 650, "emoji": "🍜"},
        {"name": "짬뽕",          "cal": 700, "emoji": "🍜"},
        {"name": "탕수육",        "cal": 800, "emoji": "🥩"},
        {"name": "마파두부",      "cal": 400, "emoji": "🌶️"},
        {"name": "딤섬",          "cal": 500, "emoji": "🥟"},
        {"name": "마라탕",        "cal": 700, "emoji": "🥢"},
        {"name": "마라샹궈",      "cal": 800, "emoji": "🌶️"},
        {"name": "훠궈",          "cal": 750, "emoji": "🫕"},
        {"name": "꿔바로우",      "cal": 820, "emoji": "🥩"},
        {"name": "양꼬치",        "cal": 600, "emoji": "🍢"},
        {"name": "깐풍기",        "cal": 780, "emoji": "🍗"},
        {"name": "유린기",        "cal": 700, "emoji": "🍗"},
        {"name": "동파육",        "cal": 850, "emoji": "🥩"},
    ],
    "안주 메뉴": [
        {"name": "치킨",          "cal": 850, "emoji": "🍗"},
        {"name": "족발",          "cal": 750, "emoji": "🍖"},
        {"name": "마른안주 세트", "cal": 300, "emoji": "🦑"},
        {"name": "두부김치",      "cal": 350, "emoji": "🥬"},
        {"name": "골뱅이소면",    "cal": 450, "emoji": "🐌"},
        {"name": "감자전",        "cal": 380, "emoji": "🥞"},
        {"name": "해물파전",      "cal": 480, "emoji": "🥞"},
        {"name": "닭발",          "cal": 420, "emoji": "🍗"},
        {"name": "삼겹살",        "cal": 700, "emoji": "🥓"},
        {"name": "소시지 야채볶음","cal": 500, "emoji": "🌭"},
        {"name": "계란말이",      "cal": 280, "emoji": "🥚"},
        {"name": "오돌뼈",        "cal": 460, "emoji": "🦴"},
        {"name": "곱창볶음",      "cal": 650, "emoji": "🫕"},
        {"name": "라볶이",        "cal": 550, "emoji": "🌶️"},
    ],
    "혼자 먹는 메뉴": [
        {"name": "편의점 도시락", "cal": 550, "emoji": "🏪"},
        {"name": "라면",          "cal": 500, "emoji": "🍜"},
        {"name": "김밥 한 줄",    "cal": 400, "emoji": "🍙"},
        {"name": "우동",          "cal": 450, "emoji": "🫕"},
        {"name": "덮밥",          "cal": 600, "emoji": "🍚"},
        {"name": "국밥",          "cal": 550, "emoji": "🍲"},
        {"name": "냉면",          "cal": 500, "emoji": "🍜"},
        {"name": "돈까스 정식",   "cal": 700, "emoji": "🥩"},
        {"name": "1인 샤브샤브",  "cal": 480, "emoji": "🍲"},
        {"name": "제육 덮밥",     "cal": 620, "emoji": "🍳"},
        {"name": "삼각김밥 세트", "cal": 420, "emoji": "🍙"},
        {"name": "소고기 국밥",   "cal": 580, "emoji": "🍲"},
        {"name": "짬뽕 1인분",    "cal": 680, "emoji": "🍜"},
        {"name": "혼밥 정식",     "cal": 650, "emoji": "🍱"},
    ],
}

CATEGORIES = list(MENU_DATA.keys())

SAMPLE_RESTAURANTS = {
    "강남구":  [
        {"name": "맛있는 식당",   "rating": 4.5, "address": "강남구 테헤란로 123", "reviews": 342},
        {"name": "행복한 밥상",   "rating": 4.3, "address": "강남구 역삼동 456",   "reviews": 218},
        {"name": "맛나라",        "rating": 4.1, "address": "강남구 논현동 789",   "reviews": 156},
    ],
    "마포구":  [
        {"name": "홍대 맛집",     "rating": 4.6, "address": "마포구 홍익로 100",   "reviews": 521},
        {"name": "합정 식당",     "rating": 4.2, "address": "마포구 합정동 200",   "reviews": 189},
    ],
    "종로구":  [
        {"name": "광화문 밥집",   "rating": 4.4, "address": "종로구 세종로 50",    "reviews": 298},
        {"name": "인사동 식당",   "rating": 4.3, "address": "종로구 인사동 30",    "reviews": 167},
    ],
    "서초구":  [
        {"name": "반포 맛집",     "rating": 4.5, "address": "서초구 반포대로 77",  "reviews": 403},
        {"name": "교대 식당",     "rating": 4.1, "address": "서초구 서초동 12",    "reviews": 134},
    ],
    "성동구":  [
        {"name": "성수 핫플",     "rating": 4.7, "address": "성동구 성수동 88",    "reviews": 672},
        {"name": "뚝섬 밥상",     "rating": 4.2, "address": "성동구 뚝섬로 45",    "reviews": 201},
    ],
    "부천시":  [
        {"name": "중동 맛집",     "rating": 4.3, "address": "부천시 중동 150",     "reviews": 287},
        {"name": "상동 식당",     "rating": 4.1, "address": "부천시 상동 88",      "reviews": 193},
    ],
}
DISTRICTS = ["선택 안 함"] + sorted(SAMPLE_RESTAURANTS.keys()) + ["기타 지역"]

# ── 세션 초기화 ───────────────────────────────────────────────
def init():
    defaults = {
        "history":          [],
        "excluded":         set(),
        "custom_menus":     [],
        "active_cat":       "저녁 메뉴",
        "active_method":    None,
        "tournament_state": None,
        "scratch_revealed": False,
        "scratch_menu":     None,
        "last_result":      None,
        "_random_result":   None,
        "_roulette_result": None,
        "_roulette_spin":   False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# ── 헬퍼 ─────────────────────────────────────────────────────
def get_menus():
    base = MENU_DATA.get(st.session_state.active_cat, [])
    all_m = base + st.session_state.custom_menus
    return [m for m in all_m if m["name"] not in st.session_state.excluded]

def add_history(menu, method):
    entry = {
        "menu":  menu["name"],
        "emoji": menu.get("emoji", "🍽️"),
        "cal":   menu.get("cal", 0),
        "method": method,
        "cat":   st.session_state.active_cat,
        "time":  datetime.now().strftime("%m/%d %H:%M"),
    }
    st.session_state.history.insert(0, entry)
    if len(st.session_state.history) > 30:
        st.session_state.history = st.session_state.history[:30]
    st.session_state.last_result = entry

def result_card(menu, method=""):
    st.markdown(f"""
    <div class="result-card">
        <div class="result-emoji">{menu.get('emoji','🍽️')}</div>
        <div class="result-name">{menu['name']}</div>
        <div class="result-cal">🔥 약 {menu.get('cal',0)} kcal &nbsp;·&nbsp; {method}</div>
    </div>
    """, unsafe_allow_html=True)

def reset_method():
    st.session_state.active_method   = None
    st.session_state.tournament_state = None
    st.session_state.scratch_revealed = False
    st.session_state.scratch_menu     = None
    st.session_state._random_result   = None
    st.session_state._roulette_result = None
    st.session_state._roulette_spin   = False

# ─────────────────────────────────────────────────────────────
# ① 제목 pill
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="title-pill-wrap"><div class="title-pill">🍽️ 오늘 뭐 먹지?</div></div>',
            unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ② 카테고리 탭 바
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#1a1a2e;border-radius:14px;padding:0.55rem 0.8rem;margin-bottom:1rem;border:1px solid #333;">
<span style="color:rgba(255,255,255,0.4);font-size:0.78rem;font-weight:700;margin-right:0.5rem">카테고리</span>
</div>
""", unsafe_allow_html=True)

row_a = st.columns(7)
row_b = st.columns(7)
all_cat_cols = row_a + row_b

for i, cat in enumerate(CATEGORIES):
    emoji = CATEGORY_EMOJI.get(cat, "🍽️")
    short = cat.replace(" 메뉴", "")
    is_active = (cat == st.session_state.active_cat)
    with all_cat_cols[i]:
        btn_type = "primary" if is_active else "secondary"
        if st.button(f"{emoji} {short}", key=f"cat_{cat}", use_container_width=True, type=btn_type):
            st.session_state.active_cat = cat
            reset_method()
            st.rerun()

st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ③ 메인 레이아웃
# ─────────────────────────────────────────────────────────────
menus = get_menus()
method = st.session_state.active_method

cur_emoji = CATEGORY_EMOJI.get(st.session_state.active_cat, "🍽️")
st.markdown(f"""
<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:1rem;">
    <span style="font-size:1.6rem">{cur_emoji}</span>
    <span style="font-size:1.25rem;font-weight:900;color:#e0e0ff">{st.session_state.active_cat}</span>
    <span style="font-size:0.85rem;color:#666;margin-left:0.3rem">({len(menus)}개 메뉴)</span>
</div>
""", unsafe_allow_html=True)

if len(menus) < 2:
    st.warning("⚠️ 메뉴가 2개 이상 필요합니다. 메뉴 관리에서 추가하거나 다른 카테고리를 선택하세요.")
elif method is None:
    row1 = st.columns(2, gap="medium")
    row2 = st.columns(2, gap="medium")

    METHODS = [
        ("random",   "랜덤",    "버튼 한 번에 즉시 추천",        "🎲", row1[0]),
        ("worldcup", "월드컵",  "1:1 대결로 최후의 1개 선택",    "🏆", row1[1]),
        ("scratch",  "스크래치","마우스로 긁어서 메뉴 확인",     "🃏", row2[0]),
        ("roulette", "룰렛",    "돌아가는 룰렛으로 결정",        "🎡", row2[1]),
    ]
    for key, label, desc, emoji, col in METHODS:
        with col:
            st.markdown(f"""
            <div class="method-card">
                <div>
                    <div class="method-card-title">{label}</div>
                    <div class="method-card-desc">{desc}</div>
                </div>
                <div class="method-card-emoji">{emoji}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"{emoji} {label} 시작", key=f"m_{key}", use_container_width=True, type="primary"):
                st.session_state.active_method = key
                if key == "worldcup":
                    pool = random.sample(menus, min(8, len(menus)))
                    if len(pool) % 2 == 1: pool = pool[:-1]
                    st.session_state.tournament_state = {
                        "round": pool, "pair_idx": 0, "winners": []
                    }
                if key == "scratch":
                    st.session_state.scratch_menu     = random.choice(menus)
                    st.session_state.scratch_revealed = False
                st.rerun()

else:
    if st.button("← 돌아가기", key="back"):
        reset_method()
        st.rerun()

    # ── 랜덤 ──────────────────────────────────────────────────
    if method == "random":
        st.markdown("### 🎲 랜덤 추천")
        if st.button("🎲 지금 바로 추천!", type="primary", use_container_width=True):
            picked = random.choice(menus)
            add_history(picked, "🎲 랜덤")
            st.session_state._random_result = picked
            st.rerun()
        if st.session_state._random_result:
            result_card(st.session_state._random_result, "🎲 랜덤")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🔄 다시 추천", use_container_width=True):
                    picked = random.choice(menus)
                    add_history(picked, "🎲 랜덤")
                    st.session_state._random_result = picked
                    st.rerun()
            with c2:
                if st.button("📍 맛집 찾기", use_container_width=True):
                    st.session_state.active_method = "restaurant"
                    st.rerun()

    # ── 룰렛 ──────────────────────────────────────────────────
    elif method == "roulette":
        st.markdown("### 🎡 룰렛")
        if st.button("🎡 룰렛 돌리기!", type="primary", use_container_width=True):
            picked = random.choice(menus)
            add_history(picked, "🎡 룰렛")
            st.session_state._roulette_result = picked
            st.session_state._roulette_spin   = True
            st.rerun()
        if st.session_state._roulette_spin and st.session_state._roulette_result:
            r = st.session_state._roulette_result
            st.markdown(f'<div style="text-align:center;margin:1rem 0"><span class="spin-emoji">{r["emoji"]}</span></div>',
                        unsafe_allow_html=True)
            result_card(r, "🎡 룰렛")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🔄 다시 돌리기", use_container_width=True):
                    picked = random.choice(menus)
                    add_history(picked, "🎡 룰렛")
                    st.session_state._roulette_result = picked
                    st.rerun()
            with c2:
                if st.button("📍 맛집 찾기", use_container_width=True):
                    st.session_state.active_method = "restaurant"
                    st.rerun()

    # ── 스크래치 ──────────────────────────────────────────────
    elif method == "scratch":
        st.markdown("### 🃏 스크래치 카드")

        m = st.session_state.scratch_menu
        if m:
            menu_name  = m["name"]
            menu_emoji = m.get("emoji", "🍽️")
            menu_cal   = m.get("cal", 0)
        else:
            menu_name, menu_emoji, menu_cal = "???", "🍽️", 0

        # ── 캔버스 스크래치 카드 (HTML + JS) ──
        scratch_html = f"""
<div style="display:flex;flex-direction:column;align-items:center;gap:1rem;">
  <p style="color:#aaa;font-size:0.95rem;margin:0">마우스(또는 손가락)로 긁어서 메뉴를 확인하세요!</p>
  <div style="position:relative;width:340px;height:200px;border-radius:20px;overflow:hidden;
              box-shadow:0 8px 32px rgba(0,0,0,0.5);">
    <!-- 아래 레이어: 결과 -->
    <div id="reveal-layer" style="position:absolute;inset:0;
         background:linear-gradient(135deg,#667eea,#764ba2);
         display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0.4rem;">
      <div style="font-size:3.5rem;line-height:1">{menu_emoji}</div>
      <div style="font-size:1.8rem;font-weight:900;color:white">{menu_name}</div>
      <div style="font-size:0.9rem;color:rgba(255,255,255,0.8);
                  background:rgba(255,255,255,0.2);border-radius:999px;padding:0.2rem 1rem">
        🔥 {menu_cal} kcal
      </div>
    </div>
    <!-- 위 레이어: 긁는 캔버스 -->
    <canvas id="scratch-canvas" width="340" height="200"
            style="position:absolute;inset:0;cursor:crosshair;border-radius:20px;touch-action:none"></canvas>
  </div>
  <p id="hint-text" style="color:#666;font-size:0.82rem;margin:0">긁은 면적이 60%를 넘으면 자동 완성돼요</p>
</div>

<script>
(function() {{
  const canvas  = document.getElementById('scratch-canvas');
  const ctx     = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;

  // 긁힌 면적 트래킹용 오프스크린
  const offscreen = document.createElement('canvas');
  offscreen.width = W; offscreen.height = H;
  const octx = offscreen.getContext('2d');

  // 스크래치 레이어 그리기 (어두운 질감)
  function drawScratchLayer(c) {{
    const grad = c.createLinearGradient(0,0,W,H);
    grad.addColorStop(0,'#2a2a4a');
    grad.addColorStop(0.5,'#3a2a5a');
    grad.addColorStop(1,'#1a1a3a');
    c.fillStyle = grad;
    c.fillRect(0,0,W,H);

    // 반짝이 패턴
    c.fillStyle='rgba(255,255,255,0.03)';
    for(let i=0;i<60;i++){{
      const x=Math.random()*W, y=Math.random()*H, r=Math.random()*3+1;
      c.beginPath(); c.arc(x,y,r,0,Math.PI*2); c.fill();
    }}
    // 텍스트
    c.fillStyle='rgba(255,255,255,0.55)';
    c.font='bold 22px "Noto Sans KR",sans-serif';
    c.textAlign='center';
    c.fillText('🪙  긁어서 확인  🪙', W/2, H/2-10);
    c.font='14px "Noto Sans KR",sans-serif';
    c.fillStyle='rgba(255,255,255,0.35)';
    c.fillText('Scratch here!', W/2, H/2+20);
  }}

  drawScratchLayer(ctx);
  drawScratchLayer(octx);

  ctx.globalCompositeOperation = 'destination-out';
  octx.globalCompositeOperation = 'destination-out';

  let painting = false;
  let revealed = false;

  function getPos(e) {{
    const rect = canvas.getBoundingClientRect();
    const scaleX = W / rect.width, scaleY = H / rect.height;
    if (e.touches) {{
      return {{
        x: (e.touches[0].clientX - rect.left) * scaleX,
        y: (e.touches[0].clientY - rect.top)  * scaleY,
      }};
    }}
    return {{
      x: (e.clientX - rect.left) * scaleX,
      y: (e.clientY - rect.top)  * scaleY,
    }};
  }}

  function scratch(pos) {{
    ctx.beginPath();
    ctx.arc(pos.x, pos.y, 28, 0, Math.PI*2);
    ctx.fill();
    octx.beginPath();
    octx.arc(pos.x, pos.y, 28, 0, Math.PI*2);
    octx.fill();
    checkReveal();
  }}

  function checkReveal() {{
    if (revealed) return;
    const data = octx.getImageData(0,0,W,H).data;
    let cleared = 0;
    for (let i=3; i<data.length; i+=4) {{ if (data[i]===0) cleared++; }}
    const pct = cleared / (W*H);
    if (pct > 0.60) {{
      revealed = true;
      // 부드럽게 남은 캔버스 페이드아웃
      let op = 1;
      function fade() {{
        op -= 0.06;
        if (op <= 0) {{ canvas.style.display='none'; document.getElementById('hint-text').textContent='✨ 오늘의 메뉴!'; return; }}
        canvas.style.opacity = op;
        requestAnimationFrame(fade);
      }}
      fade();
    }}
  }}

  canvas.addEventListener('mousedown',  e=>{{ painting=true; scratch(getPos(e)); }});
  canvas.addEventListener('mousemove',  e=>{{ if(painting) scratch(getPos(e)); }});
  canvas.addEventListener('mouseup',    ()=>{{ painting=false; }});
  canvas.addEventListener('mouseleave', ()=>{{ painting=false; }});
  canvas.addEventListener('touchstart', e=>{{ e.preventDefault(); painting=true; scratch(getPos(e)); }}, {{passive:false}});
  canvas.addEventListener('touchmove',  e=>{{ e.preventDefault(); if(painting) scratch(getPos(e)); }}, {{passive:false}});
  canvas.addEventListener('touchend',   ()=>{{ painting=false; }});
}})();
</script>
"""
        st.components.v1.html(scratch_html, height=300)

        # 이력에 추가 (한 번만)
        if not st.session_state.scratch_revealed and m:
            add_history(m, "🃏 스크래치")
            st.session_state.scratch_revealed = True

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 새 카드 뽑기", use_container_width=True, type="primary"):
                st.session_state.scratch_menu     = random.choice(menus)
                st.session_state.scratch_revealed = False
                st.rerun()
        with c2:
            if st.button("📍 맛집 찾기", use_container_width=True):
                st.session_state.active_method = "restaurant"
                st.rerun()

    # ── 월드컵 ────────────────────────────────────────────────
    elif method == "worldcup":
        ts = st.session_state.tournament_state
        if ts is None:
            st.error("토너먼트 초기화 오류. 돌아가기를 눌러주세요.")
        elif len(ts["round"]) == 1:
            st.markdown("### 🏆 최종 우승!")
            st.balloons()
            winner = ts["round"][0]
            add_history(winner, "🏆 월드컵")
            result_card(winner, "🏆 월드컵")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🔄 다시 하기", use_container_width=True):
                    pool = random.sample(menus, min(8, len(menus)))
                    if len(pool) % 2 == 1: pool = pool[:-1]
                    st.session_state.tournament_state = {"round": pool, "pair_idx": 0, "winners": []}
                    st.rerun()
            with c2:
                if st.button("📍 맛집 찾기", use_container_width=True):
                    st.session_state.active_method = "restaurant"
                    st.rerun()
        else:
            pairs   = [(ts["round"][i], ts["round"][i+1]) for i in range(0, len(ts["round"])-1, 2)]
            idx     = ts["pair_idx"]

            if idx >= len(pairs):
                next_round = ts["winners"][:]
                if len(next_round) % 2 == 1 and len(next_round) > 1:
                    next_round = next_round[:-1]
                ts["round"]    = next_round
                ts["winners"]  = []
                ts["pair_idx"] = 0
                st.rerun()
            else:
                a, b = pairs[idx]
                n    = len(ts["round"])
                st.markdown(f"### 🏆 {n}강 &nbsp; — &nbsp; {idx+1} / {len(pairs)} 경기")
                st.progress(idx / len(pairs))

                col_a, col_vs, col_b = st.columns([5, 1, 5])
                with col_a:
                    st.markdown(f"""
                    <div class="wc-option">
                        <div class="wc-emoji">{a['emoji']}</div>
                        <div class="wc-name">{a['name']}</div>
                        <div class="wc-cal">🔥 {a['cal']} kcal</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"✅ {a['name']}", key=f"wa_{idx}", use_container_width=True, type="primary"):
                        ts["winners"].append(a)
                        ts["pair_idx"] += 1
                        st.rerun()
                with col_vs:
                    st.markdown('<div style="display:flex;align-items:center;justify-content:center;height:100%;min-height:130px;font-size:1.4rem;font-weight:900;color:#444">VS</div>',
                                unsafe_allow_html=True)
                with col_b:
                    st.markdown(f"""
                    <div class="wc-option">
                        <div class="wc-emoji">{b['emoji']}</div>
                        <div class="wc-name">{b['name']}</div>
                        <div class="wc-cal">🔥 {b['cal']} kcal</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"✅ {b['name']}", key=f"wb_{idx}", use_container_width=True, type="primary"):
                        ts["winners"].append(b)
                        ts["pair_idx"] += 1
                        st.rerun()

    # ── 맛집 찾기 ─────────────────────────────────────────────
    elif method == "restaurant":
        st.markdown("### 📍 맛집 찾기")
        lr = st.session_state.last_result
        all_names    = [m["name"] for m in menus]
        default_idx  = all_names.index(lr["menu"]) if lr and lr["menu"] in all_names else 0
        search_menu  = st.selectbox("🍜 메뉴", all_names, index=default_idx)
        district     = st.selectbox("📍 지역", DISTRICTS)
        if st.button("🔍 맛집 검색", type="primary", use_container_width=True):
            if district in ("선택 안 함", "기타 지역"):
                st.warning("지역을 선택해주세요. (현재는 샘플 데이터)")
            else:
                rests = SAMPLE_RESTAURANTS.get(district, [])
                if rests:
                    st.markdown(f"**{district} 근처 {search_menu} 맛집**")
                    for r in rests:
                        stars = "⭐" * int(r["rating"])
                        st.markdown(f"""
                        <div class="rest-card">
                            <div style="font-size:1rem;font-weight:700;color:#eee">🍴 {r['name']}</div>
                            <div style="color:#888;font-size:0.85rem;margin-top:0.3rem">
                                {stars} {r['rating']} · 리뷰 {r['reviews']}개 · 📍 {r['address']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.caption("⚠️ 샘플 데이터입니다.")
                else:
                    st.warning("해당 지역 데이터가 없습니다.")

# ─────────────────────────────────────────────────────────────
# ④ 하단 탭: 이력 + 메뉴 관리
# ─────────────────────────────────────────────────────────────
st.markdown("<hr style='border:none;border-top:2px solid #222;margin:1.5rem 0 1rem'>",
            unsafe_allow_html=True)

tab_hist, tab_mgmt = st.tabs(["📋 추천 이력", "🔧 메뉴 관리"])

with tab_hist:
    if st.session_state.history:
        c1, c2, c3 = st.columns(3)
        methods_l = [h["method"] for h in st.session_state.history]
        menus_l   = [h["menu"]   for h in st.session_state.history]
        with c1: st.metric("총 추천 횟수", f"{len(st.session_state.history)}회")
        with c2: st.metric("자주 쓴 방식",  max(set(methods_l), key=methods_l.count))
        with c3: st.metric("최다 추천 메뉴", max(set(menus_l), key=menus_l.count))
        st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
        for h in st.session_state.history:
            st.markdown(f"""
            <div class="hist-item">
                <div>{h['emoji']} <b style="color:#eee">{h['menu']}</b>
                    <span style="color:#555;font-size:0.82rem"> &nbsp;·&nbsp; {h['time']} &nbsp;·&nbsp; {h['method']} &nbsp;·&nbsp; {h['cat']}</span>
                </div>
                <div style="color:#667eea;font-weight:700">{h['cal']} kcal</div>
            </div>
            """, unsafe_allow_html=True)
        if st.button("🗑️ 이력 초기화"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("아직 추천 이력이 없어요. 위에서 메뉴를 추천받아 보세요!")

with tab_mgmt:
    col_add, col_excl = st.columns(2)
    with col_add:
        st.markdown("**➕ 커스텀 메뉴 추가**")
        nm = st.text_input("메뉴 이름", placeholder="예: 순두부찌개", key="add_nm")
        nc = st.number_input("칼로리 (kcal)", 0, 3000, 500, 50, key="add_cal")
        ne = st.text_input("이모지", "🍽️", max_chars=2, key="add_emoji")
        if st.button("추가", type="primary"):
            if nm.strip():
                st.session_state.custom_menus.append({"name": nm.strip(), "cal": nc, "emoji": ne})
                st.success(f"'{nm}' 추가 완료!")
                st.rerun()
            else:
                st.error("이름을 입력하세요.")
        if st.session_state.custom_menus:
            st.markdown("**내 커스텀 메뉴**")
            for i, m in enumerate(st.session_state.custom_menus):
                ca, cb = st.columns([5, 1])
                with ca: st.write(f"{m['emoji']} {m['name']} ({m['cal']}kcal)")
                with cb:
                    if st.button("🗑️", key=f"del_{i}"):
                        st.session_state.custom_menus.pop(i)
                        st.rerun()

    with col_excl:
        st.markdown(f"**🚫 메뉴 제외 설정** — {st.session_state.active_cat}")
        src = MENU_DATA.get(st.session_state.active_cat, [])
        for m in src:
            excluded = m["name"] in st.session_state.excluded
            chk = st.checkbox(f"{m['emoji']} {m['name']}", value=excluded, key=f"ex_{m['name']}")
            if chk:  st.session_state.excluded.add(m["name"])
            else:    st.session_state.excluded.discard(m["name"])
        if st.session_state.excluded:
            st.markdown(f"<div style='color:#f5576c;font-size:0.82rem;margin-top:0.5rem'>제외 중: {', '.join(st.session_state.excluded)}</div>",
                        unsafe_allow_html=True)
