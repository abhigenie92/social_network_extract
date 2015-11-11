from bs4 import BeautifulSoup
def get_fav_retweets(tweet):		
	#retweets
	pre_filter_html_retweet=tweet.find_all("div",class_="ProfileTweet-action ProfileTweet-action--retweet js-toggleState js-toggleRt")
	if pre_filter_html_retweet:
		html_retweet=pre_filter_html_retweet[0].find_all("span",class_="ProfileTweet-actionCountForPresentation")
		text_retweet=''.join(html_retweet[0].findAll(text=True))
		if len(text_retweet)==0:
			text_retweet=0 
	else:
		pre_filter_html_retweet=tweet.find_all("span",class_="ProfileTweet-action--retweet u-hiddenVisually")
		html_retweet=pre_filter_html_retweet[0].find_all("span",class_="ProfileTweet-actionCount" )
		text_retweet=''.join(html_retweet[0].findAll(text=True)).replace(' retweets',"").replace("\n","")
		if len(text_retweet)==0:
			text_retweet=0 
	#favourites			
	pre_filter_html_fav=tweet.find_all("div",class_="ProfileTweet-action ProfileTweet-action--favorite js-toggleState")
	if pre_filter_html_fav:
		html_fav=pre_filter_html_fav[0].find_all("span",class_="ProfileTweet-actionCountForPresentation")
 		text_fav=''.join(html_fav[0].findAll(text=True))
 		if len(text_fav)==0:
 			text_fav=0
	else:
		pre_filter_html_fav=tweet.find_all("span",class_="ProfileTweet-action--favorite u-hiddenVisually")
		html_fav=pre_filter_html_fav[0].find_all("span",class_="ProfileTweet-actionCount" )
		text_fav=''.join(html_fav[0].findAll(text=True)).replace(' favorites',"").replace("\n","")
		if len(text_retweet)==0:
			text_fav=0 
	return	text_retweet,text_fav


