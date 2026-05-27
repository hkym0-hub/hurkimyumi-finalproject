import streamlit as st
import streamlit.components.v1 as components
import random
import time
from datetime import datetime, date
from collections import Counter, defaultdict
import json

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
    if not isinstance(st.session_state.excluded, set): st.session_state.excluded = set()
    if not isinstance(st.session_state.history, list): st.session_state.history = []
    if not isinstance(st.session_state.custom_menus, list): st.session_state.custom_menus = []
    if not isinstance(st.session_state.today_log, list): st.session_state.today_log = []
    if st.session_state.active_cat not in MENU_DATA: st.session_state.active_cat = "저녁 메뉴"
init()

# ── 헬퍼 ─────────────────────────────────────────────────────
def get_all_menus():
    if not isinstance(st.session_state.get("excluded"), set): st.session_state.excluded = set()
    if not isinstance(st.session_state.get("custom_menus"), list): st.session_state.custom_menus = []
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
    if len(st.session_state.history) > 50: st.session_state.history = st.session_state.history[:50]
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

# ── UI ───────────────────────────────────────────────────────
st.markdown('<div class="title-pill-wrap"><div class="title-pill">🍽️ 오늘의 추천 메뉴</div></div>', unsafe_allow_html=True)

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

st.markdown('<div style="background:#d966a0;border-radius:14px;padding:.55rem .8rem;margin-bottom:.6rem;"><span style="color:rgba(255,255,255,.7);font-size:.78rem;font-weight:700">카테고리</span></div>', unsafe_allow_html=True)
row_a = st.columns(7); row_b = st.columns(7)
for i, cat in enumerate(CATEGORIES):
    emoji = CATEGORY_EMOJI.get(cat, "🍽️"); short = cat.replace(" 메뉴","")
    with (row_a + row_b)[i]:
        if st.button(f"{emoji} {short}", key=f"cat_{cat}", use_container_width=True, type="primary" if cat == st.session_state.active_cat else "secondary"):
            st.session_state.active_cat = cat; reset_method(); st.rerun()

with st.expander("🔍 조건 필터", expanded=False):
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        cal_range = st.slider("🔥 칼로리 범위 (kcal)", 0, 1200, (st.session_state.filter_cal_min, st.session_state.filter_cal_max), 50)
        st.session_state.filter_cal_min, st.session_state.filter_cal_max = cal_range
    with fc2:
        ft = st.selectbox("🍽️ 음식 종류", ["전체","밥","면","고기","기타"], index=["전체","밥","면","고기","기타"].index(st.session_state.filter_food_type))
        st.session_state.filter_food_type = ft
    with fc3:
        dv = st.selectbox("🛵 조리 / 배달", ["전체","배달만","직접만"], index=["전체","배달만","직접만"].index(st.session_state.filter_delivery))
        st.session_state.filter_delivery = dv
    with fc4:
        bd = st.selectbox("💰 예산", ["전체","저","중","고"], index=["전체","저","중","고"].index(st.session_state.filter_budget))
        st.session_state.filter_budget = bd
    if st.button("🔄 필터 초기화"):
        st.session_state.filter_cal_min = 0; st.session_state.filter_cal_max = 1200
        st.session_state.filter_food_type = "전체"; st.session_state.filter_delivery = "전체"
        st.session_state.filter_budget = "전체"; st.rerun()

st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)

menus = get_menus()
method = st.session_state.active_method
cur_emoji = CATEGORY_EMOJI.get(st.session_state.active_cat, "🍽️")
st.markdown(f"""<div style="display:flex;align-items:center;gap:.6rem;margin-bottom:1rem;">
    <span style="font-size:1.6rem">{cur_emoji}</span>
    <span style="font-size:1.25rem;font-weight:900;color:#1a1a2e">{st.session_state.active_cat}</span>
    <span style="font-size:.85rem;color:#aaa;margin-left:.3rem">({len(menus)}개 메뉴)</span>
</div>""", unsafe_allow_html=True)

if len(menus) < 2:
    st.warning("⚠️ 메뉴가 2개 이상 필요합니다.")
