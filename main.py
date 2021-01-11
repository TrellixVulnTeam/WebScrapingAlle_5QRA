from bs4 import BeautifulSoup
from time import  sleep
import requests
import matplotlib.pyplot as mpb





class allegro_engine(object):
    """Search  engine"""
    def __init__(self, search_word):
        self.search_word = search_word
        self.engine()
    def engine(self):
        """engine procedures"""
        site = requests.get('https://allegro.pl/listing?string=' + self.search_word).text
        site_edit = BeautifulSoup(site, 'lxml')
        product_list = []
        price_list = []
        i = 0

        for title in site_edit.find_all('article'):
            h2 = title.find(class_='mgn2_14 m9qz_yp mqu1_16 mp4t_0 m3h2_0 mryx_0 munh_0')
            noedit_price = title.find(class_='_1svub _lf05o') # search product price. none edit



            if h2 != None:
                product_list.append([h2.string]) # download title of products
                product_list[i].append(h2.a['href']) # download links form allegro site





            if noedit_price != None: # create responsive product price
                price_element = noedit_price.contents
                firstpart_price = price_element[0]
                secondpart_price = price_element[1].string
                full_price = firstpart_price + secondpart_price
                product_list[i].append(full_price)
            i += 1
        product_list_len = len(product_list)

        loading = 0
        loading_precent = 100 / product_list_len
        print('Loading: ',int(loading),'%', end='\r')
        for k in range(product_list_len): # Download small piece description
            loading += loading_precent
            print('Loading: ',int(loading),'%', end='\r')
            product_site = requests.get(product_list[k][1]).text
            product_site_edit = BeautifulSoup(product_site, 'lxml')
            description = product_site_edit.find(class_='_2d49e_5pK0q')
            if description.p is None:
                product_list[k].append('Brak')
            elif description.p is not None:
                text_description = description.p.string

                if text_description is not None:
                    piece_of_text = text_description[:50]
                    product_list[k].append(piece_of_text)
                else:
                    product_list[k].append('Brak')


            sleep(0.10)
        z = 1





        for x in product_list: # create list of product information
            price_list.append(x[2])
            print('Produkt numer: ', z, '.')
            print('Tytuł: ', x[0])
            print('Krótki opis: ', x[3])
            print('Cena: ', x[2])
            print('Link do oferty: ',x[1])
            print('-' * 14, '-' * len(x[1]))

            z += 1





        i = 0
        for x in price_list: # change format of price

            x = x[:6]
            x = x.replace(',', '.')
            x = float(x)
            price_list[i] = x
            i += 1

        price_average = sum(price_list) / len(price_list)
        price_average_list = []
        average_arguments = list(range(len(price_list)))
        for x in range(len(price_list)):
            price_average_list.append(price_average)




        # Figure product price
        legend_average = 'Średnia cena produktu(',price_average,')'
        mpb.plot(price_list, color='green')
        mpb.plot(average_arguments, price_average_list, color='orange')
        mpb.title('Średnia cena produktu')
        mpb.xlabel('Numer oferty')
        mpb.ylabel('Cena')
        mpb.legend(['Cena produktu', legend_average])
        mpb.show()






#Main code

print('Napisz czego szukasz?:')
what_found = input()

allegro_engine(what_found)











