import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def GetURL1(isbn, school):
	if school==1:
		return 'http://library.sogang.ac.kr/search/tot/result?st=EXCT&si=6&q='+isbn
	elif school==2:
		return 'http://honors.hongik.ac.kr/search/tot/result?st=EXCT&si=6&q='+isbn
	elif school==3:
		return 'http://lib.ewha.ac.kr/search/tot/result?st=KWRD&si=TOTAL&service_type=brief&q='+isbn
	elif school==4:
		return 'https://library.yonsei.ac.kr/search/tot/result?st=EXCT&si=6&q='+isbn+'&folder_id=null&lmt0=YNLIB;GSISL;MUSEL;OTHER;UGSTL;YSLIB;ARCHL;BUSIL;KORCL;IOKSL;LAWSL;MULTL;MATHL;MUSIC&lmtsn=000000000006&lmtst=OR#'

 

def GetURL2(detail, school):
	if school==1:
		return 'http://library.sogang.ac.kr'+detail
	elif school==2:
		return 'http://honors.hongik.ac.kr'+detail
	elif school==3:
		return 'http://lib.ewha.ac.kr'+detail
	elif school==4:
		return 'http://library.yonsei.ac.kr'+detail

def isValid(url, school):
	resp=requests.get(url, verify=False)
	html=resp.text
	soup=BeautifulSoup(html, 'html.parser')

	if school == 1 or school==2:
		detail=soup.find_all("dd", "searchTitle")
	elif school == 3:
		detail=soup.find_all("dd", "book")
	elif school == 4:
		detail=soup.find_all("dd", "title")

	check=str(detail)
	if check == '[]':
		return (False, None)
	else:
		return (True, detail)

def FindInfo(url, school):	
	resp=requests.get(url, verify=False)
	html=resp.text
	soup=BeautifulSoup(html, 'html.parser')
	tbody=soup.find_all("tbody")
	tr=tbody[1].find_all("tr")
	
	info=[]
	for row in tr:
		td=row.find_all('td')
		l=[]
		i=0
		for a in td:
			if school==3:
				if i==8: break
				if i==5 or i==6: continue
			else:
				if i==6: break
			b=a.text.strip()
			b=b.replace("\t", "")
			b=b.replace("\n", "")
			b=b.replace("\r", "")
			l.append(b)
			i+=1
		info.append(l)
	return info

def main():
	school=int(input('1. 서강대학교, 2. 홍익대학교, 3. 이화여자대학교, 4. 연세대학교 : '))
	isbn=input('ISBN : ')
	url=GetURL1(isbn, school)
	r=isValid(url, school)

	if r[0]==False:
		print('해당 도서가 도서관에 있지 않습니다.')
		return;
	else:
		detail=r[1]
		detail=detail[0].find_all("a")[0].get('href')
		url=GetURL2(detail, school)
		info=FindInfo(url, school)
		for book in info:
			print(book)

if __name__ == '__main__':
	main()
