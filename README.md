Description and Caution:
===============
Extracting data from reddit and twitter without upper bounds.
Please get permission from twitter before extracting the data as this script scrapes off them. 

Installation:
===============
1 . Clone to your desktop
```
git clone https://github.com/abhigenie92/social_network_extract
```
or
```
git clone git://github.com/abhigenie92/social_network_extract.git

```
2 . Pre-requisites:

Make sure to you have `python 2.7` and `Firefox`/`PhantomJS` installed. For installing `PhantomJS` on `linux` machines use the script `install_phantomjs.sh` or refer to http://phantomjs.org/build.html. In some cases the former may not work and the later is advised.
```
bash install_phantomjs.sh
```
On `Windows` machines, download `PhantomJS` and place `.exe` in the folder `social_network_extract` to work.


3 . Run the following command from terminal in folder `social_network_extract`
```
python -m pip install -r requirements.txt
```

Use:
===============
a.) as a module/library
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
b.) independent script

run the `run` script from terminal
```
bash ./run 
```
The above only run for twitter script, you can alternatively add a line to run the reddit script.
This will launch python as a background process. To check for completion, please check the output in file `output.txt`. 

Output:
===============


All extracted content is stored in databases.

Database Name Format: <social_network>_MM-DD_HH-MM-SS.db


Proxies Use:
===============

Use the other branch proxies_use and follow same above instructions.
Note: This will be a bit slower than normal. 
Special thanks to @DanMcInerney whose script is used here: https://github.com/DanMcInerney/elite-proxy-finder/blob/master/elite-proxy-finder.py
