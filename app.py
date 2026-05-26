import streamlit as st
import streamlit.components.v1 as components
import random
import time
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
.stButton>button[kind="secondary"]{background:rgba(255,255,255,.15)!important;border:2px solid rgba(255,255,255,.4)!important;color:#111!important;}
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
.stMarkdown p,label,.stMetric,[data-testid="stMetricLabel"],[data-testid="stMetricValue"]{color:#111!important;}
[data-testid="stMetricValue"]{color:#1a1a2e!important;}
hr{border-color:#ddd!important;}
#MainMenu,footer,header{visibility:hidden;}
.stButton>button{border-radius:12px!important;font-weight:700!important;font-family:'Noto Sans KR',sans-serif!important;}
.stTabs [data-baseweb="tab"]{border-radius:10px!important;font-weight:600!important;font-family:'Noto Sans KR',sans-serif!important;}
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
    "저녁 메뉴": [{"name":"삼겹살","cal":700,"emoji":"🥓","food_type":"고기","delivery":False,"budget":"중"},{"name":"치킨","cal":850,"emoji":"🍗","food_type":"고기","delivery":True,"budget":"중"},{"name":"피자","cal":900,"emoji":"🍕","food_type":"기타","delivery":True,"budget":"중"},{"name":"파스타","cal":650,"emoji":"🍝","food_type":"면","delivery":True,"budget":"중"},{"name":"스테이크","cal":800,"emoji":"🥩","food_type":"고기","delivery":False,"budget":"고"},{"name":"초밥","cal":500,"emoji":"🍣","food_type":"기타","delivery":True,"budget":"고"},{"name":"된장찌개","cal":350,"emoji":"🍲","food_type":"밥","delivery":False,"budget":"저"},{"name":"갈비탕","cal":600,"emoji":"🍖","food_type":"고기","delivery":False,"budget":"중"},{"name":"불고기","cal":550,"emoji":"🔥","food_type":"고기","delivery":False,"budget":"중"},{"name":"쭈꾸미볶음","cal":450,"emoji":"🐙","food_type":"기타","delivery":True,"budget":"저"},{"name":"순두부찌개","cal":300,"emoji":"🫕","food_type":"밥","delivery":False,"budget":"저"},{"name":"부대찌개","cal":650,"emoji":"🍲","food_type":"밥","delivery":False,"budget":"저"},{"name":"곱창전골","cal":700,"emoji":"🫕","food_type":"고기","delivery":False,"budget":"중"},{"name":"닭갈비","cal":580,"emoji":"🍗","food_type":"고기","delivery":True,"budget":"저"}],
    "배달 메뉴": [{"name":"치킨","cal":850,"emoji":"🍗","food_type":"고기","delivery":True,"budget":"중"},{"name":"피자","cal":900,"emoji":"🍕","food_type":"기타","delivery":True,"budget":"중"},{"name":"짜장면","cal":650,"emoji":"🍜","food_type":"면","delivery":True,"budget":"저"},{"name":"짬뽕","cal":700,"emoji":"🍜","food_type":"면","delivery":True,"budget":"저"},{"name":"떡볶이","cal":500,"emoji":"🌶️","food_type":"기타","delivery":True,"budget":"저"},{"name":"족발","cal":750,"emoji":"🍖","food_type":"고기","delivery":True,"budget":"중"},{"name":"버거","cal":650,"emoji":"🍔","food_type":"기타","delivery":True,"budget":"저"},{"name":"마라탕","cal":700,"emoji":"🥢","food_type":"기타","delivery":True,"budget":"중"},{"name":"초밥 세트","cal":520,"emoji":"🍣","food_type":"기타","delivery":True,"budget":"고"},{"name":"국밥","cal":550,"emoji":"🍲","food_type":"밥","delivery":True,"budget":"저"},{"name":"쌀국수","cal":480,"emoji":"🍜","food_type":"면","delivery":True,"budget":"저"},{"name":"보쌈","cal":680,"emoji":"🥬","food_type":"고기","delivery":True,"budget":"중"},{"name":"감자탕","cal":620,"emoji":"🍲","food_type":"고기","delivery":True,"budget":"저"},{"name":"샌드위치","cal":450,"emoji":"🥪","food_type":"기타","delivery":True,"budget":"저"}],
    "데이트 메뉴": [{"name":"파스타","cal":650,"emoji":"🍝","food_type":"면","delivery":False,"budget":"중"},{"name":"스테이크","cal":800,"emoji":"🥩","food_type":"고기","delivery":False,"budget":"고"},{"name":"초밥 / 오마카세","cal":600,"emoji":"🍣","food_type":"기타","delivery":False,"budget":"고"},{"name":"샤브샤브","cal":450,"emoji":"🍲","food_type":"기타","delivery":False,"budget":"고"},{"name":"와인 파스타","cal":700,"emoji":"🍷","food_type":"면","delivery":False,"budget":"고"},{"name":"리조또","cal":620,"emoji":"🍚","food_type":"밥","delivery":False,"budget":"고"},{"name":"프렌치 코스","cal":900,"emoji":"🥂","food_type":"기타","delivery":False,"budget":"고"},{"name":"타파스","cal":500,"emoji":"🫒","food_type":"기타","delivery":False,"budget":"고"},{"name":"훠궈","cal":750,"emoji":"🫕","food_type":"기타","delivery":False,"budget":"중"},{"name":"브런치 카페","cal":550,"emoji":"☕","food_type":"기타","delivery":False,"budget":"중"},{"name":"이탈리안 뷔페","cal":850,"emoji":"🍽️","food_type":"기타","delivery":False,"budget":"고"},{"name":"스시 오마카세","cal":700,"emoji":"🍱","food_type":"기타","delivery":False,"budget":"고"}],
    "다이어트 메뉴": [{"name":"닭가슴살 샐러드","cal":280,"emoji":"🥗","food_type":"기타","delivery":True,"budget":"저"},{"name":"두부 스테이크","cal":200,"emoji":"🥩","food_type":"기타","delivery":False,"budget":"저"},{"name":"곤약 비빔밥","cal":250,"emoji":"🍚","food_type":"밥","delivery":False,"budget":"저"},{"name":"그릭 요거트 볼","cal":180,"emoji":"🥣","food_type":"기타","delivery":False,"budget":"저"},{"name":"채소 스프","cal":120,"emoji":"🥦","food_type":"기타","delivery":False,"budget":"저"},{"name":"연어 포케","cal":380,"emoji":"🐟","food_type":"기타","delivery":True,"budget":"중"},{"name":"닭가슴살 도시락","cal":300,"emoji":"🍱","food_type":"고기","delivery":True,"budget":"저"},{"name":"오트밀 볼","cal":220,"emoji":"🌾","food_type":"기타","delivery":False,"budget":"저"},{"name":"현미 잡곡밥 정식","cal":420,"emoji":"🍚","food_type":"밥","delivery":False,"budget":"저"},{"name":"저칼로리 김밥","cal":320,"emoji":"🍙","food_type":"기타","delivery":True,"budget":"저"},{"name":"채소 쌈밥","cal":350,"emoji":"🥬","food_type":"밥","delivery":False,"budget":"저"},{"name":"토마토 달걀볶음","cal":200,"emoji":"🍳","food_type":"기타","delivery":False,"budget":"저"},{"name":"닭가슴살 볶음밥","cal":380,"emoji":"🍳","food_type":"밥","delivery":True,"budget":"저"}],
    "가성비 메뉴": [{"name":"김밥","cal":400,"emoji":"🍙","food_type":"기타","delivery":True,"budget":"저"},{"name":"순대국밥","cal":550,"emoji":"🍲","food_type":"밥","delivery":False,"budget":"저"},{"name":"라면","cal":500,"emoji":"🍜","food_type":"면","delivery":True,"budget":"저"},{"name":"백반","cal":650,"emoji":"🍚","food_type":"밥","delivery":False,"budget":"저"},{"name":"편의점 도시락","cal":550,"emoji":"🏪","food_type":"밥","delivery":False,"budget":"저"},{"name":"분식 세트","cal":600,"emoji":"🌶️","food_type":"기타","delivery":True,"budget":"저"},{"name":"컵라면 + 삼각김밥","cal":450,"emoji":"🍙","food_type":"면","delivery":False,"budget":"저"},{"name":"뼈다귀해장국","cal":500,"emoji":"🍲","food_type":"밥","delivery":False,"budget":"저"},{"name":"돈까스 정식","cal":700,"emoji":"🥩","food_type":"고기","delivery":True,"budget":"저"},{"name":"제육볶음 백반","cal":650,"emoji":"🍳","food_type":"밥","delivery":True,"budget":"저"},{"name":"칼국수","cal":520,"emoji":"🍜","food_type":"면","delivery":False,"budget":"저"},{"name":"콩나물국밥","cal":400,"emoji":"🍲","food_type":"밥","delivery":False,"budget":"저"},{"name":"떡볶이 + 순대","cal":580,"emoji":"🌶️","food_type":"기타","delivery":True,"budget":"저"}],
    "캠핑 메뉴": [{"name":"삼겹살 구이","cal":700,"emoji":"🔥","food_type":"고기","delivery":False,"budget":"저"},{"name":"라면","cal":500,"emoji":"🍜","food_type":"면","delivery":False,"budget":"저"},{"name":"핫도그","cal":380,"emoji":"🌭","food_type":"기타","delivery":False,"budget":"저"},{"name":"불고기","cal":550,"emoji":"🥩","food_type":"고기","delivery":False,"budget":"중"},{"name":"옥수수 구이","cal":180,"emoji":"🌽","food_type":"기타","delivery":False,"budget":"저"},{"name":"감자 구이","cal":200,"emoji":"🥔","food_type":"기타","delivery":False,"budget":"저"},{"name":"부대찌개","cal":650,"emoji":"🍲","food_type":"밥","delivery":False,"budget":"저"},{"name":"닭꼬치","cal":350,"emoji":"🍢","food_type":"고기","delivery":False,"budget":"저"},{"name":"소시지 구이","cal":400,"emoji":"🌭","food_type":"고기","delivery":False,"budget":"저"},{"name":"묵은지 삼겹","cal":720,"emoji":"🥓","food_type":"고기","delivery":False,"budget":"중"},{"name":"즉석 떡볶이","cal":480,"emoji":"🌶️","food_type":"기타","delivery":False,"budget":"저"},{"name":"어묵탕","cal":300,"emoji":"🍢","food_type":"기타","delivery":False,"budget":"저"},{"name":"스팸 구이","cal":450,"emoji":"🥫","food_type":"고기","delivery":False,"budget":"저"}],
    "매운 메뉴": [{"name":"불닭볶음면","cal":530,"emoji":"🔥","food_type":"면","delivery":True,"budget":"저"},{"name":"마라탕","cal":700,"emoji":"🌶️","food_type":"기타","delivery":True,"budget":"중"},{"name":"엽기 떡볶이","cal":600,"emoji":"🌶️","food_type":"기타","delivery":True,"budget":"저"},{"name":"매운 김치찌개","cal":400,"emoji":"🍲","food_type":"밥","delivery":False,"budget":"저"},{"name":"육개장","cal":350,"emoji":"🍲","food_type":"밥","delivery":False,"budget":"저"},{"name":"마라샹궈","cal":800,"emoji":"🥢","food_type":"기타","delivery":True,"budget":"중"},{"name":"불닭 피자","cal":950,"emoji":"🍕","food_type":"기타","delivery":True,"budget":"중"},{"name":"매운 갈비찜","cal":750,"emoji":"🍖","food_type":"고기","delivery":False,"budget":"중"},{"name":"낙지볶음","cal":380,"emoji":"🐙","food_type":"기타","delivery":True,"budget":"중"},{"name":"쭈꾸미볶음","cal":420,"emoji":"🦑","food_type":"기타","delivery":True,"budget":"저"},{"name":"매운 해물탕","cal":500,"emoji":"🦀","food_type":"기타","delivery":False,"budget":"중"},{"name":"불족발","cal":780,"emoji":"🔥","food_type":"고기","delivery":True,"budget":"중"},{"name":"청양 닭볶음탕","cal":600,"emoji":"🍗","food_type":"고기","delivery":True,"budget":"저"}],
    "파티 메뉴": [{"name":"피자","cal":900,"emoji":"🍕","food_type":"기타","delivery":True,"budget":"중"},{"name":"치킨","cal":850,"emoji":"🍗","food_type":"고기","delivery":True,"budget":"중"},{"name":"파스타 플래터","cal":700,"emoji":"🍝","food_type":"면","delivery":False,"budget":"고"},{"name":"타코","cal":550,"emoji":"🌮","food_type":"기타","delivery":False,"budget":"중"},{"name":"샌드위치 플래터","cal":600,"emoji":"🥪","food_type":"기타","delivery":True,"budget":"중"},{"name":"뷔페","cal":900,"emoji":"🍽️","food_type":"기타","delivery":False,"budget":"고"},{"name":"초밥 세트","cal":560,"emoji":"🍣","food_type":"기타","delivery":True,"budget":"고"},{"name":"바비큐 플래터","cal":850,"emoji":"🔥","food_type":"고기","delivery":False,"budget":"고"},{"name":"케이터링 도시락","cal":700,"emoji":"🍱","food_type":"밥","delivery":True,"budget":"중"},{"name":"나초 + 딥","cal":500,"emoji":"🫔","food_type":"기타","delivery":False,"budget":"저"},{"name":"핑거푸드 세트","cal":450,"emoji":"🍢","food_type":"기타","delivery":False,"budget":"중"},{"name":"떡 케이크","cal":400,"emoji":"🎂","food_type":"기타","delivery":True,"budget":"중"}],
    "한식 메뉴": [{"name":"비빔밥","cal":550,"emoji":"🍚","food_type":"밥","delivery":True,"budget":"저"},{"name":"된장찌개","cal":350,"emoji":"🍲","food_type":"밥","delivery":False,"budget":"저"},{"name":"삼겹살","cal":700,"emoji":"🥓","food_type":"고기","delivery":False,"budget":"중"},{"name":"불고기","cal":550,"emoji":"🥩","food_type":"고기","delivery":False,"budget":"중"},{"name":"냉면","cal":500,"emoji":"🍜","food_type":"면","delivery":True,"budget":"중"},{"name":"갈비탕","cal":600,"emoji":"🍖","food_type":"고기","delivery":False,"budget":"중"},{"name":"삼계탕","cal":580,"emoji":"🐔","food_type":"고기","delivery":False,"budget":"중"},{"name":"순대국밥","cal":550,"emoji":"🍲","food_type":"밥","delivery":False,"budget":"저"},{"name":"해물파전","cal":480,"emoji":"🥞","food_type":"기타","delivery":False,"budget":"저"},{"name":"잡채","cal":420,"emoji":"🍜","food_type":"면","delivery":False,"budget":"중"},{"name":"감자탕","cal":620,"emoji":"🍲","food_type":"고기","delivery":True,"budget":"저"},{"name":"보쌈","cal":680,"emoji":"🥬","food_type":"고기","delivery":True,"budget":"중"},{"name":"닭갈비","cal":580,"emoji":"🍗","food_type":"고기","delivery":True,"budget":"저"},{"name":"낙지볶음","cal":380,"emoji":"🐙","food_type":"기타","delivery":True,"budget":"중"},{"name":"떡국","cal":450,"emoji":"🍲","food_type":"밥","delivery":False,"budget":"저"}],
    "일식 메뉴": [{"name":"초밥","cal":500,"emoji":"🍣","food_type":"기타","delivery":True,"budget":"고"},{"name":"라멘","cal":700,"emoji":"🍜","food_type":"면","delivery":True,"budget":"중"},{"name":"우동","cal":450,"emoji":"🍜","food_type":"면","delivery":True,"budget":"중"},{"name":"돈카츠","cal":750,"emoji":"🥩","food_type":"고기","delivery":True,"budget":"중"},{"name":"오야코동","cal":600,"emoji":"🍚","food_type":"밥","delivery":True,"budget":"중"},{"name":"타코야키","cal":380,"emoji":"🐙","food_type":"기타","delivery":True,"budget":"저"},{"name":"규동","cal":620,"emoji":"🍚","food_type":"밥","delivery":True,"budget":"저"},{"name":"나가사키 짬뽕","cal":680,"emoji":"🍜","food_type":"면","delivery":False,"budget":"중"},{"name":"오마카세","cal":700,"emoji":"🍱","food_type":"기타","delivery":False,"budget":"고"},{"name":"야키토리","cal":400,"emoji":"🍢","food_type":"고기","delivery":False,"budget":"중"},{"name":"카레라이스","cal":650,"emoji":"🍛","food_type":"밥","delivery":True,"budget":"저"},{"name":"소바","cal":400,"emoji":"🍜","food_type":"면","delivery":False,"budget":"중"},{"name":"이자카야 세트","cal":750,"emoji":"🍶","food_type":"기타","delivery":False,"budget":"고"}],
    "양식 메뉴": [{"name":"파스타","cal":650,"emoji":"🍝","food_type":"면","delivery":True,"budget":"중"},{"name":"피자","cal":900,"emoji":"🍕","food_type":"기타","delivery":True,"budget":"중"},{"name":"스테이크","cal":800,"emoji":"🥩","food_type":"고기","delivery":False,"budget":"고"},{"name":"버거","cal":650,"emoji":"🍔","food_type":"기타","delivery":True,"budget":"저"},{"name":"리조또","cal":620,"emoji":"🍚","food_type":"밥","delivery":False,"budget":"고"},{"name":"샐러드","cal":250,"emoji":"🥗","food_type":"기타","delivery":True,"budget":"중"},{"name":"그라탱","cal":700,"emoji":"🧀","food_type":"기타","delivery":False,"budget":"중"},{"name":"크림 수프","cal":350,"emoji":"🍵","food_type":"기타","delivery":False,"budget":"중"},{"name":"연어 스테이크","cal":550,"emoji":"🐟","food_type":"고기","delivery":False,"budget":"고"},{"name":"브런치 플레이트","cal":600,"emoji":"🥞","food_type":"기타","delivery":False,"budget":"중"},{"name":"함박스테이크","cal":680,"emoji":"🥩","food_type":"고기","delivery":True,"budget":"중"},{"name":"치킨 알프레도","cal":720,"emoji":"🍝","food_type":"면","delivery":True,"budget":"중"},{"name":"클램 차우더","cal":380,"emoji":"🍵","food_type":"기타","delivery":False,"budget":"중"}],
    "중식 메뉴": [{"name":"짜장면","cal":650,"emoji":"🍜","food_type":"면","delivery":True,"budget":"저"},{"name":"짬뽕","cal":700,"emoji":"🍜","food_type":"면","delivery":True,"budget":"저"},{"name":"탕수육","cal":800,"emoji":"🥩","food_type":"고기","delivery":True,"budget":"중"},{"name":"마파두부","cal":400,"emoji":"🌶️","food_type":"밥","delivery":True,"budget":"중"},{"name":"딤섬","cal":500,"emoji":"🥟","food_type":"기타","delivery":False,"budget":"중"},{"name":"마라탕","cal":700,"emoji":"🥢","food_type":"기타","delivery":True,"budget":"중"},{"name":"마라샹궈","cal":800,"emoji":"🌶️","food_type":"기타","delivery":True,"budget":"중"},{"name":"훠궈","cal":750,"emoji":"🫕","food_type":"기타","delivery":False,"budget":"고"},{"name":"꿔바로우","cal":820,"emoji":"🥩","food_type":"고기","delivery":True,"budget":"중"},{"name":"양꼬치","cal":600,"emoji":"🍢","food_type":"고기","delivery":False,"budget":"중"},{"name":"깐풍기","cal":780,"emoji":"🍗","food_type":"고기","delivery":True,"budget":"중"},{"name":"유린기","cal":700,"emoji":"🍗","food_type":"고기","delivery":True,"budget":"중"},{"name":"동파육","cal":850,"emoji":"🥩","food_type":"고기","delivery":False,"budget":"고"}],
    "안주 메뉴": [{"name":"치킨","cal":850,"emoji":"🍗","food_type":"고기","delivery":True,"budget":"중"},{"name":"족발","cal":750,"emoji":"🍖","food_type":"고기","delivery":True,"budget":"중"},{"name":"마른안주 세트","cal":300,"emoji":"🦑","food_type":"기타","delivery":True,"budget":"저"},{"name":"두부김치","cal":350,"emoji":"🥬","food_type":"기타","delivery":False,"budget":"저"},{"name":"골뱅이소면","cal":450,"emoji":"🐌","food_type":"면","delivery":False,"budget":"저"},{"name":"감자전","cal":380,"emoji":"🥞","food_type":"기타","delivery":False,"budget":"저"},{"name":"해물파전","cal":480,"emoji":"🥞","food_type":"기타","delivery":False,"budget":"저"},{"name":"닭발","cal":420,"emoji":"🍗","food_type":"고기","delivery":True,"budget":"저"},{"name":"삼겹살","cal":700,"emoji":"🥓","food_type":"고기","delivery":False,"budget":"중"},{"name":"소시지 야채볶음","cal":500,"emoji":"🌭","food_type":"고기","delivery":False,"budget":"저"},{"name":"계란말이","cal":280,"emoji":"🥚","food_type":"기타","delivery":False,"budget":"저"},{"name":"오돌뼈","cal":460,"emoji":"🦴","food_type":"고기","delivery":False,"budget":"저"},{"name":"곱창볶음","cal":650,"emoji":"🫕","food_type":"고기","delivery":True,"budget":"중"},{"name":"라볶이","cal":550,"emoji":"🌶️","food_type":"기타","delivery":True,"budget":"저"}],
    "혼자 먹는 메뉴": [{"name":"편의점 도시락","cal":550,"emoji":"🏪","food_type":"밥","delivery":False,"budget":"저"},{"name":"라면","cal":500,"emoji":"🍜","food_type":"면","delivery":False,"budget":"저"},{"name":"김밥 한 줄","cal":400,"emoji":"🍙","food_type":"기타","delivery":True,"budget":"저"},{"name":"우동","cal":450,"emoji":"🫕","food_type":"면","delivery":True,"budget":"저"},{"name":"덮밥","cal":600,"emoji":"🍚","food_type":"밥","delivery":True,"budget":"저"},{"name":"국밥","cal":550,"emoji":"🍲","food_type":"밥","delivery":False,"budget":"저"},{"name":"냉면","cal":500,"emoji":"🍜","food_type":"면","delivery":True,"budget":"중"},{"name":"돈까스 정식","cal":700,"emoji":"🥩","food_type":"고기","delivery":True,"budget":"저"},{"name":"1인 샤브샤브","cal":480,"emoji":"🍲","food_type":"기타","delivery":False,"budget":"중"},{"name":"제육 덮밥","cal":620,"emoji":"🍳","food_type":"밥","delivery":True,"budget":"저"},{"name":"삼각김밥 세트","cal":420,"emoji":"🍙","food_type":"기타","delivery":False,"budget":"저"},{"name":"소고기 국밥","cal":580,"emoji":"🍲","food_type":"밥","delivery":False,"budget":"저"},{"name":"짬뽕 1인분","cal":680,"emoji":"🍜","food_type":"면","delivery":True,"budget":"저"},{"name":"혼밥 정식","cal":650,"emoji":"🍱","food_type":"밥","delivery":True,"budget":"저"}],
}
CATEGORIES = list(MENU_DATA.keys())

FORTUNES = [
    ("새로운 걸 시도하기 좋은 날 ✨", "평소엔 안 먹던 새 메뉴에 도전해봐요!"),
    ("편안하고 익숙한 게 최고인 날 🏠", "자주 먹던 편안한 메뉴가 최고예요."),
    ("에너지가 넘치는 날 💪", "든든하고 칼로리 높은 메뉴로 충전!"),
    ("건강을 챙기고 싶은 날 🌿", "저칼로리 건강 메뉴를 선택해봐요."),
    ("기분 전환이 필요한 날 🌈", "매운 음식으로 스트레스를 날려버려요!"),
    ("특별한 하루를 만들고 싶은 날 🎉", "평소보다 조금 더 특별한 메뉴 어때요?"),
    ("절약 모드인 날 💰", "가성비 최고 메뉴를 골라봐요!"),
    ("누군가와 함께하고 싶은 날 🤝", "여럿이 나눠 먹기 좋은 메뉴로!"),
]

# ── 세션 초기화 ───────────────────────────────────────────────
def init():
    defaults = {
        "history": [], "excluded": set(), "custom_menus": [],
        "active_cat": "저녁 메뉴", "active_method": None,
        "tournament_state": None, "scratch_revealed": False,
        "scratch_menu": None, "last_result": None,
        "_random_result": None,
        "battle_result": None,
        "today_log": [],
        "fortune_today": None, "fortune_date": None,
        "tarot_cards": None, "tarot_chosen": None,
        "filter_cal_min": 0, "filter_cal_max": 1200,
        "filter_food_type": "전체", "filter_delivery": "전체", "filter_budget": "전체",
        "roulette_done": False, "roulette_winner": None,
        "roulette_winner_idx": 0,
        "dice_winner": None, "dice_face": 1
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    # 타입 강제 보정 (기존 배포 세션 호환)
    if not isinstance(st.session_state.excluded, set):
        st.session_state.excluded = set()
    if not isinstance(st.session_state.history, list):
        st.session_state.history = []
    if not isinstance(st.session_state.custom_menus, list):
        st.session_state.custom_menus = []
    if not isinstance(st.session_state.today_log, list):
        st.session_state.today_log = []
    if st.session_state.active_cat not in MENU_DATA:
        st.session_state.active_cat = "저녁 메뉴"
init()

# ── 헬퍼 ─────────────────────────────────────────────────────
def get_all_menus():
    # 방어: excluded가 set이 아닌 경우 (기존 세션 호환)
    if not isinstance(st.session_state.get("excluded"), set):
        st.session_state.excluded = set()
    if not isinstance(st.session_state.get("custom_menus"), list):
        st.session_state.custom_menus = []
    base = MENU_DATA.get(st.session_state.active_cat, [])
    return [m for m in base + st.session_state.custom_menus if m["name"] not in st.session_state.excluded]

def apply_filters(menus):
    result = menus
    if st.session_state.filter_food_type != "전체":
        result = [m for m in result if m.get("food_type") == st.session_state.filter_food_type]
    if st.session_state.filter_delivery == "배달만":
        result = [m for m in result if m.get("delivery", False)]
    elif st.session_state.filter_delivery == "직접만":
        result = [m for m in result if not m.get("delivery", False)]
    if st.session_state.filter_budget != "전체":
        result = [m for m in result if m.get("budget") == st.session_state.filter_budget]
    result = [m for m in result if st.session_state.filter_cal_min <= m.get("cal", 0) <= st.session_state.filter_cal_max]
    return result or menus

def get_menus():
    return apply_filters(get_all_menus())

def add_history(menu, method):
    kcal = menu.get("cal", 0)
    entry = {"menu": menu["name"], "emoji": menu.get("emoji","🍽️"), "cal": kcal,
             "method": method, "cat": st.session_state.active_cat,
             "time": datetime.now().strftime("%m/%d %H:%M"),
             "hour": datetime.now().hour,
             "food_type": menu.get("food_type","기타")}
    st.session_state.history.insert(0, entry)
    if len(st.session_state.history) > 50:
        st.session_state.history = st.session_state.history[:50]
    st.session_state.last_result = entry
    today = date.today().isoformat()
    st.session_state.today_log.append({"menu": menu["name"], "emoji": menu.get("emoji","🍽️"),
                                        "cal": kcal, "date": today, "time": datetime.now().strftime("%H:%M")})

def adopt_button(menu, method, key_suffix=""):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"✅ {menu['name']} (으)로 결정!", key=f"adopt_{key_suffix}", use_container_width=True, type="primary"):
            add_history(menu, method)
            st.success(f"🎉 **{menu['name']}** 이(가) 오늘의 메뉴로 기록됐어요!")
            reset_method()
            st.rerun()

def result_card(menu, method=""):
    st.markdown(f"""<div class="result-card">
        <div class="result-emoji">{menu.get('emoji','🍽️')}</div>
        <div class="result-name">{menu['name']}</div>
        <div class="result-cal">🔥 약 {menu.get('cal',0)} kcal &nbsp;·&nbsp; {method}</div>
    </div>""", unsafe_allow_html=True)

def reset_method():
    st.session_state.active_method = None
    st.session_state.tournament_state = None
    st.session_state.scratch_revealed = False
    st.session_state.scratch_menu = None
    st.session_state._random_result = None
    st.session_state.battle_result = None
    st.session_state.tarot_cards = None
    st.session_state.tarot_chosen = None
    st.session_state.roulette_done = False
    st.session_state.roulette_winner = None
    st.session_state.roulette_winner_idx = 0
    st.session_state.dice_winner = None

def get_fortune():
    today = date.today().isoformat()
    if st.session_state.fortune_date != today or st.session_state.fortune_today is None:
        random.seed(today)
        st.session_state.fortune_today = random.choice(FORTUNES)
        st.session_state.fortune_date  = today
        random.seed()
    return st.session_state.fortune_today

# ── 제목 ─────────────────────────────────────────────────────
st.markdown('<div class="title-pill-wrap"><div class="title-pill">🍽️ 오늘의 추천 메뉴</div></div>', unsafe_allow_html=True)

# ── 오늘의 운세 배너 ─────────────────────────────────────────
fortune_msg, fortune_tip = get_fortune()
all_menus_flat = [m for cat in MENU_DATA.values() for m in cat]
random.seed(date.today().isoformat() + "food")
fortune_food = random.choice(all_menus_flat)
random.seed()
st.markdown(f"""<div class="fortune-card">
    <div style="font-size:1.5rem;font-weight:900;margin-bottom:.4rem">🍀 오늘의 운세</div>
    <div style="font-size:1.1rem;font-weight:700;margin-bottom:.3rem">{fortune_msg}</div>
    <div style="font-size:.9rem;opacity:.9;margin-bottom:.8rem">{fortune_tip}</div>
    <div style="background:rgba(255,255,255,.25);border-radius:12px;padding:.5rem 1.5rem;display:inline-block;">
        👉 오늘의 추천: <b>{fortune_food['emoji']} {fortune_food['name']}</b>
    </div>
</div>""", unsafe_allow_html=True)

# ── 카테고리 탭 ──────────────────────────────────────────────
st.markdown('<div style="background:#d966a0;border-radius:14px;padding:.55rem .8rem;margin-bottom:.6rem;"><span style="color:rgba(255,255,255,.7);font-size:.78rem;font-weight:700">카테고리</span></div>', unsafe_allow_html=True)
row_a = st.columns(7); row_b = st.columns(7)
for i, cat in enumerate(CATEGORIES):
    emoji = CATEGORY_EMOJI.get(cat, "🍽️"); short = cat.replace(" 메뉴","")
    with (row_a + row_b)[i]:
        if st.button(f"{emoji} {short}", key=f"cat_{cat}", use_container_width=True,
                     type="primary" if cat == st.session_state.active_cat else "secondary"):
            st.session_state.active_cat = cat; reset_method(); st.rerun()

# ── 조건 필터 바 ─────────────────────────────────────────────
with st.expander("🔍 조건 필터", expanded=False):
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        cal_range = st.slider("🔥 칼로리 범위 (kcal)", 0, 1200,
                              (st.session_state.filter_cal_min, st.session_state.filter_cal_max), 50)
        st.session_state.filter_cal_min, st.session_state.filter_cal_max = cal_range
    with fc2:
        ft = st.selectbox("🍽️ 음식 종류", ["전체","밥","면","고기","기타"],
                          index=["전체","밥","면","고기","기타"].index(st.session_state.filter_food_type))
        st.session_state.filter_food_type = ft
    with fc3:
        dv = st.selectbox("🛵 조리 / 배달", ["전체","배달만","직접만"],
                          index=["전체","배달만","직접만"].index(st.session_state.filter_delivery))
        st.session_state.filter_delivery = dv
    with fc4:
        bd = st.selectbox("💰 예산", ["전체","저","중","고"],
                          index=["전체","저","중","고"].index(st.session_state.filter_budget))
        st.session_state.filter_budget = bd

    filtered_count = len(apply_filters(get_all_menus()))
    total_count    = len(get_all_menus())
    if filtered_count < total_count:
        st.info(f"필터 적용 중: {total_count}개 → **{filtered_count}개** 메뉴 (필터 결과가 0개면 전체 표시)")
    if st.button("🔄 필터 초기화"):
        st.session_state.filter_cal_min = 0; st.session_state.filter_cal_max = 1200
        st.session_state.filter_food_type = "전체"; st.session_state.filter_delivery = "전체"
        st.session_state.filter_budget = "전체"; st.rerun()

st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)

# ── 메인 ─────────────────────────────────────────────────────
menus  = get_menus()
method = st.session_state.active_method
cur_emoji = CATEGORY_EMOJI.get(st.session_state.active_cat, "🍽️")
st.markdown(f"""<div style="display:flex;align-items:center;gap:.6rem;margin-bottom:1rem;">
    <span style="font-size:1.6rem">{cur_emoji}</span>
    <span style="font-size:1.25rem;font-weight:900;color:#1a1a2e">{st.session_state.active_cat}</span>
    <span style="font-size:.85rem;color:#aaa;margin-left:.3rem">({len(menus)}개 메뉴)</span>
</div>""", unsafe_allow_html=True)

if len(menus) < 2:
    st.warning("⚠️ 메뉴가 2개 이상 필요합니다. 필터를 완화하거나 다른 카테고리를 선택하세요.")
elif method is None:
    METHODS = [
        ("random",   "랜덤",       "버튼 한 번에 즉시 추천",          "🎲"),
        ("roulette", "룰렛",       "회전하는 룰렛 바퀴",              "🎡"),
        ("scratch",  "스크래치",   "마우스로 직접 긁어서 확인",        "🎁"),
        ("worldcup", "월드컵",     "1:1 대결로 최후의 1개",           "🏆"),
        ("dice",     "주사위",     "주사위 굴려서 결정",              "🎲"),
        ("tarot",    "카드 뽑기",  "타로카드 스타일 3장 중 선택",     "🃏"),
        ("smart",    "스마트 추천","최근 안 먹은 메뉴 위주 추천",     "🧠"),
        ("battle",   "대결 모드",  "두 사람 의견, 랜덤 결정",     "⚔️"),
    ]
    rows = [st.columns(4, gap="medium") for _ in range(2)]
    for idx, (key, label, desc, emoji) in enumerate(METHODS):
        with rows[idx // 4][idx % 4]:
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
                if key == "tarot":
                    st.session_state.tarot_cards  = random.sample(menus, min(3, len(menus)))
                    st.session_state.tarot_chosen = None
                st.rerun()
else:
    if st.button("← 돌아가기", key="back"):
        reset_method(); st.rerun()

    # ── 랜덤 ─────────────────────────────────────────────────
    if method == "random":
        st.markdown("### 🎲 랜덤 추천")
        if st.button("🎲 지금 바로 추천!", type="primary", use_container_width=True):
            st.session_state._random_result = random.choice(menus)
            st.rerun()
        if st.session_state._random_result:
            r = st.session_state._random_result
            result_card(r, "🎲 랜덤")
            adopt_button(r, "🎲 랜덤", key_suffix=f"random_{r['name']}")
            if st.button("🔄 다시 추천", use_container_width=True):
                st.session_state._random_result = random.choice(menus)
                st.rerun()

    # ── 룰렛 (Canvas 회전 바퀴) ───────────────────────────────
    elif method == "roulette":
        st.markdown("### 🎡 룰렛 바퀴")

        winner_idx = random.randint(0, len(menus) - 1)
        if not st.session_state.roulette_done:
            st.session_state.roulette_winner_idx = winner_idx

        menu_names = [m["name"] for m in menus]
        menu_emojis = [m.get("emoji", "🍽️") for m in menus]

        import json
        names_json = json.dumps(menu_names, ensure_ascii=False)
        emojis_json = json.dumps(menu_emojis, ensure_ascii=False)
        target_idx = st.session_state.roulette_winner_idx
        already_done = "true" if st.session_state.roulette_done else "false"

        roulette_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:transparent; font-family:'Noto Sans KR',sans-serif; display:flex; flex-direction:column; align-items:center; padding:20px 10px; }}
  #roulette-wrap {{ position:relative; width:340px; height:340px; }}
  #wheel-canvas {{ border-radius:50%; box-shadow:0 8px 40px rgba(102,126,234,0.45); display:block; }}
  #needle {{ position:absolute; top:-18px; left:50%; transform:translateX(-50%); width:0; height:0;
    border-left:14px solid transparent; border-right:14px solid transparent;
    border-top:38px solid #f5576c;
    filter:drop-shadow(0 4px 8px rgba(245,87,108,0.6));
    z-index:10; }}
  #center-dot {{ position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
    width:28px; height:28px; background:white; border-radius:50%;
    box-shadow:0 2px 10px rgba(0,0,0,0.2); z-index:10; }}
  #spin-btn {{ margin-top:24px; padding:14px 56px; font-size:1.1rem; font-weight:800;
    background:linear-gradient(135deg,#667eea,#764ba2); color:white; border:none;
    border-radius:999px; cursor:pointer; box-shadow:0 6px 24px rgba(102,126,234,0.4);
    transition:transform .15s, box-shadow .15s; font-family:'Noto Sans KR',sans-serif; }}
  #spin-btn:hover {{ transform:translateY(-2px); box-shadow:0 10px 32px rgba(102,126,234,0.55); }}
  #spin-btn:disabled {{ opacity:0.5; cursor:not-allowed; transform:none; }}
  #result-box {{ margin-top:20px; padding:16px 32px; background:linear-gradient(135deg,#667eea,#764ba2);
    border-radius:16px; color:white; text-align:center; display:none; animation:fadeUp .5s ease; }}
  #result-box .r-emoji {{ font-size:2.4rem; }}
  #result-box .r-name {{ font-size:1.4rem; font-weight:900; margin-top:6px; }}
  @keyframes fadeUp {{ from {{ opacity:0; transform:translateY(16px); }} to {{ opacity:1; transform:translateY(0); }} }}
  #send-btn {{ margin-top:12px; padding:10px 32px; font-size:.95rem; font-weight:700;
    background:rgba(255,255,255,0.25); color:white; border:2px solid rgba(255,255,255,0.5);
    border-radius:999px; cursor:pointer; font-family:'Noto Sans KR',sans-serif; }}
  #send-btn:hover {{ background:rgba(255,255,255,0.4); }}
