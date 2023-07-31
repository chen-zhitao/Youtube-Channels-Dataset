import os
import sys
cur_path = os.path.dirname(os.path.abspath(__file__))
nlp_path = os.path.join(cur_path, "text_processing")
sys.path.append(nlp_path)

from text_processing import nlp
import sqlite3
from googleapiclient.discovery import build
import pickle
from datetime import datetime

# set up youtube api access
api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build('youtube','v3', developerKey=api_key)

# set up sqlite3 connection
data_directory = os.path.join(cur_path, "..", "data")
db_file = os.path.join(data_directory, "channels.db")

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# load lists of channelIds
file_path=os.path.join(data_directory, "id_2_url.pkl")
with open(file_path, 'rb') as f:
    id_2_url = pickle.load(f)
channelId_list = list(id_2_url.keys())


# load the topicId to topic title dictionary
file_path=os.path.join(data_directory, "topicId_2_topic.pkl")
with open(file_path, 'rb') as f:
    topicId_2_topic = pickle.load(f)

# load nlp
text_processor = nlp.get_nlp()

# valid sentence ending
valid_endings = {'.', '!', '?'}



def main(channelId_list):

    # call channels().list() for 50 channels at a time
    # snippets contain channel title and description
    j=0
    group_size = 50
    for i in range(0, len(channelId_list), group_size):
        id_group=channelId_list[i:i+group_size]

        requests=youtube.channels().list(part=['snippet','topicDetails'], id=id_group)
        response=requests.execute()

        # loop over the response itmes
        for channel in response['items']:
            print(f'channel {j}')
            j+=1
            # initialize list for all text data
            text_feature=[]

            channelId= channel['id']
            channel_url = id_2_url[channelId]
            
            # obtain playlist id by replacing "UC" with "UU" in channelId
            playlist_id = "UU"+channelId[2:]

            # call playlistItems().list() for this playlist to return recent videos
            playlist_request = youtube.playlistItems().list(part="snippet", maxResults=15, playlistId = playlist_id)
            try:
                playlist_response = playlist_request.execute()
            except:
                continue

            # discard channel if it has fewer than 10 videos
            if len(playlist_response['items'])<10:
                continue
            
            # if succeed, collect the following items:

            # 1. channel topics
            if 'topicDetails' in channel and 'topicIds' in channel['topicDetails']:
                topic_id_list = channel['topicDetails']['topicIds']
                for topic_id in topic_id_list:
                    if topic_id not in topicId_2_topic:
                        continue
                    text_feature.append(topicId_2_topic[topic_id]+'.')

            
            # 2. channel description
            channel_des=channel['snippet']['description']
            if channel_des:
                text_feature.append(channel_des if channel_des[-1] in valid_endings else channel_des+'.')

            # 3. titles and descriptions of the most recent videos of channel
            for i in range(min(15, len(playlist_response['items']))):
                vid=playlist_response['items'][i]

                title=vid['snippet']['title']
                if title[-1] in valid_endings:
                    text_feature.append(title)
                else:
                    text_feature.append(title+'.')

                des=vid['snippet']['description']
                if not des:
                    continue
                if des[-1] in valid_endings:
                    text_feature.append(des)
                else:
                    text_feature.append(des+'.')
                         

            # convert text_feature to one string then process
            # if the language is not primarily English, discard

            text=" ".join(text_feature)
            try:
                is_Eng = nlp.is_English(text)
                if is_Eng == False:
                    continue
            except:
                continue

            processed_text = nlp.process_text(text, text_processor)

            if len(processed_text)< 250:
                continue

            #add channelId, url, and text feature to database
            
            try:
                cursor.execute("""INSERT INTO channels VALUES (?, ?, ?);""", (channelId, channel_url, processed_text))
                conn.commit()
            except:
                continue
    print('complete')
    return 


if __name__ == "__main__":
    startTime = datetime.now()
    print(startTime)
    main(channelId_list[30000:])
    print(datetime.now()-startTime)
    
