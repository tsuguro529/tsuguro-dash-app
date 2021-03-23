from bs4 import BeautifulSoup
import re
import pandas as pd
import requests
import time


HEADER = {"User-Agent":"Chrome/88.0.4324.182"}

def get_cover_urls(sitemap_url="https://www.magazine-data.com/sitemap/sitemap.xml"):
    """
    表紙情報のurl一覧を取得する関数です。
    Args:
        sitemap_url (str) : サイトマップのurl
    """

    res = requests.get(sitemap_url, headers=HEADER)
    soup = BeautifulSoup(res.text, "html.parser")

    cover_urls = []

    flag = False
    for url in soup.select("url > loc"):
        if re.search(r"/cover/", url.text): # coverを含むもの処理
            if url.text == "https://www.magazine-data.com/cover/anan.html": # anan以降を取得
                flag = True
            if not flag:
                continue
            else:
                cover_urls.append(url.text)

    return cover_urls

def get_magazine_summary(url):
    res = requests.get(url, headers=HEADER)
    soup = BeautifulSoup(res.text, "html.parser")

    boxes = soup.select_one("#furoku_box dl")
    datas = {"巻号":[], "モデル":[], "URL":[], "発売日":[]}

    # 巻号と雑誌のurlを取得
    for cover in boxes.find_all("dt"):
        if cover.find("a"):
            magazine_url = cover.a.attrs["href"]
        else:
            magazine_url = url
        magazine_id = " ".join([w for w in cover.text.split() if w != "→"][1:])

        datas["巻号"].append(magazine_id)
        datas["URL"].append(magazine_url)

    # モデルと発売日を取得
    for model_data in boxes.select("dd p.model"):
        model, release_date = model_data.text.split("発売日：")
        model = model.split("：")[-1]

        datas["モデル"].append(model)
        datas["発売日"].append(release_date)

    df = pd.DataFrame(datas)

    # titleから雑誌名を取得
    magazine_name = soup.title.text.split("【表紙】")[0].split()
    if len(magazine_name) == 2:
        name_en, name_ja = magazine_name # 英字の雑誌なら日本語表記を取得
    else:
        name_en = magazine_name[0]
        name_ja = name_en # 日本語の雑誌はそのまま

    df["雑誌名"] = name_en
    df["ザッシ名"] = name_ja
    df["年"] = df["発売日"].map(lambda x: int(re.search(r"[0-9]+年", x).group()[:-1]))
    df["月"] = df["発売日"].map(lambda x: int(re.search(r"[0-9]+月", x).group()[:-1]))

    return df

def main():

    cover_urls = get_cover_urls()
    #全雑誌情報の取得
    # sleep内に指定した時間×雑誌数くらいの時間がかかります。
    for i, url in enumerate(cover_urls[0:3]):
        if i == 0:
            df = get_magazine_summary(url)
        else:
            df = pd.concat([df, get_magazine_summary(url)])
        time.sleep(2) # サイトに負荷をかけないように2秒待つ。少なくとも1秒以上に設定してください。

    #df = get_magazine_summary(cover_urls[0])

    for index, _df in df.iterrows():
        date = datetime.datetime.strptime(_df['発売日'],'%Y年%m月%d日').date()
        row = models_dash.Data(no=_df['巻号'], talent=_df['モデル'], url=_df['URL'], date=date, magazine=_df['雑誌名'], magazine_kana=_df['ザッシ名'], year=_df['年'], month=_df['月'])
        db_session.add(row)

    db_session.commit()
    #df.to_csv("../assets/analyze_magazine_cover.csv", encoding="cp932", index=False)

if __name__ == '__main__':
    main()
