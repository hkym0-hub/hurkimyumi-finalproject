import streamlit as st
import random
import requests
import json as _json
from datetime import datetime, date

st.set_page_config(
    page_title="오늘의 추천 메뉴",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.stApp { background: #f0f2f8; }
.block-container { padding: 1.5rem 2rem 2rem 2rem !important; max-width: 1300px; }

.title-pill-wrap { display:flex; justify-content:center; margin-bottom:1.2rem; }
.title-pill {
    background: linear-gradient(135deg, #9b7fe8, #7c5cbf);
    color: white; font-size: 1.35rem; font-weight: 900;
    padding: 0.6rem 3rem; border-radius: 999px;
    letter-spacing: 0.05em; box-shadow: 0 4px 20px rgba(124,92,191,0.35);
}
.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.15) !important;
    border: 2px solid rgba(255,255,255,0.4) !important;
    color: #111 !important;
}
.method-card {
    background: #b8c4e0; border-radius: 18px; min-height: 160px;
    padding: 1.4rem 1.2rem 1.2rem; cursor: pointer;
    transition: transform 0.15s, box-shadow 0.15s;
    display: flex; flex-direction: column; justify-content: space-between;
    position: relative; overflow: hidden;
}
.method-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.15); }
.method-card-title { font-size: 1.35rem; font-weight: 900; color: #111; }
.method-card-desc  { font-size: 0.78rem; color: #333; margin-top:0.3rem; font-weight:600; }
.method-card-emoji { position:absolute; bottom:0.8rem; right:1rem; font-size:2.5rem; opacity:0.25; }
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
.wc-option {
    background:white; border:3px solid #ddd; border-radius:16px;
    padding:1.8rem 1.2rem; text-align:center; transition:all 0.18s;
}
.wc-option:hover { border-color:#667eea; background:#f8f0ff; }
.wc-emoji { font-size:2.5rem; }
.wc-name  { font-size:1.3rem; font-weight:800; margin:0.5rem 0; color:#1a1a2e; }
.wc-cal   { font-size:0.85rem; color:#aaa; }
.hist-item {
    background:white; border-radius:10px; padding:0.7rem 1rem; margin:0.3rem 0;
    border-left:4px solid #667eea; display:flex; justify-content:space-between;
    align-items:center; box-shadow:0 2px 6px rgba(0,0,0,0.05); font-size:0.88rem; color:#111;
}
.rank-card {
    background:white; border-radius:12px; padding:0.8rem 1.1rem; margin:0.3rem 0;
    display:flex; align-items:center; gap:0.8rem;
    box-shadow:0 2px 8px rgba(0,0,0,0.07);
}
.rank-num { font-size:1.3rem; font-weight:900; color:#667eea; min-width:2rem; }
.cal-bar-wrap { background:#f0f2f8; border-radius:8px; height:12px; overflow:hidden; margin-top:0.4rem; }
.cal-bar { background:linear-gradient(90deg,#667eea,#f5576c); height:12px; border-radius:8px; }
.stMarkdown p, label, .stMetric, [data-testid="stMetricLabel"], [data-testid="stMetricValue"] { color:#111 !important; }
[data-testid="stMetricValue"] { color:#1a1a2e !important; }
.stTabs [data-baseweb="tab-panel"] { background:transparent; }
hr { border-color:#ddd !important; }
#MainMenu, footer, header { visibility:hidden; }
.stButton > button { border-radius:12px !important; font-weight:700 !important; font-family:'Noto Sans KR',sans-serif !important; }
.stTabs [data-baseweb="tab"] { border-radius:10px !important; font-weight:600 !important; font-family:'Noto Sans KR',sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# ── 데이터 ────────────────────────────────────────────────────
CATEGORY_EMOJI = {
    "저녁 메뉴":"🌙","배달 메뉴":"🛵","데이트 메뉴":"💑","다이어트 메뉴":"🥗",
    "가성비 메뉴":"💰","캠핑 메뉴":"⛺","매운 메뉴":"🌶️","파티 메뉴":"🎉",
    "한식 메뉴":"🍚","일식 메뉴":"🍣","양식 메뉴":"🍝","중식 메뉴":"🥢",
    "안주 메뉴":"🍺","혼자 먹는 메뉴":"🙋",
}

MENU_DATA = {
    "저녁 메뉴": [
        {"name":"삼겹살","cal":700,"emoji":"🥓"},{"name":"치킨","cal":850,"emoji":"🍗"},
        {"name":"피자","cal":900,"emoji":"🍕"},{"name":"파스타","cal":650,"emoji":"🍝"},
        {"name":"스테이크","cal":800,"emoji":"🥩"},{"name":"초밥","cal":500,"emoji":"🍣"},
        {"name":"된장찌개","cal":350,"emoji":"🍲"},{"name":"갈비탕","cal":600,"emoji":"🍖"},
        {"name":"불고기","cal":550,"emoji":"🔥"},{"name":"쭈꾸미볶음","cal":450,"emoji":"🐙"},
        {"name":"순두부찌개","cal":300,"emoji":"🫕"},{"name":"부대찌개","cal":650,"emoji":"🍲"},
        {"name":"곱창전골","cal":700,"emoji":"🫕"},{"name":"닭갈비","cal":580,"emoji":"🍗"},
    ],
    "배달 메뉴": [
        {"name":"치킨","cal":850,"emoji":"🍗"},{"name":"피자","cal":900,"emoji":"🍕"},
        {"name":"짜장면","cal":650,"emoji":"🍜"},{"name":"짬뽕","cal":700,"emoji":"🍜"},
        {"name":"떡볶이","cal":500,"emoji":"🌶️"},{"name":"족발","cal":750,"emoji":"🍖"},
        {"name":"버거","cal":650,"emoji":"🍔"},{"name":"마라탕","cal":700,"emoji":"🥢"},
        {"name":"초밥 세트","cal":520,"emoji":"🍣"},{"name":"국밥","cal":550,"emoji":"🍲"},
        {"name":"쌀국수","cal":480,"emoji":"🍜"},{"name":"보쌈","cal":680,"emoji":"🥬"},
        {"name":"감자탕","cal":620,"emoji":"🍲"},{"name":"샌드위치","cal":450,"emoji":"🥪"},
    ],
    "데이트 메뉴": [
        {"name":"파스타","cal":650,"emoji":"🍝"},{"name":"스테이크","cal":800,"emoji":"🥩"},
        {"name":"초밥 / 오마카세","cal":600,"emoji":"🍣"},{"name":"샤브샤브","cal":450,"emoji":"🍲"},
        {"name":"와인 파스타","cal":700,"emoji":"🍷"},{"name":"리조또","cal":620,"emoji":"🍚"},
        {"name":"프렌치 코스","cal":900,"emoji":"🥂"},{"name":"타파스","cal":500,"emoji":"🫒"},
        {"name":"훠궈","cal":750,"emoji":"🫕"},{"name":"브런치 카페","cal":550,"emoji":"☕"},
        {"name":"이탈리안 뷔페","cal":850,"emoji":"🍽️"},{"name":"스시 오마카세","cal":700,"emoji":"🍱"},
    ],
    "다이어트 메뉴": [
        {"name":"닭가슴살 샐러드","cal":280,"emoji":"🥗"},{"name":"두부 스테이크","cal":200,"emoji":"🥩"},
        {"name":"곤약 비빔밥","cal":250,"emoji":"🍚"},{"name":"그릭 요거트 볼","cal":180,"emoji":"🥣"},
        {"name":"채소 스프","cal":120,"emoji":"🥦"},{"name":"연어 포케","cal":380,"emoji":"🐟"},
        {"name":"닭가슴살 도시락","cal":300,"emoji":"🍱"},{"name":"오트밀 볼","cal":220,"emoji":"🌾"},
        {"name":"현미 잡곡밥 정식","cal":420,"emoji":"🍚"},{"name":"저칼로리 김밥","cal":320,"emoji":"🍙"},
        {"name":"채소 쌈밥","cal":350,"emoji":"🥬"},{"name":"토마토 달걀볶음","cal":200,"emoji":"🍳"},
        {"name":"닭가슴살 볶음밥","cal":380,"emoji":"🍳"},
    ],
    "가성비 메뉴": [
        {"name":"김밥","cal":400,"emoji":"🍙"},{"name":"순대국밥","cal":550,"emoji":"🍲"},
        {"name":"라면","cal":500,"emoji":"🍜"},{"name":"백반","cal":650,"emoji":"🍚"},
        {"name":"편의점 도시락","cal":550,"emoji":"🏪"},{"name":"분식 세트","cal":600,"emoji":"🌶️"},
        {"name":"컵라면 + 삼각김밥","cal":450,"emoji":"🍙"},{"name":"뼈다귀해장국","cal":500,"emoji":"🍲"},
        {"name":"돈까스 정식","cal":700,"emoji":"🥩"},{"name":"제육볶음 백반","cal":650,"emoji":"🍳"},
        {"name":"칼국수","cal":520,"emoji":"🍜"},{"name":"콩나물국밥","cal":400,"emoji":"🍲"},
        {"name":"떡볶이 + 순대","cal":580,"emoji":"🌶️"},
    ],
    "캠핑 메뉴": [
        {"name":"삼겹살 구이","cal":700,"emoji":"🔥"},{"name":"라면","cal":500,"emoji":"🍜"},
        {"name":"핫도그","cal":380,"emoji":"🌭"},{"name":"불고기","cal":550,"emoji":"🥩"},
        {"name":"옥수수 구이","cal":180,"emoji":"🌽"},{"name":"감자 구이","cal":200,"emoji":"🥔"},
        {"name":"부대찌개","cal":650,"emoji":"🍲"},{"name":"닭꼬치","cal":350,"emoji":"🍢"},
        {"name":"소시지 구이","cal":400,"emoji":"🌭"},{"name":"묵은지 삼겹","cal":720,"emoji":"🥓"},
        {"name":"즉석 떡볶이","cal":480,"emoji":"🌶️"},{"name":"어묵탕","cal":300,"emoji":"🍢"},
        {"name":"스팸 구이","cal":450,"emoji":"🥫"},
    ],
    "매운 메뉴": [
        {"name":"불닭볶음면","cal":530,"emoji":"🔥"},{"name":"마라탕","cal":700,"emoji":"🌶️"},
        {"name":"엽기 떡볶이","cal":600,"emoji":"🌶️"},{"name":"매운 김치찌개","cal":400,"emoji":"🍲"},
        {"name":"육개장","cal":350,"emoji":"🍲"},{"name":"마라샹궈","cal":800,"emoji":"🥢"},
        {"name":"불닭 피자","cal":950,"emoji":"🍕"},{"name":"매운 갈비찜","cal":750,"emoji":"🍖"},
        {"name":"낙지볶음","cal":380,"emoji":"🐙"},{"name":"쭈꾸미볶음","cal":420,"emoji":"🦑"},
        {"name":"매운 해물탕","cal":500,"emoji":"🦀"},{"name":"불족발","cal":780,"emoji":"🔥"},
        {"name":"청양 닭볶음탕","cal":600,"emoji":"🍗"},
    ],
    "파티 메뉴": [
        {"name":"피자","cal":900,"emoji":"🍕"},{"name":"치킨","cal":850,"emoji":"🍗"},
        {"name":"파스타 플래터","cal":700,"emoji":"🍝"},{"name":"타코","cal":550,"emoji":"🌮"},
        {"name":"샌드위치 플래터","cal":600,"emoji":"🥪"},{"name":"뷔페","cal":900,"emoji":"🍽️"},
        {"name":"초밥 세트","cal":560,"emoji":"🍣"},{"name":"바비큐 플래터","cal":850,"emoji":"🔥"},
        {"name":"케이터링 도시락","cal":700,"emoji":"🍱"},{"name":"나초 + 딥","cal":500,"emoji":"🫔"},
        {"name":"핑거푸드 세트","cal":450,"emoji":"🍢"},{"name":"떡 케이크","cal":400,"emoji":"🎂"},
    ],
    "한식 메뉴": [
        {"name":"비빔밥","cal":550,"emoji":"🍚"},{"name":"된장찌개","cal":350,"emoji":"🍲"},
        {"name":"삼겹살","cal":700,"emoji":"🥓"},{"name":"불고기","cal":550,"emoji":"🥩"},
        {"name":"냉면","cal":500,"emoji":"🍜"},{"name":"갈비탕","cal":600,"emoji":"🍖"},
        {"name":"삼계탕","cal":580,"emoji":"🐔"},{"name":"순대국밥","cal":550,"emoji":"🍲"},
        {"name":"해물파전","cal":480,"emoji":"🥞"},{"name":"잡채","cal":420,"emoji":"🍜"},
        {"name":"감자탕","cal":620,"emoji":"🍲"},{"name":"보쌈","cal":680,"emoji":"🥬"},
        {"name":"닭갈비","cal":580,"emoji":"🍗"},{"name":"낙지볶음","cal":380,"emoji":"🐙"},
        {"name":"떡국","cal":450,"emoji":"🍲"},
    ],
    "일식 메뉴": [
        {"name":"초밥","cal":500,"emoji":"🍣"},{"name":"라멘","cal":700,"emoji":"🍜"},
        {"name":"우동","cal":450,"emoji":"🍜"},{"name":"돈카츠","cal":750,"emoji":"🥩"},
        {"name":"오야코동","cal":600,"emoji":"🍚"},{"name":"타코야키","cal":380,"emoji":"🐙"},
        {"name":"규동","cal":620,"emoji":"🍚"},{"name":"나가사키 짬뽕","cal":680,"emoji":"🍜"},
        {"name":"오마카세","cal":700,"emoji":"🍱"},{"name":"야키토리","cal":400,"emoji":"🍢"},
        {"name":"카레라이스","cal":650,"emoji":"🍛"},{"name":"소바","cal":400,"emoji":"🍜"},
        {"name":"이자카야 세트","cal":750,"emoji":"🍶"},
    ],
    "양식 메뉴": [
        {"name":"파스타","cal":650,"emoji":"🍝"},{"name":"피자","cal":900,"emoji":"🍕"},
        {"name":"스테이크","cal":800,"emoji":"🥩"},{"name":"버거","cal":650,"emoji":"🍔"},
        {"name":"리조또","cal":620,"emoji":"🍚"},{"name":"샐러드","cal":250,"emoji":"🥗"},
        {"name":"그라탱","cal":700,"emoji":"🧀"},{"name":"크림 수프","cal":350,"emoji":"🍵"},
        {"name":"연어 스테이크","cal":550,"emoji":"🐟"},{"name":"브런치 플레이트","cal":600,"emoji":"🥞"},
        {"name":"함박스테이크","cal":680,"emoji":"🥩"},{"name":"치킨 알프레도","cal":720,"emoji":"🍝"},
        {"name":"클램 차우더","cal":380,"emoji":"🍵"},
    ],
    "중식 메뉴": [
        {"name":"짜장면","cal":650,"emoji":"🍜"},{"name":"짬뽕","cal":700,"emoji":"🍜"},
        {"name":"탕수육","cal":800,"emoji":"🥩"},{"name":"마파두부","cal":400,"emoji":"🌶️"},
        {"name":"딤섬","cal":500,"emoji":"🥟"},{"name":"마라탕","cal":700,"emoji":"🥢"},
        {"name":"마라샹궈","cal":800,"emoji":"🌶️"},{"name":"훠궈","cal":750,"emoji":"🫕"},
        {"name":"꿔바로우","cal":820,"emoji":"🥩"},{"name":"양꼬치","cal":600,"emoji":"🍢"},
        {"name":"깐풍기","cal":780,"emoji":"🍗"},{"name":"유린기","cal":700,"emoji":"🍗"},
        {"name":"동파육","cal":850,"emoji":"🥩"},
    ],
    "안주 메뉴": [
        {"name":"치킨","cal":850,"emoji":"🍗"},{"name":"족발","cal":750,"emoji":"🍖"},
        {"name":"마른안주 세트","cal":300,"emoji":"🦑"},{"name":"두부김치","cal":350,"emoji":"🥬"},
        {"name":"골뱅이소면","cal":450,"emoji":"🐌"},{"name":"감자전","cal":380,"emoji":"🥞"},
        {"name":"해물파전","cal":480,"emoji":"🥞"},{"name":"닭발","cal":420,"emoji":"🍗"},
        {"name":"삼겹살","cal":700,"emoji":"🥓"},{"name":"소시지 야채볶음","cal":500,"emoji":"🌭"},
        {"name":"계란말이","cal":280,"emoji":"🥚"},{"name":"오돌뼈","cal":460,"emoji":"🦴"},
        {"name":"곱창볶음","cal":650,"emoji":"🫕"},{"name":"라볶이","cal":550,"emoji":"🌶️"},
    ],
    "혼자 먹는 메뉴": [
        {"name":"편의점 도시락","cal":550,"emoji":"🏪"},{"name":"라면","cal":500,"emoji":"🍜"},
        {"name":"김밥 한 줄","cal":400,"emoji":"🍙"},{"name":"우동","cal":450,"emoji":"🫕"},
        {"name":"덮밥","cal":600,"emoji":"🍚"},{"name":"국밥","cal":550,"emoji":"🍲"},
        {"name":"냉면","cal":500,"emoji":"🍜"},{"name":"돈까스 정식","cal":700,"emoji":"🥩"},
        {"name":"1인 샤브샤브","cal":480,"emoji":"🍲"},{"name":"제육 덮밥","cal":620,"emoji":"🍳"},
        {"name":"삼각김밥 세트","cal":420,"emoji":"🍙"},{"name":"소고기 국밥","cal":580,"emoji":"🍲"},
        {"name":"짬뽕 1인분","cal":680,"emoji":"🍜"},{"name":"혼밥 정식","cal":650,"emoji":"🍱"},
    ],
}

CATEGORIES = list(MENU_DATA.keys())

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
        "cal_cache":        {},
        # 대결 모드
        "battle_a":         "",
        "battle_b":         "",
        "battle_result":    None,
        # 칼로리 트래커
        "today_log":        [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# ── 칼로리 API ────────────────────────────────────────────────
def fetch_calorie(menu_name: str):
    cache = st.session_state.cal_cache
    if menu_name in cache:
        return cache[menu_name]
    KR_KEY   = st.secrets.get("KR_FOOD_API_KEY", "")
    USDA_KEY = st.secrets.get("USDA_API_KEY", "")
    if KR_KEY:
        try:
            url = "https://api.data.go.kr/openapi/tn_pubr_public_nutri_food_info_api"
            r = requests.get(url, params={"serviceKey":KR_KEY,"pageNo":"1","numOfRows":"5","type":"json","foodNm":menu_name}, timeout=5)
            items = r.json().get("response",{}).get("body",{}).get("items",[]) or []
            for item in items:
                raw = item.get("enerc") or item.get("calorie") or item.get("energy")
                if raw:
                    kcal = int(float(str(raw).replace(",","")))
                    cache[menu_name] = kcal; return kcal
        except: pass
    if USDA_KEY:
        KR_TO_EN = {"삼겹살":"pork belly","치킨":"fried chicken","피자":"pizza","파스타":"pasta","스테이크":"steak","초밥":"sushi","된장찌개":"doenjang jjigae","갈비탕":"galbitang","불고기":"bulgogi","짜장면":"jajangmyeon","짬뽕":"jjamppong","떡볶이":"tteokbokki","라면":"ramen","김밥":"kimbap","비빔밥":"bibimbap","삼계탕":"samgyetang","냉면":"naengmyeon","족발":"jokbal","순대국밥":"sundae soup","칼국수":"kalguksu","우동":"udon","돈카츠":"tonkatsu","마라탕":"malatang","버거":"burger","샐러드":"salad","리조또":"risotto"}
        try:
            q = KR_TO_EN.get(menu_name, menu_name)
            r = requests.get("https://api.nal.usda.gov/fdc/v1/foods/search", params={"api_key":USDA_KEY,"query":q,"pageSize":3,"dataType":"Survey (FNDDS)"}, timeout=5)
            for food in r.json().get("foods",[]):
                for n in food.get("foodNutrients",[]):
                    if n.get("nutrientId")==1008 or n.get("nutrientName","").lower().startswith("energy"):
                        val = n.get("value") or n.get("amount")
                        if val:
                            kcal = int(float(val)); cache[menu_name]=kcal; return kcal
        except: pass
    return None

def get_cal(menu):
    fetched = fetch_calorie(menu["name"])
    return fetched if fetched is not None else menu.get("cal", 0)

# ── 헬퍼 ─────────────────────────────────────────────────────
def get_menus():
    base = MENU_DATA.get(st.session_state.active_cat, [])
    return [m for m in base + st.session_state.custom_menus if m["name"] not in st.session_state.excluded]

def add_history(menu, method):
    kcal = get_cal(menu)
    entry = {"menu":menu["name"],"emoji":menu.get("emoji","🍽️"),"cal":kcal,
             "method":method,"cat":st.session_state.active_cat,"time":datetime.now().strftime("%m/%d %H:%M")}
    st.session_state.history.insert(0, entry)
    if len(st.session_state.history) > 50:
        st.session_state.history = st.session_state.history[:50]
    st.session_state.last_result = entry
    # 칼로리 트래커 오늘 로그에도 추가
    today = date.today().isoformat()
    st.session_state.today_log.append({"menu":menu["name"],"emoji":menu.get("emoji","🍽️"),"cal":kcal,"date":today,"time":datetime.now().strftime("%H:%M")})

def result_card(menu, method=""):
    kcal = get_cal(menu)
    st.markdown(f"""
    <div class="result-card">
        <div class="result-emoji">{menu.get('emoji','🍽️')}</div>
        <div class="result-name">{menu['name']}</div>
        <div class="result-cal">🔥 약 {kcal} kcal &nbsp;·&nbsp; {method}</div>
    </div>
    """, unsafe_allow_html=True)

def reset_method():
    st.session_state.active_method    = None
    st.session_state.tournament_state = None
    st.session_state.scratch_revealed = False
    st.session_state.scratch_menu     = None
    st.session_state._random_result   = None
    st.session_state.battle_result    = None

# ─────────────────────────────────────────────────────────────
# ① 제목
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="title-pill-wrap"><div class="title-pill">🍽️ 오늘의 추천 메뉴</div></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ② 카테고리 탭 바
# ─────────────────────────────────────────────────────────────
st.markdown('<div style="background:#d966a0;border-radius:14px;padding:0.55rem 0.8rem;margin-bottom:1rem;"><span style="color:rgba(255,255,255,0.7);font-size:0.78rem;font-weight:700">카테고리</span></div>', unsafe_allow_html=True)

row_a = st.columns(7); row_b = st.columns(7)
for i, cat in enumerate(CATEGORIES):
    emoji = CATEGORY_EMOJI.get(cat, "🍽️")
    short = cat.replace(" 메뉴", "")
    col = (row_a + row_b)[i]
    with col:
        if st.button(f"{emoji} {short}", key=f"cat_{cat}", use_container_width=True,
                     type="primary" if cat == st.session_state.active_cat else "secondary"):
            st.session_state.active_cat = cat; reset_method(); st.rerun()

st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ③ 메인
# ─────────────────────────────────────────────────────────────
menus  = get_menus()
method = st.session_state.active_method
cur_emoji = CATEGORY_EMOJI.get(st.session_state.active_cat, "🍽️")

st.markdown(f"""<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:1rem;">
    <span style="font-size:1.6rem">{cur_emoji}</span>
    <span style="font-size:1.25rem;font-weight:900;color:#1a1a2e">{st.session_state.active_cat}</span>
    <span style="font-size:0.85rem;color:#aaa;margin-left:0.3rem">({len(menus)}개 메뉴)</span>
</div>""", unsafe_allow_html=True)

if len(menus) < 2:
    st.warning("⚠️ 메뉴가 2개 이상 필요합니다.")
elif method is None:
    # ── 3×3 메서드 그리드 ──
    METHODS = [
        ("random",   "랜덤",        "버튼 한 번에 즉시 추천",           "🎲"),
        ("roulette", "룰렛",        "모든 메뉴가 담긴 룰렛 바퀴",       "🎡"),
        ("scratch",  "스크래치",    "마우스로 긁어서 확인",             "🃏"),
        ("worldcup", "월드컵",      "1:1 대결로 최후의 1개",            "🏆"),
        ("dice",     "주사위",      "주사위 굴려서 결정",               "🎲"),
        ("tarot",    "카드 뽑기",   "타로카드 스타일 3장 중 선택",      "🃏"),
        ("smart",    "스마트 추천", "최근 안 먹은 메뉴 위주 추천",      "🧠"),
        ("battle",   "대결 모드",   "두 사람 의견 충돌, 룰렛으로 결정", "⚔️"),
    ]
    rows = [st.columns(4, gap="medium") for _ in range(2)]
    for idx, (key, label, desc, emoji) in enumerate(METHODS):
        col = rows[idx // 4][idx % 4]
        with col:
            st.markdown(f"""<div class="method-card">
                <div><div class="method-card-title">{label}</div>
                <div class="method-card-desc">{desc}</div></div>
                <div class="method-card-emoji">{emoji}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"{emoji} {label} 시작", key=f"m_{key}", use_container_width=True, type="primary"):
                st.session_state.active_method = key
                if key == "worldcup":
                    pool = random.sample(menus, min(8, len(menus)))
                    if len(pool) % 2 == 1: pool = pool[:-1]
                    st.session_state.tournament_state = {"round": pool, "pair_idx": 0, "winners": []}
                if key == "scratch":
                    st.session_state.scratch_menu = random.choice(menus)
                    st.session_state.scratch_revealed = False
                if key == "tarot":
                    st.session_state.tarot_cards = random.sample(menus, min(3, len(menus)))
                    st.session_state.tarot_chosen = None
                st.rerun()
else:
    if st.button("← 돌아가기", key="back"):
        reset_method(); st.rerun()

    # ══════════════════════════════════════════════════════
    # 랜덤
    # ══════════════════════════════════════════════════════
    if method == "random":
        st.markdown("### 🎲 랜덤 추천")
        if st.button("🎲 지금 바로 추천!", type="primary", use_container_width=True):
            picked = random.choice(menus)
            add_history(picked, "🎲 랜덤")
            st.session_state._random_result = picked
            st.rerun()
        if st.session_state._random_result:
            result_card(st.session_state._random_result, "🎲 랜덤")
            if st.button("🔄 다시 추천", use_container_width=True):
                picked = random.choice(menus)
                add_history(picked, "🎲 랜덤")
                st.session_state._random_result = picked
                st.rerun()

    # ══════════════════════════════════════════════════════
    # 룰렛
    # ══════════════════════════════════════════════════════
    elif method == "roulette":
        st.markdown("### 🎡 룰렛")
        menu_list_json = _json.dumps(
            [{"name":m["name"],"emoji":m.get("emoji","🍽️"),"cal":m.get("cal",0)} for m in menus],
            ensure_ascii=False)
        roulette_html = f"""
<style>
  #roulette-wrap {{ display:flex;flex-direction:column;align-items:center;gap:1.2rem;font-family:'Noto Sans KR',sans-serif;padding:0.5rem 0 1rem; }}
  #wheel-container {{ position:relative;width:360px;height:360px; }}
  #wheel-canvas {{ border-radius:50%;box-shadow:0 8px 32px rgba(0,0,0,0.2);display:block; }}
  #pointer {{ position:absolute;top:-16px;left:50%;transform:translateX(-50%);width:0;height:0;border-left:13px solid transparent;border-right:13px solid transparent;border-top:32px solid #e53935;filter:drop-shadow(0 2px 4px rgba(0,0,0,0.3));z-index:10; }}
  #spin-btn {{ background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:999px;padding:0.75rem 3rem;font-size:1.05rem;font-weight:700;cursor:pointer;box-shadow:0 4px 18px rgba(102,126,234,0.4);transition:transform 0.1s;font-family:'Noto Sans KR',sans-serif; }}
  #spin-btn:hover {{ transform:translateY(-2px); }} #spin-btn:disabled {{ opacity:0.5;cursor:not-allowed;transform:none; }}
  #result-box {{ display:none;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);border-radius:20px;padding:1.6rem 3rem;text-align:center;color:white;box-shadow:0 10px 40px rgba(102,126,234,0.4);animation:popIn 0.4s cubic-bezier(0.34,1.56,0.64,1);min-width:280px; }}
  @keyframes popIn {{ from{{transform:scale(0.7);opacity:0}} to{{transform:scale(1);opacity:1}} }}
  #result-emoji {{ font-size:3rem;line-height:1;margin-bottom:0.35rem; }}
  #result-name  {{ font-size:1.9rem;font-weight:900;margin-bottom:0.35rem; }}
  #result-cal   {{ display:inline-block;background:rgba(255,255,255,0.25);border-radius:999px;padding:0.2rem 1rem;font-size:0.88rem;font-weight:600; }}
</style>
<div id="roulette-wrap">
  <div id="wheel-container"><div id="pointer"></div><canvas id="wheel-canvas" width="360" height="360"></canvas></div>
  <button id="spin-btn" onclick="spinWheel()">🎡 룰렛 돌리기!</button>
  <div id="result-box"><div id="result-emoji"></div><div id="result-name"></div><div id="result-cal"></div></div>
</div>
<script>
(function(){{
  const MENUS={menu_list_json};
  const canvas=document.getElementById('wheel-canvas'),ctx=canvas.getContext('2d');
  const W=canvas.width,CX=W/2,CY=W/2,R=W/2-4,N=MENUS.length,arc=(2*Math.PI)/N;
  const COLORS=['#667eea','#f5576c','#4facfe','#43e97b','#fa709a','#fee140','#a18cd1','#fda085','#84fab0','#f6d365','#89f7fe','#fccb90','#d4fc79','#96fbc4','#f093fb'];
  let currentAngle=-Math.PI/2,spinning=false;
  function drawWheel(angle){{
    ctx.clearRect(0,0,W,W);
    for(let i=0;i<N;i++){{
      const start=angle+i*arc,end=start+arc;
      ctx.beginPath();ctx.moveTo(CX,CY);ctx.arc(CX,CY,R,start,end);ctx.closePath();
      ctx.fillStyle=COLORS[i%COLORS.length];ctx.fill();
      ctx.strokeStyle='rgba(255,255,255,0.7)';ctx.lineWidth=1.5;ctx.stroke();
      ctx.save();ctx.translate(CX,CY);ctx.rotate(start+arc/2);
      const isSmall=N>10,emojiSize=isSmall?13:17,nameSize=isSmall?10:12,maxLen=isSmall?5:6,textR=R-12;
      ctx.font=emojiSize+'px serif';ctx.textAlign='right';ctx.fillStyle='white';
      ctx.fillText(MENUS[i].emoji,textR-(isSmall?48:40),5);
      ctx.font='bold '+nameSize+'px "Noto Sans KR",sans-serif';
      let name=MENUS[i].name;if(name.length>maxLen)name=name.slice(0,maxLen-1)+'…';
      ctx.fillText(name,textR,5);ctx.restore();
    }}
    ctx.beginPath();ctx.arc(CX,CY,24,0,2*Math.PI);ctx.fillStyle='white';ctx.fill();
    ctx.strokeStyle='#ccc';ctx.lineWidth=2;ctx.stroke();
    ctx.font='bold 13px sans-serif';ctx.textAlign='center';ctx.fillStyle='#888';ctx.fillText('GO',CX,CY+5);
  }}
  drawWheel(currentAngle);
  window.spinWheel=function(){{
    if(spinning)return;spinning=true;
    document.getElementById('spin-btn').disabled=true;
    document.getElementById('result-box').style.display='none';
    const rounds=5+Math.random()*3,extraAngle=Math.random()*2*Math.PI;
    const totalAngle=rounds*2*Math.PI+extraAngle,duration=4200;
    const startAngle=currentAngle,startTime=performance.now();
    function easeOut(t){{return 1-Math.pow(1-t,4);}}
    function animate(now){{
      const elapsed=now-startTime,t=Math.min(elapsed/duration,1);
      currentAngle=startAngle+totalAngle*easeOut(t);drawWheel(currentAngle);
      if(t<1){{requestAnimationFrame(animate);}}
      else{{
        const ptr=((-Math.PI/2-currentAngle)%(2*Math.PI)+2*Math.PI)%(2*Math.PI);
        const idx=Math.floor(ptr/arc)%N,winner=MENUS[idx];
        const box=document.getElementById('result-box');
        document.getElementById('result-emoji').textContent=winner.emoji;
        document.getElementById('result-name').textContent=winner.name;
        document.getElementById('result-cal').textContent='🔥 약 '+winner.cal+' kcal · 🎡 룰렛';
        box.style.display='block';spinning=false;
        document.getElementById('spin-btn').disabled=false;
        document.getElementById('spin-btn').textContent='🔄 다시 돌리기!';
      }}
    }}
    requestAnimationFrame(animate);
  }};
}})();
</script>"""
        st.components.v1.html(roulette_html, height=680, scrolling=False)

    # ══════════════════════════════════════════════════════
    # 스크래치
    # ══════════════════════════════════════════════════════
    elif method == "scratch":
        st.markdown("### 🃏 스크래치 카드")
        m = st.session_state.scratch_menu
        menu_name  = m["name"]   if m else "???"
        menu_emoji = m.get("emoji","🍽️") if m else "🍽️"
        menu_cal   = m.get("cal",0)       if m else 0
        scratch_html = f"""
<div style="display:flex;flex-direction:column;align-items:center;gap:1rem;">
  <p style="color:#555;font-size:0.95rem;margin:0">마우스(또는 손가락)로 긁어서 메뉴를 확인하세요!</p>
  <div style="position:relative;width:340px;height:200px;border-radius:20px;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,0.5);">
    <div style="position:absolute;inset:0;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0.4rem;">
      <div style="font-size:3.5rem;line-height:1">{menu_emoji}</div>
      <div style="font-size:1.8rem;font-weight:900;color:white">{menu_name}</div>
      <div style="font-size:0.9rem;color:rgba(255,255,255,0.8);background:rgba(255,255,255,0.2);border-radius:999px;padding:0.2rem 1rem">🔥 {menu_cal} kcal</div>
    </div>
    <canvas id="scratch-canvas" width="340" height="200" style="position:absolute;inset:0;cursor:crosshair;border-radius:20px;touch-action:none"></canvas>
  </div>
  <p id="hint-text" style="color:#555;font-size:0.82rem;margin:0">긁은 면적이 60%를 넘으면 자동 완성돼요</p>
</div>
<script>
(function(){{
  const canvas=document.getElementById('scratch-canvas'),ctx=canvas.getContext('2d');
  const W=canvas.width,H=canvas.height;
  function drawLayer(c){{
    const g=c.createLinearGradient(0,0,W,H);
    g.addColorStop(0,'#c0b0e8');g.addColorStop(0.5,'#a890d8');g.addColorStop(1,'#9070c8');
    c.fillStyle=g;c.fillRect(0,0,W,H);
    c.fillStyle='rgba(255,255,255,0.18)';
    for(let i=0;i<80;i++){{const x=Math.random()*W,y=Math.random()*H,r=Math.random()*3+1;c.beginPath();c.arc(x,y,r,0,Math.PI*2);c.fill();}}
    c.fillStyle='rgba(255,255,255,0.85)';c.font='bold 22px "Noto Sans KR",sans-serif';c.textAlign='center';c.fillText('🪙  긁어서 확인  🪙',W/2,H/2-10);
    c.font='14px "Noto Sans KR",sans-serif';c.fillStyle='rgba(255,255,255,0.6)';c.fillText('Scratch here!',W/2,H/2+20);
  }}
  drawLayer(ctx);ctx.globalCompositeOperation='destination-out';
  const RADIUS=28,GRID=8,scratched=new Set();let revealed=false,painting=false;
  function getPos(e){{const rect=canvas.getBoundingClientRect(),sx=W/rect.width,sy=H/rect.height;
    if(e.touches)return{{x:(e.touches[0].clientX-rect.left)*sx,y:(e.touches[0].clientY-rect.top)*sy}};
    return{{x:(e.clientX-rect.left)*sx,y:(e.clientY-rect.top)*sy}};}}
  function markCells(cx,cy){{const r2=RADIUS*RADIUS,x0=Math.max(0,Math.floor((cx-RADIUS)/GRID)),x1=Math.min(Math.ceil(W/GRID),Math.ceil((cx+RADIUS)/GRID)),y0=Math.max(0,Math.floor((cy-RADIUS)/GRID)),y1=Math.min(Math.ceil(H/GRID),Math.ceil((cy+RADIUS)/GRID));
    for(let gx=x0;gx<=x1;gx++)for(let gy=y0;gy<=y1;gy++){{const px=gx*GRID+GRID/2,py=gy*GRID+GRID/2;if((px-cx)*(px-cx)+(py-cy)*(py-cy)<=r2)scratched.add(gx+','+gy);}}}}
  function scratch(pos){{ctx.beginPath();ctx.arc(pos.x,pos.y,RADIUS,0,Math.PI*2);ctx.fill();markCells(pos.x,pos.y);checkReveal();}}
  function checkReveal(){{if(revealed)return;const total=Math.ceil(W/GRID)*Math.ceil(H/GRID);if(scratched.size/total>=0.60){{revealed=true;let op=1;(function fade(){{op-=0.05;if(op<=0){{canvas.style.display='none';document.getElementById('hint-text').textContent='✨ 오늘의 메뉴!';return;}}canvas.style.opacity=op;requestAnimationFrame(fade);}})();}}}};
  canvas.addEventListener('mousedown',e=>{{painting=true;scratch(getPos(e));}});
  canvas.addEventListener('mousemove',e=>{{if(painting)scratch(getPos(e));}});
  canvas.addEventListener('mouseup',()=>painting=false);canvas.addEventListener('mouseleave',()=>painting=false);
  canvas.addEventListener('touchstart',e=>{{e.preventDefault();painting=true;scratch(getPos(e));}},{{passive:false}});
  canvas.addEventListener('touchmove',e=>{{e.preventDefault();if(painting)scratch(getPos(e));}},{{passive:false}});
  canvas.addEventListener('touchend',()=>painting=false);
}})();
</script>"""
        st.components.v1.html(scratch_html, height=310)
        if not st.session_state.scratch_revealed and m:
            add_history(m, "🃏 스크래치"); st.session_state.scratch_revealed = True
        if st.button("🔄 새 카드 뽑기", use_container_width=True, type="primary"):
            st.session_state.scratch_menu = random.choice(menus)
            st.session_state.scratch_revealed = False; st.rerun()

    # ══════════════════════════════════════════════════════
    # 월드컵
    # ══════════════════════════════════════════════════════
    elif method == "worldcup":
        ts = st.session_state.tournament_state
        if ts is None:
            st.error("토너먼트 초기화 오류.")
        elif len(ts["round"]) == 1:
            st.markdown("### 🏆 최종 우승!")
            st.balloons()
            winner = ts["round"][0]
            add_history(winner, "🏆 월드컵"); result_card(winner, "🏆 월드컵")
            if st.button("🔄 다시 하기", use_container_width=True):
                pool = random.sample(menus, min(8, len(menus)))
                if len(pool) % 2 == 1: pool = pool[:-1]
                st.session_state.tournament_state = {"round": pool, "pair_idx": 0, "winners": []}; st.rerun()
        else:
            pairs = [(ts["round"][i], ts["round"][i+1]) for i in range(0, len(ts["round"])-1, 2)]
            idx   = ts["pair_idx"]
            if idx >= len(pairs):
                nr = ts["winners"][:]
                if len(nr) % 2 == 1 and len(nr) > 1: nr = nr[:-1]
                ts["round"] = nr; ts["winners"] = []; ts["pair_idx"] = 0; st.rerun()
            else:
                a, b = pairs[idx]; n = len(ts["round"])
                st.markdown(f"### 🏆 {n}강 — {idx+1} / {len(pairs)} 경기")
                st.progress(idx / len(pairs))
                col_a, col_vs, col_b = st.columns([5, 1, 5])
                with col_a:
                    st.markdown(f'<div class="wc-option"><div class="wc-emoji">{a["emoji"]}</div><div class="wc-name">{a["name"]}</div><div class="wc-cal">🔥 {a["cal"]} kcal</div></div>', unsafe_allow_html=True)
                    if st.button(f"✅ {a['name']}", key=f"wa_{idx}", use_container_width=True, type="primary"):
                        ts["winners"].append(a); ts["pair_idx"] += 1; st.rerun()
                with col_vs:
                    st.markdown('<div style="display:flex;align-items:center;justify-content:center;height:100%;min-height:130px;font-size:1.4rem;font-weight:900;color:#ccc">VS</div>', unsafe_allow_html=True)
                with col_b:
                    st.markdown(f'<div class="wc-option"><div class="wc-emoji">{b["emoji"]}</div><div class="wc-name">{b["name"]}</div><div class="wc-cal">🔥 {b["cal"]} kcal</div></div>', unsafe_allow_html=True)
                    if st.button(f"✅ {b['name']}", key=f"wb_{idx}", use_container_width=True, type="primary"):
                        ts["winners"].append(b); ts["pair_idx"] += 1; st.rerun()

    # ══════════════════════════════════════════════════════
    # 주사위
    # ══════════════════════════════════════════════════════
    elif method == "dice":
        st.markdown("### 🎲 주사위")
        dice_html = """
<style>
  #dice-wrap { display:flex;flex-direction:column;align-items:center;gap:1.5rem;font-family:'Noto Sans KR',sans-serif;padding:1rem; }
  .dice { width:100px;height:100px;background:white;border-radius:16px;box-shadow:0 8px 32px rgba(0,0,0,0.2);display:flex;align-items:center;justify-content:center;font-size:60px;transition:transform 0.1s; }
  @keyframes shake { 0%{transform:rotate(0deg)} 20%{transform:rotate(-15deg)} 40%{transform:rotate(15deg)} 60%{transform:rotate(-10deg)} 80%{transform:rotate(10deg)} 100%{transform:rotate(0deg)} }
  .shaking { animation:shake 0.5s ease-in-out; }
  #roll-btn { background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:999px;padding:0.75rem 3rem;font-size:1.05rem;font-weight:700;cursor:pointer;font-family:'Noto Sans KR',sans-serif; }
  #dice-result { display:none;font-size:1.1rem;font-weight:700;color:#1a1a2e;text-align:center; }
</style>
<div id="dice-wrap">
  <div class="dice" id="dice-face">⚀</div>
  <button id="roll-btn" onclick="rollDice()">🎲 주사위 굴리기!</button>
  <div id="dice-result"></div>
</div>
<script>
const FACES = ['⚀','⚁','⚂','⚃','⚄','⚅'];
function rollDice() {
  const el = document.getElementById('dice-face');
  el.classList.remove('shaking'); void el.offsetWidth; el.classList.add('shaking');
  let count = 0;
  const iv = setInterval(() => {
    el.textContent = FACES[Math.floor(Math.random()*6)]; count++;
    if (count > 12) { clearInterval(iv);
      const val = Math.floor(Math.random()*6)+1;
      el.textContent = FACES[val-1];
      document.getElementById('dice-result').style.display='block';
      document.getElementById('dice-result').textContent = '🎲 ' + val + '가 나왔어요! 아래에서 결과를 확인하세요.';
      window.parent.postMessage({type:'dice_result', value: val}, '*');
    }
  }, 80);
}
</script>"""
        st.components.v1.html(dice_html, height=280)
        st.info("💡 주사위 눈 수 = 메뉴 목록에서 그 번째의 배수 위치로 선택돼요")
        if st.button("🎲 주사위 결과 반영하기", type="primary", use_container_width=True):
            val = random.randint(1, 6)
            idx = (val * 3 - 1) % len(menus)
            picked = menus[idx]
            add_history(picked, f"🎲 주사위({val})")
            st.session_state._random_result = picked; st.rerun()
        if st.session_state._random_result:
            result_card(st.session_state._random_result, "🎲 주사위")

    # ══════════════════════════════════════════════════════
    # 카드 뽑기 (타로)
    # ══════════════════════════════════════════════════════
    elif method == "tarot":
        st.markdown("### 🃏 카드 뽑기")
        if "tarot_cards" not in st.session_state or st.session_state.tarot_cards is None:
            st.session_state.tarot_cards  = random.sample(menus, min(3, len(menus)))
            st.session_state.tarot_chosen = None

        cards   = st.session_state.tarot_cards
        chosen  = st.session_state.tarot_chosen

        if chosen is None:
            st.markdown("<p style='color:#555;text-align:center;font-size:1rem'>✨ 세 장의 카드 중 하나를 고르세요</p>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            for ci, (col, card) in enumerate(zip([c1,c2,c3], cards)):
                with col:
                    st.markdown(f"""<div style="background:linear-gradient(135deg,#667eea,#764ba2);border-radius:16px;padding:2rem 1rem;text-align:center;cursor:pointer;box-shadow:0 6px 20px rgba(102,126,234,0.35);">
                        <div style="font-size:3rem">🎴</div>
                        <div style="color:white;font-weight:700;margin-top:0.5rem">카드 {ci+1}</div>
                    </div>""", unsafe_allow_html=True)
                    if st.button(f"카드 {ci+1} 선택", key=f"tarot_{ci}", use_container_width=True, type="primary"):
                        st.session_state.tarot_chosen = card
                        add_history(card, "🃏 카드뽑기"); st.rerun()
        else:
            st.markdown(f"""<div style="text-align:center;margin:1rem 0;">
                <div style="font-size:1rem;color:#888;margin-bottom:0.5rem">✨ 운명의 선택!</div>
            </div>""", unsafe_allow_html=True)
            result_card(chosen, "🃏 카드뽑기")
            st.markdown("<p style='text-align:center;color:#555;margin-top:0.5rem'>다른 카드엔 무엇이 있었을까요?</p>", unsafe_allow_html=True)
            other_cols = st.columns(2)
            others = [c for c in cards if c != chosen]
            for i, (col, card) in enumerate(zip(other_cols, others)):
                with col:
                    st.markdown(f"""<div style="background:#e8eaf6;border-radius:12px;padding:1rem;text-align:center;opacity:0.7">
                        <div style="font-size:2rem">{card['emoji']}</div>
                        <div style="font-weight:700;color:#555">{card['name']}</div>
                        <div style="font-size:0.8rem;color:#aaa">🔥 {card['cal']} kcal</div>
                    </div>""", unsafe_allow_html=True)
            if st.button("🔄 다시 뽑기", use_container_width=True, type="primary"):
                st.session_state.tarot_cards  = random.sample(menus, min(3, len(menus)))
                st.session_state.tarot_chosen = None; st.rerun()


    # ══════════════════════════════════════════════════════
    # 스마트 추천 (최근 안 먹은 메뉴)
    # ══════════════════════════════════════════════════════
    elif method == "smart":
        st.markdown("### 🧠 스마트 추천")
        recent_names = {h["menu"] for h in st.session_state.history[:10]}
        fresh = [m for m in menus if m["name"] not in recent_names]
        if not fresh:
            fresh = menus

        st.markdown(f"""<div style="background:#f0f8ff;border-radius:12px;padding:1rem;margin-bottom:1rem;border-left:4px solid #4facfe;">
            <p style="margin:0;color:#333;font-size:0.9rem">💡 최근 추천 이력 {len(recent_names)}개를 분석했어요. <b>{len(fresh)}개</b> 메뉴 중에서 추천합니다.</p>
        </div>""", unsafe_allow_html=True)

        if st.button("🧠 스마트 추천 받기", type="primary", use_container_width=True):
            picked = random.choice(fresh)
            add_history(picked, "🧠 스마트")
            st.session_state._random_result = picked; st.rerun()

        if st.session_state._random_result:
            result_card(st.session_state._random_result, "🧠 스마트 추천")

        if recent_names:
            with st.expander("📋 최근 먹은 메뉴 (제외 목록)"):
                for n in list(recent_names):
                    st.markdown(f"- {n}")

    # ══════════════════════════════════════════════════════
    # 대결 모드
    # ══════════════════════════════════════════════════════
    elif method == "battle":
        st.markdown("### ⚔️ 대결 모드")
        st.markdown("<p style='color:#555'>두 사람이 각자 원하는 메뉴를 입력하고, 룰렛으로 최종 결정!</p>", unsafe_allow_html=True)

        all_names = [m["name"] for m in menus]
        col_a, col_vs, col_b = st.columns([5, 1, 5])
        with col_a:
            st.markdown("**🙋 A의 선택**")
            a_pick = st.selectbox("A가 원하는 메뉴", all_names, key="battle_pick_a")
        with col_vs:
            st.markdown('<div style="display:flex;align-items:center;justify-content:center;height:80px;font-size:1.6rem;font-weight:900;color:#f5576c">⚔️</div>', unsafe_allow_html=True)
        with col_b:
            st.markdown("**🙋 B의 선택**")
            b_pick = st.selectbox("B가 원하는 메뉴", all_names, index=min(1, len(all_names)-1), key="battle_pick_b")

        if st.button("⚔️ 룰렛으로 결정!", type="primary", use_container_width=True):
            a_menu = next((m for m in menus if m["name"] == a_pick), None)
            b_menu = next((m for m in menus if m["name"] == b_pick), None)
            if a_menu and b_menu:
                winner = random.choice([a_menu, b_menu])
                add_history(winner, "⚔️ 대결")
                st.session_state.battle_result = {"winner": winner, "a": a_menu, "b": b_menu}
                st.rerun()

        if st.session_state.battle_result:
            br = st.session_state.battle_result
            winner = br["winner"]
            loser  = br["b"] if winner == br["a"] else br["a"]
            st.balloons()
            st.markdown(f"""<div style="text-align:center;margin:0.5rem 0 1rem;font-size:1rem;color:#888">
                {br['a']['emoji']} {br['a']['name']} &nbsp;⚔️&nbsp; {br['b']['emoji']} {br['b']['name']}
            </div>""", unsafe_allow_html=True)
            result_card(winner, "⚔️ 대결 승리!")
            st.markdown(f"<p style='text-align:center;color:#aaa;margin-top:0.5rem'>😔 {loser['name']} 는 다음 기회에...</p>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ④ 하단 탭
# ─────────────────────────────────────────────────────────────
st.markdown("<hr style='border:none;border-top:2px solid #ddd;margin:1.5rem 0 1rem'>", unsafe_allow_html=True)

tab_hist, tab_tracker, tab_rank, tab_mgmt = st.tabs(["📋 추천 이력", "🔥 칼로리 트래커", "🏅 메뉴 랭킹", "🔧 메뉴 관리"])

# ── 추천 이력 ─────────────────────────────────────────────────
with tab_hist:
    if st.session_state.history:
        c1, c2, c3 = st.columns(3)
        methods_l = [h["method"] for h in st.session_state.history]
        menus_l   = [h["menu"]   for h in st.session_state.history]
        with c1: st.metric("총 추천 횟수", f"{len(st.session_state.history)}회")
        with c2: st.metric("자주 쓴 방식",  max(set(methods_l), key=methods_l.count))
        with c3: st.metric("최다 추천 메뉴", max(set(menus_l),   key=menus_l.count))
        st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
        for h in st.session_state.history:
            st.markdown(f"""<div class="hist-item">
                <div>{h['emoji']} <b style="color:#111">{h['menu']}</b>
                <span style="color:#aaa;font-size:0.82rem"> &nbsp;·&nbsp; {h['time']} &nbsp;·&nbsp; {h['method']} &nbsp;·&nbsp; {h['cat']}</span></div>
                <div style="color:#667eea;font-weight:700">{h['cal']} kcal</div>
            </div>""", unsafe_allow_html=True)
        if st.button("🗑️ 이력 초기화"):
            st.session_state.history = []; st.rerun()
    else:
        st.info("아직 추천 이력이 없어요!")

# ── 칼로리 트래커 ─────────────────────────────────────────────
with tab_tracker:
    today = date.today().isoformat()
    today_entries = [e for e in st.session_state.today_log if e["date"] == today]
    total_cal = sum(e["cal"] for e in today_entries)
    goal_cal  = 2000

    st.markdown(f"### 오늘({today}) 칼로리")
    pct = min(total_cal / goal_cal, 1.0)
    color = "#43e97b" if pct < 0.7 else "#fee140" if pct < 0.9 else "#f5576c"
    st.markdown(f"""<div style="margin-bottom:0.5rem">
        <div style="display:flex;justify-content:space-between;margin-bottom:0.3rem">
            <span style="font-weight:700;color:#1a1a2e">{total_cal} kcal 섭취</span>
            <span style="color:#aaa">목표: {goal_cal} kcal</span>
        </div>
        <div class="cal-bar-wrap"><div class="cal-bar" style="width:{pct*100:.1f}%;background:{color}"></div></div>
        <div style="text-align:right;font-size:0.82rem;color:#aaa;margin-top:0.2rem">{pct*100:.0f}%</div>
    </div>""", unsafe_allow_html=True)

    goal_col, _ = st.columns([2, 3])
    with goal_col:
        new_goal = st.number_input("목표 칼로리 (kcal)", 1000, 4000, goal_cal, 100, key="goal_input")

    if today_entries:
        st.markdown("**오늘 먹은 메뉴**")
        for e in today_entries:
            st.markdown(f"""<div class="hist-item">
                <div>{e['emoji']} <b style="color:#111">{e['menu']}</b>
                <span style="color:#aaa;font-size:0.82rem"> &nbsp;·&nbsp; {e['time']}</span></div>
                <div style="color:#f5576c;font-weight:700">+{e['cal']} kcal</div>
            </div>""", unsafe_allow_html=True)
        if st.button("🗑️ 오늘 기록 초기화"):
            st.session_state.today_log = [e for e in st.session_state.today_log if e["date"] != today]; st.rerun()
    else:
        st.info("오늘 아직 추천받은 메뉴가 없어요!")

    # 주간 차트
    if st.session_state.today_log:
        st.markdown("**최근 7일 칼로리**")
        from collections import defaultdict
        daily = defaultdict(int)
        for e in st.session_state.today_log:
            daily[e["date"]] += e["cal"]
        sorted_days = sorted(daily.keys())[-7:]
        max_cal = max(daily.values()) if daily else 1
        for d in sorted_days:
            bar_w = daily[d] / max_cal * 100
            label = "오늘" if d == today else d[5:]
            st.markdown(f"""<div style="display:flex;align-items:center;gap:0.8rem;margin:0.3rem 0">
                <span style="width:3rem;font-size:0.82rem;color:#555">{label}</span>
                <div style="flex:1;background:#f0f2f8;border-radius:6px;height:20px;overflow:hidden">
                    <div style="width:{bar_w:.1f}%;background:linear-gradient(90deg,#667eea,#f5576c);height:20px;border-radius:6px"></div>
                </div>
                <span style="width:4rem;text-align:right;font-size:0.82rem;color:#667eea;font-weight:700">{daily[d]} kcal</span>
            </div>""", unsafe_allow_html=True)

# ── 메뉴 랭킹 ─────────────────────────────────────────────────
with tab_rank:
    st.markdown("### 🏅 메뉴 랭킹")
    if st.session_state.history:
        from collections import Counter
        cnt = Counter(h["menu"] for h in st.session_state.history)
        top = cnt.most_common(10)
        max_cnt = top[0][1] if top else 1
        medals = ["🥇","🥈","🥉"] + ["🏅"]*7
        for rank, (name, count) in enumerate(top):
            emoji = next((h["emoji"] for h in st.session_state.history if h["menu"]==name), "🍽️")
            bar_w = count / max_cnt * 100
            st.markdown(f"""<div class="rank-card">
                <div class="rank-num">{medals[rank]}</div>
                <div style="font-size:1.5rem">{emoji}</div>
                <div style="flex:1">
                    <div style="font-weight:700;color:#1a1a2e">{name}</div>
                    <div class="cal-bar-wrap" style="margin-top:0.3rem">
                        <div class="cal-bar" style="width:{bar_w:.1f}%"></div>
                    </div>
                </div>
                <div style="color:#667eea;font-weight:700;white-space:nowrap">{count}회</div>
            </div>""", unsafe_allow_html=True)

        # 방식별 통계
        st.markdown("### 📊 방식별 사용 통계")
        method_cnt = Counter(h["method"] for h in st.session_state.history)
        max_m = max(method_cnt.values())
        for m_name, m_count in method_cnt.most_common():
            bar_w = m_count / max_m * 100
            st.markdown(f"""<div style="display:flex;align-items:center;gap:0.8rem;margin:0.3rem 0">
                <span style="width:7rem;font-size:0.85rem;color:#555">{m_name}</span>
                <div style="flex:1;background:#f0f2f8;border-radius:6px;height:18px;overflow:hidden">
                    <div style="width:{bar_w:.1f}%;background:linear-gradient(90deg,#667eea,#764ba2);height:18px;border-radius:6px"></div>
                </div>
                <span style="width:2.5rem;text-align:right;font-size:0.82rem;color:#667eea;font-weight:700">{m_count}회</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("추천 이력이 쌓이면 랭킹이 표시돼요!")

# ── 메뉴 관리 ─────────────────────────────────────────────────
with tab_mgmt:
    col_add, col_excl = st.columns(2)
    with col_add:
        st.markdown("**➕ 커스텀 메뉴 추가**")
        nm = st.text_input("메뉴 이름", placeholder="예: 순두부찌개", key="add_nm")
        nc = st.number_input("칼로리 (kcal)", 0, 3000, 500, 50, key="add_cal")
        ne = st.text_input("이모지", "🍽️", max_chars=2, key="add_emoji")
        if st.button("추가", type="primary"):
            if nm.strip():
                st.session_state.custom_menus.append({"name":nm.strip(),"cal":nc,"emoji":ne})
                st.success(f"'{nm}' 추가 완료!"); st.rerun()
            else:
                st.error("이름을 입력하세요.")
        if st.session_state.custom_menus:
            st.markdown("**내 커스텀 메뉴**")
            for i, m in enumerate(st.session_state.custom_menus):
                ca, cb = st.columns([5, 1])
                with ca: st.write(f"{m['emoji']} {m['name']} ({m['cal']}kcal)")
                with cb:
                    if st.button("🗑️", key=f"del_{i}"):
                        st.session_state.custom_menus.pop(i); st.rerun()
    with col_excl:
        st.markdown(f"**🚫 메뉴 제외 설정** — {st.session_state.active_cat}")
        for m in MENU_DATA.get(st.session_state.active_cat, []):
            excluded = m["name"] in st.session_state.excluded
            chk = st.checkbox(f"{m['emoji']} {m['name']}", value=excluded, key=f"ex_{m['name']}")
            if chk:  st.session_state.excluded.add(m["name"])
            else:    st.session_state.excluded.discard(m["name"])
        if st.session_state.excluded:
            st.markdown(f"<div style='color:#f5576c;font-size:0.82rem;margin-top:0.5rem'>제외 중: {', '.join(st.session_state.excluded)}</div>", unsafe_allow_html=True)
