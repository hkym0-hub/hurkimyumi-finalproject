import streamlit as st
import random
import time
from datetime import datetime, date
from collections import Counter, defaultdict

st.set_page_config(page_title="오늘의 추천 메뉴", page_icon="🍽️", layout="wide", initial_sidebar_state="collapsed")

# (생략: 위쪽 CSS는 동일하므로 그대로 유지하세요)
# ... [이전 CSS 스타일 그대로] ...

# ── 데이터 ────────────────────────────────────────────────────
CATEGORY_EMOJI = {
    "저녁 메뉴":"🌙","배달 메뉴":"🛵","데이트 메뉴":"💑","다이어트 메뉴":"🥗",
    "가성비 메뉴":"💰","캠핑 메뉴":"⛺","매운 메뉴":"🌶️","파티 메뉴":"🎉",
    "한식 메뉴":"🍚","일식 메뉴":"🍣","양식 메뉴":"🍝","중식 메뉴":"🥢",
    "안주 메뉴":"🍺","혼자 먹는 메뉴":"🙋",
}

# (생략: MENU_DATA 및 FORTUNES는 동일하므로 그대로 유지하세요)
# ... [MENU_DATA, FORTUNES 데이터 그대로] ...

# ── 세션 초기화 ───────────────────────────────────────────────
def init():
    defaults = {
        "history": [], "excluded": set(), "custom_menus": [],
        "active_cat": "저녁 메뉴", "active_method": None,
        "tournament_state": None, "scratch_revealed": False,
        "scratch_menu": None, "last_result": None,
        "_random_result": None,
        "today_log": [],
        "fortune_today": None, "fortune_date": None,
        # 네이티브 게임 상태
        "roulette_done": False, "roulette_winner": None,
        "dice_winner": None, "dice_face": 1
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
init()

# ── 헬퍼 함수들 ───────────────────────────────────────────────
def get_all_menus():
    base = MENU_DATA.get(st.session_state.active_cat, [])
    return [m for m in base + st.session_state.custom_menus if m["name"] not in st.session_state.excluded]

def apply_filters(menus):
    result = menus
    # ... [필터 로직 동일] ...
    return result or menus

def get_menus():
    return apply_filters(get_all_menus())

def add_history(menu, method):
    kcal = menu.get("cal", 0)
    entry = {"menu": menu["name"], "emoji": menu.get("emoji","🍽️"), "cal": kcal,
             "method": method, "cat": st.session_state.active_cat,
             "time": datetime.now().strftime("%m/%d %H:%M")}
    st.session_state.history.insert(0, entry)
    st.session_state.last_result = entry
    today = date.today().isoformat()
    st.session_state.today_log.append({"menu": menu["name"], "emoji": menu.get("emoji","🍽️"), "cal": kcal, "date": today, "time": datetime.now().strftime("%H:%M")})

def adopt_button(menu, method, key_suffix=""):
    if st.button(f"✅ {menu['name']} (으)로 결정!", key=f"adopt_{key_suffix}", use_container_width=True, type="primary"):
        add_history(menu, method)
        st.success(f"🎉 **{menu['name']}** 이(가) 오늘의 메뉴로 기록됐어요!")
        reset_method()
        st.rerun()

def reset_method():
    st.session_state.active_method = None
    st.session_state.roulette_done = False
    st.session_state.roulette_winner = None
    st.session_state.dice_winner = None
    st.session_state._random_result = None

# ── 메인 게임 로직 ──────────────────────────────────────────
# [룰렛/주사위/스크래치 모드에서]
# st.button으로 결과를 생성하고, 그 결과가 st.session_state에 저장되면
# 바로 아래에 adopt_button을 띄우는 구조로 변경합니다.

# 예시: 주사위 버튼 
if method == "dice":
    if not st.session_state.dice_winner:
        if st.button("🎲 주사위 굴리기!", type="primary", use_container_width=True):
            st.session_state.dice_winner = random.choice(menus)
            st.session_state.dice_face = random.randint(1, 6)
            st.rerun()
    else:
        # 결과 표시 및 채택 버튼 (직관적!)
        winner = st.session_state.dice_winner
        st.write(f"나온 숫자: {st.session_state.dice_face}")
        result_card(winner, "🎲 주사위")
        adopt_button(winner, "🎲 주사위", key_suffix="dice_live")
