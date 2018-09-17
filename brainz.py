import musicbrainzngs as mus

def init():
    """Initialize musicbrainz."""
    mus.set_useragent("Subcake's Art Bot",1,"miller.allen.tim@gmail.com")


def get_cover(artist,album, size=250):
    """Download the cover art."""
    try:
        data = mus.search_releases(artist=artist,release=album, limit=1)
        release_id = data["release-list"][0]["id"]
        print ("RELEASE ID:",release_id)
        #print(f"album: Using release-id: {data['release-list'][0]['id']}")

        imgdata = mus.get_image_list(release_id)
        imageurl = imgdata['images'][0]['image']
        return imageurl
    except mus.NetworkError:
        get_cover(artist,album,size)

    except mus.ResponseError:
        print("MUSICBRAINZ: Couldn't find album art for",
              f"{artist} - {album}")
        return ''
