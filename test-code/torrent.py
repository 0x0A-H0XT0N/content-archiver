import qbittorrentapi

client = qbittorrentapi.Client(host="localhost:8080", username="root", password="benk2364")
# client = qbittorrentapi.Client(host="localhost:8080")

# Print version:
print(client.app_version())