</style>
</head>
<body>
<div id="roulette-wrap">
  <div id="needle"></div>
  <canvas id="wheel-canvas" width="340" height="340"></canvas>
  <div id="center-dot"></div>
</div>
<button id="spin-btn">🎡 룰렛 돌리기!</button>
<div id="result-box">
  <div class="r-emoji" id="r-emoji"></div>
  <div class="r-name" id="r-name"></div>
  <button id="send-btn">✅ 이 메뉴로 결정!</button>
</div>

<script>
const NAMES = {names_json};
const EMOJIS = {emojis_json};
const TARGET_IDX = {target_idx};
const ALREADY_DONE = {already_done};
const N = NAMES.length;
const COLORS = [
  '#667eea','#764ba2','#f093fb','#f5576c','#4facfe','#00f2fe',
  '#43e97b','#38f9d7','#fa709a','#fee140','#a18cd1','#fbc2eb',
  '#a1c4fd','#c2e9fb','#fd746c','#ff9a9e','#ffecd2','#fcb69f'
];

const canvas = document.getElementById('wheel-canvas');
const ctx = canvas.getContext('2d');
const spinBtn = document.getElementById('spin-btn');
const resultBox = document.getElementById('result-box');
const rEmoji = document.getElementById('r-emoji');
const rName = document.getElementById('r-name');
const sendBtn = document.getElementById('send-btn');

