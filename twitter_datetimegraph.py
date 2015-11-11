import sys,sqlite3,os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from pylab import figure,hist,num2date,plot_date,show,xticks,date2num
from matplotlib.dates import DateFormatter

reload(sys)                                         
sys.setdefaultencoding("utf-8")
def plot_date_time_graph(db_name,table_name):  
	format='%d %b %Y %I:%M %p'
	conn = sqlite3.connect(os.getcwd()+'/data/'+db_name+'.db')
	c=conn.cursor()
	date_time_arr=[]
	tweet_count=[]
	for row in c.execute('SELECT date_posted,time_posted From '+table_name):
		date_string= ' '.join(row)
		date_time_arr.append(datetime.strptime(date_string, format))

	for row in c.execute('SELECT retweets From '+table_name):
		tweet_count.append(row[0]+1)
		y= np.array(tweet_count)
		x=np.array(date_time_arr)
		N=len(tweet_count)
		colors = np.random.rand(N)
	numtime = [date2num(t) for t in x] 
 	# plotting the histogram
	ax = figure().gca()
	x, y, patches = hist(numtime, bins=50,alpha=.5)
	print x,y
	# adding the labels for the x axis
	tks = [num2date(p.get_x()) for p in patches] 
	xticks(tks,rotation=40)
	# formatting the dates on the x axis
	ax.xaxis.set_major_formatter(DateFormatter('%d %b %H:%M'))
	ax.set_xlabel('Time(dd-mm HH:MM)', fontsize=16)
	ax.set_ylabel('Tweet Count', fontsize=16)
	show()
 	# fig = plt.figure()
	# plt.plot(x,y,c=colors)
	# plt.xlabel('Time', fontsize=16)
	# plt.ylabel('Retweet Count', fontsize=16)
	# axes = plt.gca()
	# axes.set_ylim([min(y),max(y)+5])
	# #fig.savefig(table_name+'.png')
	# plt.show()
	# conn.close()

plot_date_time_graph('twitter_ShanghaiStampede_06-27_15-37-16','ShanghaiStampede')