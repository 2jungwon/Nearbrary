import sys
import requests
import json
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def GetURL1(isbn, school):
	if school is 1:
		return 'https://library.sogang.ac.kr/search/tot/result?st=EXCT&si=6&q='+isbn
	elif school is 2:
		return 'https://library.yonsei.ac.kr/search/tot/result?st=EXCT&si=6&q='+isbn+'&folder_id=null&lmt0=YNLIB;GSISL;MUSEL;OTHER;UGSTL;YSLIB;ARCHL;BUSIL;KORCL;IOKSL;LAWSL;MULTL;MATHL;MUSIC&lmtsn=000000000006&lmtst=OR#'
	elif school is 3:
		return 'https://lib.ewha.ac.kr/search/tot/result?st=KWRD&si=TOTAL&service_type=brief&q='+isbn
	elif school is 4:
		return 'https://honors.hongik.ac.kr/search/tot/result?st=EXCT&si=6&q='+isbn

def GetDetail(url, school):
	resp=requests.get(url, verify=False)
	html=resp.text
	soup=BeautifulSoup(html, 'html.parser')

	if school is 1 or school is 4:
		detail=soup.find("dd", "searchTitle")
	elif school is 2 or school is 3:
		detail=soup.find("dd", "book")

	if detail is None:
		return detail
	
	detail=detail.find("a").get('href')
	return detail

def GetURL2(detail, school):
	if school is 1:
		return 'https://library.sogang.ac.kr'+detail
	elif school is 2:
		return 'https://library.yonsei.ac.kr'+detail
	elif school is 3:
		return 'https://lib.ewha.ac.kr'+detail
	elif school is 4:
		return 'https://honors.hongik.ac.kr'+detail

def GetLibInfo(url, school):
	resp=requests.get(url, verify=False)
	html=resp.text
	soup=BeautifulSoup(html, 'html.parser')
	tr=soup.find_all("tbody")[1].find_all("tr")

	books=[]
	for row in tr:
		td=row.find_all("td")
		book=GetOneBook(td, school)
		if book is not None: books.append(book)
	return books

def GetOneBook(td, school):
	temp=[]
	for i in range(8):
		if school is 3 and (i is 5 or i is 6): continue
		elif i is 6: break
		item=td[i].text.strip()
		item=item.replace("\t", "")
		item=item.replace("\n", "")
		item=item.replace("\r", "")
		temp.append(item)
	book=DataTrim(temp, school)
	return book

def DataTrim(temp, school):
	if school is 1:
		book={'no': temp[0], 'location': temp[1], 'callno': temp[2], 'id': temp[3], 'status': temp[4], 'returndate': temp[5]}

	elif school is 2:
		if '국' in temp[3][1]: return None
		book={'no': temp[0], 'id': temp[1], 'callno': temp[2], 'location': temp[3], 'status': temp[4], 'returndate': temp[5]}

	elif school is 3:
		book={'no': temp[0], 'location': temp[1], 'callno': temp[2], 'status': temp[3], 'returndate': temp[4], 'id': temp[5]}

	elif school is 4:
		if '문' in temp[3][0]: return None
		book={'no': temp[0], 'id': temp[1], 'callno': temp[2], 'location': temp[3], 'status': temp[4], 'returndate': temp[5]}

	return book



def main():
	isbn=sys.argv[1]
	libinfo={}

	for i in range(1,5):
		url=GetURL1(isbn, i)
		detail=GetDetail(url, i)
		if detail is None: continue
		url=GetURL2(detail, i)
		books=GetLibInfo(url, i)

		if i is 1: libinfo['sogang']=books
		elif i is 2: libinfo['yonsei']=books
		elif i is 3: libinfo['ewha']=books
		elif i is 4: libinfo['hongik']=books

	with open('libinfo.json', 'w', encoding="utf-8") as make_file:
		json.dump(libinfo, make_file, ensure_ascii=False, indent="\t")

if __name__ == '__main__':
	main()
