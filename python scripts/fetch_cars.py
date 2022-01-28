from bs4 import BeautifulSoup
import requests
import re
import csv


car_list = ()
failed_urls = list()

def scraper(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except:
        failed_urls.append(url)
        pass

        try:
            src = response.text
            soup = BeautifulSoup(src, "html.parser")

            detail = soup.find("div", attrs={"data-test" : "vdpPreProspectTopDetails"})

            price = detail.find("div", attrs={"data-test" : "vdpPreProspectPrice"})
            price = int(re.sub("[^\d]", "", price.text))

            mileage = detail.find("p", attrs={"class" : "margin-top-1"})
            mileage = int(re.sub("[^\d]", "", mileage.text))

            titles = soup.find("h1", attrs={
                "class" : "heading-base d-flex flex-column margin-right-2",
                "data-qa" : "Heading"
            })
            name = list(titles.children)[1].text
            name = name.replace("\xa0"," ")

            features = list(soup.find("div", attrs={"data-test" : "vdpOverviewSection"}).div)
            style = features[0].div.div.p.text
            exterior_color = features[1].div.div.p.text
            interior_color = features[2].div.div.p.text
            mpg = features[3].div.div.p.text
            mpg_city, mpg_highway = re.match("(\d{1,2}) cty / (\d{1,2}) hwy", mpg).groups()
            engine = features[4].div.div.p.text
            drive_type = features[5].div.div.p.text
            fuel_type = features[6].div.div.p.text
            transmission = features[7].div.div.p.text

        except:
            failed_urls.append(url)
            pass
            
 
        car = [name,style,exterior_color,interior_color,engine,
                    drive_type,fuel_type,transmission,mileage,mpg_city,
                    mpg_highway,price]

        car_list.append(car)   


with open("cars.csv", "w") as cars:
    csvwriter = csv.writer(cars)
    csvwriter.writerows(car_list)



# By Sina Kazemi
# Github : https://github.com/sina96n/