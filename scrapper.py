from bs4 import BeautifulSoup as bs
import requests
import json
import selenium as se
from selenium import webdriver
import os
import sys
#if the internet connection is slow please change the timeout value in line26 and line38 to higher value
#cli-usage python3 scrapper.py area-name city-name 
def main() :
	output=[]
	inp_a = sys.argv[1]
	inp_c = sys.argv[2]
	inp_a.lower()
	inp_c.lower()
	inp_area = ""
	for i in range(len(inp_a)) :
		if inp_a[i] == ' ' :
			inp_area += "_"
		elif inp_a[i] == '-' :
			inp_area += "_"
		else :
			inp_area += inp_a[i]
	home = 'https://zolostays.com/pgs-in-'+inp_area+'-'+inp_c
	response = requests.get(home, timeout=30)
	print(response)
	page = bs(response.content, "html.parser")
	names = []
	locations = []
	coordinates = []
	for name in page.findAll('h2', attrs = {'class' : 'cardTitle'}) :
		names.append("\"Property Name\":"+"'"+name.get_text()+"'")
	room_T = []
	room_R = []
	for urls in page.findAll('a', attrs= {'class' : 'card'}) :
		url = urls['href']
		url = 'https://zolostays.com' + url
		response = requests.get(url, timeout=30)
		content = bs(response.content, "html.parser")
		room_types = []
		room_rates = []
		room_rate = []
		for room in content.findAll('div', attrs = {'class' : 'pills'}) :
			room_type = ""
			for number in room.findAll('div') :
				number.decompose()
			room_type = room_type+"\""+room.get_text()+"\""
			room_types.append(room_type)
		room_T.append(room_types)
		for r in content.findAll('div', attrs = { 'class':'room-type__content'}):
			room_rate = ""
			for p in r.findAll('div', attrs = {'class' : 'mobile'}) :
				if room_rate != "" :
					room_rate = room_rate + ",{"
				else :
					room_rate = room_rate+"{"
				for price in p.find_parents('div', attrs = {'class' : 'table__col'}) :
					for g in price.findAll('div', attrs = {'class' :  'mobile'}) :
						h = g.get_text()
					for number in price.findAll('div') :
						number.decompose()
					l = price.get_text()
					room_rate = room_rate+"\""+l+"\":\""+h+"\""
					room_rate = room_rate+"}"
			room_rates.append(room_rate)
		room_R.append(room_rates)
		for maps in content.findAll('a', attrs = {'class':'gmap'}) :
				url = 'http://checkshorturl.com/expand.php?u='
				link = maps["href"]
				url = url+link
				response = requests.get(url, timeout=5)
				content = bs(response.content, "html.parser")
				for u in content.findAll('a', attrs = {'target' : '_blank'} ) :
					target_url = u['href']
					break
				count = 0
				lat=""
				long=""
				pos=True
				comma = 0
				for j in range(len(target_url)) :
					if target_url[j] == '/' :
						count+= 1
					if count == 6 :
						for k in range(j+2, len(target_url)) :
							if target_url[k] == ',' :
								comma+= 1
								pos = False
								continue
							if comma == 2 :
								count+=1
								break
							if pos :
								lat+= target_url[k]
							else :
								long+= target_url[k]
					if count == 7 :
						break
				coordinates.append("\"Coordinates\":"+"\""+lat+"Latitude,"+long+"Longitude"+"\"")
	for location in page.findAll('h3', attrs = {'class' : 'dTitle'}) :
		locations.append("\"Location\":"+"'"+location.get_text()+"'")
	for i in range(len(names)) :
		out = "PG = ("+names[i]+","+locations[i]+"," + coordinates[i]+","
		room_string = ""
		for j in range(len(room_T[i])) :
			if room_string != "" :
				room_string = room_string + "," + room_T[i][j]+":"+room_R[i][j]
			else :
				room_string = room_string +room_T[i][j]+":"+room_R[i][j]
		out = out + room_string+")"
		print(out)
		output.append(out)
	if len(output) == 0 :
		print('No pgs found in the given area or Please check the spelling of the area and retype it.')
		
if __name__ == '__main__':
	main()