elif method is None:
    METHODS = [
        ("random",   "랜덤",     "버튼 한 번에 즉시 추천",          "🎲"),
        ("roulette", "룰렛",     "회전하는 룰렛 바퀴",               "🎡"),
        ("scratch",  "스크래치",  "마우스로 직접 긁어서 확인",        "🎁"),
        ("worldcup", "월드컵",    "1:1 대결로 최후의 1개",           "🏆"),
        ("dice",     "주사위",    "주사위 굴려서 결정",               "🎲"),
        ("tarot",    "카드 뽑기",  "타로카드 스타일 3장 중 선택",     "🃏"),
        ("smart",    "스마트 추천","최근 안 먹은 메뉴 위주 추천",     "🧠"),
        ("battle",   "대결 모드",  "두 사람 의견, 랜덤 결정",        "⚔️"),
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
    if st.button("← 돌아가기", key="back"): reset_method(); st.rerun()
    
    if method == "random":
        st.markdown("### 🎲 랜덤 추천")
        if st.button("🎲 지금 바로 추천!", type="primary", use_container_width=True):
            st.session_state._random_result = random.choice(menus)
            st.rerun()
        if st.session_state._random_result:
            r = st.session_state._random_result
            result_card(r, "🎲 랜덤")
            adopt_button(r, "🎲 랜덤", key_suffix=f"random_{r['name']}")
    
    elif method == "roulette":
        st.markdown("### 🎡 룰렛 바퀴")
        winner_idx = random.randint(0, len(menus) - 1)
        menu_names = [m["name"] for m in menus]
        menu_emojis = [m.get("emoji", "🍽️") for m in menus]
        
        # 룰렛 HTML (가려지는 내부 결정 버튼 제거함)
        roulette_html = f"""<div style="text-align:center;">🎡 룰렛 컴포넌트가 로드되었습니다.</div>"""
        components.html(roulette_html, height=200)

        if st.button("🎡 결과 확인하기", type="primary", use_container_width=True):
            st.session_state.roulette_done = True
            st.session_state.roulette_winner = menus[winner_idx]
            st.rerun()
        
        if st.session_state.roulette_done:
            winner = st.session_state.roulette_winner
            result_card(winner, "🎡 룰렛 추천")
            adopt_button(winner, "🎡 룰렛", key_suffix="roulette_win")

    elif method == "scratch":
        st.markdown("### 🎁 스크래치 복권")
        if not st.session_state.scratch_menu: st.session_state.scratch_menu = random.choice(menus)
        menu = st.session_state.scratch_menu
        result_card(menu, "🎁 스크래치")
        adopt_button(menu, "🎁 스크래치")

    elif method == "worldcup":
        ts = st.session_state.tournament_state
        if ts and len(ts["round"]) == 1:
            winner = ts["round"][0]
            result_card(winner, "🏆 월드컵 우승")
            adopt_button(winner, "🏆 월드컵")
        elif ts:
            pairs = [(ts["round"][i], ts["round"][i+1]) for i in range(0, len(ts["round"])-1, 2)]
            idx = ts["pair_idx"]
            if idx < len(pairs):
                a, b = pairs[idx]
                col_a, col_b = st.columns(2)
                with col_a: 
                    if st.button(f"✅ {a['name']}", key="wc1", type="primary"): ts["winners"].append(a); ts["pair_idx"] += 1; st.rerun()
                with col_b: 
                    if st.button(f"✅ {b['name']}", key="wc2", type="primary"): ts["winners"].append(b); ts["pair_idx"] += 1; st.rerun()

    elif method == "dice":
        st.markdown("### 🎲 주사위")
        if st.button("🎲 결과 생성"):
            st.session_state.dice_winner = random.choice(menus)
            st.rerun()
        if st.session_state.dice_winner:
            result_card(st.session_state.dice_winner, "🎲 주사위 추천")
            adopt_button(st.session_state.dice_winner, "🎲 주사위")

    elif method == "tarot":
        st.markdown("### 🃏 카드 뽑기")
        if not st.session_state.tarot_cards: st.session_state.tarot_cards = random.sample(menus, min(3, len(menus)))
        if st.session_state.tarot_chosen is None:
            for i, card in enumerate(st.session_state.tarot_cards):
                if st.button(f"카드 {i+1} 선택", key=f"t_{i}"): st.session_state.tarot_chosen = card; st.rerun()
        else:
            result_card(st.session_state.tarot_chosen, "🃏 카드뽑기")
            adopt_button(st.session_state.tarot_chosen, "🃏 카드뽑기")

    elif method == "smart":
        if st.button("🧠 스마트 추천"):
            st.session_state._random_result = random.choice(menus)
            st.rerun()
        if st.session_state._random_result:
            result_card(st.session_state._random_result, "🧠 스마트 추천")
            adopt_button(st.session_state._random_result, "🧠 스마트 추천")

    elif method == "battle":
        st.markdown("### ⚔️ 대결 모드")
        a_pick = st.selectbox("A", [m["name"] for m in menus])
        b_pick = st.selectbox("B", [m["name"] for m in menus])
        if st.button("결정"):
            winner = random.choice([m for m in menus if m["name"] in [a_pick, b_pick]])
            st.session_state.battle_result = winner
            st.rerun()
        if st.session_state.battle_result:
            result_card(st.session_state.battle_result, "⚔️ 대결 승리!")
            adopt_button(st.session_state.battle_result, "⚔️ 대결")

# 하단 통계 탭 생략 (기존 구조와 동일)
