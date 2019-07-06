import youtube_dl

now = youtube_dl.DateRange.day("now")
day_one = youtube_dl.DateRange.day("now")


# day_start = youtube_dl.DateRange.day("now").start
# day_final = youtube_dl.DateRange.day("2day").end

test = youtube_dl.DateRange.__init__(youtube_dl.DateRange, "20190702", "20190704")

print(test)