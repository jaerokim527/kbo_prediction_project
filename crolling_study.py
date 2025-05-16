from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

url = "https://www.koreabaseball.com/Schedule/GameCenter/DaySchedule.aspx?date=2024-03-23"
driver.get(url)
time.sleep(5)

# HTML 저장
with open("debug_20240323.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

driver.quit()
print("✅ HTML 저장 완료 (debug_20240323.html)")
