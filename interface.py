from json import dump, load
from get_data import *
from format_raw_info import *
import datetime
import os

MAIN = 0
CONFIG = 1
QUIT = 2

# helpers
def load_config():
	""" load config file, if no config found, create one
	"""
	config = {
		"query": "",
		"links": "",
		"data": "",
		"temp": "",
		"driver": ""
	}
	try:
		with open("./config.json", "r") as f:
			config = load(f)   
	except:
		save_config(config)
	return config 


def save_config(config):
	""" save config file
	"""
	config['data'] = config['data'] + "/" if config['data'] != "" and config['data'][-1] != "/"else config['data']
	config['temp'] = config['temp'] + "/" if config['temp'] != "" and config['temp'][-1] != "/" else config['temp']
	if config['data'] != "" and not os.path.isdir(config['data']):
		os.mkdir(config['data'])
	if config['temp'] != "" and not os.path.isdir(config['temp']):		
		os.mkdir(config['temp'])
	with open("./config.json", "w") as f:
		dump(config, f, indent=2)


# menu stages
def main_menu(config):
	print("SELECT OPTIONS:")
	print("1. Run Scraper for links")
	print("2. Run Scraper for listing information")
	print("3. Run Scraper for listing avalibility")
	print("4. Change config")
	print("INPUT q TO EXIT")
	option = input("> ")
	while True:
		if option == "1":
			get_links_by_location_file(config['driver'], config['query'], config['links'])
			return MAIN
		
		elif option == "2":
			get_listings_information_by_url_file(config['links'], config['temp'])
			save_raw_listing_info(config['temp'], config['data'])
			return MAIN
		elif option == "3":
			try:
				print("\nINPUT CHECK-IN CHECK-OUT TIME AS [YYYY-MM-DD YYYY-MM-DD]")
				print("OTHERWISE TODAY TOMORROW WILL BE USED")
				get = input("> ")
				if get == "q":
					return MAIN
				date_in, date_out = get.split(" ")
				datetime.strptime(date_in, "%Y-%m-%d")
				datetime.strptime(date_out, "%Y-%m-%d")
			except:
				today = datetime.date.today()
				tomorrow = today + datetime.timedelta(days=1)
				today_s = today.strftime("%Y-%m-%d")
				tmr_s = tomorrow.strftime("%Y-%m-%d")
				date_in, date_out = today_s, tmr_s
			get_availabilities_by_url_file(config['links'], date_in, date_out, config['driver'], config['temp'])
			save_raw_avalibility(config['temp'], config['data'], date_in, date_out)
			return MAIN
			
		elif option == "4":
			return CONFIG
			
		elif option == "q":
			return QUIT
		option = input("> ")





def config_menu(config):
	print("CURRENT CONFIG:")
	print("[Q] [" + config['query'] + "] - search queries (txt file for multiple queries)")
	print("[L] [" + config['links'] + "] - output of found links from search")
	print("[D] [" + config['data'] + "] - folder to store accomendation information and avalibility")
	print("[T] [" + config['temp'] + "] - folder for intermediate or temp data")
	print("[R] [" + config['driver'] + "] - filename of the chrome driver")
	print("INPUT q TO GO BACK TO MAIN\nINPUT [OPTION] [DEST] TO CHNAGE CONFIG")
	while True:
		get = input("> ")
		if get == "q":
			return MAIN

		try:
			t, v = get.split(" ")
			target = {'Q': 'query', 'L': 'links', 'D': 'data', 'T': 'temp', 'R': 'driver'}
			if t in target.keys():
				config[target[t]] = v
				save_config(config)

		except: 
			pass



if __name__ == "__main__":
	state = MAIN
	config = load_config()

	while state != QUIT:
		print()
		if state == MAIN:
			state = main_menu(config)
		elif state == CONFIG:
			state = config_menu(config)
		else:
			state = QUIT


