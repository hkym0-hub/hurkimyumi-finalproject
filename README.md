# 🍽️ 오늘 뭐 먹지?

매일 반복되는 "오늘 뭐 먹지?" 고민을 해결하는 메뉴 추천 Streamlit 웹앱입니다.

## ✨ 기능

| 기능 | 설명 |
|------|------|
| 🎲 랜덤 | 버튼 한 번으로 즉시 추천 |
| 🏆 월드컵 | 1:1 토너먼트로 최후의 1개 결정 |
| 🃏 스크래치 | 긁어서 메뉴 확인 |
| 🎡 룰렛 | 돌아가는 룰렛으로 결정 |
| 📍 맛집 찾기 | 지역 선택 후 주변 맛집 추천 (Step 3에서 API 연동) |
| 📋 추천 이력 | 과거 추천 기록 저장 및 통계 |
| 🔧 메뉴 관리 | 커스텀 메뉴 추가 / 제외 설정 |

## 🗂️ 카테고리

- **상황별**: 저녁, 배달, 데이트, 캠핑, 파티, 혼밥, 술안주
- **선호도별**: 다이어트, 매운맛, 가성비
- **음식 종류별**: 한식, 일식, 양식, 중식

## 🚀 실행 방법

### 로컬 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Streamlit Community Cloud 배포
1. 이 레포를 GitHub에 올린다
2. [share.streamlit.io](https://share.streamlit.io) 접속
3. 레포 연결 후 `app.py` 선택 → Deploy

## 🛠️ 기술 스택

- **언어**: Python 3.10+
- **프레임워크**: Streamlit
- **개발 환경**: Google Colab + GitHub
- **Step 3 예정**: Kakao Local API 또는 Google Places API 맛집 연동

## 📁 파일 구조

```
menu_app/
├── app.py              # 메인 앱
├── requirements.txt    # 패키지 목록
├── README.md           # 설명서
└── .streamlit/
    └── config.toml     # 테마 설정
```

## 📌 개발 로드맵

- [x] Step 1: 기본 레이아웃 + 샘플 데이터
- [ ] Step 2: 룰렛 애니메이션 고도화, 월드컵 브래킷 UI
- [ ] Step 3: 실제 메뉴 데이터 + 칼로리 API + 맛집 API 연동
