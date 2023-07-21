import pickle
import os

def process_topic_id():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    PATH = os.path.join(current_dir, "..","..","data/topic_id_list.txt")
    with open(PATH) as f:
        lines=f.readlines()
    id_2_topic={}
    for s in lines:
        topicId, topic = s.split('\t')
        id_2_topic[topicId]=topic.rstrip()
    return id_2_topic




def save_data(obj, title):
    """
    Save an object (list, dictionary...) to a pickle file with name title to the data directory
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(current_dir, "..","..","data")
    file_path = os.path.join(target_dir, title+ '.pkl')
    with open(file_path, "wb") as f:
        pickle.dump(obj, f)
    return

