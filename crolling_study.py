from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Service 객체를 명시적으로 설정
service = Service(ChromeDriverManager().install())

# Chrome WebDriver 실행
driver = webdriver.Chrome(service=service)

# 웹페이지 접속
driver.get('https://www.koreabaseball.com/')