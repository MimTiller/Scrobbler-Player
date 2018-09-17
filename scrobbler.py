import kivy
from kivy.app import App
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.lang import Builder
import requests,sys
import os
from kivy.config import Config
from time import sleep
import brainz, getplaying
from kivy.loader import Loader
from kivy.properties import ObjectProperty

Config.read('config.ini')
Config.set('graphics', 'top', 660)
Config.set('graphics','left',1100)
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '200')
Config.set('graphics', 'borderless', 'True')
Config.set('graphics','resizable',0)
Config.write()

output_filename = "scrobble-output.txt"


class MainLayout(GridLayout):
	cols = 2
	def __init__(self,**kwargs):
		super(MainLayout,self).__init__(**kwargs)
		self.img = 'unknown.png'
		self.previous = None
		self.last_song = ''
		self.artist=''
		self.album=''
		self.song=''
		# self.add_widget(self.image)
		Clock.schedule_interval(self.update_pic, 5)



	def update_pic(self,dt):
		self.ids.albumart.reload()
		info = getplaying.get_playing(self.previous)
		if info:
			self.artist = info[0]
			self.album = info[1]
			self.song = info[2]
			self.img  = info[3]
			self.previous = info[4]
			self.dl_image(self.img)
		if str(self.song) == self.ids.Songinfo.text:
			print (str(self.song),self.ids.Songinfo.text)
		else:
			self.ids.albumart.reload()
			self.update_text(self.artist,self.album, self.song,self.img)

	def update_text(self,artist, album, song,img):
		self.ids.Songinfo.text = str(song)
		self.ids.Artistinfo.text = artist
		self.ids.Albuminfo.text =  album

	def dl_image(self,url):	
		if url not in (None,'Nonetype',''):
			print("LAST.FM: Found image!")
			self.ids.albumart.source = str(url)
		else:
			print ("LAST.FM: couldnt find image")
			if self.artist != '':
				brainz.init()
				album_art = brainz.get_cover(self.artist, self.album)
				if album_art:
					self.ids.albumart.source = str(album_art)
					print("MUSICBRAINZ: Found image!")
			else:
				print ("Couldnt find any artwork....switching to unknown")
				self.ids.albumart.source = 'unknown.png'

		


# main loop
class NowPlaying(App):
	size_hint=[None,None]
	def build(self):
		self.icon = 'music.png'
		Loader.loading_image = 'loading.gif'
		build = Builder.load_file('scrobbler.kv')
		return build

if __name__ == "__main__":
	NowPlaying().run()


    
    
