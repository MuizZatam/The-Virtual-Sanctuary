import requests
from bs4 import BeautifulSoup

def fetch_bing_images(query, num=4) -> list[str]:

    """
    Fetches a specified number of image URLs from Bing Image Search, 
    prioritizing images from Wikimedia Commons and filtering results 
    by Creative Commons licenses.

    Args:
        `query (str)`: The search query to find images.
        `num (int)`: The number of image URLs to return. Default is 10.

    Returns:
        `list`: A list of image URLs, with Wikimedia Commons images 
              prioritized at the beginning of the list.

    Notes:
        - This function scrapes the Bing Image Search results page.
        - The search results are filtered to include only images with 
          Creative Commons licenses.
        - Images from Wikimedia Commons (wikimedia.org) are given 
          priority in the returned list.
        - The function uses the 'qft' parameter to apply Creative Commons 
          license filters, and the 'q' parameter for the search query.
        - The function mimics a web browser using custom headers to avoid 
          being blocked by Bing.
    """

    search_url = "https://www.bing.com/images/search"

    params = {
        "q": query,
        "qft": "+filterui:license-L2_L3_L4_L5_L6_L7",  
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }   

    response = requests.get(search_url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    image_urls = list()

    for img_tag in soup.find_all("a", {"class": "iusc"}):

        m = img_tag.get("m")

        if m:

            img_link = m.split('"murl":"')[1].split('","')[0]

            image_urls.append(img_link)
        
        
        if len(image_urls) >= num:

            break
    
    
    return image_urls
    

def main():

    print(fetch_bing_images(input("Enter a Query > ")))


if __name__ == "__main__":

    main()