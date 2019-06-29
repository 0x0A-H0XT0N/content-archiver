import json


class Json:
    """
    Handle JSON requests.
    """
    def encode(data, write_filename):
        """
        Encode a obj (if available) to a file
        Do NOT handle exceptions or errors
        :param data: Data obj to write on the file, should be compatible with JSON
        :param write_filename: Name of the file to write
        Should have ".json" at the end.
        :return: Nothing.
        """
        with open(write_filename, "w") as write_file:
            json.dump(data, write_file)

    def decode(read_filename, return_content=1):
        """
        Read a .json file and transfer the data to a global variable
        :param read_filename: Name of the file to be read, NEED the .json at the end
        :param return_content:  1 (default) for not returning the content inside the json file
                                0 for returning the content at the end
        :return: Make a global variable called "json_decode", all content in there
        If return_content is 1, does NOT return anything
        If return_content is 0, DOES return the content
        """
        global json_decode
        with open(read_filename) as json_data:
            json_decode = json.load(json_data)
            if return_content == 0:
                return json_decode


ydl_opts = {
    'simulate':             False,
    'forcetitle':           True,

    'format': 'bestaudio/best',

    'restrictfilenames':    True,   # if true, dont use "&" and " " characters when writing the file
    'ignoreerrors':         True,   # if true, dont stop downloading videos if a error occurs
    'nooverwrites':         True,   # if true, dont overwrite a file if it exists
    'playlistreverse':      False,  # if true, downloads all videos (from playlist) in the reverse order
    'no_warnings':          True,   # if true, dont show warnings (good for age restricted videos)
    'outtmpl':               '/mnt/phoenix/mgtow_archive/%(uploader)s/%(title)s.%(ext)s',


    # 'writeautomaticsub':    True,
    # 'subtitlesformat':      'srt'

}

json_handler = Json

# json_handler.encode(ydl_opts, "test.json")
json_handler.decode('test.json')
youtube_options = json_handler.decode('test.json', return_content=0)
print(youtube_options)