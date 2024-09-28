import sys
import logging
import time

# Generate a unique filename based on the current time
filename = f"app_{time.strftime('%Y-%m-%d_%H-%M-%S')}.log"

# Configure the logging to write to a new file each time
logging.basicConfig(
    filename=filename,  # Specify the log file name
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Set the format of log messages
    filemode='w'  # Create a new file each time (overwrite existing)
)

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

"""depracted... tensorflow-gpu use not decided yet"""
# import tensorflow as tf
# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

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

driver = None

def init_webdriver():
    global driver
    if driver is None:  # Check if driver is already initialized
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

def close_webdriver():
    global driver
    if driver is not None:
        driver.quit()
        driver = None

def get_page_instance_with_url_selenium(url, cookies):
    init_webdriver()  # Ensure the WebDriver is initialized
    
    if not cookies:
        raise ValueError("Cookies must be provided for authentication.")
    driver.get(url)
    # Add cookies to the WebDriver
    for key, value in cookies.items():
        driver.add_cookie({'name': key, 'value': value})
    # Load cookie
    driver.refresh()
    # Wait for a specific element to load (change 'element_selector' to an actual selector)
    try:
        # Wait for the document to be fully loaded
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        
        # Optional: wait for a specific element that indicates content is fully loaded
        # WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, 'specific_element_selector'))
        # )

        # If needed, add a slight delay
        time.sleep(2)  # Adjust the duration as necessary

        # Now you can get the page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    except TimeoutException:
        print("Loading took too much time!")

    soup = BeautifulSoup(driver.page_source, 'html.parser')  # Parse the page source
    return soup

"""depracated due to complexity reasons"""
# def search_profiles(keyword):
#     page_number = 1  # Start with the first page
#     profile_links = []  # Initialize a list to store matched profile links

#     while True:  # Start an infinite loop to fetch pages
#         # Construct the search URL with the current page number
#         search_url = f"{base_url}#page={page_number}&text={keyword}"
#         # Find all anchor tags with href attributes
#         all_href_obj = all_urls_on_page(search_url)

#         # Break the loop if no href markers are found
#         if not all_href_obj:
#             print("no links found on page")
#             break
        
#         profile_links.extend(profile_links_on_page(all_href_obj))#find all links from the href objects and extend it to the main list

#         # Increment the page number for the next iteration
#         page_number += 1

#     return profile_links  # Return the list of matched profile links

def url_of_page_num(base_url,pageNum,player_name):
    return f"{base_url}#page={pageNum}&text={player_name}"

def get_recent_game_page_url(profile_url):
    return profile_url+"/games"

"""depracated... due to use of selenium, require to load jscript of page and this will not correctly load the page"""
# def check_games_for_keyword(profile_url, keyword, cookies):
#     # Construct the URL for the player's games
#     games_url = f"{profile_url}games/"
#     response = requests.get(games_url, cookies=cookies)  # Fetch the games page
#     soup = BeautifulSoup(response.text, 'html.parser')  # Parse the games page HTML
    
#     # Check if the page contains the keyword "Helldivers"
#     if keyword.lower() in soup.text.lower():
#         return profile_url  # Return the profile URL if keyword is found
#     return None  # Return None if not found
"""depracated... without selenium the page cannot load correctly to show the game/profile urls"""
# def all_urls_on_page(page_url, cookies):
#     try:
#         response = requests.get(page_url, cookies=cookies)  # Make a GET request with the cookie
#         response.raise_for_status()  # Raise an error for bad responses
#         soup_page_instance = BeautifulSoup(response.text, 'html.parser')  # Parse the response HTML
#         all_href_obj = soup_page_instance.find_all('a', href=True)  # Get all href objects
        
#         # Extract and return the URLs
#         urls = [href_obj['href'] for href_obj in all_href_obj]  # Strip URLs from href attributes
#         return urls
#     except requests.RequestException as e:
#         print(f"An error occurred while fetching the page: {e}")
#         return []  # Return an empty list in case of an error

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
    profile_href_objs = soup_page_instance.find_all('a', class_='searchPersonaName')
    
    for href_obj in profile_href_objs:
        profile_links_on_page.append(href_obj['href'])
        logging.info(f"profile url found: {href_obj['href']}")
        print(f"profile url found: {href_obj['href']}")
    return profile_links_on_page

def soup_page_instance_containing_keyword(soup_page_instance, keyword) -> bool:
    # Convert the soup instance to text and check for the keyword
    return keyword.lower() in soup_page_instance.get_text().lower()

# def get_page_instance_by_url(url, cookies) -> BeautifulSoup:
"""depracted since the page cannot load correctly without jscript"""
#     response = requests.get(url, cookies=cookies)  # Make a GET request with the cookie
#     return BeautifulSoup(response.text, 'html.parser')  # Parse and return the soup instance

def profile_links_on_page_url(url, cookies):
    soup_page_instance = get_page_instance_with_url_selenium(url, cookies)  # Get the BeautifulSoup instance
    return profile_links_on_page(soup_page_instance)  # Extract profile links using the soup instance

def game_links_on_page(soup_page_instance)->list[str]:
    game_links_on_page = []
    all_href_objs = soup_page_instance.find_all('a')
    print(all_href_objs)
    desired_prefix = "https://store.steampowered.com/app/"
    game_href_objs = [
    href_obj for href_obj in all_href_objs 
    if 'href' in href_obj.attrs and href_obj['href'].startswith(desired_prefix)
    ]
    for href_obj in game_href_objs:
        game_links_on_page.append(href_obj['href'])
        logging.info(f"game url found: {href_obj['href']}")
        print(f"game url found: {href_obj['href']}")
    return game_links_on_page

def gamelink_containing_game_id(game_link,target_id)->bool:
    return game_link.endswith(str(target_id))

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
    target_id = 394510
    pageNum = 1
    while True:
        profile_urls = profile_links_on_page_url(url_of_page_num(base_url,pageNum,player_name),cookies) # find the urls of profiles
        profile_recentgamepage_urls = [get_recent_game_page_url(profile_url) for profile_url in profile_urls] # concatenate the recent game page url
        recentgamepage_instances = {
                                    profile_recentgamepage_url: 
                                    get_page_instance_with_url_selenium(profile_recentgamepage_url,cookies)
                                    for profile_recentgamepage_url in profile_recentgamepage_urls
                                    } # dictionary of recentgame page instances, each url correspond to a page
        
        recentgamepage_containing_gameId = [] # pages containing target keyword

        for url, recentgamepage_instance in recentgamepage_instances.items():
            for each_game_url in game_links_on_page(recentgamepage_instance):
                if gamelink_containing_game_id(each_game_url,target_id):
                    recentgamepage_containing_gameId.append(url)
                    print(f'Eligible pages found:{recentgamepage_containing_gameId}')
                    logging.info(f'Eligible pages found:{recentgamepage_containing_gameId}')
        pageNum += 1

if __name__ == "__main__":
    main()  # Call the main function