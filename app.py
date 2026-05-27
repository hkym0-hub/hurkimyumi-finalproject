import streamlit as st
import streamlit.components.v1 as components
import random
import time
import json
import os
from datetime import datetime, date
from collections import Counter, defaultdict

st.set_page_config(page_title="오늘의 추천 메뉴", page_icon="🍽️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&display=swap');
html,body,[class*="css"]{font-family:'Noto Sans KR',sans-serif;}
.stApp{background:#f0f2f8;}
.block-container{padding:1.5rem 2rem 2rem!important;max-width:1300px;}
.title-pill-wrap{display:flex;justify-content:center;margin-bottom:1.2rem;}
.title-pill{background:linear-gradient(135deg,#9b7fe8,#7c5cbf);color:white;font-size:1.35rem;font-weight:900;padding:0.6rem 3rem;border-radius:999px;letter-spacing:.05em;box-shadow:0 4px 20px rgba(124,92,191,.35);}
.method-card{background:#b8c4e0;border-radius:18px;min-height:150px;padding:1.4rem 1.2rem 1.2rem;transition:transform .15s,box-shadow .15s;display:flex;flex-direction:column;justify-content:space-between;position:relative;overflow:hidden;}
.method-card:hover{transform:translateY(-4px);box-shadow:0 12px 32px rgba(0,0,0,.15);}
.method-card-title{font-size:1.25rem;font-weight:900;color:#111;}
.method-card-desc{font-size:.78rem;color:#333;margin-top:.3rem;font-weight:600;}
.method-card-emoji{position:absolute;bottom:.8rem;right:1rem;font-size:2.5rem;opacity:.25;}
.result-card{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);border-radius:20px;padding:2.5rem;text-align:center;color:white;margin:1rem 0;box-shadow:0 10px 40px rgba(102,126,234,.4);}
.result-emoji{font-size:4rem;line-height:1;margin-bottom:.5rem;}
.result-name{font-size:2.4rem;font-weight:900;margin-bottom:.5rem;}
.result-cal{display:inline-block;background:rgba(255,255,255,.25);border-radius:999px;padding:.3rem 1.2rem;font-size:.95rem;font-weight:600;}
.wc-option{background:white;border:3px solid #ddd;border-radius:16px;padding:1.8rem 1.2rem;text-align:center;transition:all .18s;}
.wc-option:hover{border-color:#667eea;background:#f8f0ff;}
.wc-emoji{font-size:2.5rem;}.wc-name{font-size:1.3rem;font-weight:800;margin:.5rem 0;color:#1a1a2e;}.wc-cal{font-size:.85rem;color:#aaa;}
.hist-item{background:white;border-radius:10px;padding:.7rem 1rem;margin:.3rem 0;border-left:4px solid #667eea;display:flex;justify-content:space-between;align-items:center;box-shadow:0 2px 6px rgba(0,0,0,.05);font-size:.88rem;color:#111;}
.rank-card{background:white;border-radius:12px;padding:.8rem 1.1rem;margin:.3rem 0;display:flex;align-items:center;gap:.8rem;box-shadow:0 2px 8px rgba(0,0,0,.07);}
.cal-bar-wrap{background:#f0f2f8;border-radius:8px;height:12px;overflow:hidden;margin-top:.4rem;}
.cal-bar{background:linear-gradient(90deg,#667eea,#f5576c);height:12px;border-radius:8px;}
.info-card{background:white;border-radius:14px;padding:1.2rem;box-shadow:0 4px 14px rgba(0,0,0,.07);}
.fortune-card{background:linear-gradient(135deg,#f6d365,#fda085);border-radius:20px;padding:2rem;text-align:center;color:white;box-shadow:0 8px 28px rgba(253,160,133,.4);margin-bottom:1rem;}
#MainMenu,footer,header{visibility:hidden;}
.stButton>button{border-radius:12px!important;font-weight:700!important;font-family:'Noto Sans KR',sans-serif!important;}
</style>
""", unsafe_allow_html=True)

# (데이터 생략 - 기존 코드 동일)
CATEGORY_EMOJI = {"저녁 메뉴":"🌙","배달 메뉴":"🛵","데이트 메뉴":"💑","다이어트 메뉴":"🥗","가성비 메뉴":"💰","캠핑 메뉴":"⛺","매운 메뉴":"🌶️","파티 메뉴":"🎉","한식 메뉴":"🍚","일식 메뉴":"🍣","양식 메뉴":"🍝","중식 메뉴":"🥢","안주 메뉴":"🍺","혼자 먹는 메뉴":"🙋"}
MENU_DATA = {"저녁 메뉴": [{"name":"삼겹살","cal":700,"emoji":"🥓","food_type":"고기","delivery":False,"budget":"중"},{"name":"치킨","cal":850,"emoji":"🍗","food_type":"고기","delivery":True,"budget":"중"},{"name":"피자","cal":900,"emoji":"🍕","food_type":"기타","delivery":True,"budget":"중"},{"name":"파스타","cal":650,"emoji":"🍝","food_type":"면","delivery":True,"budget":"중"}], "배달 메뉴": [{"name":"치킨","cal":850,"emoji":"🍗","food_type":"고기","delivery":True,"budget":"중"},{"name":"피자","cal":900,"emoji":"🍕","food_type":"기타","delivery":True,"budget":"중"}], "데이트 메뉴": [{"name":"파스타","cal":650,"emoji":"🍝","food_type":"면","delivery":False,"budget":"중"},{"name":"스테이크","cal":800,"emoji":"🥩","food_type":"고기","delivery":False,"budget":"고"}], "다이어트 메뉴": [{"name":"샐러드","cal":280,"emoji":"🥗","food_type":"기타","delivery":True,"budget":"저"}], "가성비 메뉴": [{"name":"김밥","cal":400,"emoji":"🍙","food_type":"기타","delivery":True,"budget":"저"}], "캠핑 메뉴": [{"name":"삼겹살","cal":700,"emoji":"🔥","food_type":"고기","delivery":False,"budget":"저"}], "매운 메뉴": [{"name":"마라탕","cal":700,"emoji":"🌶️","food_type":"기타","delivery":True,"budget":"중"}], "파티 메뉴": [{"name":"피자","cal":900,"emoji":"🍕","food_type":"기타","delivery":True,"budget":"중"}], "한식 메뉴": [{"name":"비빔밥","cal":550,"emoji":"🍚","food_type":"밥","delivery":True,"budget":"저"}], "일식 메뉴": [{"name":"초밥","cal":500,"emoji":"🍣","food_type":"기타","delivery":True,"budget":"고"}], "양식 메뉴": [{"name":"파스타","cal":650,"emoji":"🍝","food_type":"면","delivery":True,"budget":"중"}], "중식 메뉴": [{"name":"짜장면","cal":650,"emoji":"🍜","food_type":"면","delivery":True,"budget":"저"}], "안주 메뉴": [{"name":"치킨","cal":850,"emoji":"🍗","food_type":"고기","delivery":True,"budget":"중"}], "혼자 먹는 메뉴": [{"name":"도시락","cal":550,"emoji":"🏪","food_type":"밥","delivery":False,"budget":"저"}]}
CATEGORIES = list(MENU_DATA.keys())
FORTUNES = [("새로운 걸 시도하기 좋은 날 ✨", "새 메뉴에 도전해봐요!"), ("편안한 게 최고인 날 🏠", "자주 먹던 메뉴가 최고예요.")]
SAVE_PATH = os.path.join(os.path.expanduser("~"), ".menu_app_data.json")

# (초기화 및 함수 정의 생략 - 기존 코드 동일)
def init():
    if "persistent_loaded" not in st.session_state: st.session_state.history = []; st.session_state.today_log = []; st.session_state.custom_menus = []; st.session_state.persistent_loaded = True
    defaults = {"excluded": set(), "active_cat": "저녁 메뉴", "active_method": None, "roulette_winner": None}
    for k, v in defaults.items():
        if k not in st.session_state: st.session_state[k] = v
init()

def add_history(menu, method):
    entry = {"menu": menu["name"], "emoji": menu.get("emoji", "🍽️"), "cal": menu.get("cal", 0), "method": method, "cat": st.session_state.active_cat, "time": datetime.now().strftime("%m/%d %H:%M")}
    st.session_state.history.insert(0, entry)
    st.session_state.last_result = entry

def adopt_button(menu, method, key_suffix=""):
    if st.button(f"✅ {menu['name']} (으)로 결정!", key=f"adopt_{key_suffix}", use_container_width=True, type="primary"):
        add_history(menu, method)
        st.success(f"🎉 **{menu['name']}** 이(가) 오늘의 메뉴로 기록됐어요!")
        st.session_state.active_method = None
        st.session_state.roulette_winner = None
        st.rerun()

def result_card(menu, method=""):
    st.markdown(f"""<div class="result-card">
        <div class="result-emoji">{menu.get('emoji', '🍽️')}</div>
        <div class="result-name">{menu['name']}</div>
        <div class="result-cal">🔥 약 {menu.get('cal', 0)} kcal &nbsp;·&nbsp; {method}</div>
    </div>""", unsafe_allow_html=True)

# ── 메인 UI
st.markdown('<div class="title-pill-wrap"><div class="title-pill">🍽️ 오늘의 추천 메뉴</div></div>', unsafe_allow_html=True)
menus = MENU_DATA.get(st.session_state.active_cat, [])

if st.session_state.active_method is None:
    if st.button("🎡 룰렛 시작하기", use_container_width=True, type="primary"):
        st.session_state.active_method = "roulette"
        st.rerun()
else:
    if st.button("← 돌아가기"):
        st.session_state.active_method = None
        st.session_state.roulette_winner = None
        st.rerun()
    
    # ── 룰렛
    st.markdown("### 🎡 룰렛 바퀴")
    names_js = json.dumps([{"name": m["name"], "emoji": m.get("emoji", "🍽️")} for m in menus])
    
    roulette_html = f"""
    <canvas id="roulette-canvas" width="300" height="300" style="display:block;margin:auto;"></canvas>
    <button id="spin-btn" onclick="spin()" style="display:block;margin:20px auto;padding:10px 20px;">🎡 돌리기</button>
    <script>
    const MENUS = {names_js};
    const canvas = document.getElementById('roulette-canvas');
    const ctx = canvas.getContext('2d');
    // ... (룰렛 그리기 로직은 기존과 동일하므로 생략 가능)
    function spin() {{
        const idx = Math.floor(Math.random() * MENUS.length);
        window.parent.postMessage({{'type': 'streamlit:setComponentValue', 'value': idx}}, '*');
    }}
    </script>
    """
    
    comp = components.html(roulette_html, height=400)
    
    # 수정된 결과 연동 부분
    if comp is not None:
        st.session_state.roulette_winner = menus[comp]

    if st.session_state.roulette_winner:
        result_card(st.session_state.roulette_winner, "🎡 룰렛 추천")
        adopt_button(st.session_state.roulette_winner, "🎡 룰렛", key_suffix="roulette_win")
