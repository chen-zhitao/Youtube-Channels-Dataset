
# Youtube Channels Dataset

16K+ popular Youtube channels dataset for data science projects such as channel classification, natural language processing, and recommender system. Channels are mostly in English.

The dataset in CSV format can be found in data/channels.csv in this Github repository. Alternatively, you can download it from kaggle <https://www.kaggle.com/datasets/zhitaochen/channels>.

Each entry in the dataset includes:
* channelId: a unique id for each channel on Youtube
* url: url to the channel's homepage on Youtube
* description: a text describing the channels's content (see Collection Methodology for details)



## Collection Methodology

1.  Retrieve top and popular Youtube channels lists from [Youtubers.me](https://us.youtubers.me) for all Youtube Categories and several countries (e.g. US, UK, India). Record the url to each channel's Youtube homepage.
2.  Using [Beautiful Soup](https://pypi.org/project/beautifulsoup4/), parse the HTML for each channel's homepage and record their unique Youtube channelId, to be used in the Youtube Data API.
3. Using the [Youtube Data API](https://developers.google.com/youtube/v3), retrieve the following text data for each channel:
* The channel's topic categories
* Channel description provided by the creator
* Titles and descriptions of up to 15 most recent videos of the channel
4. Combining natural language processor from [spaCy](https://spacy.io) and Python regular expression, process the texts data collected from the previous step. Non-English channels are discarded. Urls, social media handles, and hashtags are removed.
5. Store channelId, channel url, and processed text data to dataset using sqlite3.

## Acknowledgements
- [Youtubers.me](https://us.youtubers.me)
- [Awesome README](https://github.com/matiassingers/awesome-readme)

