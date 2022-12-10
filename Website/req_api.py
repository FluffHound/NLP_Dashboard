import requests
from datetime import datetime

def req(calon, link):
    ## Sentiment
    r = requests.post(
        f"{link}/api/sentiment",
        json={"status": "minta datanya dong", "calon": calon},
    )
    data = r.json()
    times = data['All time']['last_update']
    times = datetime.strptime(times,'%a, %d %b %Y %H:%M:%S %Z')
    times = times.strftime("tanggal %d-%m-%Y pukul %H:%M:%S")
    ## LDA
    r2 = requests.post(
            f"{link}/api/LDA",
            json={"status": "minta datanya dong", "calon": calon},
        )
    save = open(f"static/iframeTM/lda_{calon}.html", "wb").write(r2.content)
    ## Wordcloud Sentiment
    waktu = ['All time','14 Hari','7 Hari','Hari ini']
    sent = ['pos','neg','neu']

    for i in waktu:
        for j in sent:
            r3 = requests.post(
            f"{link}/api/wordcloudsent", json={"status": "minta datanya dong", "calon": calon,'waktu':i,'sentiment':j},)
            save = open(f"static/assets/Wordcloud/{calon}/wordcloud_mention_{calon}_{i}_{j}.jpg", "wb").write(r3.content)

    ## Wordcloud Profile
    r4 = requests.post(
        f"{link}/api/wordcloudprofile",
        json={"status": "minta datanya dong", "calon": calon},
    )
    save = open(f"static/assets/Wordcloud/{calon}/wordcloud_profile_{calon}.jpg", "wb").write(r4.content)

    return times