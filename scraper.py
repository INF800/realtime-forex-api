import requests
from bs4 import BeautifulSoup 
import csv 
import pandas as pd
import sys, time


class CurPairScraper():
	
	def __init__(self, url):
		self.names=[]
		self.prices=[]
		self.changes=[]
		self.percentChanges=[]
		
		self.supported_urls = ["https://finance.yahoo.com/currencies"]
		if url in self.supported_urls:
			self.url = url
		else:
			raise Exception("URL Not Supported. Currently we support only https://finance.yahoo.com/currencies")


	def get_pandasDF(self):
		r= requests.get(self.url)
		data=r.text
		soup=BeautifulSoup(data, features='lxml')
		
		for i in range(40, 404, 14):
			for listing in soup.find_all('tr', attrs={'data-reactid':i}):
				
				for name in listing.find_all('td', attrs={'data-reactid':i+3}):
					self.names.append(name.text)
				for price in listing.find_all('td', attrs={'data-reactid':i+4}):
					self.prices.append(price.text)
				for change in listing.find_all('td', attrs={'data-reactid':i+5}):
					self.changes.append(change.text)
				for percentChange in listing.find_all('td', attrs={'data-reactid':i+7}):
					self.percentChanges.append(percentChange.text)
					
		all_cur_pairs = pd.DataFrame({"names": self.names, "prices": self.prices, "changes": self.changes, "per_changes": self.percentChanges})
		self.names = []
		self.prices = []
		self.changes = []
		self.percentChanges = []
		return all_cur_pairs
	
	
	def obj_genrator(self):
		
		all_pairs = self.get_pandasDF()
		num_rows  = len(all_pairs)
		for row in range(num_rows): 
			yield {
				"row_num"    : str(row),
				"total_rows" : str(num_rows),
				"name"       : all_pairs.loc[row, "names"],
				"price"      : all_pairs.loc[row, "prices"],
				"change"     : all_pairs.loc[row, "changes"],
				"per_change" : all_pairs.loc[row, "per_changes"]
			}
		
		
#end class







if __name__ == "__main__":
	"""
	#usage:
	=======
	
	scraper = CurPairScraper("https://finance.yahoo.com/currencies")
	
	while (True):
		for pair_info in scraper.obj_genrator():
			print(pair_info)
	"""
	pass