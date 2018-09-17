import requests,sys

def get_playing(previous):
	base_url = "http://ws.audioscrobbler.com/2.0/"
	method = "user.getrecenttracks"
	user = "crazyguitarman"
	key = "e38cc7822bd7476fe4083e36ee69748e"
	data_format = "json"
	extended = '1'
	limit = '50'
	
	payload = {"method": method,
					"user": user,
					"api_key": key,
					"format": data_format,
					"extended": extended,
					"limit": limit}
	try:				
		r = requests.get(base_url, payload)
		#read data as json response
		data = r.json()
	except:
		print ("Last.FM API not responding..")
		pass
	
	try:
		latest_track = data['recenttracks']['track'][0]
	except KeyError:
		print ("passing")
		pass

	# check if latest track is playing now
	playing = latest_track.get('@attr')
	if playing == None:
		#print ("didnt grab anything")
		scrobble = None
		artist = ''
		album =  ''
		song = ''
		img = ''
	elif playing != previous:
		try: 
			img = latest_track['image'][-1]['#text']
			#print (self.img)
			artist = latest_track['artist']['name']
			song = latest_track['name']
			album = latest_track['album']['#text']
			scrobble = "Now Playing: '{0}' by '{1}' on the album '{2}'".format(song, artist, album)
		except:
			img = ''
			artist = ''
			album = ''
			song =''
			scrobble = ''

	if scrobble != previous:
		print ("{0}, updating file".format(scrobble))
		try:
			with open(os.path.normpath(output_filename), "w") as f:
				f.write(scrobble)
			self.last_song = scrobble
		except:
			pass
		# else:
		# print "{}, not updating file".format(scrobble)
		if img == None:
			img = ''
		return artist, album, song, img, scrobble
