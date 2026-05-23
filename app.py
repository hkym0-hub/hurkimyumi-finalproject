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

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}
.stApp { background: #f0f2f8; }

/* 전체 패딩 조정 */
.block-container { padding: 1.5rem 2rem 2rem 2rem !important; max-width: 1200px; }

/* ── 제목 pill ── */
.title-pill-wrap {
    display: flex;
    justify-content: center;
    margin-bottom: 1.4rem;
}
.title-pill {
    background: linear-gradient(135deg, #9b7fe8, #7c5cbf);
    color: white;
    font-size: 1.35rem;
    font-weight: 900;
    padding: 0.6rem 3rem;
    border-radius: 999px;
    letter-spacing: 0.05em;
    box-shadow: 0 4px 20px rgba(124,92,191,0.35);
}

/* ── 카테고리 탭 바 ── */
.cat-bar-wrap {
    background: #d966a0;
    border-radius: 12px;
    padding: 0.5rem 0.8rem;
    margin-bottom: 1.5rem;
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
    align-items: center;
}
.cat-btn {
    background: transparent;
    border: none;
    color: white;
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 0.88rem;
    font-weight: 600;
    padding: 0.35rem 0.9rem;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.15s;
    white-space: nowrap;
}
.cat-btn:hover { background: rgba(255,255,255,0.25); }
.cat-btn.active { background: white; color: #d966a0; }

/* ── 레이아웃: 왼쪽 분류 패널 + 오른쪽 메인 ── */
.layout-wrap { display: flex; gap: 1.2rem; align-items: flex-start; }

/* ── 왼쪽 분류 패널 ── */
.side-panel {
    background: white;
    border-radius: 14px;
    padding: 1rem 0.8rem;
    min-width: 130px;
    max-width: 140px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    flex-shrink: 0;
}
.side-title { font-size: 0.75rem; font-weight: 700; color: #aaa; margin-bottom: 0.6rem; text-transform: uppercase; letter-spacing: 0.05em; }
.side-item {
    font-size: 0.88rem;
    font-weight: 600;
    color: #555;
    padding: 0.4rem 0.6rem;
    border-radius: 8px;
    cursor: pointer;
    margin-bottom: 0.25rem;
    transition: all 0.15s;
}
.side-item:hover { background: #f5f0ff; color: #7c5cbf; }
.side-item.active { background: #ede9ff; color: #7c5cbf; font-weight: 700; }

/* ── 2×2 메서드 그리드 ── */
.methods-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    flex: 1;
}

/* ── 메서드 카드 ── */
.method-card {
    background: #b8c4e0;
    border-radius: 18px;
    min-height: 200px;
    padding: 1.8rem 1.5rem 1.5rem 1.5rem;
    cursor: pointer;
    transition: transform 0.15s, box-shadow 0.15s, background 0.15s;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
}
.method-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.15);
    background: #a8b8d8;
}
.method-card-title {
    font-size: 1.6rem;
    font-weight: 900;
    color: white;
    text-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.method-card-desc {
    font-size: 0.82rem;
    color: rgba(255,255,255,0.85);
    margin-top: 0.5rem;
    font-weight: 600;
}
.method-card-emoji {
    position: absolute;
    bottom: 1rem;
    right: 1.2rem;
    font-size: 3rem;
    opacity: 0.35;
}

/* ── 결과 카드 ── */
.result-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    color: white;
    margin: 1.2rem 0;
    box-shadow: 0 10px 40px rgba(102,126,234,0.4);
}
.result-emoji { font-size: 4rem; line-height: 1; margin-bottom: 0.5rem; }
.result-name { font-size: 2.4rem; font-weight: 900; margin-bottom: 0.5rem; }
.result-cal {
    display: inline-block;
    background: rgba(255,255,255,0.25);
    border-radius: 999px;
    padding: 0.3rem 1.2rem;
    font-size: 0.95rem;
    font-weight: 600;
}

/* ── 룰렛 스핀 ── */
@keyframes spin-slow {
    0%   { transform: rotate(0deg) scale(1); }
    50%  { transform: rotate(1080deg) scale(1.2); }
    100% { transform: rotate(1440deg) scale(1); }
}
.spin-emoji {
    display: inline-block;
    font-size: 5rem;
    animation: spin-slow 2s cubic-bezier(0.25,0.46,0.45,0.94) forwards;
}

/* ── 스크래치 카드 ── */
.scratch-hidden {
    background: linear-gradient(135deg, #c0c0c0 25%, #a8a8a8 50%, #c0c0c0 75%);
    background-size: 20px 20px;
    border-radius: 20px;
    padding: 3rem 2rem;
    text-align: center;
    cursor: pointer;
    border: 3px dashed #999;
    position: relative;
}
.scratch-label {
    font-size: 1.1rem;
    font-weight: 700;
    color: #666;
    margin-top: 1rem;
}
.scratch-coins { font-size: 3rem; }

/* ── 월드컵 ── */
.wc-option {
    background: white;
    border: 3px solid #ddd;
    border-radius: 16px;
    padding: 1.8rem 1.2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.18s;
}
.wc-option:hover { border-color: #667eea; background: #f8f0ff; transform: translateY(-3px); }
.wc-emoji { font-size: 2.5rem; }
.wc-name { font-size: 1.3rem; font-weight: 800; margin: 0.5rem 0; color: #1a1a2e; }
.wc-cal { font-size: 0.85rem; color: #aaa; }
.vs-badge {
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem; font-weight: 900; color: #ccc;
}

/* ── 이력 아이템 ── */
.hist-item {
    background: white;
    border-radius: 10px;
    padding: 0.7rem 1rem;
    margin: 0.35rem 0;
    border-left: 4px solid #667eea;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    font-size: 0.88rem;
}

/* ── 맛집 카드 ── */
.rest-card {
    background: white;
    border-radius: 14px;
    padding: 1rem 1.3rem;
    margin: 0.5rem 0;
    box-shadow: 0 4px 14px rgba(0,0,0,0.07);
    border-left: 5px solid #f5576c;
}

/* Streamlit 요소 숨김/조정 */
#MainMenu, footer, header { visibility: hidden; }
.stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}
.stButton > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    transition: all 0.15s !important;
}
div[data-testid="stHorizontalBlock"] { gap: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ── 데이터 ────────────────────────────────────────────────────
MENU_DATA = {
    "상황별": {
        "저녁": [
            {"name": "삼겹살", "cal": 700, "emoji": "🥓"},
            {"name": "치킨", "cal": 850, "emoji": "🍗"},
            {"name": "피자", "cal": 900, "emoji": "🍕"},
            {"name": "파스타", "cal": 650, "emoji": "🍝"},
            {"name": "스테이크", "cal": 800, "emoji": "🥩"},
            {"name": "초밥", "cal": 500, "emoji": "🍣"},
            {"name": "된장찌개", "cal": 350, "emoji": "🍲"},
        ],
        "배달": [
            {"name": "치킨", "cal": 850, "emoji": "🍗"},
            {"name": "피자", "cal": 900, "emoji": "🍕"},
            {"name": "짜장면", "cal": 650, "emoji": "🍜"},
            {"name": "짬뽕", "cal": 700, "emoji": "🍜"},
            {"name": "떡볶이", "cal": 500, "emoji": "🌶️"},
            {"name": "족발", "cal": 750, "emoji": "🐾"},
            {"name": "버거", "cal": 650, "emoji": "🍔"},
        ],
        "데이트": [
            {"name": "파스타", "cal": 650, "emoji": "🍝"},
            {"name": "스테이크", "cal": 800, "emoji": "🥩"},
            {"name": "초밥", "cal": 500, "emoji": "🍣"},
            {"name": "샤브샤브", "cal": 450, "emoji": "🍲"},
            {"name": "오마카세", "cal": 700, "emoji": "🍱"},
        ],
        "캠핑": [
            {"name": "삼겹살 구이", "cal": 700, "emoji": "🔥"},
            {"name": "라면", "cal": 500, "emoji": "🍜"},
            {"name": "핫도그", "cal": 400, "emoji": "🌭"},
            {"name": "불고기", "cal": 550, "emoji": "🥩"},
            {"name": "옥수수 구이", "cal": 180, "emoji": "🌽"},
        ],
        "파티": [
            {"name": "피자", "cal": 900, "emoji": "🍕"},
            {"name": "치킨", "cal": 850, "emoji": "🍗"},
            {"name": "파스타", "cal": 650, "emoji": "🍝"},
            {"name": "타코", "cal": 550, "emoji": "🌮"},
        ],
        "혼밥": [
            {"name": "편의점 도시락", "cal": 550, "emoji": "🏪"},
            {"name": "라면", "cal": 500, "emoji": "🍜"},
            {"name": "김밥", "cal": 400, "emoji": "🍙"},
            {"name": "순대국밥", "cal": 550, "emoji": "🍲"},
            {"name": "우동", "cal": 450, "emoji": "🫕"},
        ],
        "술안주": [
            {"name": "치킨", "cal": 850, "emoji": "🍗"},
            {"name": "족발", "cal": 750, "emoji": "🐾"},
            {"name": "마른안주", "cal": 300, "emoji": "🦑"},
            {"name": "두부김치", "cal": 350, "emoji": "🥬"},
            {"name": "골뱅이소면", "cal": 450, "emoji": "🍜"},
        ],
    },
    "선호도별": {
        "다이어트": [
            {"name": "샐러드", "cal": 150, "emoji": "🥗"},
            {"name": "닭가슴살 도시락", "cal": 300, "emoji": "🍱"},
            {"name": "두부 스테이크", "cal": 200, "emoji": "🥩"},
            {"name": "곤약 비빔밥", "cal": 250, "emoji": "🍚"},
            {"name": "그릭 요거트 볼", "cal": 200, "emoji": "🥣"},
        ],
        "매운맛": [
            {"name": "불닭볶음면", "cal": 530, "emoji": "🔥"},
            {"name": "마라탕", "cal": 700, "emoji": "🌶️"},
            {"name": "엽기 떡볶이", "cal": 600, "emoji": "🌶️"},
            {"name": "매운 김치찌개", "cal": 400, "emoji": "🍲"},
            {"name": "육개장", "cal": 350, "emoji": "🍲"},
        ],
        "가성비": [
            {"name": "편의점 도시락", "cal": 550, "emoji": "🏪"},
            {"name": "김밥", "cal": 400, "emoji": "🍙"},
            {"name": "순대국밥", "cal": 550, "emoji": "🍲"},
            {"name": "라면", "cal": 500, "emoji": "🍜"},
            {"name": "백반", "cal": 650, "emoji": "🍚"},
        ],
    },
    "음식 종류별": {
        "한식": [
            {"name": "비빔밥", "cal": 550, "emoji": "🍚"},
            {"name": "된장찌개", "cal": 350, "emoji": "🍲"},
            {"name": "삼겹살", "cal": 700, "emoji": "🥓"},
            {"name": "불고기", "cal": 550, "emoji": "🥩"},
            {"name": "냉면", "cal": 500, "emoji": "🍜"},
        ],
        "일식": [
            {"name": "초밥", "cal": 500, "emoji": "🍣"},
            {"name": "라멘", "cal": 700, "emoji": "🍜"},
            {"name": "우동", "cal": 450, "emoji": "🍜"},
            {"name": "돈카츠", "cal": 750, "emoji": "🥩"},
            {"name": "오야코동", "cal": 600, "emoji": "🍚"},
        ],
        "양식": [
            {"name": "파스타", "cal": 650, "emoji": "🍝"},
            {"name": "피자", "cal": 900, "emoji": "🍕"},
            {"name": "스테이크", "cal": 800, "emoji": "🥩"},
            {"name": "버거", "cal": 650, "emoji": "🍔"},
            {"name": "리조또", "cal": 600, "emoji": "🍚"},
        ],
        "중식": [
            {"name": "짜장면", "cal": 650, "emoji": "🍜"},
            {"name": "짬뽕", "cal": 700, "emoji": "🍜"},
            {"name": "탕수육", "cal": 800, "emoji": "🥩"},
            {"name": "마파두부", "cal": 400, "emoji": "🌶️"},
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

# ── 세션 상태 초기화 ──────────────────────────────────────────
def init_session():
    defaults = {
        "history": [],
        "excluded": set(),
        "custom_menus": [],
        "tournament_state": None,
        "scratch_revealed": False,
        "scratch_menu": None,
        "last_result": None,
        "active_cat_type": "상황별",
        "active_cat_sub": "저녁",
        "active_method": None,   # "random" | "worldcup" | "scratch" | "roulette"
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ── 헬퍼 ─────────────────────────────────────────────────────
def get_menus():
    ct = st.session_state.active_cat_type
    cs = st.session_state.active_cat_sub
    base = MENU_DATA.get(ct, {}).get(cs, [])
    all_m = base + st.session_state.custom_menus
    return [m for m in all_m if m["name"] not in st.session_state.excluded]

def add_history(menu, method):
    st.session_state.history.insert(0, {
        "menu": menu["name"], "emoji": menu.get("emoji", "🍽️"),
        "cal": menu.get("cal", 0), "method": method,
        "cat": st.session_state.active_cat_sub,
        "time": datetime.now().strftime("%m/%d %H:%M"),
    })
    if len(st.session_state.history) > 30:
        st.session_state.history = st.session_state.history[:30]
    st.session_state.last_result = {"menu": menu["name"], "emoji": menu.get("emoji","🍽️"), "cal": menu.get("cal",0), "method": method}

def result_card(menu, method=""):
    st.markdown(f"""
    <div class="result-card">
        <div class="result-emoji">{menu.get('emoji','🍽️')}</div>
        <div class="result-name">{menu['name']}</div>
        <div class="result-cal">🔥 약 {menu.get('cal',0)} kcal &nbsp;|&nbsp; {method}</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ① 제목 pill
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="title-pill-wrap"><div class="title-pill">🍽️ 오늘 뭐 먹지?</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ② 카테고리 탭 바 (핑크 바)
# ─────────────────────────────────────────────────────────────
ct = st.session_state.active_cat_type
cs = st.session_state.active_cat_sub
sub_list = list(MENU_DATA[ct].keys())

# 탭 버튼들을 Streamlit columns로 구현
sub_cols = st.columns(len(sub_list) + 1)
with sub_cols[0]:
    st.markdown(f"<div style='padding:0.4rem 0.5rem;font-size:0.8rem;font-weight:700;color:#d966a0;background:#ffe0f0;border-radius:8px;text-align:center'>{ct}</div>", unsafe_allow_html=True)
for i, sub in enumerate(sub_list):
    with sub_cols[i + 1]:
        is_active = sub == cs
        btn_style = "primary" if is_active else "secondary"
        if st.button(sub, key=f"cattab_{sub}", use_container_width=True, type=btn_style):
            st.session_state.active_cat_sub = sub
            st.session_state.active_method = None
            st.session_state.scratch_revealed = False
            st.session_state.scratch_menu = None
            st.session_state.tournament_state = None
            st.rerun()

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ③ 메인 레이아웃: 왼쪽 사이드 + 오른쪽 2×2 그리드
# ─────────────────────────────────────────────────────────────
side_col, main_col = st.columns([1, 5], gap="medium")

# ── 왼쪽: 분류 선택 패널 ──────────────────────────────────────
with side_col:
    st.markdown("""<div style='background:white;border-radius:14px;padding:1rem 0.8rem;
                box-shadow:0 2px 12px rgba(0,0,0,0.07);'>""", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.72rem;font-weight:700;color:#aaa;margin-bottom:0.6rem;letter-spacing:0.05em'>분류</div>", unsafe_allow_html=True)
    for cat_type_name in MENU_DATA.keys():
        is_sel = cat_type_name == st.session_state.active_cat_type
        style = "background:#ede9ff;color:#7c5cbf;font-weight:700;" if is_sel else "color:#555;"
        st.markdown(f"""
        <div style='{style}font-size:0.88rem;padding:0.45rem 0.6rem;border-radius:8px;
                    margin-bottom:0.25rem;cursor:pointer' id='side_{cat_type_name}'>
            {"▸ " if is_sel else ""}{cat_type_name}
        </div>
        """, unsafe_allow_html=True)
        if st.button(cat_type_name, key=f"side_{cat_type_name}", use_container_width=True):
            st.session_state.active_cat_type = cat_type_name
            st.session_state.active_cat_sub = list(MENU_DATA[cat_type_name].keys())[0]
            st.session_state.active_method = None
            st.session_state.scratch_revealed = False
            st.session_state.scratch_menu = None
            st.session_state.tournament_state = None
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ── 오른쪽: 2×2 메서드 그리드 or 결과 화면 ───────────────────
with main_col:
    menus = get_menus()
    method = st.session_state.active_method

    # ── 메서드 선택 화면 (2×2 그리드) ──
    if method is None:
        row1 = st.columns(2, gap="medium")
        row2 = st.columns(2, gap="medium")

        METHODS = [
            ("random",   "랜덤", "버튼 한 번에 즉시 추천", "🎲", row1[0]),
            ("worldcup", "월드컵", "1:1 대결로 최후의 1개 선택", "🏆", row1[1]),
            ("scratch",  "스크래치", "긁어서 메뉴 확인", "🃏", row2[0]),
            ("roulette", "룰렛", "돌아가는 룰렛으로 결정", "🎡", row2[1]),
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
                if st.button(f"{emoji} {label} 시작", key=f"method_{key}", use_container_width=True, type="primary"):
                    if len(menus) < 2:
                        st.error("메뉴가 2개 이상 필요합니다. 카테고리를 바꾸거나 메뉴를 추가해주세요.")
                    else:
                        st.session_state.active_method = key
                        st.session_state.scratch_revealed = False
                        st.session_state.scratch_menu = None
                        if key == "worldcup":
                            pool = random.sample(menus, min(8, len(menus)))
                            if len(pool) % 2 == 1:
                                pool = pool[:-1]
                            st.session_state.tournament_state = {
                                "round": pool,
                                "pair_idx": 0,
                                "winners": [],
                                "round_num": len(pool),
                            }
                        if key == "scratch":
                            st.session_state.scratch_menu = random.choice(menus)
                        st.rerun()

    # ── 결과 화면들 ──
    else:
        # 뒤로가기
        if st.button("← 돌아가기", key="back_btn"):
            st.session_state.active_method = None
            st.session_state.tournament_state = None
            st.session_state.scratch_revealed = False
            st.session_state.scratch_menu = None
            st.rerun()

        # ── 랜덤 ──
        if method == "random":
            st.markdown("### 🎲 랜덤 추천")
            if st.button("🎲 지금 바로 추천!", type="primary", use_container_width=True):
                picked = random.choice(menus)
                add_history(picked, "🎲 랜덤")
                st.session_state._random_result = picked
                st.rerun()
            if hasattr(st.session_state, "_random_result") and st.session_state._random_result:
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

        # ── 룰렛 ──
        elif method == "roulette":
            st.markdown("### 🎡 룰렛")
            if st.button("🎡 룰렛 돌리기!", type="primary", use_container_width=True):
                picked = random.choice(menus)
                add_history(picked, "🎡 룰렛")
                st.session_state._roulette_result = picked
                st.session_state._roulette_spin = True
                st.rerun()
            if hasattr(st.session_state, "_roulette_spin") and st.session_state._roulette_spin:
                r = st.session_state._roulette_result
                st.markdown(f'<div style="text-align:center;margin:1rem 0"><span class="spin-emoji">{r["emoji"]}</span></div>', unsafe_allow_html=True)
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

        # ── 스크래치 ──
        elif method == "scratch":
            st.markdown("### 🃏 스크래치 카드")
            if not st.session_state.scratch_revealed:
                st.markdown("""
                <div class="scratch-hidden">
                    <div class="scratch-coins">🪙🪙🪙</div>
                    <div class="scratch-label">아래 버튼을 눌러 메뉴를 확인하세요!</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
                if st.button("✨ 긁어서 확인!", type="primary", use_container_width=True):
                    if st.session_state.scratch_menu is None:
                        st.session_state.scratch_menu = random.choice(menus)
                    st.session_state.scratch_revealed = True
                    add_history(st.session_state.scratch_menu, "🃏 스크래치")
                    st.rerun()
            else:
                result_card(st.session_state.scratch_menu, "🃏 스크래치")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("🔄 다시 긁기", use_container_width=True):
                        st.session_state.scratch_menu = random.choice(menus)
                        st.session_state.scratch_revealed = False
                        st.rerun()
                with c2:
                    if st.button("📍 맛집 찾기", use_container_width=True):
                        st.session_state.active_method = "restaurant"
                        st.rerun()

        # ── 월드컵 ──
        elif method == "worldcup":
            ts = st.session_state.tournament_state
            if ts is None:
                st.error("토너먼트 초기화 오류. 돌아가기를 눌러주세요.")
            elif len(ts["round"]) == 1:
                # 우승자
                winner = ts["round"][0]
                st.markdown("### 🏆 최종 우승!")
                st.balloons()
                result_card(winner, "🏆 월드컵")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("🔄 다시 하기", use_container_width=True):
                        pool = random.sample(menus, min(8, len(menus)))
                        if len(pool) % 2 == 1:
                            pool = pool[:-1]
                        st.session_state.tournament_state = {
                            "round": pool, "pair_idx": 0,
                            "winners": [], "round_num": len(pool),
                        }
                        st.rerun()
                with c2:
                    if st.button("📍 맛집 찾기", use_container_width=True):
                        st.session_state.active_method = "restaurant"
                        st.rerun()
            else:
                pairs = [(ts["round"][i], ts["round"][i+1]) for i in range(0, len(ts["round"])-1, 2)]
                idx = ts["pair_idx"]

                if idx >= len(pairs):
                    # 라운드 마무리
                    ts["round"] = ts["winners"][:]
                    if len(ts["round"]) % 2 == 1 and len(ts["round"]) > 1:
                        ts["round"] = ts["round"][:-1]  # 홀수 처리
                    ts["winners"] = []
                    ts["pair_idx"] = 0
                    st.rerun()
                else:
                    a, b = pairs[idx]
                    remaining = len(ts["round"])
                    total_pairs = len(pairs)
                    st.markdown(f"### 🏆 {remaining}강 — {idx+1}/{total_pairs} 경기")
                    progress = idx / total_pairs
                    st.progress(progress)

                    col_a, col_vs, col_b = st.columns([5, 1, 5], gap="small")
                    with col_a:
                        st.markdown(f"""
                        <div class="wc-option">
                            <div class="wc-emoji">{a['emoji']}</div>
                            <div class="wc-name">{a['name']}</div>
                            <div class="wc-cal">🔥 {a['cal']} kcal</div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"✅ {a['name']}", key=f"wc_a_{idx}", use_container_width=True, type="primary"):
                            ts["winners"].append(a)
                            ts["pair_idx"] += 1
                            st.rerun()
                    with col_vs:
                        st.markdown('<div class="vs-badge" style="height:100%;min-height:120px">VS</div>', unsafe_allow_html=True)
                    with col_b:
                        st.markdown(f"""
                        <div class="wc-option">
                            <div class="wc-emoji">{b['emoji']}</div>
                            <div class="wc-name">{b['name']}</div>
                            <div class="wc-cal">🔥 {b['cal']} kcal</div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"✅ {b['name']}", key=f"wc_b_{idx}", use_container_width=True, type="primary"):
                            ts["winners"].append(b)
                            ts["pair_idx"] += 1
                            st.rerun()

        # ── 맛집 찾기 (결과에서 이동) ──
        elif method == "restaurant":
            st.markdown("### 📍 맛집 찾기")
            lr = st.session_state.last_result
            all_names = [m["name"] for m in menus]
            default_idx = all_names.index(lr["menu"]) if lr and lr["menu"] in all_names else 0
            search_menu = st.selectbox("🍜 메뉴", all_names, index=default_idx)
            district = st.selectbox("📍 지역", DISTRICTS)
            if st.button("🔍 맛집 검색", type="primary", use_container_width=True):
                if district in ("선택 안 함", "기타 지역"):
                    st.warning("지역을 선택해주세요. (현재는 샘플 데이터)")
                else:
                    rests = SAMPLE_RESTAURANTS.get(district, [])
                    if rests:
                        for r in rests:
                            stars = "⭐" * int(r["rating"])
                            st.markdown(f"""
                            <div class="rest-card">
                                <div style="font-size:1rem;font-weight:700">🍴 {r['name']}</div>
                                <div style="color:#888;font-size:0.85rem;margin-top:0.3rem">
                                    {stars} {r['rating']} · 리뷰 {r['reviews']}개 · 📍 {r['address']}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        st.caption("⚠️ 샘플 데이터입니다. Step 3에서 Kakao/Google Places API로 교체 예정.")
                    else:
                        st.warning("해당 지역 데이터가 없습니다.")

# ─────────────────────────────────────────────────────────────
# ④ 하단: 이력 + 메뉴관리 탭
# ─────────────────────────────────────────────────────────────
st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
st.markdown("<hr style='border:none;border-top:2px solid #e0e0e0;margin:0 0 1rem 0'>", unsafe_allow_html=True)

bot_tab1, bot_tab2 = st.tabs(["📋 추천 이력", "🔧 메뉴 관리"])

with bot_tab1:
    if st.session_state.history:
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("총 추천", f"{len(st.session_state.history)}회")
        with c2:
            methods_list = [h["method"] for h in st.session_state.history]
            st.metric("자주 쓴 방식", max(set(methods_list), key=methods_list.count))
        with c3:
            menus_list = [h["menu"] for h in st.session_state.history]
            st.metric("최다 추천 메뉴", max(set(menus_list), key=menus_list.count))
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        for h in st.session_state.history:
            st.markdown(f"""
            <div class="hist-item">
                <div>{h['emoji']} <b>{h['menu']}</b> &nbsp;<span style="color:#aaa">{h['time']} · {h['method']} · {h['cat']}</span></div>
                <div style="color:#667eea;font-weight:700">{h['cal']}kcal</div>
            </div>
            """, unsafe_allow_html=True)
        if st.button("🗑️ 이력 초기화"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("아직 추천 이력이 없어요. 위에서 메뉴를 추천받아 보세요!")

with bot_tab2:
    c_add, c_excl = st.columns(2)
    with c_add:
        st.markdown("**➕ 커스텀 메뉴 추가**")
        nm = st.text_input("메뉴 이름", placeholder="예: 순두부찌개", key="add_name")
        nc = st.number_input("칼로리", 0, 3000, 500, 50, key="add_cal")
        ne = st.text_input("이모지", "🍽️", max_chars=2, key="add_emoji")
        if st.button("추가", type="primary"):
            if nm.strip():
                st.session_state.custom_menus.append({"name": nm.strip(), "cal": nc, "emoji": ne})
                st.success(f"'{nm}' 추가!")
                st.rerun()
            else:
                st.error("이름을 입력하세요.")
        if st.session_state.custom_menus:
            st.markdown("**내 메뉴 목록**")
            for i, m in enumerate(st.session_state.custom_menus):
                ca, cb = st.columns([5, 1])
                with ca: st.write(f"{m['emoji']} {m['name']} ({m['cal']}kcal)")
                with cb:
                    if st.button("🗑️", key=f"del_{i}"):
                        st.session_state.custom_menus.pop(i)
                        st.rerun()
    with c_excl:
        st.markdown("**🚫 메뉴 제외 설정**")
        cs_now = st.session_state.active_cat_sub
        ct_now = st.session_state.active_cat_type
        src = MENU_DATA.get(ct_now, {}).get(cs_now, [])
        if src:
            for m in src:
                excluded = m["name"] in st.session_state.excluded
                chk = st.checkbox(f"{m['emoji']} {m['name']}", value=excluded, key=f"ex_{m['name']}")
                if chk:
                    st.session_state.excluded.add(m["name"])
                else:
                    st.session_state.excluded.discard(m["name"])
        else:
            st.caption("현재 카테고리의 메뉴가 없습니다.")
        if st.session_state.excluded:
            st.markdown(f"<div style='color:#f5576c;font-size:0.85rem'>제외된 메뉴: {', '.join(st.session_state.excluded)}</div>", unsafe_allow_html=True)
