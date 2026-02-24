import os
import requests
from bs4 import BeautifulSoup
from google import genai

def get_news():
    # 뉴스 RSS 주소 (예: 구글 뉴스)
    url = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
    response = requests.get(url)
    # 여기서 'lxml'을 사용하여 에러를 방지합니다.
    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item', limit=5)
    
    news_list = []
    for item in items:
        news_list.append(f"제목: {item.title.text}\n링크: {item.link.text}")
    return "\n\n".join(news_list)

def main():
    # 최신 google-genai 방식 (2026 표준)
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    raw_news = get_news()
    
    prompt = f"다음 뉴스 리스트를 요약해줘:\n\n{raw_news}"
    
    # 모델 호출 방식 변경
    response = client.models.generate_content(
        # model="gemini-2.0-flash",
        model="gemini-1.5-flash",
        contents=prompt
    )
    
    print("--- 오늘의 뉴스 요약 ---")
    print(response.text)

if __name__ == "__main__":
    main()
