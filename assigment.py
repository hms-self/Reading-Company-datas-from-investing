import bs4
import requests
from bs4 import BeautifulSoup
import csv


with open('all_stocks_last.csv', 'w', newline='') as newcsv_file:
  with open('all_stocks.csv', 'r',encoding='utf-8-sig') as pastcsv_file:

    csv_reader= csv.reader(pastcsv_file)

    csv_writer=csv.writer(newcsv_file)
    csv_writer.writerow(['Symbol', 'Industry', 'Sector', 'N_employees', 'Info', 'Info_short']) #headers
    lines=list(csv_reader)


    for i in range(len(lines)):

      try:
        symbol=lines[i][0]
        url='https://tr.investing.com/search/?q='+lines[i][0]  #searching page for each stocks
        r=requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})
        soup=BeautifulSoup(r.content,'lxml')
        pluslink=soup.find('a',{'class':"js-inner-all-results-quote-item row"}).get("href") #Company profile link which are all unique and detected in 'search page' at line21
        url2='https://tr.investing.com'+pluslink+'-company-profile' #final link that we want to reach
        r2=requests.get(url2,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})
        soup2=BeautifulSoup(r2.content,'lxml')
        industry=soup2.find('div',{'class':"companyProfileHeader"}).find_all('a')[0].text #first element of all 'a'
        sector=soup2.find('div',{'class':"companyProfileHeader"}).find_all('a')[1].text #second element " " "
        employees=soup2.find('div',attrs={'class':"companyProfileHeader"}).find('p').text
        info=soup2.find('div',attrs={'class':"companyProfileBody"}).text #All info
        info_short_pre=info.split('.') #spliting each sentences with '.'
        #There exist a company whose length of info sentences are less then 3 or 2
        if len(info_short_pre)>=3:
            info_short=info_short_pre[0]+'.'+info_short_pre[1]+'.'+info_short_pre[2]+'.'
        elif len(info_short_pre)==2:
            info_short=info_short_pre[0]+'.'+info_short_pre[1]+'.'
        elif len(info_short_pre)==1:
            info_short=info_short_pre[0]+'.'

      except Exception: #There exist a blank stock names
        if len(lines[i][0])==0:
            symbol='boş hisse alanı'
            industry = ''
            sector = ''
            employees = ''
            info = ''
            info_short = ''
        else: #There exist a company whose information does not exist in investing.com
          symbol=lines[i][0]
          industry='investing bilgisi yok.'
          sector='investing bilgisi yok.'
          employees='investing bilgisi yok.'
          info='investing bilgisi yok.'
          info_short='investing bilgisi yok.'


      a=i+1
      csv_writer.writerow([symbol,industry,sector,employees,info.strip('\n'),info_short.strip('\n')])

    newcsv_file.close()


