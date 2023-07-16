import os
import requests
import bs4
from bs4 import BeautifulSoup
import pickle
from datetime import datetime


### Get channel urls from Youtubers.me top lists
# The urls for each list are in data/urls.txt

def get_top_list_urls():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    PATH = os.path.join(current_dir, "..","..","data/urls.txt")
    with open(PATH) as f:
        l=f.read().splitlines()
    return l

"""
# On Youtubers.me, if we click on the channel icon on the list,
we do not get redirected to the youtube channel homepage.
We are led to the channel's page on YouTubers.me and its url ends with /youtuber-stats.
But if we visit the same url with /youtuber-stats replaced by youtube,
then we are re-directed to the youtube channel's page.
"""


def get_redirected_url(url):
    response = requests.get(url, allow_redirects=False)
    redirected_url = response.headers.get('Location')
    return redirected_url


def get_channel_urls(url):
    """
    input: a youtubers.me top list url

    output: a list of youtube channel homepage urls for channels on the top list
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    channel_urls = []

    table_element = soup.find('table')

    if table_element:
        anchor_elements = table_element.find_all('a', href=lambda href: href and '/youtuber-stats' in href)[:1000]
        for element in anchor_elements:
            init_url = "https://us.youtubers.me" + element['href'].replace("youtuber-stats", "youtube")
            youtube_url = get_redirected_url(init_url)
            channel_urls.append(youtube_url)

    return channel_urls


# unfortunately we have to extract url one batch at a time by hand
# otherwise we may exceed the visit limits to youtubers.me

if __name__ == "__main__":

    for n in range(70,75):
        print('Running')
        startTime = datetime.now()
        print(startTime)
        top_lists_urls=get_top_list_urls()
        init_url=top_lists_urls[n]
        url_list = get_channel_urls(init_url)

        # save the url list with pickle
        current_dir = os.path.dirname(os.path.abspath(__file__))
        target_dir = os.path.join(current_dir, "..","..","data")
        file_path = os.path.join(target_dir, "url_list_"+ str(n)+".pkl")
        with open(file_path, "wb") as f:
            pickle.dump(url_list, f)
        print(f'finished run {n}')
        print(datetime.now()-startTime)
        print()
    print('Complete')
