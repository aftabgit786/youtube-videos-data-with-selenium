from flask import Flask, request, render_template
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from utils import scroll_to_page_end, extract_videos_data

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    url = request.form["url"]
    if "/videos" not in url:
        url = url.rstrip("/") + "/videos"
    driver = webdriver.Chrome()
    driver.get(url)
    scroll_to_page_end(driver)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    data = extract_videos_data(soup)
    channel_name = url.split("/")[-2].replace("@", "")
    df = pd.DataFrame(data)
    videos = df.to_dict("records")
    return render_template("result.html", videos=videos)

if __name__ == "__main__":
    app.run(debug=True)
