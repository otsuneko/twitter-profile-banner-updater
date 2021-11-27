import os
import io
import time
import tweepy
import chromedriver_binary
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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

# AtCoderとCodeforcesのレート推移画像の取得及びリサイズ
user_name = os.environ['USER_NAME']
ac_url = "https://atcoder.jp/users/" + user_name
cf_url = "https://codeforces.com/profile/" + user_name

options = Options()
options.binary_location = "C:\\Program Files\\Google\Chrome\\Application\\chrome.exe"
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# AtCoder
driver.get(ac_url)
driver.set_window_size(1920, 1080)
img_png = driver.get_screenshot_as_png()
time.sleep(1)
img_io = io.BytesIO(img_png)
img_ac = Image.open(img_io)
x,y = 700,370
width,height = 630,445
img_ac = img_ac.crop((x, y, x+width, y+height))
img_ac = img_ac.resize((int(img_ac.width * 0.9), int(img_ac.height * 0.9)))
img_ac.save('atcoder.png')

# Codeforces
driver.get(cf_url)
driver.set_window_size(1920, 1080)
img_png = driver.get_screenshot_as_png()
time.sleep(1)
img_io = io.BytesIO(img_png)
img_cf = Image.open(img_io)
x,y = 370,580
width,height = 880,345
img_cf = img_cf.crop((x, y, x+width, y+height))
img_cf = img_cf.resize((700,400))
img_cf.save('codeforces.png')

# Twitterのプロフィールヘッダ用にAtCoderとCodeforcesのレート推移画像の連結及びリサイズ
img_concat = concat_h(img_cf, img_ac)
img_concat = img_concat.resize((int(img_concat.width * 0.95), img_concat.height))
img_concat.save('kyopro.png')

driver.quit()

# Twitter APIを使ってプロフィールヘッダ画像をレート推移画像に変更
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
api.update_profile_banner('kyopro.png')