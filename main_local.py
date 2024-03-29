import os
import io
import time
# import tweepy
import numpy as np
from PIL import Image
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
load_dotenv()

# 画像を横並びで連結
def concat_h(img1, img2, color="black"):
    dst = Image.new(
        "RGB", (img1.width + img2.width, max(img1.height, img2.height)), color
    )
    dst.paste(img1, (0, 0))
    dst.paste(img2, (img1.width, 0))

    return dst

# AtCoder(AlgoとHeuristic)のレート推移画像の取得及びリサイズ
user_name = os.environ['USER_NAME']
ac_a_url = "https://atcoder.jp/users/" + user_name + "?contestType=algo"
ac_h_url = "https://atcoder.jp/users/" + user_name + "?contestType=heuristic"

options = webdriver.ChromeOptions()
options.add_argument('--headless')
# chromedriver = "/home/otsuneko/.pyenv/versions/pypy3.10-7.3.12/lib/pypy3.10/site-packages/selenium/webdriver/chrome"
# service = Service(executable_path=chromedriver)
# driver = webdriver.Chrome(service=service, options=options)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# AtCoder(Algo)
driver.get(ac_a_url)
driver.set_window_size(1920, 1080)
img_png = driver.get_screenshot_as_png()
time.sleep(1)
img_io = io.BytesIO(img_png)
img_ac_a = Image.open(img_io)
x,y = 690,330
width,height = 630,450
img_ac_a = img_ac_a.crop((x, y, x+width, y+height))
img_ac_a.save('atcoder_a.png')

# AtCoder(Heuristic)
driver.get(ac_h_url)
driver.set_window_size(1920, 1080)
img_png = driver.get_screenshot_as_png()
time.sleep(1)
img_io = io.BytesIO(img_png)
img_ac_h = Image.open(img_io)
x,y = 690,330
width,height = 630,450
img_ac_h = img_ac_h.crop((x, y, x+width, y+height))
img_ac_h.save('atcoder_h.png')

driver.quit()

# Twitter APIを使ってプロフィールヘッダ画像をレート推移画像に変更
# API_KEY = os.environ['API_KEY']
# API_SECRET = os.environ['API_SECRET']
# ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
# ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

# auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
# auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# api = tweepy.API(auth)
# api.update_profile_banner('kyopro.png')

# 現在のプロフィールヘッダ画像を取得
# user_id = os.environ['USER_ID']
# screen_name = os.environ['SCREEN_NAME']
# img_current = api.get_profile_banner(user_id, user_name)

# 最新のレート推移画像キャプチャ成功時(白画像でない時)のみプロフィールヘッダ画像を更新
img_ac_a_white = np.array(Image.new("RGB", (img_ac_a.width, img_ac_a.height), (255, 255, 255)))
img_ac_h_white = np.array(Image.new("RGB", (img_ac_h.width, img_ac_h.height), (255, 255, 255)))

if not np.array_equal(np.array(img_ac_a), img_ac_a_white) and not np.array_equal(np.array(img_ac_h), img_ac_h_white):
    # Twitterのプロフィールヘッダ用にAtCoder(AlgoとHeuristic)のレート推移画像の連結及びリサイズ
    img_concat = concat_h(img_ac_a, img_ac_h)
    img_concat = img_concat.resize((1500, 500))
    img_concat.save('kyopro.png')
    # api.update_profile_banner("kyopro.png", file=img_bytes.getvalue())