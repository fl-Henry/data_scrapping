# Async data scrapping

The data extracting URL:

    https://parsinger.ru/html/index1_page_1.html


The data includes every product from the site. 
The products are divided into several categories, and each 
category has several product pages.

The extracted data is saved to a file (data.json).

Data output:

    {
        "p_header": "GT 2 NIGHT BLACK DIANA-B19S HUAWEI",
        "article": "80605940",
        "brand": "Huawei",
        "model": "Watch GT 2 Diana-B19S",
        "price": "15850 руб",
        "old_price": "16010 руб",
        "site": "www.huawei.ru",
        "image_url": "https://parsinger.ru/img/1/1/1_19.jpg",
        "item_url": "https://parsinger.ru/html/watch/1/1_19.html",
        "category_url": "https://parsinger.ru/html/index1_page_3.html"
    }