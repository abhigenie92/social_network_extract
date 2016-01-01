#Things to fix still
#1.Correct date and time conversion, some weird issue with UTC specification-DONE
#2.Extract more than 1000 reddits
import praw,time,sys,sqlite3,os
from datetime import datetime
from bs4 import BeautifulSoup
reload(sys)                                         
sys.setdefaultencoding("utf-8")                           #change underlying encoding in python
import socket
socket.getaddrinfo('localhost', 8080)                     #takes care of error in host

def write_data_to_db(search,title,subreddit,selftext_html,ups,created_date,created_time,num_comments,score,url,permalink):
	db_name=('reddit '+search.title().replace(" ","")+'_'+str(datetime.now())[5:19]+'.db').replace(" ","_").replace(":","-")
	path='data\\'+db_name
	print path
	conn = sqlite3.connect(path)
	table_name=search.title().replace(" ","")
	conn.execute('CREATE TABLE '+table_name+' (title text,subreddit text,selftext_html text,ups numeric,created_date text,\
		created_time text,num_comments numeric,score numeric,url text,permalink text)')
	values=zip(title,subreddit,selftext_html,ups,created_date,created_time,num_comments,score,url,permalink)
	conn.executemany("INSERT INTO "+table_name+ "(title,subreddit,selftext_html,ups,created_date,\
		created_time,num_comments,score,url,permalink)VALUES (?,?,?,?,?,?,?,?,?,?)",values)
	conn.commit()
	conn.close()

def get_data_reddit(search):              
	username="stampede_bot"
	password="stampedes123"
	r = praw.Reddit(user_agent='Access Denied')
	r.login(username,password,disable_warning=True)
	posts=r.search(search, subreddit=None,sort=None,syntax=None,limit=None)
	title=[];subreddit=[];selftext_html=[];description=[];ups=[];created_date=[];created_time=[];num_comments=[];score=[];url=[];permalink=[]
	#Note selftext_html is blank in posts with no text and only urls. The url is stored in url[] and permalink is link to the reddit post.
	for index,post in enumerate(posts):	
		dateandtime=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(post.created_utc))	
		date,timec=dateandtime.split(" ")
		selftext=post.selftext_html
		if selftext:
			soup = BeautifulSoup(selftext)
			selftext=soup.get_text()
		title.append(post.title);subreddit.append(str(post.subreddit));selftext_html.append(selftext);   \
		ups.append(post.ups);created_date.append(date);created_time.append(timec);num_comments.append(post.num_comments);score.append(post.score) \
		;url.append(post.url); permalink.append(post.permalink)
	print "Reddits extracted: "+str(len(title))	
	return search,title,subreddit,selftext_html,ups,created_date,created_time,num_comments,score,url,permalink
def search_reddit(query):
	write_data_to_db(*get_data_reddit(query))   #* used to unpack values

if __name__ == '__main__':
	directory='./data'
	if not os.path.exists(directory):
		os.makedirs(directory)
	search_query='china stampede'
	search_reddit(search_query)
