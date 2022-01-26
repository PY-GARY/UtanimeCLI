import requests, re, html, os, webbrowser, time

class Utanime():
    def __init__(self):
        self.names = []
        self.seasons = []
        self.series_url = []
        self.episodes = []
        self.episodes_url = []
        a = 1

    def clear(self):
        os.system('cls')

    def getNames(self):
        resp = html.unescape(requests.get('https://utanime.me/series').text)
        names = re.findall(r'<h2 class="title fz4 sm-fz5 fwn mab0">(.*)<\/h2>', resp)
        names_url = re.findall(r'(https:\/\/utanime\.me\/serie\/.*\/)', resp)
        self.series_url = self.series_url+names_url
        self.names = self.names+names
        resp = html.unescape(requests.get('https://utanime.me/series/page/2/').text)
        names = re.findall(r'<h2 class="title fz4 sm-fz5 fwn mab0">(.*)<\/h2>', resp)
        self.names = self.names+names
        names_url = re.findall(r'(https:\/\/utanime\.me\/serie\/.*\/)', resp)
        self.series_url = self.series_url+names_url
        resp = html.unescape(requests.get('https://utanime.me/series/page/3/').text)
        names = re.findall(r'<h2 class="title fz4 sm-fz5 fwn mab0">(.*)<\/h2>', resp)
        self.names = self.names+names
        names_url = re.findall(r'(https:\/\/utanime\.me\/serie\/.*\/)', resp)
        self.series_url = self.series_url+names_url
        # print(*self.names, sep = "\n")


    def getSeasons(self):
        resp = requests.get(self.series_url[self.choice]).text
        season = re.findall(r">T(\d\d)", resp)
        self.seasons = self.seasons+season
        # print(*self.seasons, sep = "\n")

    def getEpisodes(self):
        resp = requests.get(self.series_url[self.choice]).text
        episode = re.findall(r'mab">(.*)<.*\n.*yellow-co">', resp)
        self.episode_url = re.findall(r'brd1"> <a href="(.*)\/', resp)
        self.episodes_url = self.episodes_url+episode
        self.episodes = self.episodes+episode
        # print(*self.episodes, sep = "\n")

    def playEpisode(self):
        s = requests.session()
        resp = s.get(self.episode_url[self.choice]).text
        id = re.findall(r'"id" value="(\d*)', resp)
        resp2 = s.get('https://utanime.me/?trembed=0&trid='+id[0]).text.split('" src="https://streamtape.com/e/')[1].split('"')[0]
        r = 'https://stape.fun/e/'+resp2
        webbrowser.open(r)
        print(f'\n\tLink: {r}\n')

    def final(self):
        os.system('pause')
        ut.clear()
        choice = input('Did u want to return to the main menu ? (y/n): ')
        if choice == 'y':
            ut.main()
        elif choice == 'n':
            os.system('exit')
        else:
            print('Error...')
            time.sleep(3)
            os.system('exit')

    def main(self):
        ut.__init__()
        ut.clear()
        ut.getNames()
        ut.clear()
        for i in self.names:
            print(self.names.index(i) +1, end=' - '+ i + '\n')
        self.choice = int(input('\n=> '))-1
        ut.clear()
        ut.getSeasons()
        for i in self.seasons:
            print(i.strip('0')+' - Season '+i)
        self.choice = int(input('\n=> '))-1
        ut.clear()
        ut.getEpisodes()
        for i in self.episodes:
            print(self.episodes.index(i) +1, end=' - '+ i + '\n')
        self.choice = int(input('\n=> '))-1
        ut.playEpisode()
        ut.final()


if __name__ == '__main__':
        ut = Utanime()
        ut.main()