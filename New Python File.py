import sys

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

"""depracated... for checking dependencies"""
# print("Imported packages:")
# for module in sys.modules.keys():
#     print(module)
"""dont know why the hell this thing prompts using tensorflow and took a lot of time but its working"""
# try:
#     import TensorFlow as tf
#     # If imported successfully, delete it
#     del tf
#     print("TensorFlow was imported and has been removed.")
# except ImportError:
#     print("TensorFlow is not installed.")

# # Your Steam cookie for authentication
# cookies = {
#     'steamLoginSecure': '76561198404740688%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MEY0NF8yNEVFQkQ5NV8yMzAxOSIsICJzdWIiOiAiNzY1NjExOTg0MDQ3NDA2ODgiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3Mjc2MjA1MDQsICJuYmYiOiAxNzE4ODkyNTcwLCAiaWF0IjogMTcyNzUzMjU3MCwgImp0aSI6ICIxMEEwXzI1MUNERTgxXzhBMDE0IiwgIm9hdCI6IDE3MjQ0MDQxMjgsICJydF9leHAiOiAxNzQyNzMzNDc0LCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiMTE1LjE2NC41NS4xMTQiLCAiaXBfY29uZmlybWVyIjogIjExNS4xNjQuNTUuMTE0IiB9._YwmsA2t8AZyqNbNEcct7rhncka6NfYnT-Sn3SGZWIAINDug7yDI4ApfCBBsNy_O6PDSq6huhCF4JnLlfgdpCA',  # Replace with your actual Steam login secure cookie
# }

# # Base URL for searching user profiles on Steam
# base_url = 'https://steamcommunity.com/search/users/'

def get_page_instance_with_url_selenium(url, cookies):
    if not cookies:
        raise ValueError("Cookies must be provided for authentication.")

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Optional: run in headless mode
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    driver.get(url)

    # Add cookies to the WebDriver
    for key, value in cookies.items():
        driver.add_cookie({'name': key, 'value': value})

    driver.refresh()  # Refresh the page to include cookies
    time.sleep(100)  # Wait for the page to load fully
    soup = BeautifulSoup(driver.page_source, 'html.parser')  # Parse the page source
    driver.quit()
    return soup


def search_profiles(keyword):
    page_number = 1  # Start with the first page
    profile_links = []  # Initialize a list to store matched profile links

    while True:  # Start an infinite loop to fetch pages
        # Construct the search URL with the current page number
        search_url = f"{base_url}#page={page_number}&text={keyword}"
        # Find all anchor tags with href attributes
        all_href_obj = all_urls_on_page(search_url)

        # Break the loop if no href markers are found
        if not all_href_obj:
            print("no links found on page")
            break
        
        profile_links.extend(profile_links_on_page(all_href_obj))#find all links from the href objects and extend it to the main list

        # Increment the page number for the next iteration
        page_number += 1

    return profile_links  # Return the list of matched profile links

def url_of_page_num(base_url,pageNum,player_name):
    return f"{base_url}#page={pageNum}&text={player_name}"

def check_games_for_keyword(profile_url, keyword, cookies):
    # Construct the URL for the player's games
    games_url = f"{profile_url}games/"
    response = requests.get(games_url, cookies=cookies)  # Fetch the games page
    soup = BeautifulSoup(response.text, 'html.parser')  # Parse the games page HTML
    
    # Check if the page contains the keyword "Helldivers"
    if keyword.lower() in soup.text.lower():
        return profile_url  # Return the profile URL if keyword is found
    return None  # Return None if not found

def all_urls_on_page(page_url, cookies):
    try:
        response = requests.get(page_url, cookies=cookies)  # Make a GET request with the cookie
        response.raise_for_status()  # Raise an error for bad responses
        soup_page_instance = BeautifulSoup(response.text, 'html.parser')  # Parse the response HTML
        all_href_obj = soup_page_instance.find_all('a', href=True)  # Get all href objects
        
        # Extract and return the URLs
        urls = [href_obj['href'] for href_obj in all_href_obj]  # Strip URLs from href attributes
        return urls
    except requests.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")
        return []  # Return an empty list in case of an error

def is_profile_url(url)-> bool:
    return url.startswith("https://steamcommunity.com/id/")

def profile_links_in_urls(urls):
    profile_links_on_page = [
        url for url in urls if is_profile_url(url)
    ]
    for url in profile_links_on_page:
        print(f"profile url found: {url}")  # Print each found profile URL

    return profile_links_on_page  # Return the list of matched profile links

def profile_links_on_page(soup_page_instance):
    profile_links_on_page = []
    # Collect links that match the profile link class
    all_href_objs = soup_page_instance.find_all('a', class_='searchPersonaName')
    
    for href_obj in all_href_objs:
        profile_links_on_page.append(href_obj['href'])
        print(f"profile url found: {href_obj['href']}")
        
    return profile_links_on_page

# def get_page_instance_by_url(url, cookies) -> BeautifulSoup:
"""depracted since the page cannot load correctly without jscript"""
#     response = requests.get(url, cookies=cookies)  # Make a GET request with the cookie
#     return BeautifulSoup(response.text, 'html.parser')  # Parse and return the soup instance

def profile_links_on_page_url(url, cookies):
    soup_page_instance = get_page_instance_with_url_selenium(url, cookies)  # Get the BeautifulSoup instance
    return profile_links_on_page(soup_page_instance)  # Extract profile links using the soup instance

# def main():
#     keyword = "Helldivers"  # Set the keyword to search for
#     matched_profiles = search_profiles(keyword)  # Call the function to search profiles

#     # Check each profile's games for the keyword
#     matched_keyword_profiles = []
#     for profile in matched_profiles:
#         if check_games_for_keyword(profile, keyword):
#             matched_keyword_profiles.append(profile)
#             print(f"Matched profile url found: {profile}")

#     print(matched_keyword_profiles)  # Print the matched profile links

def main():

    cookies = {
    'steamLoginSecure': '76561198404740688%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MEY0NF8yNEVFQkQ5NV8yMzAxOSIsICJzdWIiOiAiNzY1NjExOTg0MDQ3NDA2ODgiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3Mjc2MjA1MDQsICJuYmYiOiAxNzE4ODkyNTcwLCAiaWF0IjogMTcyNzUzMjU3MCwgImp0aSI6ICIxMEEwXzI1MUNERTgxXzhBMDE0IiwgIm9hdCI6IDE3MjQ0MDQxMjgsICJydF9leHAiOiAxNzQyNzMzNDc0LCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiMTE1LjE2NC41NS4xMTQiLCAiaXBfY29uZmlybWVyIjogIjExNS4xNjQuNTUuMTE0IiB9._YwmsA2t8AZyqNbNEcct7rhncka6NfYnT-Sn3SGZWIAINDug7yDI4ApfCBBsNy_O6PDSq6huhCF4JnLlfgdpCA',  # Replace with your actual Steam login secure cookie
}
    player_name="404+Not+Found"
    base_url = 'https://steamcommunity.com/search/users/'
    pageNum=1
    print(profile_links_on_page_url(url_of_page_num(base_url,pageNum,player_name),cookies))

if __name__ == "__main__":
    main()  # Call the main function
