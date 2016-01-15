# socialnetwork_extract
Description and Caution:
===============
Extracting data from reddit and twitter without upper bounds.
Please get permission from twitter before extracting the data as this script scrapes off them. 

Installation:
===============
1. Install Anaconda Python 2.7 64 bit distribution Link: http://continuum.io/downloads#all
2. Clone to your desktop

```
git clone https://github.com/abhigenie92/social_network_extract
```
3. cd into cloned folder 
```
cd social_network_extract
```
4. and run the following command from terminal
```
python -m pip install -r requirements.txt
```

Use:
===============
Note please add the directory to your search path. An example is shown below:
```
import sys
sys.path.insert(0, "<path to social_network_extract>")
```
Twitter:
```
from twitter_script import search_twitter
search_twitter('china disaster")
```
Reddit:
```
from reddit_script import search_reddit
search_reddit('china disaster")
```
All extracted content is stored in databases
