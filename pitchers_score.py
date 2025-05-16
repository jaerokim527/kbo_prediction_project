from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import shutil

download_dir = os.path.abspath("downloads")

options = Options()
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
driver.get("https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx")

try:
    # 엑셀 다운로드 버튼이 로딩될 때까지 대기
    wait = WebDriverWait(driver, 10)
    excel_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn_excel")))
    excel_button.click()
    print("✅ 엑셀 다운로드 버튼 클릭 성공")
    time.sleep(5)  # 다운로드 대기
except Exception as e:
    print(f"❌ 버튼 클릭 실패: {e}")
    driver.quit()
    exit()

driver.quit()

# 다운로드된 파일 확인
files = os.listdir(download_dir)
xlsx_files = [f for f in files if f.endswith(".xlsx")]
if xlsx_files:
    old_path = os.path.join(download_dir, xlsx_files[0])
    new_path = os.path.abspath("pitcher_stats.xlsx")
    shutil.move(old_path, new_path)
    print("✅ pitcher_stats.xlsx 저장 완료")
else:
    print("❌ 다운로드된 Excel 파일이 없습니다.")