const sliceAngle = (2 * Math.PI) / N;
let currentAngle = 0;
let spinning = false;
let finalAngle = 0;

function drawWheel(angle) {{
  ctx.clearRect(0, 0, 340, 340);
  const cx = 170, cy = 170, r = 165;
  for (let i = 0; i < N; i++) {{
    const start = angle + i * sliceAngle;
    const end = start + sliceAngle;
    // slice
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, r, start, end);
    ctx.closePath();
    ctx.fillStyle = COLORS[i % COLORS.length];
    ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,0.6)';
    ctx.lineWidth = 2;
    ctx.stroke();
    // text
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(start + sliceAngle / 2);
    ctx.textAlign = 'right';
    ctx.fillStyle = 'white';
    ctx.font = 'bold 13px "Noto Sans KR", sans-serif';
    ctx.shadowColor = 'rgba(0,0,0,0.4)';
    ctx.shadowBlur = 4;
    const label = EMOJIS[i] + ' ' + (NAMES[i].length > 6 ? NAMES[i].slice(0,6)+'…' : NAMES[i]);
    ctx.fillText(label, r - 12, 5);
    ctx.restore();
  }}
  // outer ring
  ctx.beginPath();
  ctx.arc(cx, cy, r, 0, 2*Math.PI);
  ctx.strokeStyle = 'rgba(255,255,255,0.8)';
  ctx.lineWidth = 4;
  ctx.stroke();
}}

