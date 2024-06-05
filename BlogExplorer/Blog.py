from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from collections import deque
import openai



class Blog:
    
    def __init__(self, url: str):
        
        self.url = url
        self.title = None
        self.icon = None
        self.friends = []   # only save links as string[]

    def fetch_details(self):

        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        self.title = soup.find('title').text
        
        icon_link = soup.find('link', rel='icon')
        if icon_link:
            icon_link = icon_link.get('href')
            icon_link = urljoin(self.url, icon_link)
        self.icon = icon_link
        

    def fetch_friends(self):
        
        try:
            prompt = f"Extracted friends list with their links from HTML:\f {soup}."
            response = openai.Completion.create(
                engine="text-davinci-003",  # 选择合适的模型
                prompt=prompt,
                max_tokens=150
            )
            print(response.choices[0].text.strip())
        except Exception as e:
            print("Failed to interact with OpenAI API:", e)