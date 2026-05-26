import streamlit as st
import random
import time
from datetime import datetime, date
from collections import Counter, defaultdict

# ── 설정 ──────────────────────────────────────────────────────
st.set_page_config(page_title="오늘의 추천 메뉴", page_icon="🍽️", layout="wide", initial_sidebar_state="collapsed")

# ── 데이터 (이전과 동일) ──────────────────────────────────────────
# [여기에 기존 MENU_DATA, CATEGORY_EMOJI, FORTUNES 코드를 그대로 두세요]
# (코드 길이가 너무 길어 중간 데이터 부분은 생략했습니다. 기존 파일의 해당 부분을 유지하세요.)

# ── 세션 초기화 ───────────────────────────────────────────────
def init():
    defaults = {
        "history": [], "excluded": set(), "custom_menus": [],
        "active_cat": "저녁 메뉴", "active_method": None,
        "result_menu": None, "today_log": [],
        "filter_cal_min": 0, "filter_cal_max": 1200,
        "filter_food_type": "전체", "filter_delivery": "전체", "filter_budget": "전체"
    }
    for k, v in defaults.items():
        if k not in st.session_state: st.session_state[k] = v
init()

# ── 주요 로직 ────────────────────────────────────────────────
def reset_method():
    st.session_state.active_method = None
    st.session_state.result_menu = None
    st.rerun()

def add_history(menu, method):
    entry = {"menu": menu["name"], "emoji": menu.get("emoji","🍽️"), "cal": menu.get("cal",0), "method": method}
    st.session_state.history.insert(0, entry)
    st.session_state.today_log.append({**entry, "date": date.today().isoformat()})

# ── UI 렌더링 ────────────────────────────────────────────────
st.markdown('<div class="title-pill-wrap"><div class="title-pill">🍽️ 오늘의 추천 메뉴</div></div>', unsafe_allow_html=True)

# 카테고리/필터 등... (기존 UI 로직 그대로 유지)

menus = [m for m in MENU_DATA.get(st.session_state.active_cat, []) if m["name"] not in st.session_state.excluded]

# 게임 선택 화면
if st.session_state.active_method is None:
    cols = st.columns(4)
    if cols[0].button("🎲 랜덤"): st.session_state.active_method = "random"; st.rerun()
    if cols[1].button("🎡 룰렛"): st.session_state.active_method = "roulette"; st.rerun()
    if cols[2].button("🎁 스크래치"): st.session_state.active_method = "scratch"; st.rerun()
    if cols[3].button("🎲 주사위"): st.session_state.active_method = "dice"; st.rerun()

else:
    if st.button("⬅️ 돌아가기"): reset_method()

    # --- 게임별 로직 ---
    # 1. 랜덤
    if st.session_state.active_method == "random":
        if st.button("🎲 결과 뽑기"): st.session_state.result_menu = random.choice(menus)
    
    # 2. 룰렛
    elif st.session_state.active_method == "roulette":
        if st.button("🎡 룰렛 돌리기!"):
            with st.spinner('룰렛 회전 중...'):
                time.sleep(1)
                st.session_state.result_menu = random.choice(menus)
    
    # 3. 스크래치 (박스 열기)
    elif st.session_state.active_method == "scratch":
        if st.button("🎁 비밀 상자 열기"):
            st.session_state.result_menu = random.choice(menus)

    # 4. 주사위
    elif st.session_state.active_method == "dice":
        if st.button("🎲 주사위 굴리기!"):
            st.session_state.result_menu = random.choice(menus)
            st.balloons()

    # --- 결과 출력 및 채택 (모든 게임 공통) ---
    if st.session_state.result_menu:
        res = st.session_state.result_menu
        st.markdown(f"""<div class="result-card">
            <div class="result-emoji">{res.get('emoji','🍽️')}</div>
            <div class="result-name">{res['name']}</div>
        </div>""", unsafe_allow_html=True)
        
        # 100% 확실하게 뜨는 채택 버튼
        if st.button(f"✅ {res['name']} (으)로 결정!", type="primary", use_container_width=True):
            add_history(res, st.session_state.active_method)
            st.success("🎉 채택 완료!")
            st.session_state.result_menu = None
            st.rerun()