drawWheel(0);

// The needle points DOWN from top = angle 3π/2 = 270°
// So the winning slice center should be at 3π/2
// slice i center angle (from wheel's 0) = i * sliceAngle + sliceAngle/2
// We want: currentAngle + i*sliceAngle + sliceAngle/2 = 3π/2  (mod 2π)
// => currentAngle = 3π/2 - i*sliceAngle - sliceAngle/2

function spin() {{
  if (spinning) return;
  spinning = true;
  spinBtn.disabled = true;

  const targetAngle = (3 * Math.PI / 2) - TARGET_IDX * sliceAngle - sliceAngle / 2;
  const extraSpins = (5 + Math.floor(Math.random() * 4)) * 2 * Math.PI;
  finalAngle = targetAngle + extraSpins;

  const duration = 4500;
  const start = performance.now();
  const startAngle = currentAngle;

  function easeOut(t) {{
    return 1 - Math.pow(1 - t, 4);
  }}

  function animate(now) {{
    const elapsed = now - start;
    const t = Math.min(elapsed / duration, 1);
    currentAngle = startAngle + (finalAngle - startAngle) * easeOut(t);
    drawWheel(currentAngle);
    if (t < 1) {{
      requestAnimationFrame(animate);
    }} else {{
      spinning = false;
      currentAngle = finalAngle % (2 * Math.PI);
      showResult();
    }}
  }}
  requestAnimationFrame(animate);
}}

