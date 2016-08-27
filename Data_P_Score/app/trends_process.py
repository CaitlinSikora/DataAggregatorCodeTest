from pytrends.pyGTrends import pyGTrends
import time
from random import randint

google_username = "poorricharddance@gmail.com"
google_password = "AHollowDream"

# connect to Google
connector = pyGTrends(google_username, google_password)

# make request
data = connector.request_report("Pizza")

print data