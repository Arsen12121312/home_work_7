import httpx
import parsel
from parsel import Selector
from db import save_to_db


def fetch_data(url):
    with httpx.Client() as client:
        response = client.get(url)
        response.raise_for_status()
        return response.text


def parse_data(html):
    root = Selector(html)
    items = root.css(".table tbody tr")

    results = []
    for item in items:
        name = item.css(".title::text").get()
        phone = item.css(".phone::text").get()
        city = item.css(".city::text").get()
        date = item.css(".date::text").get()
        address = item.css(".address::text").get()
        cost = item.css(".cost::text").get()
        description = item.css(".description::text").get()

        result = {
            "name": name,
            "phone": phone,
            "city": city,
            "date": date,
            "address": address,
            "cost": cost,
            "description": description,
        }
        results.append(result)

    return results


def main():
    url = "https://www.house.kg/snyat"
    html = fetch_data(url)
    data = parse_data(html)
    save_to_db(data)


if __name__ == "__main__":
    main()


# db.py

import sqlite3


def save_to_db(data):
    conn = sqlite3.connect('houses.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''CREATE TABLE houses
                     (name text, phone text, city text, date text, address text, cost text, description text)''')
    except sqlite3.OperationalError:
        pass

    for item in data:
        cursor.execute("INSERT INTO houses VALUES (?,?,?,?,?,?,?)",
                       (item['name'], item['phone'], item['city'], item['date'], item['address'], item['cost'], item['description']))

    conn.commit()
    conn.close()