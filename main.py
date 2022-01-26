from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime
class pesquisa_youtube:
    def __init__(self):
        self.conexao_youtube()
    def conexao_youtube(self):
        self.youtubeApiKey = "AIzaSyA4P6EuvKFP4CCWAL3kdjL-DVwVyA93osk"
        self.youtube = build('youtube', 'v3', developerKey=self.youtubeApiKey)

        #Extraindo videos de uma Playlist
        self.playlistId= 'PL17CDA1B0FF3421F5' #Dicas de Pandas Playlist
        self.playlistName = 'c.v rl'
        self.nextPage_token = None
        self.playlist_videos = []

        self.res = self.youtube.playlistItems().list(part='snippet', playlistId = self.playlistId, maxResults = 30).execute()
        self.playlist_videos = self.res['items']
        self.videosIds = list(map(lambda x: x['snippet']['resourceId']['videoId'], self.playlist_videos))
        
        self.state = []
        for self.videosid in self.videosIds:
            self.res =self.youtube.videos().list(part='statistics', id=self.videosid).execute()
            self.state += self.res['items'] 
            print(self.state)
        
        self.videos_title = list(map(lambda x: x['snippet']['title'],self.playlist_videos))
        self.video_thumbnails = list(map(lambda x: x['snippet']['thumbnails']['high']['url'],self.playlist_videos))
        self.published_date = list(map(lambda x: x['snippet']['public'],self.playlist_videos))
        self.description = list(map(lambda x: x['snippet']['description'],self.playlist_videos))
        self.videoid = list(map(lambda x: x['snippet']['resourceId']['videoId'],self.playlist_videos))

        self.liked= list(map(lambda x: x['statistic']['likeCount'],self.playlist_videos))
        self.desliked = list(map(lambda x: x['statistic']['dislikedCount'],self.playlist_videos))
        self.views = list(map(lambda x: x['statistic']['viewCount'],self.playlist_videos))
        self.comment = list(map(lambda x: x['statistic']['commentCount'],self.playlist_videos))
        
        self.extraction_date = [str(datetime.now())]*len(self.videosIds) 
        self.playlist_df = pd.DataFrame({
                    'title':self.videos_title,
                    'video_id':self.videoid,
                    'video_description':self.description,
                    'published_date': self.published_date,
                    'extraction_date':self.extraction_date,
                    'likes': self.liked,
                    'dislikes':self.disliked,
                    'views':self.views,
                    'comment':self.comment,
                    'thumbnail':self.video_thumbnails
                    })

pesquisa_youtube()
