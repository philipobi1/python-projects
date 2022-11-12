import requests
from urllib.parse import urlencode
from requests.auth import HTTPBasicAuth
from pprint import pprint
import datetime
import os
import json
import math
import sys
from time import time

def progressbar(iterable,fn=lambda a:'',bar=30,length=None):
    total= length or len(iterable)
    for counter,item in enumerate(iterable):
        percent = (counter+1)/total
        sys.stdout.write('\r'+('#'*round(percent*bar)).ljust(bar)+f' | '+f'{round(percent*100)}%'.ljust(4)+f' | {fn(item)}'[:bar].ljust(bar))
        sys.stdout.flush()
        yield item
    print('')

def dir(path):
    path = os.path.join(path,str(utcnow()))
    os.mkdir(path)
    return path

def userinput(request,test=lambda r:bool(r)):
    r=input(request)
    return r if test(r) else userinput(request,test)

utcnow = lambda : math.floor(datetime.datetime.utcnow().timestamp())

itemgetter = lambda *keys: (lambda obj:(obj.get(key,None) for key in keys))

auth_scopes=[
    'ugc-image-upload',
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-private',
    'user-follow-modify',
    'user-follow-read',
    'user-library-modify',
    'user-library-read',
    'user-read-playback-position',
    'playlist-modify-private',
    'playlist-read-collaborative',
    'user-read-email',
    'playlist-read-private',
    'user-top-read',
    'playlist-modify-public',
    'user-read-currently-playing',
    'user-read-recently-played'
]

redirecturi='https://example.com/callback/'

class Log():
    def __init__(self,path):
        self.path = os.path.join(path,'log.txt')
        with open(self.path,'a') as f:
            f.write(f'time: {utcnow()}\n')
        print(f'created log file at location {self.path}')
    def write(self,msg):
        with open(self.path,'a') as f:
            f.write(msg+'\n')

class Token():

    def __init__(self,path='C:\\Users\\PC\\Documents\\coding\\spotify\\token.json'):
        self.path = path
        if os.path.isfile(self.path):
            self.load()
        else:
            self.client_id = userinput('client id')
            self.client_secret = userinput('client secret')
            
            self.access_token,self.refresh_token = itemgetter('access_token','refresh_token')(self.apipost(
                'https://accounts.spotify.com/api/token',
                auth=HTTPBasicAuth(self.client_id,self.client_secret),
                data={
                    'code':self.accessCode(),
                    'grant_type':'authorization_code',
                    'redirect_uri':redirecturi
                }))

            self.expires = utcnow()+3600
            self.export()

    def apipost(self,url,**kwargs):
        response = requests.post(url,**kwargs)
        if not response.ok:
            print(response.status_code)
            print(response.text)
            raise Exception('HTTP Request Error')
        return response.json()

    
    def accessCode(self):
                    
        url = 'https://accounts.spotify.com/authorize?' + urlencode({
                        'client_id':self.client_id,
                        'response_type':'code',
                        'redirect_uri': redirecturi,
                        'scope': ' '.join(auth_scopes)
                    })
        print('please paste the accesscode obtained by logging in via the following link')
        print(url)
        code = userinput('accesscode')
        return code
    
    def authCode(self,code):#no longer used

        response = requests.post(
            'https://accounts.spotify.com/api/token',
            auth=HTTPBasicAuth(self.client_id,self.client_secret),
            data={
                    'code':code,
                    'grant_type':'authorization_code',
                    'redirect_uri':redirecturi
                })

        if not response.ok:
            pprint(response.text)
            raise Exception('HTTP Request Error')

        return response.json()
    
    def load(self):
        with open(self.path) as f:
            self.expires,self.refresh_token,self.access_token,self.client_id,self.client_secret = itemgetter(
                'expires','refresh_token','access_token','client_id','client_secret')(json.loads(f.read()))


    def export(self):
        print(f'writing token to {self.path}')
        with open(self.path,'w') as f:
            data = self.__dict__
            data.pop('path')
            f.write(json.dumps(data))

        

    def refresh(self):

        self.access_token = self.apipost(
            'https://accounts.spotify.com/api/token',
            auth=HTTPBasicAuth(self.client_id,self.client_secret),
            data={
                    'refresh_token':self.refresh_token,
                    'grant_type':'refresh_token'
                }).get('access_token')
        self.expires = utcnow() + 3600
        self.export()
    
    def get(self):
        if utcnow() > self.expires:
            self.refresh()
            return self.access_token
        else:
            return self.access_token
            
