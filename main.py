import os
import io
import time
import tweepy
import numpy as np
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager
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
options.add_argument('--headless')
options.add_argument('--lang=ja-JP')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get('https://google.com')

# AtCoder
driver.get(ac_url)
driver.set_window_size(1920, 1080)
time.sleep(15)
img_png = driver.get_screenshot_as_png()
img_io = io.BytesIO(img_png)
img_ac = Image.open(img_io)
x,y = 700,340
width,height = 630,445
img_ac = img_ac.crop((x, y, x+width, y+height))
img_ac = img_ac.resize((int(img_ac.width * 0.9), int(img_ac.height * 0.9)))

# Codeforces
driver.get(cf_url)
driver.set_window_size(1920, 1080)
time.sleep(15)
img_png = driver.get_screenshot_as_png()
img_io = io.BytesIO(img_png)
img_cf = Image.open(img_io)
x,y = 370,510
width,height = 880,345
img_cf = img_cf.crop((x, y, x+width, y+height))
img_cf = img_cf.resize((700,400))

driver.quit()

# Twitter APIを使ってプロフィールヘッダ画像をレート推移画像に変更
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# 現在のプロフィールヘッダ画像を取得
# user_id = os.environ['USER_ID']
# screen_name = os.environ['SCREEN_NAME']
# img_current = api.get_profile_banner(user_id, user_name)

# 最新のレート推移画像キャプチャ成功時(白画像でない時)のみプロフィールヘッダ画像を更新
img_ac_white = np.array(Image.new("RGB", (img_ac.width, img_ac.height), (255, 255, 255)))
img_cf_white = np.array(Image.new("RGB", (img_cf.width, img_cf.height), (255, 255, 255)))

if not np.array_equal(np.array(img_ac), img_ac_white) and not np.array_equal(np.array(img_cf), img_cf_white):
    # Twitterのプロフィールヘッダ用にAtCoderとCodeforcesのレート推移画像の連結及びリサイズ
    img_concat = concat_h(img_cf, img_ac)
    img_concat = img_concat.resize((int(img_concat.width * 0.95), img_concat.height))

    # Herokuは一時ファイル保存できなかったのでバイナリデータで更新
    img_bytes = io.BytesIO()
    img_concat.save(img_bytes, 'png')
    api.update_profile_banner("kyopro.png", file=img_bytes.getvalue())
