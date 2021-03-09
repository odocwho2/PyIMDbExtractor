import requests
import pandas as pd
from bs4 import BeautifulSoup
from tkinter import *

def extract():
    EpisodesScrap = []
    seasonStartInt = int(seasonStart.get())
    seasonEndInt = int(seasonEnd.get())
    linkInput = link.get()
    linkInput = linkInput[:-1]
    for season in range(seasonStartInt, seasonEndInt + 1):
        r = requests.get(linkInput + str(season))
        soup = BeautifulSoup(r.text, 'html.parser')
        episode_info = soup.findAll('div', class_='info')
        for episode in episode_info:
            episodeSeason = season
            try:
                episodeNumber = episode.meta['content']
            except:
                episodeNumber = "No episode NR"
            try:
                episodeTitle = episode.a['title']
            except:
                episodeTitle = "No episode Title"
            try:
                episodeAirDate = episode.find('div', class_='airdate').text.strip()
            except:
                episodeAirDate = "1/1/1900"
            try:
                episodeRating = episode.find('span', class_='ipl-rating-star__rating').text
            except:
                episodeRating = "0.00"
            episodeData = [episodeSeason, episodeNumber, episodeTitle, episodeAirDate, episodeRating]
            EpisodesScrap.append(episodeData)
    EpisodesScrap = pd.DataFrame(EpisodesScrap,columns=['episodeSeason', 'episodeNumber', 'episodeTitle', 'episodeAirDate', 'episodeRating'])
    EpisodesScrap['episodeRating'] = EpisodesScrap.episodeRating.astype(float)
    EpisodesScrap['episodeAirDate'] = pd.to_datetime(EpisodesScrap.episodeAirDate)
    EpisodesScrap.to_csv('SeriesExtract.csv', index=False)
# GUI
GUI = Tk()
GUI.title("IMDB Extractor")
GUI.geometry("500x300")
GUI.eval('tk::PlaceWindow . center')
Label(GUI, text="TV show link", justify='center').grid(row=0, column=0, sticky=W)
link = Entry(GUI, width=55, textvariable='LinkEntry')
link.grid(row=0, column=1, sticky=W)
Label(GUI, text="ex:https://www.imdb.com/title/tt0000000/episodes?season=1").grid(row=1, column=1, sticky=W)
Label(GUI, text="Start season number:").grid(row=2, column=0, sticky=W)
seasonStart = Entry(GUI, width=5)
seasonStart.grid(row=2, column=1, sticky=W, pady=10)
Label(GUI, text="End season number:").grid(row=3, column=0, sticky=W)
seasonEnd = Entry(GUI, width=5)
seasonEnd.grid(row=3, column=1, sticky=W)
submit = Button(GUI, text="Start Extracting", width=15, command=extract)
submit.grid(row=5, column=0, sticky=W, pady=10)
GUI.mainloop()
