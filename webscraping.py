from selenium import webdriver
from bs4 import BeautifulSoup
import os, sys
import pandas as pd
import requests


df = pd.DataFrame()

# This look loop trough each page os the given website 
for i in range(3):
    url = f"https://www.onthemarket.com/for-sale/property/uk/?page={i}"

    options = webdriver.ChromeOptions()
    options.add_argument('headless') 
    driver = webdriver.Chrome(options=options)

    # Load the webpage
    driver.get(url)

    # Wait for the webpage to load
    driver.implicitly_wait(10)

    html_content = driver.page_source
    driver.quit()

    # BeautifulSoup is method to find the elements
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the property cards
    property_cards = soup.find_all('li', class_="otm-PropertyCard isOwu")

    property_agent_card = soup.find_all('div',class_="otm-PropertyCardAgent")

    
    for property, card in zip(property_cards, property_agent_card):
        # Extract property details
        title = property.find('span', class_="title").text.strip()
        location = property.find('span', class_="address").text.strip()
        price = property.find('div', class_="otm-Price").text.strip()
        Extrainfo = property.find_all('li', class_="otm-ListItemOtmBullet before:bg-brand-contrast")
        extra_info_list = [info.text.strip() for info in Extrainfo]
        bedroom_div = property.find('div', class_='otm-BedBathCount flex items-center')
        bedrooms = bedroom_div.find('div').text.strip()
        bathroom = property.find('div', class_='otm-BedBathCount flex items-center').find_all('div')[1].text.strip()
            
        # Extract agent details
        agent_info = card.find('div', class_="otm-Telephone text-link font-semibold flex items-center cursor-pointer").text.strip()
        marketed = card.find('small').text.strip()
        marketed_by = marketed.split("Marketed by ")[1] if 'Marketed by' in marketed else None
            
        # Print property and agent details
        print(f'Title: {title}')
        print(f'Location: {location}')
        print(f'Price: {price}')
        print(f'Extra Info: {", ".join(extra_info_list)}')
        print(f'Bedrooms: {bedrooms}')
        print(f'Bathroom: {bathroom}')
        print('Agent Contact:', agent_info)
        print('Marketed By:', marketed_by)
        print()
        

        # Create a dictionary to store property details and transform it into a temporary DataFrame
        data = {
            'Title': title,
            'Location': location,
            'Price': price,
            'Extra Info': ", ".join(extra_info_list),
            'Bedrooms': bedrooms,
            'Bathroom': bathroom,
            'Agent Contact': agent_info,
            'Marketed By': marketed_by
        }
        
    
        # ------------------------------------------------------------
        # Save the data to a CSV file:
        # - If the file doesn't exist, it will be created with headers.
        # - If the file exists, the data will be appended without adding headers again.
        # Note: This code assumes that the CSV file, if existing, already has the correct header row.
        # If starting fresh, ensure to remove any existing CSV file before running this script.
        # ------------------------------------------------------------
 
        # Convert the dictionary to a temporary DataFrame
        df = pd.DataFrame([data])
        
        # Check if the file exists
        if not os.path.exists("real_estate.csv"):
            # Write the DataFrame to a new file with headers
            df.to_csv("real_estate.csv", index=False)
        else:
            # Append the DataFrame to the existing file without writing the headers again
            df.to_csv("real_estate.csv", mode='a', header=False, index=False)
            