from bs4 import BeautifulSoup
import certifi
import urllib3

#urllib3.disable_warnings()
http = urllib3.PoolManager(
	cert_reqs='CERT_REQUIRED',
	ca_certs=certifi.where())

BASE_URL = "https://swappa.com/"

def get_listing_links(action_path,device_path,max_price,min_storage):
	r = http.request('GET',BASE_URL + action_path + device_path)
	html = r.data
	soup = BeautifulSoup(html, "lxml")
	
	section_main = soup.find("section",id="section_main")
		
	listing_previews = section_main.find_all("div",{"class":"listing_preview"})

	price_matched_listings = [listing for listing in listing_previews if int(listing["data-price"]) <= max_price]

	storage_matched_listings = [listing for listing in price_matched_listings if int(listing["data-storage"]) >= min_storage]

	listing_links = ["<a href='" 
					+ BASE_URL 
					+ listing["data-url"] 
					+ "'>" 
					+ device_path
					+ "-"
					+ listing["data-condition"] 
					+ "-" 
					+ listing["data-price"] 
					+ "-"
					+ listing["data-storage"]
					+ "</a><br/>" 					
					for listing in storage_matched_listings]

	html_str="<html>"+''.join(listing_links)+"</html>"

	Html_file=open(device_path+".html","w")
	Html_file.write(html_str)
	Html_file.close()

	print(html_str)

get_listing_links("buy/","apple-iphone-6s-plus-a1634-unlocked",450,3)
get_listing_links("buy/","apple-iphone-6s-a1633-unlocked",400,3)
