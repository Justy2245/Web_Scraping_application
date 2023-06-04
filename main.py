from bs4 import BeautifulSoup
import requests

def display(list):
    for x in list:
        print("Title: ", end='')
        print(x[0])
        print("Price: ", end='')
        print(x[1][0])
        print("Stock: ", end='')
        print(x[1][1])
        print('')

bookDict = {}
count = 0
for n in range(1,50):
    #print(f"Page {n}")
    #website only has 50 pages so iterate through each one
    pageurl = f"https://books.toscrape.com/catalogue/page-{n}.html"
    path = requests.get(pageurl).text

    soup = BeautifulSoup(path, 'lxml')

    div = soup.find_all('div', class_='image_container')
    for x in div:
        parser = x.find('a')['href']
        #go to each book page individually to get data
        url = f"https://books.toscrape.com/catalogue/{parser}"
        path1 = requests.get(url).text
        soup1 = BeautifulSoup(path1, 'lxml')
        title = soup1.find('h1').text
        #print(title)
        price = soup1.find('p', class_='price_color').text
        #print(price[1:])
        bookDict.setdefault(f'{title}', []).append(price[1:])
        stockCheck = "In stock"
        temp = soup1.find_all('td')
        for n in temp:
            if stockCheck in n.string:
                for m in n.string.split():
                    #when the text is split there is a ( before the number
                    if m.replace('(', '').isdigit():
                        #print(m.replace('(', ''))
                        bookDict.setdefault(f'{title}', []).append(m.replace('(', ''))
        #print("")
        count += 1
i = 0
while i == 0:
    print("Number of books stored: ", end='')
    print(count)
    print("1. Sort by title and display")
    print("2. Sort by price and display")
    print("3. Exit")
    print("Enter choice: ", end='')
    choice = input()
    print(choice)
    if choice == '1':
        temp = sorted(bookDict.items())
        display(temp)
    elif choice == '2':
        temp = sorted(bookDict.items(), key=lambda p: p[1])
        display(temp)
    elif choice == '3':
        i = 1
    else:
        print("Invalid Choice")


