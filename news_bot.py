import os
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# 1. 설정: Gemini AI 연결 (나중에 금고에 넣을 열쇠)
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_news():
    # 2. 뉴스 수집 (구글 뉴스 RSS를 활용해 실시간 정보를 가져옵니다)
    topics = ["World Economy", "International Politics", "Elon Musk Tesla", "6G Telecommunication"]
    combined_news = ""
    
    for topic in topics:
        url = f"https://news.google.com/rss/search?q={topic}&hl=en-US&gl=US&ceid=US:en"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')[:3]  # 주제별로 상위 3개 뉴스만
        
        for item in items:
            combined_news += f"Topic: {topic}\nTitle: {item.title.text}\nLink: {item.link.text}\n\n"
            
    return combined_news

def summarize_news(news_text):
    # 3. Gemini에게 요약 요청 (아버님이 원하시는 말투로 설정)
    prompt = f"""
    당신은 세계 최고의 뉴스 분석가입니다. 아래 제공된 뉴스 목록을 보고 60대 한국 남성이 이해하기 쉽게 요약해 주세요.
    
    [주제별 요약 지침]
    1. 경제/정치: 트럼프 정책과 전쟁 상황이 한국에 미칠 영향 위주로.
    2. 자동차/일론 머스크: 테슬라와 자율주행 소식을 자세히.
    3. 통신: 6G나 최신 IT 기기 소식.
    
    뉴스 내용:
    {news_text}
    
    형식은 '오늘 아침 세계 소식'이라는 제목으로 시작하고, 각 항목은 3줄 이내로 요약해 주세요.
    """
    
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    raw_news = get_news()
    summary = summarize_news(raw_news)
    
    # 4. 결과 출력 (나중에 이 내용이 이메일이나 노션으로 갑니다)
    print(summary)
    
    # 결과물 저장
    with open("daily_report.txt", "w", encoding="utf-8") as f:
        f.write(summary)
