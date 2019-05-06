import requests
from bs4 import BeautifulSoup

def GetURL1(isbn, school):
	if school==1:
		return 'http://library.sogang.ac.kr/search/tot/result?st=EXCT&si=6&q='+isbn
	elif school==2:
		return 'http://honors.hongik.ac.kr/search/tot/result?st=EXCT&si=6&q='+isbn

def GetURL2(detail, school):
	if school==1:
		return 'http://library.sogang.ac.kr'+detail
	elif school==2:
		return 'http://honors.hongik.ac.kr'+detail

def isValid(url):
	resp=requests.get(url)
	html=resp.text
	soup=BeautifulSoup(html, 'html.parser')
	detail=soup.find_all("dd", "searchTitle")
	check=str(detail)
	if check == '[]':
		return (False, None)
	else:
		return (True, detail)

def FindInfo(url):	
	resp=requests.get(url)
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
			if i>6: break
			b=a.text.strip()
			b=b.replace("\t", "")
			b=b.replace("\n", "")
			b=b.replace("\r", "")
			l.append(b)
			i+=1
		info.append(l)
	return info

def main():
	school=int(input('1. 서강대학교, 2. 홍익대학교 : '))
	isbn=input('ISBN : ')
	url=GetURL1(isbn, school)
	r=isValid(url)
	if r[0]==False:
		print('해당 도서가 도서관에 있지 않습니다.')
		return;
	else:
		detail=r[1]
		detail=detail[0].find_all("a")[0].get('href')
		url=GetURL2(detail, school)
		info=FindInfo(url)
		for book in info:
			print(book)

if __name__ == '__main__':
	main()
