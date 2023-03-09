# url = 'https://parsinger.ru/html/index1_page_1.html'

import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Item:
    def __init__(self, p_header):
        self.p_header = p_header
        self.article = None
        self.brand = None
        self.model = None
        self.price = None
        self.old_price = None
        self.site = None
        self.image_url = None
        self.item_url = None
        self.category_url = None

    def __str__(self):
        return f"{self.p_header}\n" \
               f"price:           {self.price}\n" \
               f"old price:       {self.old_price}\n" \
               f"article:         {self.article}\n" \
               f"brand and model: {self.brand} {self.model}\n" \
               f"vendor site:     {self.site}\n" \
               f"image url:       {self.image_url}\n" \
               f"item url:        {self.item_url}\n" \
               f"category url:    {self.category_url}\n"


def cut_last(url, last_char):
    counter = len(url) - 1
    char = url[counter]
    while char != last_char:
        counter -= 1
        char = url[counter]
    result_url = url[:counter]
    return result_url


async def get_categories_url(session, categories_list_url):
    categories_url_list = []
    response = await session.get(url=categories_list_url)
    soup = BeautifulSoup(await response.text(), 'lxml')
    nav_menu = soup.find('div', class_='nav_menu').find_all('a')
    base_url = cut_last(categories_list_url, '/')
    for item in nav_menu:
        categories_url_list.append(f'{base_url}/{item["href"]}')
    return categories_url_list


async def get_pagen_url(session, url_with_pagen, pagen_url_list=[]):
    response = await session.get(url=url_with_pagen)
    soup = BeautifulSoup(await response.text(), 'lxml')
    pagen = soup.find('div', class_='pagen').find_all('a')
    base_url = cut_last(url_with_pagen, '/')
    for item in pagen:
        pagen_url_list.append(f'{base_url}/{item["href"]}')


async def get_item_url(session, url_with_items, item_url_list=[]):
    response = await session.get(url=url_with_items)
    soup = BeautifulSoup(await response.text(), 'lxml')
    item_list = soup.find('div', class_='item_card').find_all('div', class_='sale_button')
    base_url = cut_last(url_with_items, '/')
    for item in item_list:
        item_soup = BeautifulSoup(item.__str__(), 'lxml')
        item_href = item_soup.find('a')['href']
        item_url_list.append(f'{base_url}/{item_href}')


async def get_item_data(session, item_url, item_data_list=[]):
    response = await session.get(url=item_url)
    soup = BeautifulSoup(await response.text(), 'lxml')
    p_header = soup.find('p', id='p_header').text
    item = Item(p_header)
    item.article = soup.find('p', class_='article').text.split(':')[1].strip()
    item.brand = soup.find('li', id='brand').text.split(':')[1].strip()
    item.model = soup.find('li', id='model').text.split(':')[1].strip()
    item.price = soup.find('span', id='price').text
    item.old_price = soup.find('span', id='old_price').text
    if soup.find('li', id='site') is not None:
        item.site = soup.find('li', id='site').text.split(':')[1].strip()
    item.image_url = soup.find('div', class_='image_box').find('img')['src']
    item.item_url = item_url
    item.category_url = cut_last(soup.find('a', id='a_back')['href'], '#')

    item_data_list.append(item)


def data_to_json(item_list, path: str):
    with open(path, 'w', encoding='utf-8') as file:
        pass

    data_list = []
    for item in item_list:
        item_json = {
            'p_header': item.p_header,
            'article': item.article,
            'brand': item.brand,
            'model': item.model,
            'price': item.price,
            'old_price': item.old_price,
            'site': item.site,
            'image_url': item.image_url,
            'item_url': item.item_url,
            'category_url': item.category_url,
        }
        data_list.append(item_json)

    with open(path, 'a', encoding='utf-8') as file:
        json.dump(data_list, file, indent=4, ensure_ascii=False)


async def main(main_url, debug=False):
    ua = UserAgent()
    fake_ua = {'user-agent': ua.random}
    if debug:
        print('----------------------01----------------------')
        print('fake_ua')
        print(fake_ua)
    else:
        print('Process: .', end='')

    connector = None
    async with aiohttp.ClientSession(connector=connector, headers=fake_ua) as session:

        categories_url_list = await get_categories_url(session, main_url)
        if debug:
            print('----------------------02----------------------')
            print('categories_url_list')
            print(categories_url_list)
        else:
            print('.', end='')

        pagen_url_list = []
        tasks = []
        for cat_url in categories_url_list:
            task = asyncio.create_task(get_pagen_url(session, cat_url, pagen_url_list))
            tasks.append(task)
        await asyncio.gather(*tasks)
        if debug:
            print('----------------------03----------------------')
            print('pagen_url_list')
            print(pagen_url_list)
        else:
            print('.', end='')

        item_url_list = []
        tasks = []
        for page_url in pagen_url_list:
            task = asyncio.create_task(get_item_url(session, page_url, item_url_list))
            tasks.append(task)
        await asyncio.gather(*tasks)
        if debug:
            print('----------------------04----------------------')
            print('item_url_list')
            print(item_url_list)
        else:
            print('.', end='')

        item_data_list = []
        tasks = []
        for item_url in item_url_list:
            task = asyncio.create_task(get_item_data(session, item_url, item_data_list))
            tasks.append(task)
        await asyncio.gather(*tasks)
        if debug:
            print('----------------------05----------------------')
            print('item_data_list')
            print(item_data_list)
        else:
            print('.', end='')

        data_to_json(item_data_list, 'data.json')

        if debug:
            print('----------------------06----------------------')
            print('data is saved')
        else:
            print('. Done')


if __name__ == '__main__':
    home_url = 'https://parsinger.ru/html/index1_page_1.html'
    asyncio.run(main(home_url, debug=False))
