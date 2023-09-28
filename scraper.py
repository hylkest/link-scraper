import time
import requests
from bs4 import BeautifulSoup
import urllib.parse
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="links",
    port="8889"
)

mycursor = mydb.cursor()


print(mydb)

visited_links = set()  # To keep track of visited links

def get_all_links_recursive(url, depth=1, max_depth=3):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all the anchor (a) tags on the page
            links = soup.find_all('a')

            # Extract and print all the href attributes (links)
            for link in links:
                href = link.get('href')

                # Make sure the link is not empty and is an absolute URL
                if href and not href.startswith('#') and not href.startswith('javascript:'):
                    # Create an absolute URL if it's a relative URL
                    absolute_url = urllib.parse.urljoin(url, href)

                    # Check if the link hasn't been visited before
                    if absolute_url not in visited_links:
                        visited_links.add(absolute_url)
                        # print(f"Depth {depth}: {absolute_url}")
                        print(absolute_url)
                        sql = "INSERT INTO links (main_link, link_name) VALUES (%s, %s)"
                        val = (f"{initial_url}", f"{absolute_url}")
                        mycursor.execute(sql, val)

                        mydb.commit()

                        # Recursively scrape links up to a certain depth
                        if depth < max_depth:
                            get_all_links_recursive(absolute_url, depth + 1, max_depth)

        elif response.status_code == 400:
            print("404")
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Prompt the user for the URL of the initial webpage to scrape
    initial_url = input("Enter the URL of the initial webpage to scrape: ")

    # Set the maximum depth for recursion (e.g., how many pages deep to scrape)
    max_depth = int(input("Enter the maximum depth for recursion: "))

    # Call the recursive function to scrape links
    get_all_links_recursive(initial_url, max_depth=max_depth)
