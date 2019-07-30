import qbittorrentapi

client = qbittorrentapi.Client(host="localhost:8080")

# Print version:
print("version: ", client.app_version())

# Print default save path:
print("default save path: ", client.app_default_save_path())

# Print a dict of preferences
print("preferences: ", client.app_preferences())

# Set a preference
preferences = dict()
preferences["web_ui_username"] = "root"
client.app_set_preferences(preferences)

# Print download and upload limit from Transfer
if client.transfer_download_limit() == 0:
    print("Transfer Download limit: \u221e")
else:
    print("Transfer Download limit: ", client.transfer_download_limit())
if client.transfesr_upload_limit() == 0:
    print("Transfer Upload limit: \u221e")
else:
    print("Transfer Upload limit: ", client.transfer_upload_limit())

# List active torrents
completed_torrents = client.torrents_info(status_filter="active")
for torrent in completed_torrents:
    print("Completed torrent name: ", torrent.name)

torrent_list = client.torrents_info()
for torrent in torrent_list:
    pass

client.torrents_add()



