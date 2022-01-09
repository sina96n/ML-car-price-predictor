from bs4 import BeautifulSoup
import requests


MAX_PAGE  = 250
# defining base_url to create a list of all page urls
BASE_URL  = "https://www.truecar.com/used-cars-for-sale/listings/"
# defining host_name for creating urls for each car ad
HOST_NAME = "https://www.truecar.com" 


pages = list()
urls = list()
failed_pages = list()


def url_scraper():
    with open("pages.txt", "w") as f:
        for i in range(1,MAX_PAGE+1):
            page = BASE_URL + "?page=" + str(i)
            f.write(page+"\n")
            pages.append(page)

    for page in pages:
        try:
            response = requests.get(page)
            response.raise_for_status()
        except:
            failed_pages.append(page)
            continue

        src = response.text
        soup = BeautifulSoup(src, "html.parser")

        ads = soup.find_all("a", attrs={
            "data-test" : "vehicleCardLink"
        })
         
        url_list = [HOST_NAME+link["href"] for link in ads]
        with open("urls.txt", "a+") as f:
            for url in url_list:
                urls.append(url)
                f.write(url+"\n")