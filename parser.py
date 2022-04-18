import requests
from bs4 import BeautifulSoup
import database


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36'}
urls = []
i = 1
rooms = [1, 2, 3]
for room in rooms:
    while True:
        try:
            respons = requests.get(f'https://domovita.by/minsk/{room}-room-flats/rent?page={i}&order=price',
                                   headers=headers
                                   )
            print(respons.status_code)
            if respons.status_code == 404:
                break
            soup = BeautifulSoup(respons.text, 'lxml')
            a = soup.find_all('a', class_="mb-5 title title--listing")
            i += 1
        except:
            break
        for x in a:
            urls.append((x.get("href"), room))
            print(x.get("href"))
    i = 1

database.update_false()
database.change_false()
database.conn.commit()
for i in range(0, int(len(urls))-1):
    try:
        flat = requests.get(urls[i][0])
        soup = BeautifulSoup(flat.text, 'lxml')
        discription = soup.find('div', class_="object-head__name").text
        price = soup.find('div', class_="calculator__price-main").text
        phone = soup.find('a', class_='owner-info__phone').text
        id_flat = soup.find('div', class_="publication-info__wrapper").text[12:19]
        rum = urls[i][1]

        if id_flat in database.select_id():
            price_id = database.select_price(id_flat)
            if price == price_id[0]:
                database.update_flag(id_flat, "update", True)
            else:
                database.update_flag(id_flat, "change", True)
                database.update_price(id_flat, price)
                database.update_flag(id_flat, "update", True)
        else:
            database.set_data(id_flat, rum, discription, price, phone, urls[i][0])
            database.update_flag(id_flat, "update", True)
    except AttributeError:
        print("что-то идет не так((")
    print(rum)
    print(discription)
    print(price)
    print(phone)
    print(urls[i][0])
    print("*"*40)
print("Процес завершен")
database.conn.commit()
database.delete_update_false()
database.conn.commit()
