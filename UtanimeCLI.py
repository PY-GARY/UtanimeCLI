import requests, re, html, os, webbrowser
import unicodedata

download_dir = os.getcwd() # TODO create config.ini file and read attributes from it

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

class Utanime():
    def __init__(self):
        self.names = []
        self.seasons = []
        self.series_url = []
        self.episodes = []
        self.episodes_url = []
        a = 1

    def clear(self): # added multi os support
        if os.name in ('nt', 'dos'):
            command = 'cls'
        os.system(command)

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


    def getSeasons(self):
        resp = requests.get(self.series_url[self.choice]).text
        season = re.findall(r">T(\d\d)", resp)
        self.seasons = self.seasons+season

    def getEpisodes(self):
        resp = requests.get(self.series_url[self.choice]).text
        episode = re.findall(r'mab">(.*)<\/h2>\n<span class="pdx brd1 dib vat black-bg mar yellow-co">'+str(self.choice2), resp)
        self.episode_url = resp.split('mab brd1"> <a href="')[1].split('-1')[0]
        self.episodes = self.episodes+episode

    def download_file(self,url,local_filename): # download large files
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
        return local_filename
        
    def playEpisode(self):
        s = requests.session()
        resp = s.get(self.episode_url+'-'+str(self.choice2)+'x'+str(self.choice)).text
        id = re.findall(r'"id" value="(\d*)', resp)
        resp2 = s.get('https://utanime.me/?trembed=0&trid='+id[0]).text.split('" src="https://streamtape.com/e/')[1].split('"')[0]
        r = 'https://stape.fun/e/'+resp2
        resp = s.get(r)
        botlink_matcher = '<div id="robotlink" style="display:none;">'
        botlinkIndex = resp.text.find(botlink_matcher) + len(botlink_matcher)
        botlink_step1 = resp.text[botlinkIndex:]
        botlink = 'https:/' + botlink_step1[0:botlink_step1.find('token=')]
        token_step1 = (botlink_step1[botlink_step1.find('</div>'):])
        token_step2 = token_step1[token_step1.find("token="):]
        token_antibot = token_step2[6:token_step2.find("'")]
        botlink = botlink + 'token=' + token_antibot
        webbrowser.open(botlink)

    def dlEpisode(self): # TODO multithreader
        s = requests.session()
        resp = s.get(self.episode_url+'-'+str(self.choice2)+'x'+str(self.choice)).text
        id = re.findall(r'"id" value="(\d*)', resp)
        resp2 = s.get('https://utanime.me/?trembed=0&trid='+id[0]).text.split('" src="https://streamtape.com/e/')[1].split('"')[0]
        r = 'https://stape.fun/e/'+resp2
        resp = s.get(r)
        botlink_matcher = '<div id="robotlink" style="display:none;">'
        botlinkIndex = resp.text.find(botlink_matcher) + len(botlink_matcher)
        botlink_step1 = resp.text[botlinkIndex:]
        botlink = 'https:/' + botlink_step1[0:botlink_step1.find('token=')]
        token_step1 = (botlink_step1[botlink_step1.find('</div>'):])
        token_step2 = token_step1[token_step1.find("token="):]
        token_antibot = token_step2[6:token_step2.find("'")]
        botlink = botlink + 'token=' + token_antibot
        print('[+] downloading '+ botlink +' ...');
        print('[*] it may take a time, please wait');
        file = s.get(botlink)
        open(download_dir+strip_accents(str(self.episodes[self.choice]).replace(" ","_"))+'.mp4', 'wb').write(file.content)
        print('[+] done')

    def main(self):
        ut.__init__()
        ut.clear()
        ut.getNames()
        ut.clear()
        for i in self.names:
            print(str(self.names.index(i) +1) + ' - '+ i)
        self.choice = int(input('\n=> '))-1
        ut.clear()
        ut.getSeasons()
        for i in self.seasons:
            print(i.strip('0')+' - Season '+i)
        self.choice2 = int(input('\n=> '))
        ut.clear()
        ut.getEpisodes()
        for i in self.episodes:
            print(str(self.episodes.index(i) +1) + ' - '+ i)
        self.choice = int(input('\n=> '))
        dlOrPlay = input("Did you want to download (dl) or play (play) ? : ")
        if(dlOrPlay == 'dl'):
            ut.dlEpisode()
        elif(dlOrPlay == 'play'):
            ut.playEpisode()
        else:
            os.system('exit')


if __name__ == '__main__':
        ut = Utanime()
        ut.main()
