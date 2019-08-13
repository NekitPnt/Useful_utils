import requests
from bs4 import BeautifulSoup
from pprint import pprint
import jsonReadWrite as jRW

#with open('test.html', 'w') as output_file:
#    output_file.write(r.text)
#print('ok')

# from lxml import html
'''
# Beautiful Soup
soup = BeautifulSoup(r.text, "html.parser")
# <div class="ratings__item__text">
best = str(soup.find_all('div', {'class': 'ratings__item__text'}))
film_list = str(soup.find('blockquote'))#, {'class': 'wrap-excuse__middle'})
film_list = film_list.replace('<blockquote>', '')
film_list = film_list.replace('</blockquote>', '')
#print(film_list, type(film_list))
best = best.replace(', <div class="ratings__item__text">', '')
best = best.replace('</p>', '')
best = best.replace('</div>', '')
best = best.replace('<p>', '')
print(best)
with open('test.txt', 'w') as output_file:
    output_file.write(best)
'''

res = ''

def write_excuse(num):
    print(num)
    url = 'http://copout.me/get-excuse/%d' % num
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    ex = str(soup.find('blockquote'))
    if ex != 'None':
        print(ex)
        ex = ex.replace('<blockquote>', '')
        ex = ex.replace('</blockquote>', '')
        global res 
        res += ex + '\n\n'
        with open('base.txt', 'w', encoding="utf8") as output_file:
            output_file.write(res)

#for i in range(2970, 10000):
 #   write_excuse(i)
# 2970
#with open('base.txt', 'w', encoding="utf8") as output_file:
#    output_file.write(res)
# порядок
# div class='book'
# p
# div class='row-fluid'
result = []
    
url = 'https://tproger.ru/digest/movies-for-hackers/'
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
#pprint(soup)

films = soup.find('div', {'class': 'entry-content'})
names = films.find_all('h3')
years = films.find_all('p', {'class': 'book-meta'})
links = films.find_all('a', {'class': 'btn bluth tproger btn-'})
descr = films.find_all('p')
#for i in range(len(names)):
print(len(names), len(years), len(descr), len(links))
#pprint(films)
res = {'descr': []}
for i in films:
    #print(i)
    #if i.get('p'):
    if i.div:
        #print(i.get('class'))
        if i.get('class') == ['book']:
            res['name'] = i.h3.text
            res['year'] = i.p.text
            if i.img:
                res['pic'] = str(i.img.get('data-srcset')).split(' ')[-2]
            links = i.find_all('a', {'class': 'btn bluth tproger btn-'})
            res['links'] = []
            for link in links:
                res['links'].append(link.text + ' - ' + link.get('href'))
        elif 'class="row-fluid"' in str(i):
            result.append(res)
            res = {'descr': []}
    else:
        res['descr'].append(i.text)


jRW.write_json(result, 'films.json')
