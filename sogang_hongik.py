import requests
from bs4 import BeautifulSoup
from parse import *

# 1차 크롤링 - isbn값을 통해, controlno값 : CAT뭐시기저시기를 받아온다.
def GetURL1(isbn, school):
	if school==1:
        return 'http://library.sogang.ac.kr/search/tot/result?st=EXCT&si=6&q='+isbn
	elif school==2:
        return 'http://honors.hongik.ac.kr/search/tot/result?st=EXCT&si=6&q='+isbn
    elif school==4:
            return 'https://library.yonsei.ac.kr/main/searchBrief?q='+isbn
#2차 크롤링 - 1차 크롤링을 통해 받아온 값을 이용해서 대출 가능 여부 정보를 가져온다.
def GetURL2(bookid, school):
	if school==1:
		return 'http://library.sogang.ac.kr/search/detail/'+bookid
	elif school==2:
		return 'http://honors.hongik.ac.kr/search/detail/'+bookid


def isValid(url):
	resp=requests.get(url)
	html=resp.text
	soup=BeautifulSoup(html, 'html.parser')
	bookid=soup.find_all("span", "bookimg")
	check=str(bookid)
	if check == '[]':
		return (False, None)
	else:
		return (True, bookid)

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
    school=int(input('1. 서강대학교, 2. 홍익대학교, 4.연세대학교 : '))
	isbn=input('ISBN : ')
	url=GetURL1(isbn, school)
    if school <= 3:
        r=isValid(url)
        if r[0]==False:
            print('해당 도서가 도서관에 있지 않습니다.')
            return;
        else:
            bookid=r[1]
            bookid=str(bookid[0].get('id'))
            bookid=parse("bookImg_{}", bookid)[0]
            url=GetURL2(bookid, school)
            info=FindInfo(url)
            for book in info:
                print(book)
    else:
        resp = request.get(url)
        html = resp.text
        soup = BeautifulSoup(html, 'lxml')

        get_bookSection = soup.find('div',{'class' : 'bookSection'})
        print(get_bookSection)
if __name__ == '__main__':
	main()

