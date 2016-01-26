# socialnetwork_extract
Description and Caution:
===============
Extracting data from reddit and twitter without upper bounds.
Please get permission from twitter before extracting the data as this script scrapes off them. 

Installation:
===============
1. Make sure to you have python 2.7 and PhantomJS installed. For installing PhantomJS on linux machines use the script 'install_phantomjs.sh'.
```
bash install_phantomjs.sh
```
On Windows machines, download PhantomJS and place `.exe` in the folder social_network_extract to work.
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
All extracted content is stored in databases.

Database Name Format: <social_network>_MM-DD_HH-MM-SS.db
