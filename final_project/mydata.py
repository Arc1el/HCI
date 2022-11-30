# -*- coding: euc-kr -*-

from bs4 import BeautifulSoup
import requests
import pandas as pd
import io
import time
import re

def otp_generator(data):
  gen_otp_url = "http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd"
  gen_otp_data = data
  otp = requests.post(gen_otp_url, params = gen_otp_data)
  otp = BeautifulSoup(otp.content, "html.parser").text
  return otp

def stock_df_generator(otp):
  down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
  otp_key = {"code" : otp}
  referer = {"referer" : "http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd"}
  dat = requests.post(down_url, data= otp_key, headers = referer).content.decode('euc-kr')
  df = io.StringIO(dat)
  df = pd.read_csv(df, sep = ',', engine='python', encoding="euc-kr")
  return df[1:5]

def kospi(date):
  kospi_req_data = {"idxIndMidclssCd" : "02",
                "trdDd" : date,
                "share" : '2',
                "money" : '3',
                "csvxls_isNo" : 'false',
                "name" : 'fileDown',
                "url" : 'dbms/MDC/STAT/standard/MDCSTAT00101'}

  kospi_otp = otp_generator(kospi_req_data)
  kospi_df = stock_df_generator(kospi_otp)

  kospi = []
  for i in range(4):
    temp = []
    temp.append(kospi_df.loc[i+1]["지수명"])
    temp.append(kospi_df.loc[i+1]["종가"])
    temp.append(kospi_df.loc[i+1]["대비"])
    temp.append(kospi_df.loc[i+1]["등락률"])
    temp.append(kospi_df.loc[i+1]["시가"])
    temp.append(kospi_df.loc[i+1]["고가"])
    temp.append(kospi_df.loc[i+1]["저가"])
    temp.append(kospi_df.loc[i+1]["거래량"])
    temp.append(kospi_df.loc[i+1]["거래대금"])
    temp.append(kospi_df.loc[i+1]["상장시가총액"])

    kospi.append(temp)

  return kospi

def kosdaq(date):
  kosdaq_req_data = {"idxIndMidclssCd" : "03",
                "trdDd" : date,
                "share" : '2',
                "money" : '3',
                "csvxls_isNo" : 'false',
                "name" : 'fileDown',
                "url" : 'dbms/MDC/STAT/standard/MDCSTAT00101'}

  kosdaq_otp = otp_generator(kosdaq_req_data)
  kosdaq_df = stock_df_generator(kosdaq_otp)

  kosdaq = []
  for i in range(4):
    temp = []
    temp.append(kosdaq_df.loc[i+1]["지수명"])
    temp.append(kosdaq_df.loc[i+1]["종가"])
    temp.append(kosdaq_df.loc[i+1]["대비"])
    temp.append(kosdaq_df.loc[i+1]["등락률"])
    temp.append(kosdaq_df.loc[i+1]["시가"])
    temp.append(kosdaq_df.loc[i+1]["고가"])
    temp.append(kosdaq_df.loc[i+1]["저가"])
    temp.append(kosdaq_df.loc[i+1]["거래량"])
    temp.append(kosdaq_df.loc[i+1]["거래대금"])
    temp.append(kosdaq_df.loc[i+1]["상장시가총액"])

    kosdaq.append(temp)

  return kosdaq

def get_soup(title):
  url = "https://www.asiae.co.kr/common/comp_kind/comp_kind2014.htm?sm=2&mkg=1"
  response = requests.get(url)
  if response.status_code == 200:
      soup = BeautifulSoup(response.content.decode("euc-kr", "replace"), 'html.parser')
      soup = str(soup.find_all("script")[4])
      soup = soup[103:]
      soup = re.sub("\t", "", soup)
      soup = re.sub("\n", "", soup)
      soup = re.sub("http://cwstatic.asiae.co.kr/asiae_2009/common/", "", soup)
      soup = re.sub('<img src="ico_down.gif" alt="" align="absmiddle" />', "", soup)
      soup = re.sub('<img src="ico_up.gif" alt="" align="absmiddle" />', "", soup)
      soup = re.sub('<img src="ico_hold.gif" alt="" align="absmiddle" />', "", soup)
      soup = re.sub(", 'downf01'", "", soup)
      soup = re.sub(", 'ico_down.gif'", "", soup)
      soup = re.sub(", 'upf01'", "", soup)
      soup = re.sub(", 'ico_up.gif'", "", soup)
      soup = re.sub(", 'holdf01'", "", soup)
      soup = re.sub(", 'ico_hold.gif'", "", soup)
      soup = re.sub('strArrayList', "", soup)
      soup = re.sub("new Array", "", soup)
      soup = re.sub('', "", soup)
      soup = soup.split(";")
      soup = pd.DataFrame(soup) 

      return soup
  else : 
      print(response.status_code)

def search(title):
  soup = get_soup(title)
  soup.columns = ["data"]

  temp_df = soup[soup["data"].str.contains(title)]
  temp_str = temp_df.to_string(index=False).split("\n")

  search = []

  try:
    for i in range(1, len(temp_str)):
      token = temp_str[i].split("'")
      title = token[1]
      price = token[3]
      fullday = token[5][1:]
      fluctuation = token[7]
      code = token[9]

      temp_arr = []
      
      temp_arr.append(title)
      temp_arr.append(price)
      temp_arr.append(fullday)
      temp_arr.append(fluctuation)
      temp_arr.append(code)

      search.append(temp_arr)
    return search
  except:
    return [["검색결과없음","00","00","00","00"]]

def analysis_stock(code):
  url = "https://cc.naver.com/cc?m=1&nsc=finance.stockend&u=https://finance.naver.com/item/coinfo.naver?code=" + code
  response = requests.get(url)
  response.raise_for_status()
  soup = BeautifulSoup(response.text, "lxml")

  #eps = soup.find('em', attrs={"id" : "_eps"})
  ems = soup.find("div", attrs={"id" : "tab_con1"})
  ems = ems.find_all("em")

  #시가총액, 시총순위, 상장주식수, 액면가, 매매단위
  market_cap = ems[0].get_text().strip()
  cap_rank = ems[1].get_text()
  num_of_stock = ems[2].get_text()
  par_val = ems[3].get_text()
  trading_unit = ems[4].get_text()

  #외국인한도주식수(A), 외국인보유주식수(B), 외국인소진율(B/A)
  limit_forign = ems[5].get_text()
  held_forign = ems[6].get_text()
  rate_forign = ems[7].get_text()

  #52주최고, 52주최저
  week_52_high = ems[10].get_text()
  week_52_low = ems[11].get_text()

  #PER, EPS, BPS
  per = ems[12].get_text()
  eps = ems[13].get_text()
  bps = ems[17].get_text()

  #동일업종PER, 동일업종 등락률
  same_per = ems[19].get_text()
  same_rate = ems[20].get_text().strip()


  str1 = "시가총액 : " + market_cap + "억원 ,시총순위 : " + cap_rank + " ,상장주식수 : " + num_of_stock + " ,액면가 : " + par_val + " ,매매단위 : " + trading_unit
  str2 = "외국인한도주식수(A) : " + limit_forign + " ,외국인보유주식수(B) : " + held_forign + " ,외국인소진율(B/A) : " + rate_forign
  str3 = "52주최고 : " + week_52_high + " ,52주최저 : " + week_52_low
  str4 = "PER : " + per + " ,EPS : " + eps + " ,BPS : " + bps + " ,동일업종PER : " + same_per + " ,동일업종 등락률 : " + same_rate
  
  return (str1, str2, str3, str4)
