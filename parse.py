import csv
from browser import Browser
from utils import BeautifulSoup
import os
import time


def read_file():
    with open('input.csv') as csvfile:
        return list(csv.DictReader(csvfile, delimiter=';'))
        # for row in readCSV:
        #     print(row)
        #     print(row[0])
        #     print(row[0], row[1], row[2],)


def save_to_file(file_path, data):
    with open(file_path, 'a') as f:
        w = csv.DictWriter(f, fieldnames=data.keys(), delimiter=';')
        # add headers if file is empty
        if os.stat(file_path).st_size == 0:
            w.writeheader()
        w.writerow(data)


def main():
    for row in read_file():
        browser = Browser(debug=False, use_debug_proxy=False)
        create_post_url = "https://www.123saunas.com/customer/account/createpost/"
        # first request call is necessary to get cookies enabled
        browser.get(create_post_url)
        res = browser.get(create_post_url)
        html_text = res.text
        soap_page = BeautifulSoup(html_text)

        form_key = soap_page.find('input', {'name': 'form_key'}).get('value')
        res2 = browser.post('https://www.123saunas.com/customer/account/createpost/', {
            "success_url": "",
            "error_url": "",
            "form_key": form_key,
            "firstname": row['FirstName'],
            "middlename": "",
            "lastname": row['Lastname'],
            "email": row['Email'],
            "password": row['Password'],
            "confirmation": row['Password_confirm'],
            "persistent_remember_me": "on",
        }, headers={'Content-Type': 'application/x-www-form-urlencoded'})

        if res2.url == "https://www.123saunas.com/customer/account/index/":
            save_to_file("valid_reg.txt", row)
        else:
            save_to_file("checkagain_reg.txt", row)

        time.sleep(10)


main()
