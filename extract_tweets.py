from bs4 import BeautifulSoup
from datetime import datetime
from unidecode import unidecode
import retweetsAndFavExtract
def extract_tweets(alltweets):
	text_tweet=[];text_date=[];text_time=[];text_username=[];text_profilename=[];text_retweet=[];text_fav=[];
	#alltweets = soup.find_all(attrs={'role' : 'presentation','class':"original-tweet-container"})
	for index,tweet in enumerate(alltweets):
		#Text of tweet
		html_tweet= tweet.find_all("p", class_="TweetTextSize js-tweet-text tweet-text")
		#print html_tweet
		#print "new" 
		#print html_tweet[0]
		try:
			text=''.join(html_tweet[0].findAll(text=True))
		except Exception as e:
			continue
		text=unidecode(text.replace('\n',''))
		text_tweet.append(text)
		#print text_tweet	
		#Date and time of tweet
		html_date=tweet.find_all("a", class_="tweet-timestamp js-permalink js-nav js-tooltip")
		time,date=html_date[0]["title"].split(" - ")
		text_date.append(date)
		text_time.append(time)
		#Username of tweeter
		html_username=tweet.find_all("span",class_="username js-action-profile-name")
		text_username.append(''.join(html_username[0].findAll(text=True)).replace("@",""))
		#profile name
		html_profilename=tweet.find_all("strong",class_="fullname js-action-profile-name show-popup-with-id")
		if len(html_profilename)==0:
				html_profilename=tweet.find_all("strong",class_="fullname js-action-profile-name show-popup-with-id fullname-rtl")
		#print html_profilename
		text_profilename.append(''.join(html_profilename[0].findAll(text=True)))
		#Retweets and fav
		map(lambda l,v: l.append(v), (text_retweet, text_fav), retweetsAndFavExtract.get_fav_retweets(tweet))
	print "Tweets extracted:",str(len(alltweets))
	return text_tweet,text_date,text_time,text_username,text_profilename,text_retweet,text_fav