from bs4 import BeautifulSoup
import requests, csv


csvfile = open("data.csv", 'a')



def scrape_website(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2810.1 Safari/537.36'
    
    headers = { 'User-Agent' : user_agent }

    session = requests.session()
    response = session.get(url, headers=headers)
    
    dict_ = {}

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        f_box = soup.find_all(class_="amenities")
        
        for box in f_box:
            if box is not None:
                title = box.find(class_ = "amenitiesTitle")
                value = box.find(class_ = "amenitiesContent")
                if title is not None and value is not None:
                    title_text = title.text.strip()
                    value_text = value.text.strip()

                    if title_text == "Category" or title_text=="Rent Price" or title_text=="Bathroom" or title_text=="Bedroom":

                        if title_text == "Rent Price":
                            value_text = int(value_text.replace("Rs. ", "").replace(',', ''))

                        if title_text == "Bathroom" or title_text == "Bedroom":
                            try:
                                value_text = int(value_text)
                            except:
                                value_text = int(value_text[0])

                        if title_text=="Category":
                            if value_text == "1 BHK":
                                value_text = 1
                            if value_text == "2BHK":
                                value_text = 2
                            if value_text == "3BHK":
                                value_text = 3

                        dict_[title_text] = value_text
                    
                    
    else:

        print("Error ocurred during response parsing  Status code:" + str(response.status_code))
    return dict_


links = open('links.txt', 'rt')




fieldnames = ['Category','Rent Price', 'Bathroom', 'Bedroom']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

for link in links.readlines():

    retr_data = scrape_website(link.strip())
    print(retr_data)
    writer.writerow(retr_data)