function showResult() {{
  rEmoji.textContent = EMOJIS[TARGET_IDX];
  rName.textContent = NAMES[TARGET_IDX];
  resultBox.style.display = 'block';
}}

if (ALREADY_DONE) {{
  // restore to final position and show result
  const targetAngle = (3 * Math.PI / 2) - TARGET_IDX * sliceAngle - sliceAngle / 2;
  currentAngle = targetAngle % (2 * Math.PI);
  drawWheel(currentAngle);
  showResult();
  spinBtn.textContent = '🔄 다시 돌리기';
  spinBtn.disabled = false;
  spinBtn.onclick = function() {{
    resultBox.style.display = 'none';
    window.parent.postMessage({{type:'streamlit:setComponentValue', value: 'respin'}}, '*');
  }};
}} else {{
  spinBtn.onclick = function() {{
    spin();
    spinBtn.textContent = '🔄 다시 돌리기';
    window.parent.postMessage({{type:'streamlit:setComponentValue', value: 'spinning:' + TARGET_IDX}}, '*');
  }};
}}

sendBtn.onclick = function() {{
  window.parent.postMessage({{type:'streamlit:setComponentValue', value: 'adopt:' + TARGET_IDX}}, '*');
}};
</script>
</body>
</html>
"""

        result = components.html(roulette_html, height=520, scrolling=False)

        if not st.session_state.roulette_done:
            st.info("💡 룰렛 바퀴를 돌려서 오늘의 메뉴를 결정하세요!")
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("🎡 Python으로 룰렛 돌리기!", key="roulette_spin_py", type="primary", use_container_width=True):
                    st.session_state.roulette_winner = menus[st.session_state.roulette_winner_idx]
                    st.session_state.roulette_done = True
                    st.rerun()
        else:
            winner = st.session_state.roulette_winner
            st.balloons()
            result_card(winner, "🎡 룰렛 추천")
            adopt_button(winner, "🎡 룰렛", key_suffix="roulette_win")
            if st.button("🔄 다시 돌리기", use_container_width=True):
                st.session_state.roulette_done = False
                st.session_state.roulette_winner = None
                st.session_state.roulette_winner_idx = random.randint(0, len(menus)-1)
                st.rerun()

    # ── 스크래치 (Canvas 진짜 긁기) ─────────────────────────────
    elif method == "scratch":
        st.markdown("### 🎁 스크래치 복권")

        if not st.session_state.scratch_menu:
            st.session_state.scratch_menu = random.choice(menus)

        menu = st.session_state.scratch_menu
        menu_name = menu["name"]
        menu_emoji = menu.get("emoji", "🍽️")
        menu_cal = menu.get("cal", 0)

        scratch_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:transparent; font-family:'Noto Sans KR',sans-serif;
    display:flex; flex-direction:column; align-items:center; padding:20px 10px; }}
  #scratch-wrap {{ position:relative; width:360px; height:220px; border-radius:20px;
    overflow:hidden; box-shadow:0 8px 40px rgba(0,0,0,0.2); cursor:crosshair; user-select:none; }}
  #result-layer {{ position:absolute; inset:0; background:linear-gradient(135deg,#667eea,#764ba2);
    display:flex; flex-direction:column; align-items:center; justify-content:center; }}
  #result-emoji {{ font-size:3.2rem; line-height:1; }}
  #result-name {{ font-size:1.8rem; font-weight:900; color:white; margin-top:8px; text-shadow:0 2px 8px rgba(0,0,0,0.3); }}
  #result-cal {{ font-size:.9rem; color:rgba(255,255,255,0.8); margin-top:4px; }}
  #scratch-canvas {{ position:absolute; inset:0; }}
  #hint {{ margin-top:14px; font-size:.9rem; color:#888; font-weight:600; text-align:center; }}
  #pct-bar-wrap {{ width:360px; height:10px; background:#e0e0e0; border-radius:999px; margin-top:10px; overflow:hidden; }}
  #pct-bar {{ height:10px; background:linear-gradient(90deg,#667eea,#f5576c); border-radius:999px; width:0%; transition:width .1s; }}
  #done-msg {{ margin-top:14px; font-size:1rem; font-weight:800; color:#667eea; display:none; animation:pop .4s cubic-bezier(.175,.885,.32,1.275); }}
  @keyframes pop {{ from {{ transform:scale(0.5); opacity:0; }} to {{ transform:scale(1); opacity:1; }} }}
  #adopt-btn {{ margin-top:14px; padding:12px 44px; font-size:1rem; font-weight:800;
    background:linear-gradient(135deg,#667eea,#764ba2); color:white; border:none;
    border-radius:999px; cursor:pointer; display:none; font-family:'Noto Sans KR',sans-serif;
    box-shadow:0 6px 20px rgba(102,126,234,0.4); animation:pop .4s .1s both cubic-bezier(.175,.885,.32,1.275); }}
  #adopt-btn:hover {{ filter:brightness(1.1); }}
  #retry-btn {{ margin-top:8px; padding:8px 28px; font-size:.9rem; font-weight:700;
    background:white; color:#667eea; border:2px solid #667eea;
    border-radius:999px; cursor:pointer; display:none; font-family:'Noto Sans KR',sans-serif; }}
</style>
</head>
<body>
<div id="scratch-wrap">
  <div id="result-layer">
    <div id="result-emoji">{menu_emoji}</div>
    <div id="result-name">{menu_name}</div>
    <div id="result-cal">🔥 {menu_cal} kcal</div>
  </div>
  <canvas id="scratch-canvas" width="360" height="220"></canvas>
</div>
<div id="hint">🖱️ 마우스 또는 손가락으로 긁어보세요!</div>
<div id="pct-bar-wrap"><div id="pct-bar"></div></div>
<div id="done-msg">🎉 완전히 긁었어요!</div>
<button id="adopt-btn">✅ {menu_name} (으)로 결정!</button>
<button id="retry-btn">🔄 다시 뽑기</button>

<script>
const canvas = document.getElementById('scratch-canvas');
const ctx = canvas.getContext('2d');
const W = 360, H = 220;

// Draw scratch layer - shiny silver scratch card style
const grad = ctx.createLinearGradient(0, 0, W, H);
grad.addColorStop(0, '#c0c0c0');
grad.addColorStop(0.3, '#e8e8e8');
grad.addColorStop(0.5, '#f5f5f5');
grad.addColorStop(0.7, '#d0d0d0');
grad.addColorStop(1, '#a8a8a8');
ctx.fillStyle = grad;
ctx.fillRect(0, 0, W, H);

// Pattern on top
ctx.fillStyle = 'rgba(0,0,0,0.06)';
for (let x = 0; x < W; x += 28) {{
  for (let y = 0; y < H; y += 28) {{
    ctx.beginPath();
    ctx.arc(x, y, 3, 0, Math.PI*2);
    ctx.fill();
  }}
}}

// Text on scratch layer
ctx.fillStyle = 'rgba(120,120,120,0.7)';
ctx.font = 'bold 22px "Noto Sans KR",sans-serif';
ctx.textAlign = 'center';
ctx.fillText('🎁 긁어서 메뉴 확인!', W/2, H/2 - 10);
ctx.font = '14px "Noto Sans KR",sans-serif';
ctx.fillText('← SCRATCH HERE →', W/2, H/2 + 20);

ctx.globalCompositeOperation = 'destination-out';

let isDrawing = false;
let totalPixels = W * H;
let scratchedPct = 0;
let revealed = false;

function getPos(e) {{
  const rect = canvas.getBoundingClientRect();
  const scaleX = W / rect.width;
  const scaleY = H / rect.height;
  if (e.touches) {{
    return {{ x: (e.touches[0].clientX - rect.left) * scaleX, y: (e.touches[0].clientY - rect.top) * scaleY }};
  }}
  return {{ x: (e.clientX - rect.left) * scaleX, y: (e.clientY - rect.top) * scaleY }};
}}

function scratch(e) {{
  if (!isDrawing) return;
  e.preventDefault();
  const pos = getPos(e);
  ctx.beginPath();
  ctx.arc(pos.x, pos.y, 28, 0, Math.PI*2);
  ctx.fill();
  checkProgress();
}}

function checkProgress() {{
  const imageData = ctx.getImageData(0, 0, W, H);
  let transparent = 0;
  for (let i = 3; i < imageData.data.length; i += 4) {{
    if (imageData.data[i] === 0) transparent++;
  }}
  scratchedPct = Math.min((transparent / totalPixels) * 100, 100);
  document.getElementById('pct-bar').style.width = scratchedPct + '%';

  if (scratchedPct > 60 && !revealed) {{
    revealed = true;
    // Clear all
    ctx.clearRect(0, 0, W, H);
    document.getElementById('hint').style.display = 'none';
    document.getElementById('done-msg').style.display = 'block';
    document.getElementById('adopt-btn').style.display = 'inline-block';
    document.getElementById('retry-btn').style.display = 'inline-block';
  }}
}}

canvas.addEventListener('mousedown', e => {{ isDrawing = true; scratch(e); }});
canvas.addEventListener('mousemove', scratch);
canvas.addEventListener('mouseup', () => isDrawing = false);
canvas.addEventListener('mouseleave', () => isDrawing = false);
canvas.addEventListener('touchstart', e => {{ isDrawing = true; scratch(e); }}, {{passive:false}});
canvas.addEventListener('touchmove', scratch, {{passive:false}});
canvas.addEventListener('touchend', () => isDrawing = false);

document.getElementById('adopt-btn').onclick = function() {{
  window.parent.postMessage({{type:'streamlit:setComponentValue', value: 'adopt'}}, '*');
}};
document.getElementById('retry-btn').onclick = function() {{
  window.parent.postMessage({{type:'streamlit:setComponentValue', value: 'retry'}}, '*');
}};
</script>
</body>
</html>
"""

        comp_result = components.html(scratch_html, height=400, scrolling=False)

        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ 이 메뉴로 결정!", key="scratch_adopt", type="primary", use_container_width=True):
                add_history(menu, "🎁 스크래치")
                st.success(f"🎉 **{menu['name']}** 이(가) 오늘의 메뉴로 기록됐어요!")
                reset_method()
                st.rerun()
        with col2:
            if st.button("🔄 다시 뽑기", key="scratch_retry", use_container_width=True):
                st.session_state.scratch_menu = random.choice(menus)
                st.rerun()

    # ── 월드컵 ───────────────────────────────────────────────
    elif method == "worldcup":
        ts = st.session_state.tournament_state
        if ts is None:
            st.error("토너먼트 초기화 오류.")
        elif len(ts["round"]) == 1:
            st.markdown("### 🏆 최종 우승!")
            st.balloons()
            winner = ts["round"][0]
            result_card(winner, "🏆 월드컵 우승")
            adopt_button(winner, "🏆 월드컵", key_suffix=f"wc_{winner['name']}")
            if st.button("🔄 다시 하기", use_container_width=True):
                pool = random.sample(menus, min(8, len(menus)))
                if len(pool) % 2 == 1: pool = pool[:-1]
                st.session_state.tournament_state = {"round": pool, "pair_idx": 0, "winners": []}
                st.rerun()
        else:
            pairs = [(ts["round"][i], ts["round"][i+1]) for i in range(0, len(ts["round"])-1, 2)]
            idx   = ts["pair_idx"]
            if idx >= len(pairs):
                nr = ts["winners"][:]
                if len(nr) % 2 == 1 and len(nr) > 1: nr = nr[:-1]
                ts["round"] = nr; ts["winners"] = []; ts["pair_idx"] = 0; st.rerun()
            else:
                a, b = pairs[idx]; n = len(ts["round"])
                st.markdown(f"### 🏆 {n}강 — {idx+1} / {len(pairs)} 경기"); st.progress(idx / len(pairs))
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

    # ── 주사위 ──────────────────────────────────────────────
    elif method == "dice":
        st.markdown("### 🎲 주사위")
        if not st.session_state.get('dice_winner'):
            st.markdown("""<div style="display:flex;flex-direction:column;align-items:center;padding:2.5rem 0;opacity:0.35;">
                <div style="font-size:7.5rem; line-height:1; color:#555;">⚀</div>
                <div style="font-size:0.95rem; font-weight:600; margin-top:0.8rem;">아래 버튼을 눌러 주사위를 굴려보세요!</div>
            </div>""", unsafe_allow_html=True)
            if st.button("🎲 주사위 굴리기!", type="primary", use_container_width=True):
                st.session_state.dice_winner = random.choice(menus)
                st.session_state.dice_face = random.randint(1, 6)
                st.rerun()
        else:
            winner = st.session_state.dice_winner
            face = st.session_state.dice_face
            faces = ['⚀','⚁','⚂','⚃','⚄','⚅']
            st.markdown(f"""<div style="display:flex;flex-direction:column;align-items:center;padding:1.5rem 0;">
                <div style="font-size:7.5rem; line-height:1; color:#1a1a2e;">{faces[face-1]}</div>
                <div style="font-size:1.1rem; font-weight:800; color:#667eea; margin-top:0.8rem;">주사위 {face} → 당첨!</div>
            </div>""", unsafe_allow_html=True)
            st.markdown("---")
            result_card(winner, f"🎲 주사위 추천 (숫자 {face})")
            adopt_button(winner, "🎲 주사위", key_suffix="dice_live")
            if st.button("🔄 다시 굴리기", use_container_width=True):
                st.session_state.dice_winner = None
                st.rerun()

    # ── 카드 뽑기 ────────────────────────────────────────────
    elif method == "tarot":
        st.markdown("### 🃏 카드 뽑기")
        if not st.session_state.tarot_cards:
            st.session_state.tarot_cards  = random.sample(menus, min(3, len(menus)))
            st.session_state.tarot_chosen = None
        cards = st.session_state.tarot_cards; chosen = st.session_state.tarot_chosen
        if chosen is None:
            st.markdown("<p style='color:#555;text-align:center;font-size:1rem'>✨ 세 장의 카드 중 하나를 고르세요</p>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            for ci, (col, card) in enumerate(zip([c1,c2,c3], cards)):
                with col:
                    st.markdown(f"""<div style="background:linear-gradient(135deg,#667eea,#764ba2);border-radius:16px;padding:2rem 1rem;text-align:center;cursor:pointer;box-shadow:0 6px 20px rgba(102,126,234,.35);">
                        <div style="font-size:3rem">🎴</div>
                        <div style="color:white;font-weight:700;margin-top:.5rem">카드 {ci+1}</div>
                    </div>""", unsafe_allow_html=True)
                    if st.button(f"카드 {ci+1} 선택", key=f"tarot_{ci}", use_container_width=True, type="primary"):
                        st.session_state.tarot_chosen = card
                        st.rerun()
        else:
            result_card(chosen, "🃏 카드뽑기")
            adopt_button(chosen, "🃏 카드뽑기", key_suffix=f"tarot_{chosen['name']}")
            st.markdown("<p style='text-align:center;color:#555;margin-top:.5rem'>다른 카드엔 무엇이 있었을까요?</p>", unsafe_allow_html=True)
            others = [c for c in cards if c != chosen]
            ocols = st.columns(len(others))
            for col, card in zip(ocols, others):
                with col:
                    st.markdown(f"""<div style="background:#e8eaf6;border-radius:12px;padding:1rem;text-align:center;opacity:.7">
                        <div style="font-size:2rem">{card['emoji']}</div>
                        <div style="font-weight:700;color:#555">{card['name']}</div>
                        <div style="font-size:.8rem;color:#aaa">🔥 {card['cal']} kcal</div>
                    </div>""", unsafe_allow_html=True)
            if st.button("🔄 다시 뽑기", use_container_width=True, type="secondary"):
                st.session_state.tarot_cards  = random.sample(menus, min(3, len(menus)))
                st.session_state.tarot_chosen = None
                st.rerun()

    # ── 스마트 추천 ──────────────────────────────────────────
    elif method == "smart":
        st.markdown("### 🧠 스마트 추천")
        recent_names = {h["menu"] for h in st.session_state.history[:10]}
        fresh = [m for m in menus if m["name"] not in recent_names] or menus
        st.markdown(f"""<div style="background:#f0f8ff;border-radius:12px;padding:1rem;margin-bottom:1rem;border-left:4px solid #4facfe;">
            <p style="margin:0;color:#333;font-size:.9rem">💡 최근 이력 <b>{len(recent_names)}</b>개 분석 완료 · <b>{len(fresh)}</b>개 새 메뉴 중 추천</p>
        </div>""", unsafe_allow_html=True)
        if st.button("🧠 스마트 추천 받기", type="primary", use_container_width=True):
            st.session_state._random_result = random.choice(fresh)
            st.rerun()
        if st.session_state._random_result:
            r = st.session_state._random_result
            result_card(r, "🧠 스마트 추천")
            adopt_button(r, "🧠 스마트 추천", key_suffix=f"smart_{r['name']}")
        if recent_names:
            with st.expander("📋 최근 먹은 메뉴 (제외 목록)"):
                cols = st.columns(3)
                for i, n in enumerate(list(recent_names)):
                    with cols[i % 3]: st.markdown(f"- {n}")

    # ── 대결 모드 ─────────────────────────────────────────────
    elif method == "battle":
        st.markdown("### ⚔️ 대결 모드")
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
        if st.button("⚔️ 랜덤 결정!", type="primary", use_container_width=True):
            a_menu = next((m for m in menus if m["name"] == a_pick), None)
            b_menu = next((m for m in menus if m["name"] == b_pick), None)
            if a_menu and b_menu:
                winner = random.choice([a_menu, b_menu])
                st.session_state.battle_result = {"winner": winner, "a": a_menu, "b": b_menu}
                st.rerun()
        if st.session_state.battle_result:
            br = st.session_state.battle_result; winner = br["winner"]; loser = br["b"] if winner == br["a"] else br["a"]
            st.balloons()
            st.markdown(f"""<div style="text-align:center;margin:.5rem 0 1rem;font-size:1rem;color:#888">
                {br['a']['emoji']} {br['a']['name']} &nbsp;⚔️&nbsp; {br['b']['emoji']} {br['b']['name']}</div>""", unsafe_allow_html=True)
            result_card(winner, "⚔️ 대결 승리!")
            adopt_button(winner, "⚔️ 대결", key_suffix=f"battle_{winner['name']}")
            st.markdown(f"<p style='text-align:center;color:#aaa;margin-top:.5rem'>😔 {loser['name']} 는 다음 기회에...</p>", unsafe_allow_html=True)

# ── 하단 탭 ──────────────────────────────────────────────────
st.markdown("<hr style='border:none;border-top:2px solid #ddd;margin:1.5rem 0 1rem'>", unsafe_allow_html=True)
tab_hist, tab_tracker, tab_rank, tab_analysis, tab_feed, tab_mgmt = st.tabs([
    "📋 추천 이력", "🔥 칼로리 트래커", "🏅 메뉴 랭킹", "📊 식습관 분석", "💡 추천 피드", "🔧 메뉴 관리"
])

# ── 추천 이력 ─────────────────────────────────────────────────
with tab_hist:
    if st.session_state.history:
        c1, c2, c3 = st.columns(3)
        methods_l = [h["method"] for h in st.session_state.history]
        menus_l   = [h["menu"]   for h in st.session_state.history]
        with c1: st.metric("총 채택 횟수", f"{len(st.session_state.history)}회")
        with c2: st.metric("자주 쓴 방식",  max(set(methods_l), key=methods_l.count))
        with c3: st.metric("최다 채택 메뉴", max(set(menus_l),   key=menus_l.count))
        st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
        for h in st.session_state.history:
            st.markdown(f"""<div class="hist-item">
                <div>{h['emoji']} <b style="color:#111">{h['menu']}</b>
                <span style="color:#aaa;font-size:.82rem"> · {h['time']} · {h['method']} · {h['cat']}</span></div>
                <div style="color:#667eea;font-weight:700">{h['cal']} kcal</div>
            </div>""", unsafe_allow_html=True)
        if st.button("🗑️ 이력 초기화"):
            st.session_state.history = []; st.rerun()
    else:
        st.info("아직 채택한 메뉴가 없어요! 추천 결과에서 '✅ 이 메뉴로 결정!' 버튼을 눌러 기록하세요.")

# ── 칼로리 트래커 ─────────────────────────────────────────────
with tab_tracker:
    today = date.today().isoformat()
    today_entries = [e for e in st.session_state.today_log if e["date"] == today]
    total_cal = sum(e["cal"] for e in today_entries)
    goal_cal  = 2000
    pct = min(total_cal / goal_cal, 1.0)
    color = "#43e97b" if pct < 0.7 else "#fee140" if pct < 0.9 else "#f5576c"
    st.markdown(f"### 오늘({today}) 칼로리")
    st.markdown(f"""<div style="margin-bottom:.5rem">
        <div style="display:flex;justify-content:space-between;margin-bottom:.3rem">
            <span style="font-weight:700;color:#1a1a2e">{total_cal} kcal 섭취</span>
            <span style="color:#aaa">목표: {goal_cal} kcal</span>
        </div>
        <div class="cal-bar-wrap"><div class="cal-bar" style="width:{pct*100:.1f}%;background:{color}"></div></div>
        <div style="text-align:right;font-size:.82rem;color:#aaa;margin-top:.2rem">{pct*100:.0f}%</div>
    </div>""", unsafe_allow_html=True)
    if today_entries:
        st.markdown("**오늘 채택한 메뉴**")
        for e in today_entries:
            st.markdown(f"""<div class="hist-item">
                <div>{e['emoji']} <b style="color:#111">{e['menu']}</b>
                <span style="color:#aaa;font-size:.82rem"> · {e['time']}</span></div>
                <div style="color:#f5576c;font-weight:700">+{e['cal']} kcal</div>
            </div>""", unsafe_allow_html=True)
        if st.button("🗑️ 오늘 기록 초기화"):
            st.session_state.today_log = [e for e in st.session_state.today_log if e["date"] != today]; st.rerun()
    else:
        st.info("오늘 아직 채택한 메뉴가 없어요!")
    if st.session_state.today_log:
        st.markdown("**최근 7일 칼로리**")
        daily = defaultdict(int)
        for e in st.session_state.today_log: daily[e["date"]] += e["cal"]
        sorted_days = sorted(daily.keys())[-7:]; max_cal = max(daily.values())
        for d in sorted_days:
            bw = daily[d] / max_cal * 100; label = "오늘" if d == today else d[5:]
            st.markdown(f"""<div style="display:flex;align-items:center;gap:.8rem;margin:.3rem 0">
                <span style="width:3rem;font-size:.82rem;color:#555">{label}</span>
                <div style="flex:1;background:#f0f2f8;border-radius:6px;height:20px;overflow:hidden">
                    <div style="width:{bw:.1f}%;background:linear-gradient(90deg,#667eea,#f5576c);height:20px;border-radius:6px"></div>
                </div>
                <span style="width:4rem;text-align:right;font-size:.82rem;color:#667eea;font-weight:700">{daily[d]} kcal</span>
            </div>""", unsafe_allow_html=True)

# ── 메뉴 랭킹 ─────────────────────────────────────────────────
with tab_rank:
    st.markdown("### 🏅 메뉴 랭킹")
    if st.session_state.history:
        cnt = Counter(h["menu"] for h in st.session_state.history)
        top = cnt.most_common(10); max_cnt = top[0][1]
        medals = ["🥇","🥈","🥉"] + ["🏅"]*7
        for rank, (name, count) in enumerate(top):
            emoji = next((h["emoji"] for h in st.session_state.history if h["menu"]==name), "🍽️")
            bw = count / max_cnt * 100
            st.markdown(f"""<div class="rank-card">
                <div class="rank-num">{medals[rank]}</div>
                <div style="font-size:1.5rem">{emoji}</div>
                <div style="flex:1"><div style="font-weight:700;color:#1a1a2e">{name}</div>
                <div class="cal-bar-wrap" style="margin-top:.3rem"><div class="cal-bar" style="width:{bw:.1f}%"></div></div></div>
                <div style="color:#667eea;font-weight:700;white-space:nowrap">{count}회</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("### 📊 방식별 통계")
        mc = Counter(h["method"] for h in st.session_state.history); mm = max(mc.values())
        for mn, mv in mc.most_common():
            bw = mv / mm * 100
            st.markdown(f"""<div style="display:flex;align-items:center;gap:.8rem;margin:.3rem 0">
                <span style="width:8rem;font-size:.85rem;color:#555">{mn}</span>
                <div style="flex:1;background:#f0f2f8;border-radius:6px;height:18px;overflow:hidden">
                    <div style="width:{bw:.1f}%;background:linear-gradient(90deg,#667eea,#764ba2);height:18px;border-radius:6px"></div>
                </div>
                <span style="width:2.5rem;text-align:right;font-size:.82rem;color:#667eea;font-weight:700">{mv}회</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("채택한 메뉴가 쌓이면 랭킹이 표시돼요!")

# ── 식습관 분석 ───────────────────────────────────────────────
with tab_analysis:
    st.markdown("### 📊 나의 식습관 분석")
    if len(st.session_state.history) >= 3:
        hist = st.session_state.history
        avg_cal = sum(h["cal"] for h in hist) // len(hist)
        max_cal_entry = max(hist, key=lambda h: h["cal"])
        min_cal_entry = min(hist, key=lambda h: h["cal"])
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""<div class="info-card" style="text-align:center">
                <div style="font-size:2rem">🔥</div>
                <div style="font-size:.85rem;color:#888;margin:.3rem 0">평균 칼로리</div>
                <div style="font-size:1.8rem;font-weight:900;color:#f5576c">{avg_cal} kcal</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            top_cat = Counter(h["cat"] for h in hist).most_common(1)[0][0]
            cat_emoji = CATEGORY_EMOJI.get(top_cat, "🍽️")
            st.markdown(f"""<div class="info-card" style="text-align:center">
                <div style="font-size:2rem">{cat_emoji}</div>
                <div style="font-size:.85rem;color:#888;margin:.3rem 0">가장 많이 먹는 카테고리</div>
                <div style="font-size:1.3rem;font-weight:900;color:#667eea">{top_cat}</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            top_type = Counter(h.get("food_type","기타") for h in hist).most_common(1)[0][0]
            type_emoji = {"밥":"🍚","면":"🍜","고기":"🥩","기타":"🍽️"}.get(top_type,"🍽️")
            st.markdown(f"""<div class="info-card" style="text-align:center">
                <div style="font-size:2rem">{type_emoji}</div>
                <div style="font-size:.85rem;color:#888;margin:.3rem 0">선호 음식 종류</div>
                <div style="font-size:1.8rem;font-weight:900;color:#43e97b">{top_type}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("**⏰ 추천 시간대 패턴**")
        hour_cnt = Counter(h.get("hour", 12) for h in hist)
        time_slots = {"아침 (6-9시)": range(6,10), "점심 (10-14시)": range(10,15),
                      "오후 (15-17시)": range(15,18), "저녁 (18-21시)": range(18,22),
                      "야식 (22-5시)": list(range(22,24))+list(range(0,6))}
        slot_counts = {slot: sum(hour_cnt.get(h,0) for h in hours) for slot, hours in time_slots.items()}
        max_slot = max(slot_counts.values()) if slot_counts else 1
        for slot, count in slot_counts.items():
            if count > 0:
                bw = count / max_slot * 100
                st.markdown(f"""<div style="display:flex;align-items:center;gap:.8rem;margin:.3rem 0">
                    <span style="width:8rem;font-size:.85rem;color:#555">{slot}</span>
                    <div style="flex:1;background:#f0f2f8;border-radius:6px;height:18px;overflow:hidden">
                        <div style="width:{bw:.1f}%;background:linear-gradient(90deg,#4facfe,#667eea);height:18px;border-radius:6px"></div>
                    </div>
                    <span style="width:2rem;text-align:right;font-size:.82rem;color:#667eea;font-weight:700">{count}회</span>
                </div>""", unsafe_allow_html=True)
        st.markdown("**🏆 칼로리 기록**")
        col_hi, col_lo = st.columns(2)
        with col_hi:
            st.markdown(f"""<div class="info-card">
                <div style="font-size:.85rem;color:#888">🔥 최고 칼로리</div>
                <div style="font-size:1.2rem;font-weight:700;margin:.3rem 0">{max_cal_entry['emoji']} {max_cal_entry['menu']}</div>
                <div style="color:#f5576c;font-weight:700">{max_cal_entry['cal']} kcal</div>
            </div>""", unsafe_allow_html=True)
        with col_lo:
            st.markdown(f"""<div class="info-card">
                <div style="font-size:.85rem;color:#888">🥗 최저 칼로리</div>
                <div style="font-size:1.2rem;font-weight:700;margin:.3rem 0">{min_cal_entry['emoji']} {min_cal_entry['menu']}</div>
                <div style="color:#43e97b;font-weight:700">{min_cal_entry['cal']} kcal</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("📊 분석을 위해 메뉴를 3회 이상 채택해보세요!")

# ── 추천 피드 ─────────────────────────────────────────────────
with tab_feed:
    st.markdown("### 💡 추천 피드")
    st.markdown("**🔄 최근 채택한 메뉴 다시 먹기**")
    if st.session_state.history:
        recent = st.session_state.history[:5]
        rcols = st.columns(min(len(recent), 5))
        for col, h in zip(rcols, recent):
            with col:
                st.markdown(f"""<div style="background:white;border-radius:12px;padding:.8rem;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.07);">
                    <div style="font-size:1.8rem">{h['emoji']}</div>
                    <div style="font-size:.85rem;font-weight:700;color:#1a1a2e;margin:.3rem 0">{h['menu']}</div>
                    <div style="font-size:.75rem;color:#aaa">{h['cal']} kcal</div>
                </div>""", unsafe_allow_html=True)
                if st.button("다시 먹기", key=f"reorder_{h['menu']}_{h['time']}", use_container_width=True):
                    matched = next((m for cat in MENU_DATA.values() for m in cat if m["name"]==h["menu"]), None)
                    if matched: add_history(matched, "🔄 재먹기"); st.success(f"{h['menu']} 기록됨!"); st.rerun()
    else:
        st.info("채택한 메뉴 이력이 없어요.")
    st.markdown("---")
    st.markdown("**🔗 비슷한 메뉴 추천**")
    if st.session_state.last_result:
        lr = st.session_state.last_result
        last_name = lr["menu"]; last_cal = lr["cal"]; last_type = lr.get("food_type","기타")
        all_flat = [m for cat in MENU_DATA.values() for m in cat]
        similar = [m for m in all_flat
                   if m["name"] != last_name and
                   (m.get("food_type") == last_type or abs(m.get("cal",0) - last_cal) <= 200)]
        similar = random.sample(similar, min(4, len(similar)))
        st.markdown(f"<p style='color:#555;font-size:.9rem'>'{last_name}' 과 비슷한 메뉴들</p>", unsafe_allow_html=True)
        scols = st.columns(len(similar)) if similar else []
        for col, m in zip(scols, similar):
            with col:
                st.markdown(f"""<div style="background:white;border-radius:12px;padding:.8rem;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.07);">
                    <div style="font-size:1.8rem">{m['emoji']}</div>
                    <div style="font-size:.85rem;font-weight:700;color:#1a1a2e;margin:.3rem 0">{m['name']}</div>
                    <div style="font-size:.75rem;color:#aaa">{m['cal']} kcal · {m.get('food_type','')}</div>
                </div>""", unsafe_allow_html=True)
                if st.button("채택", key=f"sim_{m['name']}", use_container_width=True):
                    add_history(m, "🔗 비슷한 메뉴"); st.success(f"{m['name']} 기록됨!"); st.rerun()
    else:
        st.info("먼저 메뉴를 채택하면 비슷한 메뉴를 추천해드려요!")

# ── 메뉴 관리 ─────────────────────────────────────────────────
with tab_mgmt:
    col_add, col_excl = st.columns(2)
    with col_add:
        st.markdown("**➕ 커스텀 메뉴 추가**")
        nm = st.text_input("메뉴 이름", placeholder="예: 순두부찌개", key="add_nm")
        nc = st.number_input("칼로리 (kcal)", 0, 3000, 500, 50, key="add_cal")
        ne = st.text_input("이모지", "🍽️", max_chars=2, key="add_emoji")
        nft = st.selectbox("음식 종류", ["밥","면","고기","기타"], key="add_ft")
        nbd = st.selectbox("예산", ["저","중","고"], key="add_bd")
        ndv = st.checkbox("배달 가능", key="add_dv")
        if st.button("추가", type="primary"):
            if nm.strip():
                st.session_state.custom_menus.append({"name":nm.strip(),"cal":nc,"emoji":ne,"food_type":nft,"budget":nbd,"delivery":ndv})
                st.success(f"'{nm}' 추가 완료!"); st.rerun()
            else: st.error("이름을 입력하세요.")
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
            if chk: st.session_state.excluded.add(m["name"])
            else:   st.session_state.excluded.discard(m["name"])
        if st.session_state.excluded:
            st.markdown(f"<div style='color:#f5576c;font-size:.82rem;margin-top:.5rem'>제외 중: {', '.join(st.session_state.excluded)}</div>", unsafe_allow_html=True)
