from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import requests as req
import json
import re

current_page = 1

objeto = input("O que vc quer achar? ")

objeto = objeto.replace(" ", "+")

my_url = "https://busca.magazineluiza.com.br/busca?q=" + objeto + "&page=1"

header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}

filename = "magalu_" + objeto + ".csv"

f = open(filename, "w")

headers = "Produto, Link, Preco\n"

f.write(headers)

uClient = uReq(my_url)

page_html = uClient.read()

page_soup = soup(page_html, "html.parser")

last = page_soup.find("li", class_ = "neemu-pagination-last")

last_page = last.a["href"][last.a["href"].find("page=") + 5 : len(last.a["href"])]
# re.split('\\blow\\b',string)[-1]

# print(last_page)

items = page_soup.find_all("li", class_ = "nm-product-item")

count = 0

while current_page < int(10):
	my_url_new = my_url[:len(my_url) - 1] + str(current_page)

	# print(my_url_new)

	# print(current_page)

	uClient = uReq(my_url_new)

	page_html = uClient.read()

	page_soup = soup(page_html, "html.parser")

	last = page_soup.find("li", class_ = "neemu-pagination-last")

	items = page_soup.find_all("li", class_ = "nm-product-item")

	last_page = last.a["href"][last.a["href"].find("page=") + 5 : len(last.a["href"])]

	for item in items:
			name = item.a["title"]
			link = item.a["href"]
			get_price = json.loads(item.a["data-product"])

			#print(name, link[2:], get_price['price'])

			f.write(name.replace(",",".") + "," + link[2:] + "," + get_price["price"].replace(",",".") + "\n")
			# print(current_page)
			count += 1
			

	current_page += 1

print(10*"#","Finalizado",10*"#")

print("Foram encontrados " + str(count) + objeto.replace("+", " "))

f.close()