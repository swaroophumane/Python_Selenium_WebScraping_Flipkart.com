from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pandas import DataFrame
import time


while True:
    try:
        userinput = int(input("How Many Pages You Wants to Scrap (In Number) : "))
        Searchtext = input("What you want to Search (Text You wants to search) : ").replace(" ","%20")

        if (userinput>0) & (len(Searchtext)>0) & (Searchtext.isalpha())& (Searchtext != " "):
            break
        else:
            print("--- Please Enter Correct Values --- Try Again!")
            print()
    except:
        print("--- Please Enter Correct Values --- Try Again!")
        print()

# Running headless Chrome (PhantomJS is Old Now and Deprecated)
options = Options()
options.add_argument('--headless')
#options.add_argument('--disable-gpu')
browser = webdriver.Chrome('chromedriver', chrome_options=options)

#browser = webdriver.Chrome()

ProductName = []
ProductPrice = []
ProductDescription = []
ProductRating = []
ProductReviewCount = []
ProductPreviousPrice = []
ProductPercentOff = []

try: 
    for x in range(1,userinput+1):
        print('Page Number - ******************************************* {}'.format(x) + '\n')
        print()
    
        browser.get('https://www.flipkart.com/search?as=off&as-show=on&otracker=start&page={}&q={}&viewType=grid'.format(x,Searchtext))
        mysoup = BeautifulSoup(browser.page_source,'html5lib')

        if mysoup.find("div",{"class": "_1-2Iqu row"}):
            allcards = mysoup.findAll("div", {"class": "_1-2Iqu row"})
            for i in allcards:
                # Fetching Name of item
                print(i.find("div",{"class" : "_3wU53n"}).text)
                ProductName.append(i.find("div",{"class" : "_3wU53n"}).text)
                #Fetching Price
                try:
                    print(i.find("div",{'class':'_1vC4OE _2rQ-NK'}).text)
                    ProductPrice.append(i.find("div",{'class':'_1vC4OE _2rQ-NK'}).text)
                except:
                    print("Either Price is not Available or Item out of Stock")
                    ProductPrice.append("Either Price is not Available or Item out of Stock")
                #Short Description
                try:
                    print(i.find("li",{"class" : "tVe95H"}).text)
                    ProductDescription.append(i.find("li",{"class" : "tVe95H"}).text)
                except:
                    print("No Attribute is listed")
                    ProductDescription.append("No Attribute is listed")
                #Fetching Star Rating (Out of 5)
                try:
                    print(i.find("div",{"class" : "hGSR34 _2beYZw"}).text)
                    ProductRating.append(i.find("div",{"class" : "hGSR34 _2beYZw"}).text)
                except:
                    print("No Rating")
                    ProductRating.append("No Rating")
                #Fetching Count of review and Rating
                try:
                    print(i.find('span',{'class':'_38sUEc'}).text)
                    ProductReviewCount.append(i.find("span",{"class" : "_38sUEc"}).text)
                except:
                    print("No Review")
                    ProductReviewCount.append("No Review")
                # Product Previous Price
                try:
                    print(i.find('div',{'class':'_3auQ3N _2GcJzG'}).text)
                    ProductPreviousPrice.append(i.find("div",{"class" : "_3auQ3N _2GcJzG"}).text)
                except:
                    print("No Previous Price")
                    ProductPreviousPrice.append("No Previous Price")
                # Discount Off on Product
                try:
                    print(i.find('div',{'class':'VGWI6T'}).text)
                    ProductPercentOff.append(i.find("div",{"class" : "VGWI6T"}).text)
                except:
                    print("No Discount")
                    ProductPercentOff.append("No Discount")

            print("----------------------------------------------------------------")
        else:
            allcards = mysoup.findAll("div", {"class": "_3liAhj"})
            for i in allcards:
                # Fetching Name of item
                print(i.find("a",{"class" : "_2cLu-l"}).text)
                ProductName.append(i.find("a",{"class" : "_2cLu-l"}).text)
                # Below Code is For Fetching Price of item
                try:
                    print(i.find("div",{"class" : "_1vC4OE"}).text)
                    ProductPrice.append(i.find("div",{"class" : "_1vC4OE"}).text)
                except:
                    print("Either Price is not Available or Item out of Stock")
                    ProductPrice.append("Either Price is not Available or Item out of Stock")
                #Short Description
                try:
                    print(i.find("div",{"class" : "_1rcHFq"}).text)
                    ProductDescription.append(i.find("div",{"class" : "_1rcHFq"}).text)
                except:
                    print("No Attribute is listed")
                    ProductDescription.append("No Attribute is listed")
                #Fetching Star Rating (Out of 5)
                try:
                    print(i.find('div',{'class':'hGSR34 _2beYZw'}).text)
                    ProductRating.append((i.find('div',{'class':'hGSR34 _2beYZw'}).text))
                except:
                    print("No Rating")
                    ProductRating.append("No Rating")
                #Fetching Count of review and Rating
                try:
                    print(i.find('span',{'class':'_38sUEc'}).text)
                    ProductReviewCount.append(i.find("span",{"class" : "_38sUEc"}).text)
                except:
                    print("No Review")
                    ProductReviewCount.append("No Review")
                # Product Previous Price
                try:
                    print(i.find('div',{'class':'_3auQ3N'}).text)
                    ProductPreviousPrice.append(i.find("div",{"class" : "_3auQ3N"}).text)
                except:
                    print("No Previous Price")
                    ProductPreviousPrice.append("No Previous Price")
                # Discount Off on Product
                try:
                    print(i.find('div',{'class':'VGWI6T'}).text)
                    ProductPercentOff.append(i.find("div",{"class" : "VGWI6T"}).text)
                except:
                    print("No Discount")
                    ProductPercentOff.append("No Discount")

            print("----------------------------------------------------------------\n")
        time.sleep(5)
except HTTPError as e:
    print(e)
except URLError:
    print("Server down or incorrect domain")
else:
    print("Excel File Writing Started")
    df = DataFrame({'Product Name': ProductName,'Current Product Price': ProductPrice, 'Product Description': ProductDescription, 'Product Rating': ProductRating,'Product Rating & Review Count':ProductReviewCount,'Previous Product Price' : ProductPreviousPrice,'Product Percent Off': ProductPercentOff})
    df = df[["Product Name","Product Description","Current Product Price","Previous Product Price","Product Percent Off","Product Rating","Product Rating & Review Count"]]
    df.to_excel('FlipkartDataExtract.xlsx', sheet_name='Flipkart-Data', index=False)
    browser.close()
    print("Excel File Writing Completed")
    print("Page Scraping is Done")