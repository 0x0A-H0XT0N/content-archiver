import qbittorrentapi

client = qbittorrentapi.Client(host="localhost:8080")

# Print version:
# print(client.app_version())

print(client.auth_log_in())
