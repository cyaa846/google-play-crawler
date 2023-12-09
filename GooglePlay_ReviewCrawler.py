from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from bs4 import BeautifulSoup
import time
import pandas as pd

# 初始化 Chrome WebDriver
driver = webdriver.Chrome()

# 要爬取的 Google Play 應用程式頁面 URL
app_url = "https://play.google.com/store/apps/details?id=com.chinaairlines.mobile30"

# 前往應用程式頁面
driver.get(app_url)
time.sleep(1)  # 等待頁面載入

# 模擬向下捲動頁面以載入完整頁面
scroll_count = 3
for i in range(scroll_count):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  # 等待頁面載入

# 點擊「查看所有評論」按鈕
driver.find_element(
    By.XPATH,
    '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[4]/section/div/div[2]/div[5]/div/div/button/span',
).click()
time.sleep(2)  # 等待頁面載入

# 模擬向下捲動頁面以載入更多評論
reviewsbar = driver.find_element(By.CLASS_NAME, "odk6He")
scroll_origin = ScrollOrigin.from_element(reviewsbar)
scroll_count = 20
for i in range(scroll_count):
    ActionChains(driver).scroll_from_origin(scroll_origin, 0, 10000).perform()
    time.sleep(2)  # 等待頁面載入

# 抓取整個網頁內容
page_source = driver.page_source

# 關閉瀏覽器
driver.quit()

# 使用 BeautifulSoup 解析網頁內容
soup = BeautifulSoup(page_source, "html.parser")

# 找到評論元素
reviews = soup.find_all("div", class_="RHo1pe")

pd_comment_date = []
pd_rating_value = []
pd_comment_text = []

# 逐一提取評論內容並輸出
for review in reviews:
    # 提取評論日期
    date_section = review.find("span", class_="bp9Aid")
    comment_date = date_section.get_text(strip=True) if date_section else None
    pd_comment_date.append(comment_date)

    # 提取評分
    rating = review.find("div", class_="iXRFPc")
    rating_value = rating["aria-label"][4] if rating else None
    pd_rating_value.append(rating_value)

    # 提取評論內容文字
    comment_section = review.find("div", class_="h3YV2d")
    comment_text = comment_section.get_text(strip=True) if comment_section else None
    pd_comment_text.append(comment_text)

# 創建 DataFrame
data = {"日期": pd_comment_date, "評分": pd_rating_value, "留言": pd_comment_text}
df = pd.DataFrame(data)

# 將 DataFrame 存為 CSV 檔案
df.to_csv("GooglePlay_Reviews.csv", index=False)
