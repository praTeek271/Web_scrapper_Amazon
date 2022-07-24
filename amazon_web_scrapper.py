import csv
from bs4 import BeautifulSoup as bs
from selenium import webdriver      # works with the Chrome  and firefox browser only


def navigate_url(url, index):
    if "&page=" in url:
        next_btn_url = url.replace(f"&page={index-1}",f"&page={index}")
    else:
        next_btn_url=url[:30]+f"&page={index}"+url[30:]

    sr_pg=index-1
    next_btn_url=next_btn_url.replace(url[-7:],f"sr_pg_{sr_pg}")
    # returning next page url
    print("Navigting to next page...")
    return(next_btn_url)

def extract_data():
    # --------------->    for accessing all the names of the products all at once

    
    for product_no in range(1,len(result_data)):
        item=result_data[product_no]
        atag=item.h2.a
        name=atag.text.strip("\n")
        product_url="https://amazon.in"+atag.get('href')
        price=''
        rating=''
        no_of_reviews=''

        try:
            price=item.find('span','a-offscreen').text.strip()
            price=price.replace(price[:1],"Rs ")
        except(AttributeError):
            price=''
        try:
            rating=item.i.text.strip()
        except(AttributeError):
            rating=''
        try:
            no_of_reviews=item.find('span','a-size-base s-underline-text').text.strip()
        except(AttributeError):
            no_of_reviews=''
        
        description,asin,manufacturer,dimension=product_info(product_url)
        
        names.append([name,price,rating,no_of_reviews,product_url,description,dimension,asin,manufacturer])

        
        names.append([name,price,rating,no_of_reviews,product_url])
    print("Extraction of page complete...")

def product_info(url):
    driver_pr=webdriver.Chrome()
    driver_pr.get(url)
    
    soup=bs(driver_pr.page_source,'html.parser')
    dresult=soup.findAll('div',{'id':'feature-bullets'})
    
    try:
        results_parent=soup.find('div',{'id':'detailBullets_feature_div'})
        results=results_parent.findAll('span',{'class':'a-list-item'})
    except:
        # results=['','','','','','','','','']
        pass
    


    # description of the product
    try:
        description=dresult[0].text.strip("\n").replace('   ',"\n*")
    except:
        description=""
    print("Description fetched")
    
    # ASIN of the product
    try:
        asin=results[3].text.strip("\n").strip()
        unwanted_string_asin="ASIN\n                                    \u200f\n                                        :\n                                    \u200e\n"
        asin=asin.replace(unwanted_string_asin,"").strip()
    except:
        asin=None
    print("ASIN fetched")

    # Manufacturer of the product
    try:
        manufacturer=results[7].text.strip("\n").strip()
        unwanted_string_manufacturer="Manufacturer\n                                    \u200f\n                                        :\n                                    \u200e\n"
        manufacturer=manufacturer.replace(unwanted_string_manufacturer,"").strip()
    except:
        manufacturer=''
    print("Manufacturer fetched")
    # Product Dimensions
    try:
        dimension=results[0].text.strip("\n").strip()
        unwanted_string_dimension="Product Dimensions\n                                    \u200f\n                                        :\n                                    \u200e\n"
        dimension=dimension.replace(unwanted_string_dimension,"").strip()
    except:
        dimension=''
    print("Product Dimensions fetched")

    driver_pr.close()
    return(description,asin,manufacturer,dimension)




def save_data_in_csv(data):
  
    with open('product_results.csv', 'w',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Product_Name','Price','Rating',"No_of_reviews",'Url'])
        writer.writerows(data)

    print("Detais being saved in 'product_results.csv' file ")


if __name__=="__main__":

    driver=webdriver.Chrome()
    names=[]
    url="https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
    for page in range(2,21):
        driver.get(url)
        soup=bs(driver.page_source,'html.parser')
        result_data=soup.findAll('div',{'data-component-type':'s-search-result'})
        
        extract_data()
        print("Page {0} extraction complete.".format(page))
        url=navigate_url(url, page)
        

    driver.close()
    print("All the Extraction process is complete. of all the 20 pages...")
    save_data_in_csv(names)


