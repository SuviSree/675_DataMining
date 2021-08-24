
import tweepy as tw
import csv
import datetime


#Fill Twitter Keys
consumer_key      = "" 
consumer_secret   = ""
access_token       = ""
access_token_secret = ""

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Define the search term and the date_since date as variables
#search_words = "#FarmersProtest" #in seq the tweet file is generated
#search_words = "#FarmBills"
#search_words = "#FarmerFirst"
#search_words = "#farmer"
#search_words = "#FarmersWithModi"
#search_words = "#FranceBeheading"
#search_words ="#ViennaTerrorAttack"
#search_words ="#USElection2020"
search_words="#ViennaAttack"
#Mention date range for which you want to scrap tweets
date_since = "2020-11-04"
date_until = "2020-11-05"
suff=datetime.datetime.now().time()
filename = search_words+"Tweet_"+date_since+"_Vishal.csv"
# Open/create a file to append data to
csvFile = open(filename, 'a+',encoding="utf-8",newline='')
csvWriter = csv.writer(csvFile,delimiter='~')

for tweet in tw.Cursor(api.search,
              q=search_words,
              lang="en",
              until=date_until,
              since=date_since).items():
    newt=tweet._json  
    data=(newt['created_at'],newt['id_str'],newt['text'],newt['geo'],newt['coordinates'],newt['place'],newt['retweet_count'],newt['retweeted'],newt['lang'],newt['user']['location'],newt['user']['id_str'],newt['user']['name'],newt['user']['screen_name'],newt['user']['description'],newt['user']['created_at'],newt['user']['utc_offset'],newt['user']['time_zone'],newt['user']['geo_enabled'],newt['user']['verified'],newt['user']['lang'])
    csvWriter.writerow([data])
    print(tweet.created_at)
print("Done")
csvFile.close()