from dottorrent import Torrent

trackers_list = [
    "udp://tracker4.itzmx.com:2710/announce",
    "udp://tracker2.itzmx.com:6961/announce",
    "https://t.quic.ws:443/announce",
    "https://tracker.fastdownload.xyz:443/announce",
    "http://torrent.nwps.ws:80/announce",
    "udp://explodie.org:6969/announce",
    "http://tracker2.itzmx.com:6961/announce",
    "https://tracker.gbitt.info:443/announce",
    "http://tracker4.itzmx.com:2710/announce",
    "udp://tracker.trackton.ga:7070/announce",
    "udp://tracker.tvunderground.org.ru:3218/announce",
    "http://explodie.org:6969/announce",
    "http://open.trackerlist.xyz:80/announce",
    "udp://retracker.baikal-telecom.net:2710/announce",
    "http://open.acgnxtracker.com:80/announce",
    "udp://tracker.swateam.org.uk:2710/announce",
    "udp://tracker.iamhansen.xyz:2000/announce",
    "http://tracker.gbitt.info:80/announce",
    "udp://retracker.lanta-net.ru:2710/announce",
    "http://tracker.tvunderground.org.ru:3218/announce",
    "udp://retracker.netbynet.ru:2710/announce",
    "udp://tracker.supertracker.net:1337/announce",
    "udp://ipv4.tracker.harry.lu:80/announce",
    "udp://tracker.uw0.xyz:6969/announce",
    "udp://zephir.monocul.us:6969/announce",
    "udp://tracker.moeking.me:6969",
    "udp://tracker.filemail.com:6969/announce",
    "udp://tracker.filepit.to:6969/announce",
    "wss://tracker.openwebtorrent.com:443/announce",
    "http://gwp2-v19.rinet.ru:80/announce",
    "http://vps02.net.orel.ru:80/announce",
    "http://tracker.port443.xyz:6969/announce",
    "http://mail2.zelenaya.net:80/announce",
    "http://open.acgtracker.com:1096/announce",
    "http://tracker.vivancos.eu/announce",
    "udp://carapax.net:6969/announce",
    "udp://tracker.novg.net:6969/announce",
    "http://tracker.novg.net:6969/announce",
    "http://carapax.net:6969/announce",
    "udp://torrentclub.tech:6969/announce",
    "udp://home.penza.com.ru:6969/announce",
    "udp://tracker.dyn.im:6969/announce",
]

root_path = "/mnt/phoenix/mgtow-archive/"
channel_path = "Happy_Humble_Hermit/"
full_channel_path = root_path + channel_path


source_str = "mgtow-archive"
comment_str = "Videos downloaded using mgtow-archive, github project page: https://github.com/PhoenixK7PB/mgtow-archive"
created_by_str = "https://github.com/PhoenixK7PB/mgtow-archive"

torrent = Torrent(path=root_path + "download_archive", trackers=trackers_list, piece_size=None, source=source_str,
                  comment=comment_str, created_by=created_by_str)
print(torrent.get_info())
torrent.generate()
with open(root_path + "download_archive.torrent", 'wb') as f:
    torrent.save(f)
print("DONE!")
