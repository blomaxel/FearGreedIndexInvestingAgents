import datetime

timestamp_milliseconds = 1684368000000.0
timestamp_seconds = timestamp_milliseconds / 1000

# Convert to UTC date and time
utc_date_time = datetime.datetime.utcfromtimestamp(timestamp_seconds)

print("UTC Date and Time:", utc_date_time)