class Spotify():
    
    def __init__(self,path='C:\\Users\\PC\\Documents\\coding\\spotify\\backups\\'):
        self.token = Token()
        self.path = dir(path)
        self.log = Log(self.path)
        self.userid = self.apiget('https://api.spotify.com/v1/me').get('id','')

    def apicall(self,method,**kwargs):
        if not kwargs.get('headers',0):
            kwargs['headers'] = {'Authorization':f'Bearer {self.token.get()}'}
        response = method(**kwargs)
        if not response.ok:
            print(response.status_code)
            pprint(response.text)
            raise Exception('HTTP Request Error')
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {'text': response.text}

    def apiget(self,url,**kwargs):
        return self.apicall(requests.get,url=url,**kwargs)

    def apidelete(self,url,**kwargs):
        return self.apicall(requests.delete,url=url,**kwargs)

    def apipost(self,url,**kwargs):
        return self.apicall(requests.post,url=url,**kwargs)
    
    def apiput(self,url,**kwargs):
        return self.apicall(requests.put,url=url,**kwargs)
    
    def msg(self,m,pr=0):
        self.log.write(m)
        if pr:
            print(m)

    def fetcher(self,url,fields=None,max=50):
        
        offset = 0
        
        while 1:
            query = {'limit': max,'offset': offset}
            
            if fields:
                query['fields']=fields

            data = self.apiget(url+'?'+urlencode(query))
            
            for item in data.get('items',[]):
                yield item

            if data['next'] == None:
                break

            offset+=max

    def get_playlists(self):
        for playlist in self.fetcher('https://api.spotify.com/v1/me/playlists'):
            print(playlist.get('name'))

    def save_playlists(self):
        
        self.msg('Backing up all user playlists',1)

        total = self.apiget('https://api.spotify.com/v1/me/playlists?'+urlencode({'limit':1})).get('total',0)

        for playlist in progressbar(
            self.fetcher('https://api.spotify.com/v1/me/playlists'),
            fn=lambda p: p.get('name',''),
            length=total
            ):
            id = playlist.get('id','')
            
            with open(os.path.join(self.path,f'{playlist["id"]}.json'),'w') as f:
                f.write(json.dumps({
                    'description':playlist.get('description',''),
                    'id': id,
                    'name':playlist.get('name',''),
                    'owner':(playlist.get('owner',0) or {}).get('id',''),
                    'tracks_no':(playlist.get('tracks',0) or {}).get('total',0),
                    
                    'tracks':  [{
                        'added_at':track.get('added_at',''),
                        'added_by':(track.get('added_by',0) or {}).get('id',''),
                        'uri':(track.get('track',0) or {}).get('uri',''),
                        'name':(track.get('track',0) or {}).get('name',''),
                        'album':((track.get('track',0) or {}).get('album',0) or {}).get('name',''),
                        'artists':[artist.get('name','') for artist in (track.get('track',0) or {}).get('artists',[]) if artist]
                    } for track in self.fetcher(
                        f'https://api.spotify.com/v1/playlists/{id}/tracks',
                        fields='items(added_at,added_by.id,track(name,uri,artists(name),album(name))),next'
                        ) if track]
                }))

            self.msg(f'saved playlist {id}')

        self.msg(f'Saved playlists to {self.path}',1)
            
    def save_library(self):
        
        self.msg('Backing up saved tracks',1)
            
        tracks = [{
            'added_at':track.get('added_at',''),
            'uri':(track.get('track',0) or {}).get('uri',''),
            'name':(track.get('track',0) or {}).get('name',''),
            'album':((track.get('track',0) or {}).get('album',0) or {}).get('name',''),
            'artists':[artist.get('name','') for artist in (track.get('track',{}) or {}).get('artists',[]) if artist]
        } for track in self.fetcher('https://api.spotify.com/v1/me/tracks') if track]
            
        with open(os.path.join(self.path,'saved_tracks.json'),'w') as f:
            f.write(json.dumps({
                'tracks_no':len(tracks),
                'tracks':tracks
            }))

        self.msg(f'Backed up saved tracks to {self.path}',1)

    def save_playlist(self,id):

        self.msg(f'Backing up playlist {id}',1)
        
        fields = 'description,name,owner.id,tracks.total'
        playlist = self.apiget(f'https://api.spotify.com/v1/playlists/{id}?'+urlencode({'fields':fields}))

        with open(os.path.join(self.path,f'{id}.json'),'w') as f:
            f.write(json.dumps({
                    'description':playlist.get('description',''),
                    'id':id,
                    'name':playlist.get('name',''),
                    'owner':(playlist.get('owner',0) or {}).get('id',''),
                    'tracks_no':(playlist.get('tracks',0) or {}).get('total',0),
                    'tracks': [{
                        'added_at':track.get('added_at',''),
                        'added_by':(track.get('added_by',0) or {}).get('id',''),
                        'uri':(track.get('track',0) or {}).get('uri',''),
                        'name':(track.get('track',0) or {}).get('name',''),
                        'album':((track.get('track',0) or {}).get('album',0) or {}).get('name',''),
                        'artists':[artist.get('name','') for artist in (track.get('track',0) or {}).get('artists',[]) if artist]} 
                        for track in self.fetcher(
                            f'https://api.spotify.com/v1/playlists/{id}/tracks',
                            fields='items(added_at,added_by.id,track(name,uri,artists(name),album(name))),next'
                        ) if track]
                }))

        self.msg(f'saved backup of playlist to {self.path}')

    def remove_playlist_tracks(self,playlist,tracks,snapshot = None):
        snapshot = snapshot or self.apiget(f'https://api.spotify.com/v1/playlists/{playlist}?'+urlencode({'fields':'snapshot_id'})).get('snapshot_id',None)

        response = self.apidelete(
            f'https://api.spotify.com/v1/playlists/{playlist}/tracks',
            data=json.dumps({
                'tracks':[{'uri':uri} for uri in tracks[:100]],
                'snapshot_id':snapshot
            })).get('snapshot_id',None)
        for uri in tracks[:100]:
            self.msg(f'removed track {uri} from playlist {playlist}')

        if len(tracks)>100:
            self.remove_playlist_tracks(playlist,tracks[100:],response)

    def remove_saved_tracks(self,tracks):
        self.apidelete(
            'https://api.spotify.com/v1/me/tracks',
            data=json.dumps({'ids':tracks[:50]})
        )
        for id in tracks[:50]:
            self.msg(f'removed track {id} from saved tracks')
        if len(tracks)>50:
            self.remove_saved_tracks(tracks[50:])

    def add_playlist_tracks(self,playlist,tracks,i=0):
        self.apipost(
            f'https://api.spotify.com/v1/playlists/{playlist}/tracks',
            data=json.dumps({'uris':tracks[:100],'position':100*i})
            )
        for uri in tracks[:100]:
            self.msg(f'added track {uri} to playlist {playlist}')
        if len(tracks)>100:
            self.add_playlist_tracks(playlist,tracks[100:],i+1)

    def private_playlist(self,playlist):
        self.apiput(
            f'https://api.spotify.com/v1/playlists/{playlist}',
            data=json.dumps({'public':False})
        )
        self.msg(f'privated playlist {playlist}',1)

    def private_playlists(self):
        for id in [playlist.get('id','') for playlist in self.fetcher('https://api.spotify.com/v1/me/playlists') if (playlist.get('owner',0) or {}).get('id','')==self.userid]:
            self.private_playlist(id)

    def create_playlist(self,name,description='',public=False):
        id = self.apipost(
            f'https://api.spotify.com/v1/users/{self.userid}/playlists',
            data=json.dumps({'name':name,'description':description,'public':public})
        ).get('id','')
        self.msg(f'created playlist {name}, id={id}',1)
        return id

    def clear_playlist(self,playlist):
        tracks = [(track.get('track',0) or {}).get('uri','') for track in self.fetcher(
            f'https://api.spotify.com/v1/playlists/{playlist}/tracks',
            fields='items(track(uri)),next'
            )]
        self.msg(f'clearing playlist {playlist}',1)
        self.remove_playlist_tracks(
            playlist,
            tracks
        )
    
    def backup(self):
        self.msg('backing up user playlists and library',1)
        self.save_playlists()
        self.save_library()
        self.msg('completed backup',1)

    def copy_playlist(self,pid,id=None,name=None):
        
        playlist = self.apiget( f'https://api.spotify.com/v1/playlists/{pid}?'+urlencode({'fields':'description,name,owner.id'}))
        id = id or self.create_playlist(
            name = name or playlist.get('name','playlist copy'),
            description = f'Copy of playlist by user {(playlist.get("owner",0) or {}).get("id","")} | Original description: '+playlist.get('description','') 
        )

        self.msg(f'copying playlist {pid} to playlist {id}',1)
        self.add_playlist_tracks(
            id,
            tracks=[(track.get('track',0) or {}).get('uri','') for track in self.fetcher(
                f'https://api.spotify.com/v1/playlists/{pid}/tracks',
                fields='items(track(uri)),next'
            )]
        )

    def move_saved_tracks(self,id=None,name=None):
        id = id or self.create_playlist(
            name = name or 'saved tracks',
            description = f'saved tracks have been moved here, time: {utcnow()}'
        )
        self.save_library()
        self.save_playlist(id)
        tracks=[(track.get('track',0) or {}).get('uri','') for track in self.fetcher('https://api.spotify.com/v1/me/tracks')]
        self.msg(f'copying saved tracks to playlist {id}',1)
        self.add_playlist_tracks(id,tracks=tracks)
        self.msg('removing saved tracks',1)
        self.remove_saved_tracks([uri.rsplit(':',1).pop() for uri in tracks])

def func():
    Spotify().get_playlists()
func()