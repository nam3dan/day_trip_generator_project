from lxml import html
import requests
import random

def get_destinations():
	'''
	This function is used to create the list of travel destinations. I wanted to flex my scraping abilities, so it pulls from Forbes.com.
	The function scrapes the Top Suggested locations, and removes locations which are not covered by Yelp. More on this later.
	'''

	url = 'https://www.forbes.com/sites/laurabegleybloom/2022/07/27/ranked-the-worlds-20-best-cities-in-2022-according-to-time-out/?sh=1dae77a87526'
	headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
	response = requests.request("GET", url, headers=headers)
	tree = html.fromstring(response.content)
	city_list_scrape = []
	pop_list = ['Medellín, Colombia','Marrakesh, Morocco','Cape Town, South Africa','Mumbai, India','MedellÃ\xadn, Colombia']
	for i in range (1,20):
		xpath_query = '//*[@id="article-stream-0"]/div[2]/div[2]/div[1]/div[3]/div[1]/h3[' + str(i) + ']/strong/text()'
		if tree.xpath(xpath_query) == []:
			continue
		else:
			city_raw = tree.xpath(xpath_query)[0]
			city_remove_unicode = city_raw.replace('\u200b\u200b','')
			city_final = city_remove_unicode.split('. ')[1]
			city_list_scrape.append(city_final)
			for i in city_list_scrape:
				if i in pop_list:
					city_list_scrape.pop(city_list_scrape.index(i))

	return city_list_scrape

def city_selector(city_list):
	city_selection, city_list = selection_rotator("Destination", city_list)
	return (city_selection, city_list)

def food_search(city_name):
	print("\nExcellent Choice! Now Let's look into Dining!\n")
	query_term = city_name.replace(', ','%2C+').replace(' ','%2C+')
	url = 'https://www.yelp.com/search?find_desc=food&find_loc=' + query_term
	headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36', 'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'}
	response = requests.request("GET", url, headers=headers)
	tree = html.fromstring(response.content)
	food_list = []
	try:
		for i in range(3,12):
			xpath_query_food = '//*[@id="main-content"]/div/ul/li['+ str(i) +']/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/div/div/h3/span/a/text()'
			restaurant = tree.xpath(xpath_query_food)[0].replace("â\x80\x99","'")
			food_list.append(restaurant)
	except:
		for i in range(8,17):
			xpath_query_food = '//*[@id="main-content"]/div/ul/li['+ str(i) +']/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/div/div/h3/span/a/text()'
			restaurant = tree.xpath(xpath_query_food)[0].replace("â\x80\x99","'")
			food_list.append(restaurant)
	food_selection, food_list = selection_rotator("Dining Experience", food_list)
	return(food_selection, food_list)

def entertainment_search(city_name):
	print("\nExcellent Choice! Now Let's look into Entertainment!\n")
	query_term = city_name.replace(', ','%2C+')
	url = 'https://www.yelp.com/search?find_desc=Entertainment&find_loc=' + query_term
	headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36', 'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'}
	response = requests.request("GET", url, headers=headers)
	tree = html.fromstring(response.content)
	entertainment_list = []
	try:
		for i in range(3,12):
			xpath_query_entertainment = '//*[@id="main-content"]/div/ul/li['+ str(i) +']/div/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div/h3/span/a/text()'
						#//*[@id="main-content"]/div/ul/li[3]/div/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div/h3/span/a
			venue = tree.xpath(xpath_query_entertainment)[0].replace("â\x80\x99","'")
			entertainment_list.append(venue)
	except:
		for i in range(8,17):
			xpath_query_entertainment = '//*[@id="main-content"]/div/ul/li['+ str(i) +']/div/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div/h3/span/a/text()'
						#//*[@id="main-content"]/div/ul/li[3]/div/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div/h3/span/a
			venue = tree.xpath(xpath_query_entertainment)[0].replace("â\x80\x99","'")
			entertainment_list.append(venue)
	entertainment_selection, entertainment_list = selection_rotator("Entertainment", entertainment_list)
	return(entertainment_selection, entertainment_list)

def greeting():
	city_list = get_destinations()
	print("\n\n\n\n\n\n\n\nHello and Welcome to nam3dan's Dope Ass Travel Agency")
	city_search_choice = False
	while city_search_choice == False:s
		city_search_choice_selection = int(input("\n\nWould you like to 1)look through our list of Citys or 2) do a custom search? Please respond with either a 1 or 2.: "))
		if city_search_choice_selection == 1:
			print("\n Generating a list of Top Travel Destinations")
			city_search_choice = True
			selected_city, city_list = city_selector(city_list)
		elif city_search_choice_selection == 2:
			custom_city = input("\n Please input custom search in 'City, Country' format: ")
			selected_city = custom_city
			city_search_choice = True
	selected_restaurant, food_list = food_search(selected_city)
	selected_entertainment, entertainment_list = entertainment_search(selected_city)


def selection_rotator(keyword, selection_list):
	full_list = []
	confirmed_selection = False
	while confirmed_selection == False:
		random_selection = selection_list[random.randint(0,len(selection_list)-1)]
		print("\nWe have selected %s as your %s.\n" % (random_selection, keyword))
		confirmation = input("\nDo you want to confirm this option? (y|n): ")
		if confirmation == "y":
			confirmed_food = True
			selected_option = random_selection
			selection_list = full_list + selection_list
			return (selected_option, selection_list)
		else:
			if len(selection_list)>1:
				full_list.append(selection_list.pop(selection_list.index(random_selection)))
			else:
				selection_list = full_list + selection_list
