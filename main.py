import os
import io
import time
import tweepy
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 画像を横並びで連結
def concat_h(img1, img2, color="black"):
    dst = Image.new(
        "RGB", (img1.width + img2.width, max(img1.height, img2.height)), color
    )
    dst.paste(img1, (0, 0))
    dst.paste(img2, (img1.width, 0))

    return dst

# AtCoderとCodeforcesのレート推移画像の取得及びリサイズ
user_name = os.environ['USER_NAME']
ac_url = "https://atcoder.jp/users/" + user_name
cf_url = "https://codeforces.com/profile/" + user_name

options = Options()
# options.add_argument('--headless')
# options.add_argument('--lang=ja')
driver = webdriver.Chrome(options=options)

# AtCoder
driver.get(ac_url)
driver.set_window_size(1920, 1080)
img_png = driver.get_screenshot_as_png()
time.sleep(10)
img_io = io.BytesIO(img_png)
img_ac = Image.open(img_io)
img_ac = img_ac.crop((700, 310, 1330, 755))
img_ac = img_ac.resize((int(img_ac.width * 0.9), int(img_ac.height * 0.9)))

# Codeforces
driver.get(cf_url)
driver.set_window_size(1920, 1080)
img_png = driver.get_screenshot_as_png()
time.sleep(10)
img_io = io.BytesIO(img_png)
img_cf = Image.open(img_io)
img_cf = img_cf.crop((370, 510, 1250, 855))
img_cf = img_cf.resize((700,400))

# Twitterのプロフィールヘッダ用にAtCoderとCodeforcesのレート推移画像の連結及びリサイズ
img_concat = concat_h(img_cf, img_ac)
img_concat = img_concat.resize((int(img_concat.width * 0.95), img_concat.height))

driver.quit()

# Twitter APIを使ってプロフィールヘッダ画像をレート推移画像に変更
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# Herokuは一時ファイル保存できなかったのでバイナリデータで更新
img_bytes = io.BytesIO()
img_concat.save(img_bytes, 'png')
api.update_profile_banner("kyopro.png", file=img_bytes.getvalue())