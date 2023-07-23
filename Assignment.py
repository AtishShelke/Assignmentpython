import csv
import requests
from bs4 import BeautifulSoup



def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    description= soup.find("span", attrs={"class": "a-list-item"})
    asin_number = soup.find("td", attrs={"class": "a-size-base prodDetAttrValue"})
    product_description = soup.find("div", attrs={"id": "productDescription"})
    manufacturer_name = soup.find("td", class_="a-size-base prodDetAttrValue")

    return {
        "Description": description.text.strip(),
        "ASIN": asin_number,
        "Product Description": product_description.text.strip(),
        "Manufacturer": manufacturer_name,
    }

def scrape_products(url, pages):
    all_products = []
    base_url = "https://www.amazon.in"
    
    for page in range(1, pages + 1):
        page_url = f"{url}&page={page}"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        products = soup.find_all("div", class_="sg-row")
        for product in products:
           
            product_name = product.find("span", attrs={"class": "a-size-medium a-color-base a-text-normal"})
            product_price = product.find("span", attrs={"class": "a-price-whole"})
            rating = product.find("span", attrs={"class": "a-icon-alt"})
            num_reviews = product.find("span", attrs={"class": "a-size-base s-underline-text"})
            try:
                product_url = product.find("a", attrs={"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})["href"]
            except (TypeError, KeyError):
                product_url = None
            if product_name and product_price and rating and num_reviews and product_url:
                product_data = {
                    "Product URL": base_url + product_url,
                    "Product Name": product_name.text.strip(),
                    "Product Price": product_price.text.strip(),
                    "Rating": rating.text.strip(),
                    "Number of Reviews": num_reviews.text.strip(),
                }
                all_products.append(product_data)
    
    return all_products

if __name__ == "__main__":
    website_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"  
    new_url =  website_url[:-1]
    num_pages_to_scrape = 2  # Reduced for demonstration purposes

    scraped_data = scrape_products(new_url,num_pages_to_scrape)

    with open("products788.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews",
                      "Description", "ASIN", "Product Description", "Manufacturer"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for product_data in scraped_data:
            if product_data["Product URL"]:
                additional_info = scrape_product_details(product_data["Product URL"])
                product_data.update(additional_info)
                writer.writerow(product_data)
                
    print("Scraping completed and data saved to 'products.csv'")

