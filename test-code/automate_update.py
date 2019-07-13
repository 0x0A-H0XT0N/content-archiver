import youtube_dl
import sys
from urllib import request

version = youtube_dl.update.__version__

youtube_dl.update.update_self(to_screen=sys.stdin, verbose=True, opener=request.OpenerDirector)
print(version)
