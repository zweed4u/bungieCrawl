import os, json, requests, threading
colorCodes = {
    'red':'\033[31m',
    'orange':'\033[33m',
    'blue':'\033[34m',
    'purple':'\033[35m',
    'cyan':'\033[36m',
    'lightgrey':'\033[37m',
    'darkgrey':'\033[90m',
    'lightred':'\033[91m',
    'lightgreen':'\033[92m',
    'yellow':'\033[93m',
    'lightblue':'\033[94m',
    'pink':'\033[95m',
    'lightcyan':'\033[96m',
    'fail':'\033[31m',
    'colorend':'\033[0m'
}

apikey="API KEY HERE"
minhash=100000
maxhash=10000000000
headers={
	"X-API-Key": apikey
}
baseurl="http://www.bungie.net/platform/Destiny/Manifest/InventoryItem/"
increment=(maxhash-minhash)/4
quartile1=minhash+increment
quartile2=minhash+(increment*2)
quartile3=minhash+(increment*3)
quartile4=minhash+(increment*4) # top - synonymous with maxhash
assert maxhash == quartile4, "Error Message: Math is wrong - check allocation of threaded ids"

def scrape(starthash, endhash):
	session=requests.session()
	while starthash<endhash:
		response=session.get('{}{}'.format(baseurl, str(starthash)), headers=headers)
		try:
			# file io would be good here to not have to keep track of terminal output
			print("[[{}]] {} :: {}".format(str(threading.current_thread().getName()), starthash, response.json()['Response']['data']['inventoryItem']['itemName']))
			# lol os.system("say [[rate 400]] hash found at {}".format(starthash))
		except:
			print("[[{}]] {} :: {}ERROR RESOLVING JSON KEYS{}".format(str(threading.current_thread().getName()), starthash, colorCodes['fail'], colorCodes['colorend']))
		starthash+=1

if __name__ == '__main__':
	t1 = threading.Thread(target=scrape, args=(int(minhash),int(quartile1),)) #arbitrary
	t1.start()

	t2 = threading.Thread(target=scrape, args=(int(quartile1),int(quartile2),)) #arbitrary
	t2.start()

	t3 = threading.Thread(target=scrape, args=(int(quartile2),int(quartile3),)) #arbitrary
	t3.start()

	t4 = threading.Thread(target=scrape, args=(int(quartile3),int(quartile4),)) #arbitrary
	t4.start()
