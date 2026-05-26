import streamlit as st
import random
import time
from datetime import datetime, date
from collections import Counter, defaultdict

st.set_page_config(page_title="오늘의 추천 메뉴", page_icon="🍽️", layout="wide", initial_sidebar_state="collapsed")

# ── 데이터 및 스타일은 이전과 동일하게 유지 ──
# (코드 간결화를 위해 스타일 및 데이터 정의 부분은 생략 없이 그대로 사용하세요)
# [기존 CSS와 MENU_DATA를 그대로 붙여넣으세요]
# (여기에 기존 코드의 CSS와 MENU_DATA, CATEGORY_EMOJI, FORTUNES 등을 넣으세요)

# ── 세션 초기화 ───────────────────────────────────────────────
def init():
    defaults = {
        "history": [], "excluded": set(), "custom_menus": [],
        "active_cat": "저녁 메뉴", "active_method": None,
        "result_menu": None, # 게임 결과 저장용
        "today_log": [], "fortune_today": None, "fortune_date": None,
        "filter_cal_min": 0, "filter_cal_max": 1200,
        "filter_food_type": "전체", "filter_delivery": "전체", "filter_budget": "전체",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
init()

# ── 공통 함수 ────────────────────────────────────────────────
def reset_method():
    st.session_state.active_method = None
    st.session_state.result_menu = None
    st.rerun()

def add_history(menu, method):
    entry = {"menu": menu["name"], "emoji": menu.get("emoji","🍽️"), "cal": menu.get("cal",0),
             "method": method, "cat": st.session_state.active_cat,
             "time": datetime.now().strftime("%m/%d %H:%M")}
    st.session_state.history.insert(0, entry)
    st.session_state.today_log.append({**entry, "date": date.today().isoformat()})

# ── 화면 렌더링 ──────────────────────────────────────────────
st.markdown('<div class="title-pill-wrap"><div class="title-pill">🍽️ 오늘의 추천 메뉴</div></div>', unsafe_allow_html=True)

# [카테고리 선택 및 필터 로직 동일]
# ... (카테고리/필터 코드 유지) ...

menus = apply_filters([m for m in MENU_DATA.get(st.session_state.active_cat, []) + st.session_state.custom_menus if m["name"] not in st.session_state.excluded])

# ── 게임 로직 (파이썬 네이티브 방식) ──────────────────────────
method = st.session_state.active_method

if method is None:
    # [메뉴 선택 버튼들...]
    # 각 버튼 클릭 시 st.session_state.active_method = '게임이름' 으로 설정
    pass 
else:
    if st.button("← 돌아가기"): reset_method()
    
    # 1. 랜덤 추천
    if method == "random":
        if st.button("🎲 결과 보기"):
            st.session_state.result_menu = random.choice(menus)
    
    # 2. 주사위 (Native)
    elif method == "dice":
        if st.button("🎲 주사위 굴리기!"):
            st.session_state.result_menu = random.choice(menus)
            st.balloons()
            
    # 3. 룰렛 (Native 애니메이션)
    elif method == "roulette":
        if st.button("🎡 룰렛 돌리기!"):
            with st.spinner('룰렛이 돌아가는 중...'):
                time.sleep(1.5)
                st.session_state.result_menu = random.choice(menus)
            st.rerun()

    # ── 결과 표시 및 채택 버튼 (어떤 게임이든 이 로직을 탐) ─────────
    if st.session_state.result_menu:
        res = st.session_state.result_menu
        st.markdown(f"""<div class="result-card">
            <div class="result-emoji">{res.get('emoji','🍽️')}</div>
            <div class="result-name">{res['name']}</div>
        </div>""", unsafe_allow_html=True)
        
        # 채택 버튼
        if st.button(f"✅ {res['name']} (으)로 결정!", type="primary", use_container_width=True):
            add_history(res, method)
            st.success(f"🎉 {res['name']} 채택 완료!")
            st.session_state.result_menu = None # 초기화
            st.rerun()
