import os,sqlite3,pdb
from random import randint
from pprint import pprint

def get_proxy():
	if os.path.exists('/libs/hide_my_python/hello.db'):
		os.remove('./libs/hide_my_python/hello.db')
	os.system('python3 ./libs/hide_my_python/hide_my_python.py -n 100 -pr http -s -o hello.db')
	conn = sqlite3.connect('./libs/hide_my_python/hello.db')
	c=conn.cursor()
	proxies=[]
	for row in c.execute('SELECT * From proxies'):
		proxies.append(row)
	num_proxies=len(proxies)
	proxy_selected=proxies[randint(0,num_proxies-1)]
	pdb.set_trace()
	return proxy_selected[1]+':'+str(proxy_selected[2]),proxy_selected[3].lower()



def get_proxy_fastest_more_than_one():
    if os.path.exists('./proxy_details.txt'):
        os.remove('./proxy_details.txt')
    print 'Getting proxy'
    os.system('python ./elite-proxy-finder.py -s 10 > ./proxy_details.txt')
    text_file = open("./output.txt", "r")
    lines = text_file.readlines()
    line_nos=range(7,44,4)
    ip_addr_port=[]
    for line in line_nos:
        ip_addr_port.append(lines[line].split('|')[0].replace(' ',''))
    return ip_addr_port

def get_proxy_fastest():
    if os.path.exists('./proxy_details.txt'):
        os.remove('./proxy_details.txt')
    print 'Getting proxy'
    os.system('python ./elite-proxy-finder.py -s 1 > ./proxy_details.txt')
    text_file = open("./proxy_details.txt", "r")
    lines = text_file.readlines()
    line=7
    try:
    	ip_addr_port=lines[line].split('|')[0].replace(' ','')
    	return [ip_addr_port]
    except Exception:
        return False

if __name__ == '__main__':
    get_proxy_fastest()
