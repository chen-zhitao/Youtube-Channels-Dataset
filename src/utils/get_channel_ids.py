import pickle
import os
import requests
import re
import json
import bs4
from bs4 import BeautifulSoup

def load_urls():
    # load all saved urls and remove duplicates
    out=[]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    PATH = os.path.join(current_dir, "..","..","data/url_lists/url_list_")
    for i in range(75):
        with open(PATH+str(i)+'.pkl', 'rb') as file:
            url_list = pickle.load(file)
        out=out+url_list
    out=list(filter(lambda item: item is not None, out))
    return list(set(out))



def get_channel_id(channel_url):
    
    # if the channel url contains "channel/UCXXXXX"
    # then UCXXXXX is the channel id
    match_id = re.search(r"channel/(UC[a-zA-Z0-9-_]+)", channel_url)
    if match_id:
        channel_id = match_id.group(1)
        return channel_id

    # otherwise we examine the html of the channel homepage
    response = requests.get(channel_url,allow_redirects=True)
    soup=BeautifulSoup(response.text, "html.parser")

    """
    The channel id is stored under ytInitialData - header - c4TabbedHeaderRenderer
    Simplying searching for "channelid" may not return the main channel id
    because the html also contains channelid(s) of other channels by the same uploader
    """
    data= re.search(r"var ytInitialData = ({.*});", str(soup.prettify())).group(1)

    json_data=json.loads(data)
    return json_data['header']['c4TabbedHeaderRenderer']['channelId']



def load_url_master_list():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    PATH = os.path.join(current_dir, "..","..","data/url_list_master.pkl")
    with open(PATH, 'rb') as file:
        url_list = pickle.load(file)
    return url_list



def get_and_save_id(url_list):
    # given a url_list, get channelid for all urls
    # save id-url pair in a dictionary

    id_2_url={}
    for i, url in enumerate(url_list):
        try:
            channelId = get_channel_id(url)
            id_2_url[channelId]=url
        except:
            print(i)
            print(url)
    return id_2_url




if __name__ == "__main__":

    # load dictionary storing channelId-url pairs
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(current_dir, "..","..","data")
    file_path = os.path.join(target_dir, "id_2_url.pkl")
    with open(file_path, "rb") as f:
        id_2_url = pickle.load(f)
    
    print(len(id_2_url))



    """
    # load saved url list
    url_master_list = load_url_master_list()
     

    # get a list of channel ids from the url_list
    # and store the id-url pair in a dictionary

    id_2_url = get_and_save_id(url_master_list)


    
    # save id-url pair
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(current_dir, "..","..","data")
    file_path = os.path.join(target_dir, "id_2_url.pkl")
    
    with open(file_path, 'wb') as f:
        pickle.dump(id_2_url,f)
    """

    

    """
    # load and save url list without duplicate
    url_list=load_urls()
    print(len(url_list))
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(current_dir, "..","..","data")
    file_path = os.path.join(target_dir, "url_list_master.pkl")
    with open(file_path, "wb") as f:
        pickle.dump(url_list, f)
    """
    
    