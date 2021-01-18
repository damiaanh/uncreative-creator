import praw
import urllib.request
import os

class Scraper:

    def __init__(self, path):
        self.path = path
        self.subreddits = []
        self.posts = []
        self.videos = []
        self.limit = 10
        self.reddit = praw.Reddit(
        client_id="XXXXXXXXXXXX",
        client_secret="XXXXXXXXXXXXX",
        password="XXXXXXXXX",
        user_agent="scraper",
        username="redditbotytproject"
        )
        self.getSubreddits()
        self.getPosts()
        for p in self.posts:
            try:
                self.getURL(p)
            except Exception as e:
                print(e)
        self.downloadVideos()

    def getSubreddits(self):
        with open("subreddits.txt") as f:
            for line in f:
                line = line.rstrip("\n").lower()
                self.subreddits.append(line)

    def getPosts(self):
        for sub in self.subreddits:
            for post in self.reddit.subreddit(sub).hot(limit=self.limit):
                self.posts.append(post)

    def getURL(self, post):
        videourl = post.media['reddit_video']['fallback_url']
        videourl = videourl.split("?")[0]
        audiourl = videourl.rsplit("_", 1)[0] + "_audio.mp4"
        print(audiourl)
        name = str(post.title[:30].rstrip())
        name = "".join(e for e in name if e.isalnum()) +".mp4"
        self.videos.append((videourl, audiourl, name))

    def downloadVideos(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
        path = self.path + "/video_only/"
        os.mkdir(path)
        for url in self.videos:
            name = path+url[2]
            self.downloadAudio(url)
            print("requesting video for:", url[0], url[2])
            if not os.path.isfile(name):
                urllib.request.urlretrieve(url[0], name)



    def downloadAudio(self, video):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
        path = self.path + "/audio_only/"
        if os.path.exists(self.path + "/audio_only/") != True:
            os.mkdir(path)
        name = path+video[2]
        print("requesting audio for:", video[1], video[2])
        try:
            urllib.request.urlretrieve(video[1], name)
        except:
            pass
