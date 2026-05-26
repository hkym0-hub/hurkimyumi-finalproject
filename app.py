import streamlit as st
import random
import time
from datetime import datetime, date
from collections import Counter, defaultdict

st.set_page_config(page_title="오늘의 추천 메뉴", page_icon="🍽️", layout="wide", initial_sidebar_state="collapsed")

# ── 스타일 ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&display=swap');
html,body,[class*="css"]{font-family:'Noto Sans KR',sans-serif;}
.stApp{background:#f0f2f8;}
.result-card{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);border-radius:20px;padding:2.5rem;text-align:center;color:white;margin:1rem 0;box-shadow:0 10px 40px rgba(102,126,234,.4);}
.result-emoji{font-size:4rem;line-height:1;margin-bottom:.5rem;}
.result-name{font-size:2.4rem;font-weight:900;margin-bottom:.5rem;}
.result-cal{display:inline-block;background:rgba(255,255,255,.25);border-radius:999px;padding:.3rem 1.2rem;font-size:.95rem;font-weight:600;}
.method-card{background:#b8c4e0;border-radius:18px;min-height:150px;padding:1.4rem 1.2rem 1.2rem;margin-bottom:1rem;transition:transform .15s;}
.method-card:hover{transform:translateY(-4px);}
.fortune-card{background:linear-gradient(135deg,#f6d365,#fda085);border-radius:20px;padding:2rem;text-align:center;color:white;margin-bottom:1rem;}
</style>
""", unsafe_allow_html=True)

# ── 데이터 및 세션 초기화 ──────────────────────────────────────────
# [이전과 동일한 MENU_DATA, CATEGORY_EMOJI 사용]
MENU_DATA = {
    "저녁 메뉴": [{"name":"삼겹살","cal":700,"emoji":"🥓"},{"name":"치킨","cal":850,"emoji":"🍗"},{"name":"피자","cal":900,"emoji":"🍕"}],
    "배달 메뉴": [{"name":"짜장면","cal":650,"emoji":"🍜"},{"name":"마라탕","cal":700,"emoji":"🥢"}],
}
CATEGORIES = list(MENU_DATA.keys())

def init():
    defaults = {
        "history": [], "active_cat": "저녁 메뉴", "active_method": None,
        "result_menu": None, "today_log": [], "scratch_opened": False
    }
    for k, v in defaults.items():
        if k not in st.session_state: st.session_state[k] = v
init()

# ── 함수들 ─────────────────────────────────────────────────────
def reset_game():
    st.session_state.active_method = None
    st.session_state.result_menu = None
    st.session_state.scratch_opened = False
    st.rerun()

def add_history(menu, method):
    entry = {"menu": menu["name"], "emoji": menu.get("emoji","🍽️"), "cal": menu.get("cal",0), "method": method}
    st.session_state.history.insert(0, entry)
    st.session_state.today_log.append({**entry, "date": date.today().isoformat()})

# ── UI 렌더링 ──────────────────────────────────────────────────
st.markdown('<div class="title-pill-wrap"><div class="title-pill">🍽️ 오늘의 추천 메뉴</div></div>', unsafe_allow_html=True)

# 카테고리
cat_cols = st.columns(len(CATEGORIES))
for i, cat in enumerate(CATEGORIES):
    if cat_cols[i].button(cat, type="primary" if cat == st.session_state.active_cat else "secondary"):
        st.session_state.active_cat = cat
        reset_game()

# 메뉴 리스트
menus = MENU_DATA.get(st.session_state.active_cat, [])

# 게임 모드 선택
if st.session_state.active_method is None:
    m_cols = st.columns(4)
    if m_cols[0].button("🎲 랜덤"): st.session_state.active_method = "random"; st.rerun()
    if m_cols[1].button("🎡 룰렛"): st.session_state.active_method = "roulette"; st.rerun()
    if m_cols[2].button("🎁 스크래치"): st.session_state.active_method = "scratch"; st.rerun()
    if m_cols[3].button("🎲 주사위"): st.session_state.active_method = "dice"; st.rerun()

else:
    if st.button("⬅️ 돌아가기"): reset_game()

    # 1. 랜덤 모드
    if st.session_state.active_method == "random":
        if st.button("🎲 결과 보기"): st.session_state.result_menu = random.choice(menus)
    
    # 2. 룰렛 모드 (파이썬 애니메이션)
    elif st.session_state.active_method == "roulette":
        if st.button("🎡 룰렛 돌리기!"):
            with st.spinner('룰렛이 돌아가는 중...'):
                time.sleep(1.5)
                st.session_state.result_menu = random.choice(menus)
    
    # 3. 스크래치 (박스 열기)
    elif st.session_state.active_method == "scratch":
        if not st.session_state.scratch_opened:
            if st.button("🎁 상자 열기"):
                st.session_state.result_menu = random.choice(menus)
                st.session_state.scratch_opened = True
        else:
            if st.button("🔄 새 상자 열기"): st.session_state.scratch_opened = False; st.rerun()

    # 4. 주사위
    elif st.session_state.active_method == "dice":
        if st.button("🎲 주사위 굴리기!"):
            st.session_state.result_menu = random.choice(menus)
            st.session_state.dice_num = random.randint(1, 6)

    # ── 채택 로직 (공통) ──────────────────────────────────────────
    if st.session_state.result_menu:
        res = st.session_state.result_menu
        # 결과 화면
        st.markdown(f"""<div class="result-card">
            <div class="result-emoji">{res.get('emoji','🍽️')}</div>
            <div class="result-name">{res['name']}</div>
        </div>""", unsafe_allow_html=True)
        
        # 채택 버튼 (딱 하나만!)
        if st.button(f"✅ {res['name']} (으)로 결정!", type="primary", use_container_width=True):
            add_history(res, st.session_state.active_method)
            st.success("🎉 채택 완료!")
            reset_game()
