import streamlit as st
import random
import json
from datetime import datetime

# ── 페이지 설정 ────────────────────────────────────────────────
st.set_page_config(
    page_title="오늘 뭐 먹지? 🍽️",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

/* 메인 배경 */
.stApp { background: #f8f9fa; }

/* 사이드바 */
[data-testid="stSidebar"] { background: #1a1a2e; }
[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label { color: #e0e0e0 !important; }

/* 타이틀 */
.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 900;
    color: #1a1a2e;
    margin-bottom: 0.2rem;
}
.main-sub {
    text-align: center;
    color: #888;
    font-size: 1rem;
    margin-bottom: 2rem;
}

/* 결과 카드 */
.result-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    color: white;
    margin: 1rem 0;
    box-shadow: 0 10px 40px rgba(102,126,234,0.4);
}
.result-menu-name {
    font-size: 2.5rem;
    font-weight: 900;
    margin-bottom: 0.5rem;
}
.result-calorie {
    font-size: 1.1rem;
    opacity: 0.9;
    background: rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 0.3rem 1rem;
    display: inline-block;
    margin-top: 0.5rem;
}
.result-category {
    font-size: 0.9rem;
    opacity: 0.8;
    margin-top: 0.8rem;
}

/* 메뉴 방식 카드 */
.method-card {
    background: white;
    border-radius: 15px;
    padding: 1.2rem;
    text-align: center;
    border: 2px solid #eee;
    cursor: pointer;
    transition: all 0.2s;
    margin: 0.3rem;
}
.method-card:hover { border-color: #667eea; transform: translateY(-2px); }
.method-card.selected { border-color: #667eea; background: #f0f0ff; }

/* 이력 아이템 */
.history-item {
    background: white;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0;
    border-left: 4px solid #667eea;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.history-menu { font-weight: 700; color: #1a1a2e; }
.history-time { font-size: 0.75rem; color: #aaa; }

/* 메뉴 아이템 */
.menu-item {
    background: white;
    border-radius: 10px;
    padding: 0.7rem 1rem;
    margin: 0.3rem 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

/* 버튼 커스텀 */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}

/* 룰렛 애니메이션 */
@keyframes spin {
    0%   { transform: rotate(0deg); }
    100% { transform: rotate(720deg); }
}
.roulette-spin {
    display: inline-block;
    animation: spin 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    font-size: 4rem;
}

/* 스크래치 카드 */
.scratch-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    border-radius: 20px;
    padding: 3rem;
    text-align: center;
    color: white;
    cursor: pointer;
    font-size: 1.2rem;
    font-weight: 700;
}

/* 토너먼트 카드 */
.tournament-option {
    background: white;
    border: 3px solid #e0e0e0;
    border-radius: 15px;
    padding: 1.5rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 1.3rem;
    font-weight: 700;
}
.tournament-option:hover { border-color: #667eea; background: #f8f0ff; }

/* 맛집 카드 */
.restaurant-card {
    background: white;
    border-radius: 15px;
    padding: 1.2rem 1.5rem;
    margin: 0.5rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    border-left: 5px solid #f5576c;
}
.restaurant-name { font-size: 1.1rem; font-weight: 700; color: #1a1a2e; }
.restaurant-meta { color: #888; font-size: 0.85rem; margin-top: 0.3rem; }

/* 섹션 헤더 */
.section-header {
    font-size: 1.4rem;
    font-weight: 900;
    color: #1a1a2e;
    border-bottom: 3px solid #667eea;
    padding-bottom: 0.5rem;
    margin-bottom: 1.5rem;
}

/* 카테고리 배지 */
.badge {
    display: inline-block;
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
    margin: 0.2rem;
}
.badge-situation { background: #e8f4fd; color: #2196F3; }
.badge-preference { background: #fce4ec; color: #E91E63; }
.badge-cuisine { background: #e8f5e9; color: #4CAF50; }
</style>
""", unsafe_allow_html=True)

# ── 데이터 ────────────────────────────────────────────────────
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

# 샘플 맛집 데이터 (실제 앱에서는 Kakao/Google API로 대체)
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

# ── 세션 상태 초기화 ──────────────────────────────────────────
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

# ── 유틸리티 함수 ─────────────────────────────────────────────
def get_all_menus_flat(category_type=None, subcategory=None):
    """선택된 카테고리에서 활성 메뉴 목록 반환"""
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
    <div class="result-card">
        <div style="font-size:4rem">{menu.get('emoji','🍽️')}</div>
        <div class="result-menu-name">{menu['name']}</div>
        <div class="result-calorie">🔥 약 {menu.get('cal',0)} kcal</div>
        <div class="result-category">추천 방식: {method}</div>
    </div>
    """, unsafe_allow_html=True)

# ── 사이드바 ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍽️ 오늘 뭐 먹지?")
    st.markdown("---")

    # 카테고리 선택
    st.markdown("### 📂 카테고리 선택")
    cat_type = st.selectbox("대분류", ["전체"] + list(MENU_DATA.keys()), key="cat_type")
    cat_sub = None
    if cat_type != "전체":
        cat_sub = st.selectbox("소분류", list(MENU_DATA[cat_type].keys()), key="cat_sub")

    st.markdown("---")

    # 추천 이력
    st.markdown("### 📋 추천 이력")
    if st.session_state.history:
        for h in st.session_state.history[:5]:
            st.markdown(f"""
            <div class="history-item">
                <div>
                    <span style="font-size:1.2rem">{h['emoji']}</span>
                    <span class="history-menu"> {h['menu']}</span>
                    <div class="history-time">{h['time']} · {h['method']}</div>
                </div>
                <div style="font-size:0.8rem;color:#aaa">{h['cal']}kcal</div>
            </div>
            """, unsafe_allow_html=True)
        if len(st.session_state.history) > 5:
            st.caption(f"외 {len(st.session_state.history)-5}개 더 있음")
        if st.button("🗑️ 이력 초기화", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    else:
        st.caption("아직 추천 이력이 없어요.")

    st.markdown("---")
    st.caption("v1.0 · Python + Streamlit")

# ── 메인 화면 ─────────────────────────────────────────────────
st.markdown('<div class="main-title">오늘 뭐 먹지? 🍽️</div>', unsafe_allow_html=True)
st.markdown('<div class="main-sub">결정 장애를 위한 메뉴 추천 서비스</div>', unsafe_allow_html=True)

# 현재 카테고리 뱃지 표시
if cat_type != "전체" and cat_sub:
    badge_class = "badge-situation" if cat_type == "상황별" else ("badge-preference" if cat_type == "선호도별" else "badge-cuisine")
    st.markdown(f'<div style="text-align:center;margin-bottom:1rem"><span class="badge {badge_class}">{cat_type} › {cat_sub}</span></div>', unsafe_allow_html=True)

# 탭 구성
tab1, tab2, tab3, tab4 = st.tabs(["🎯 추천받기", "🔧 메뉴 관리", "📍 맛집 찾기", "📜 전체 이력"])

# ────────────────────────────────────────────────────────────
# TAB 1: 추천받기
# ────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-header">추천 방식을 선택하세요</div>', unsafe_allow_html=True)

    col_q, col_r, col_w, col_rnd, col_s = st.columns(5)

    with col_q:
        quick = st.button("⚡ 빠른 추천", use_container_width=True, type="primary")
    with col_r:
        roulette = st.button("🎡 룰렛", use_container_width=True)
    with col_w:
        worldcup = st.button("🏆 월드컵", use_container_width=True)
    with col_rnd:
        randompick = st.button("🎲 랜덤 픽", use_container_width=True)
    with col_s:
        scratch = st.button("🃏 스크래치", use_container_width=True)

    st.markdown("---")
    menus = get_all_menus_flat(
        cat_type if cat_type != "전체" else None,
        cat_sub
    )

    if len(menus) < 2:
        st.warning("⚠️ 해당 카테고리에 메뉴가 부족합니다. 메뉴를 추가하거나 카테고리를 변경해 주세요.")
    else:
        # ── 빠른 추천 ──
        if quick:
            st.session_state.tournament_state = None
            st.session_state.scratch_revealed = False
            picks = random.sample(menus, min(3, len(menus)))
            st.markdown("### ⚡ 빠른 추천 결과")
            cols = st.columns(len(picks))
            for i, pick in enumerate(picks):
                with cols[i]:
                    st.markdown(f"""
                    <div style="background:white;border-radius:15px;padding:1.5rem;text-align:center;
                                box-shadow:0 4px 15px rgba(0,0,0,0.1);border-top:4px solid #667eea;">
                        <div style="font-size:2.5rem">{pick['emoji']}</div>
                        <div style="font-weight:700;font-size:1.1rem;margin:0.5rem 0">{pick['name']}</div>
                        <div style="color:#888;font-size:0.85rem">🔥 {pick['cal']} kcal</div>
                    </div>
                    """, unsafe_allow_html=True)
            add_to_history(picks[0], "⚡ 빠른 추천", cat_sub or "전체")

        # ── 룰렛 ──
        elif roulette:
            st.session_state.tournament_state = None
            st.session_state.scratch_revealed = False
            picked = random.choice(menus)
            st.markdown("### 🎡 룰렛 결과")
            st.markdown(f'<div style="text-align:center"><span class="roulette-spin">{picked["emoji"]}</span></div>', unsafe_allow_html=True)
            show_result_card(picked, "🎡 룰렛")
            add_to_history(picked, "🎡 룰렛", cat_sub or "전체")

        # ── 랜덤 픽 ──
        elif randompick:
            st.session_state.tournament_state = None
            st.session_state.scratch_revealed = False
            picked = random.choice(menus)
            st.markdown("### 🎲 랜덤 픽 결과")
            show_result_card(picked, "🎲 랜덤 픽")
            add_to_history(picked, "🎲 랜덤 픽", cat_sub or "전체")

        # ── 스크래치 ──
        elif scratch:
            st.session_state.tournament_state = None
            st.session_state.scratch_menu = random.choice(menus)
            st.session_state.scratch_revealed = False

        # 스크래치 UI
        if st.session_state.scratch_menu and not st.session_state.scratch_revealed:
            st.markdown("### 🃏 스크래치 카드")
            st.markdown('<div class="scratch-card">👆 아래 버튼을 눌러 메뉴를 확인하세요!</div>', unsafe_allow_html=True)
            if st.button("🔍 긁어서 확인하기!", use_container_width=True, type="primary"):
                st.session_state.scratch_revealed = True
                add_to_history(st.session_state.scratch_menu, "🃏 스크래치", cat_sub or "전체")
                st.rerun()

        if st.session_state.scratch_revealed and st.session_state.scratch_menu:
            st.markdown("### 🃏 스크래치 결과")
            show_result_card(st.session_state.scratch_menu, "🃏 스크래치")

        # ── 월드컵(토너먼트) ──
        if worldcup:
            pool = random.sample(menus, min(8, len(menus)))
            if len(pool) < 2:
                pool = menus[:]
            st.session_state.tournament_state = {
                "pool": pool,
                "round": pool[:],
                "current_pair_idx": 0,
                "winners": [],
                "round_num": 1,
            }
            st.session_state.scratch_revealed = False

        if st.session_state.tournament_state:
            ts = st.session_state.tournament_state
            st.markdown(f"### 🏆 월드컵 토너먼트 — {len(ts['round'])}강")

            # 현재 대결 쌍
            idx = ts["current_pair_idx"]
            pairs = [(ts["round"][i], ts["round"][i+1]) for i in range(0, len(ts["round"])-1, 2)]
            if len(ts["round"]) % 2 == 1:
                ts["winners"].append(ts["round"][-1])  # 홀수면 자동 통과

            if idx < len(pairs):
                a, b = pairs[idx]
                st.markdown(f"**{idx+1}번째 대결** / 총 {len(pairs)}경기")
                col_a, mid, col_b = st.columns([5, 1, 5])
                with col_a:
                    st.markdown(f"""
                    <div class="tournament-option">
                        <div style="font-size:2rem">{a['emoji']}</div>
                        <div>{a['name']}</div>
                        <div style="font-size:0.8rem;color:#aaa">🔥 {a['cal']} kcal</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"✅ {a['name']} 선택", key=f"pick_a_{idx}", use_container_width=True):
                        ts["winners"].append(a)
                        ts["current_pair_idx"] += 1
                        if ts["current_pair_idx"] >= len(pairs):
                            if len(ts["winners"]) == 1:
                                add_to_history(ts["winners"][0], "🏆 월드컵", cat_sub or "전체")
                                st.session_state.tournament_state = None
                            else:
                                ts["round"] = ts["winners"]
                                ts["winners"] = []
                                ts["current_pair_idx"] = 0
                                ts["round_num"] += 1
                        st.rerun()
                with mid:
                    st.markdown('<div style="text-align:center;font-size:1.5rem;padding-top:2rem;font-weight:900;color:#aaa">VS</div>', unsafe_allow_html=True)
                with col_b:
                    st.markdown(f"""
                    <div class="tournament-option">
                        <div style="font-size:2rem">{b['emoji']}</div>
                        <div>{b['name']}</div>
                        <div style="font-size:0.8rem;color:#aaa">🔥 {b['cal']} kcal</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"✅ {b['name']} 선택", key=f"pick_b_{idx}", use_container_width=True):
                        ts["winners"].append(b)
                        ts["current_pair_idx"] += 1
                        if ts["current_pair_idx"] >= len(pairs):
                            if len(ts["winners"]) == 1:
                                add_to_history(ts["winners"][0], "🏆 월드컵", cat_sub or "전체")
                                st.session_state.tournament_state = None
                            else:
                                ts["round"] = ts["winners"]
                                ts["winners"] = []
                                ts["current_pair_idx"] = 0
                                ts["round_num"] += 1
                        st.rerun()
            else:
                # 라운드 종료 처리
                ts["round"] = ts["winners"]
                ts["winners"] = []
                ts["current_pair_idx"] = 0
                ts["round_num"] += 1
                st.rerun()

        # 마지막 결과가 월드컵 우승자인 경우
        if st.session_state.last_result and st.session_state.last_result.get("method") == "🏆 월드컵":
            lr = st.session_state.last_result
            st.markdown("### 🏆 월드컵 최종 우승!")
            show_result_card({"name": lr["menu"], "emoji": lr["emoji"], "cal": lr["cal"]}, "🏆 월드컵")

# ────────────────────────────────────────────────────────────
# TAB 2: 메뉴 관리
# ────────────────────────────────────────────────────────────
with tab2:
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown('<div class="section-header">➕ 메뉴 추가</div>', unsafe_allow_html=True)
        new_name = st.text_input("메뉴 이름", placeholder="예: 순두부찌개")
        new_cal = st.number_input("칼로리 (kcal)", min_value=0, max_value=3000, value=500, step=50)
        new_emoji = st.text_input("이모지", value="🍽️", max_chars=2)
        if st.button("메뉴 추가하기", type="primary", use_container_width=True):
            if new_name.strip():
                st.session_state.custom_menus.append({"name": new_name.strip(), "cal": new_cal, "emoji": new_emoji})
                st.success(f"'{new_name}' 추가 완료!")
                st.rerun()
            else:
                st.error("메뉴 이름을 입력해주세요.")

        st.markdown("---")
        st.markdown('<div class="section-header">🚫 메뉴 제외 설정</div>', unsafe_allow_html=True)
        if cat_type != "전체" and cat_sub:
            source = MENU_DATA.get(cat_type, {}).get(cat_sub, [])
            for m in source:
                is_excluded = m["name"] in st.session_state.excluded
                chk = st.checkbox(f"{m['emoji']} {m['name']} ({m['cal']}kcal)", value=is_excluded, key=f"excl_{m['name']}")
                if chk and m["name"] not in st.session_state.excluded:
                    st.session_state.excluded.add(m["name"])
                elif not chk and m["name"] in st.session_state.excluded:
                    st.session_state.excluded.discard(m["name"])
        else:
            st.caption("카테고리를 선택하면 해당 메뉴의 제외 설정이 표시됩니다.")

    with col_right:
        st.markdown('<div class="section-header">📝 내 커스텀 메뉴</div>', unsafe_allow_html=True)
        if st.session_state.custom_menus:
            for i, m in enumerate(st.session_state.custom_menus):
                col_name, col_del = st.columns([5, 1])
                with col_name:
                    st.markdown(f"""
                    <div class="menu-item">
                        <span>{m['emoji']} {m['name']}</span>
                        <span style="color:#aaa;font-size:0.85rem">🔥 {m['cal']} kcal</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col_del:
                    if st.button("🗑️", key=f"del_{i}"):
                        st.session_state.custom_menus.pop(i)
                        st.rerun()
        else:
            st.info("아직 추가한 메뉴가 없습니다.")

        st.markdown("---")
        st.markdown('<div class="section-header">📊 제외된 메뉴</div>', unsafe_allow_html=True)
        if st.session_state.excluded:
            for name in list(st.session_state.excluded):
                col_n, col_r = st.columns([5, 1])
                with col_n:
                    st.markdown(f"🚫 {name}")
                with col_r:
                    if st.button("복원", key=f"restore_{name}"):
                        st.session_state.excluded.discard(name)
                        st.rerun()
        else:
            st.info("제외된 메뉴가 없습니다.")

# ────────────────────────────────────────────────────────────
# TAB 3: 맛집 찾기
# ────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-header">📍 내 주변 맛집 찾기</div>', unsafe_allow_html=True)
    st.info("💡 Step 3에서 Kakao Local API 또는 Google Places API와 연동 예정입니다. 현재는 샘플 데이터로 동작합니다.")

    col_menu, col_district = st.columns(2)
    with col_menu:
        all_menus_flat = get_all_menus_flat()
        menu_names = [m["name"] for m in all_menus_flat]
        if st.session_state.last_result:
            default_idx = menu_names.index(st.session_state.last_result["menu"]) if st.session_state.last_result["menu"] in menu_names else 0
        else:
            default_idx = 0
        search_menu = st.selectbox("🍜 어떤 메뉴?", menu_names, index=default_idx)
    with col_district:
        district = st.selectbox("📍 어느 지역?", DISTRICTS)

    if st.button("🔍 맛집 검색하기", type="primary", use_container_width=True):
        if district == "선택 안 함":
            st.warning("지역을 선택해 주세요.")
        elif district == "기타 지역":
            st.info("현재 샘플 데이터에 없는 지역입니다. API 연동 후 전국 검색이 가능합니다.")
        else:
            restaurants = SAMPLE_RESTAURANTS.get(district, [])
            if restaurants:
                st.markdown(f"### 🗺️ {district} 근처 **{search_menu}** 맛집")
                for r in restaurants:
                    stars = "⭐" * int(r["rating"])
                    st.markdown(f"""
                    <div class="restaurant-card">
                        <div class="restaurant-name">🍴 {r['name']}</div>
                        <div class="restaurant-meta">
                            {stars} {r['rating']}  ·  리뷰 {r['reviews']}개  ·  📍 {r['address']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.caption("⚠️ 샘플 데이터입니다. 실제 식당 정보와 다를 수 있습니다.")
            else:
                st.warning("해당 지역의 맛집 정보가 없습니다.")

# ────────────────────────────────────────────────────────────
# TAB 4: 전체 이력
# ────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-header">📜 전체 추천 이력</div>', unsafe_allow_html=True)
    if st.session_state.history:
        # 통계
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.metric("총 추천 횟수", f"{len(st.session_state.history)}회")
        with col_s2:
            methods = [h["method"] for h in st.session_state.history]
            most_method = max(set(methods), key=methods.count)
            st.metric("가장 많이 쓴 방식", most_method)
        with col_s3:
            menus_hist = [h["menu"] for h in st.session_state.history]
            most_menu = max(set(menus_hist), key=menus_hist.count)
            st.metric("가장 많이 추천된 메뉴", most_menu)
        st.markdown("---")
        for h in st.session_state.history:
            st.markdown(f"""
            <div class="history-item">
                <div style="display:flex;align-items:center;gap:1rem">
                    <span style="font-size:1.5rem">{h['emoji']}</span>
                    <div>
                        <div class="history-menu">{h['menu']}</div>
                        <div class="history-time">{h['time']} · {h['method']} · {h.get('category','')}</div>
                    </div>
                </div>
                <div style="text-align:right">
                    <div style="font-weight:700;color:#667eea">{h['cal']} kcal</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        if st.button("🗑️ 전체 이력 삭제", type="secondary"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("아직 추천 이력이 없습니다. 추천받기 탭에서 메뉴를 추천받아보세요!")
