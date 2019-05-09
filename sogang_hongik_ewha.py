import requests, re, json
from bs4 import BeautifulSoup

def GetURL1(isbn, school):
	if school==1:
		return 'http://library.sogang.ac.kr/search/tot/result?st=EXCT&si=6&q='+isbn
	elif school==2:
		return 'http://honors.hongik.ac.kr/search/tot/result?st=EXCT&si=6&q='+isbn
	elif school==3:
		return 'http://lib.ewha.ac.kr/search/tot/result?st=KWRD&si=TOTAL&service_type=brief&q='+isbn
	elif school==4:
		return "https://library.yonsei.ac.kr/main/searchBrief?q="+isbn


def GetURL2(detail, school):
	if school==1:
		return 'http://library.sogang.ac.kr'+detail
	elif school==2:
		return 'http://honors.hongik.ac.kr'+detail
	elif school==3:
		return 'http://lib.ewha.ac.kr'+detail


def isValid(url, school):
	if school == 4:
		resp=requests.get(url, verify=False)
	else:
		resp=requests.get(url)
	html=resp.text
	soup=BeautifulSoup(html, 'lxml')
	if school == 1 or school==2:
		detail=soup.find_all("dd", "searchTitle")
	elif school ==3:
		detail=soup.find_all("dd", "book")
	elif school == 4:
		detail = soup.find_all("dt","listTitle")
	check=str(detail)
	if check == '[]':
		return (False, None)
	else:
		return (True, detail)

def FindInfo(url, school):
	resp=requests.get(url)
	html=resp.text
	soup=BeautifulSoup(html, 'lxml')
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
	school=int(input('1. 서강대학교, 2. 홍익대학교, 3. 이화여자대학교 , 4.연세대학교: '))
	isbn=input('ISBN : ')
	url=GetURL1(isbn, school)
	bookExistenceInfo=isValid(url, school)
	if bookExistenceInfo[0]==False:
		print('해당 도서가 도서관에 있지 않습니다.')
		return;
	else:
		print('해당 도서가 존재합니다.')
		if school == 4:
			# get으로 bs4에서 속성값을 뽑아내면, 뽑아낸 값의 타입은 자동으로 스트링이 되는 모양이다.
			detail = bookExistenceInfo[1][0].find('a').get('href')
			#print(type(detail))
			ajaxprm_link = detail
			ajaxprm_seqno = ajaxprm_link.split("/")[3]
			ajaxprm_controlno = ajaxprm_seqno[3:]
			ajaxprm_kind = 'Catalog'
			ajaxprm_url = "https://library.yonsei.ac.kr/main/holdingAjax"
			print(ajaxprm_controlno)
#CAT000001770009 : 9788970508504
			#ajaxdata = "controlno="+ajaxprm_controlno+"&holdingType="+ajaxprm_kind
			ajaxdata = {'conltrolno':ajaxprm_controlno, 'holdingType':ajaxprm_kind}
			#cookie = {'id' :  }
			print(ajaxprm_controlno + ":" + ajaxprm_kind)
			req_header = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
			res = requests.post(url = ajaxprm_url, headers = req_header, data = ajaxdata, verify=False)
			print(res)
		else:
			detail=bookExistenceInfor[1]
			detail=detail[0].find_all("a")[0].get('href')
			url=GetURL2(detail, school)
			info=FindInfo(url, school)
			for book in info:
				print(book)

if __name__ == '__main__':
	main()
