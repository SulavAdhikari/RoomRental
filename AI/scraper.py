from bs4 import BeautifulSoup
import requests

url = "https://kothabhada.com/all-properties?title=&category_id%5B%5D=2&category_id%5B%5D=6&category_id%5B%5D=7&categoryType=B&min=&max=&page="

def scrape_website(url):
     
    response = requests.get(url)

    links = []
    if response.status_code == 200:
         
        soup = BeautifulSoup(response.content, 'html.parser')

        columns = soup.find_all(class_="col-md-3")
        for column in columns:
            cont = column.find(class_='singleBoxContent')
            if cont is not None:
                link = column.find('a')
                if link is not None:
                    links.append(link)
        


        for link in links:
            print(link.get('href'))
            file = open('links.txt', 'a')
            file.write(link.get('href') + "\n")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

for i in range(1, 18):

    scrape_website(url + str(i))

