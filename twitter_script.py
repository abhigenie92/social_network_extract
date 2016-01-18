#Things to fix still
#1.Scroll down to get unlimited tweets-DONE
#2.Fix other language profile names-DONE
#3.Fix remove of photos thumbnails as tweets-DONE
#4.Better way to print the progress-?
from bs4 import BeautifulSoup
from datetime import datetime
from scrollDownHtmlCode import return_html_code
from pprint import pprint
from unidecode import unidecode

#from twitter_datetimegraph import plot_date_time_graph 
import sys,requests,retweetsAndFavExtract,sqlite3,os,pdb
reload(sys)
sys.setdefaultencoding("utf-8")

def get_twitter_data(query):
	search = query.replace(" ","%20")	
	text_tweet=[];text_date=[];text_time=[];text_username=[];text_profilename=[];text_retweet=[];text_fav=[];
	url='https://twitter.com/search?q='+search+'&src=typd&lang=en'
	#req = requests.get(url)
	#soup = BeautifulSoup(req.content)
	print "Opening Firefox Browser, minimize in case you want."
	html_full=return_html_code(url)
	soup = BeautifulSoup(html_full, "html.parser")
	alltweets = soup.find_all(attrs={'data-item-type' : 'tweet','class':"js-stream-item stream-item stream-item expanding-stream-item "})
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
	print "Date of most old tweet:",str(text_date[len(text_date)-1])
	return query,text_tweet,text_date,text_time,text_username,text_profilename,text_retweet,text_fav

def write_data_to_db(search,text_tweet,text_date,text_time,text_username,text_profilename,text_retweet,text_fav):
	db_name=('twitter '+search.title().replace(" ","")+'_'+str(datetime.now())[5:19]+'.db').replace(" ","_").replace(":","-")
	path='data'+os.path.sep+db_name
	conn = sqlite3.connect(path)
	table_name=search.title().replace(" ","")
	conn.execute('CREATE TABLE '+table_name+' (content text,date_posted text,time_posted text,username \
		text,profilename text,retweets numeric,favs numeric)')
	values=zip(text_tweet,text_date,text_time,text_username,text_profilename,text_retweet\
				,text_fav)
	conn.executemany("INSERT INTO "+table_name+ "(content,date_posted,time_posted,username,profilename,\
				retweets,favs)VALUES (?,?,?,?,?,?,?)",values)
	conn.commit()
	conn.close()
	return db_name
def search_twitter(query):
	db_name=write_data_to_db(*get_twitter_data(query))
	print 'Data stored at - .'+os.path.sep+'data'+os.path.sep+ db_name
	#plot_date_time_graph(db_name,search.title().replace(" ",""))
if __name__ == '__main__':
	directory='data' # stores the output
	if not os.path.exists(directory): os.makedirs(directory)
	search_twitter('Alcoholics Anonymous');
