from bs4 import BeautifulSoup

golf_url = "http://mitt.golf.is/pages/rastimar/rastimayfirlit/?hvenaer=0&hvar=50&search=1&club=100&day=2018-06-27"
soup = BeautifulSoup(golf_url)

rows = soup.find_all('table') #Would return all the <asn></asn> tags found!






with open('data/golffile2.txt', 'w') as f3:
   f3.write(str(rows))
f3.close()