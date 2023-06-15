import requests 
from bs4 import BeautifulSoup as bs


url = 'https://finance.naver.com/sise/lastsearch2.naver'  
response = requests.get(url)    
html_text = response.text
html = bs(html_text, 'html.parser')
names = html.select('tr a')
prices = html.select('tr td.number')

name_list=[]
for name in names:
    name_list.append(name.text)
    

dictionary = {}

i=0
j=0
for price in prices:
    if(i%10==1):
       dictionary[name_list[j]]=price.text
       j+=1
    i+=1
