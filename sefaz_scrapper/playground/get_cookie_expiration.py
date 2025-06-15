import datetime

timestamp = 1780958071

dt = datetime.datetime.utcfromtimestamp(timestamp)
print(dt.strftime('%Y-%m-%d %H:%M:%S'))
# Output: 2026-06-08 22:34:31