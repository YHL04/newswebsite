

import re
import json
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

from pprint import pprint


def channel_videos_scraper(channel):
    yt_search = "https://www.youtube.com/%s/videos" % channel
    url_search = urlopen(yt_search)
    page = url_search.read()

    html_code = bs(page, "html.parser")

    # pattern = r'<script nonce="[-\w]+">\n\s+var ytInitialData = (.+)'
    # script_data = re.search(pattern=pattern, string=youtube_html.prettify())[1].replace(';', '')

    """
    richItemRenderer -> content -> videoRenderer -> navigationEndpoint -> commandMetadata -> webCommandMetadata -> url
    
    
    """

    # # # Define a regular expression pattern to extract the JSON data from the script tag
    # pattern = r'<script nonce="[-\w]+">\n\s+var ytInitialData = (.+)'
    # script_data = re.search(pattern=pattern, string=youtube_html.prettify())[1].replace(';', '')
    #
    # # Load the JSON data into a Python dictionary
    # json_data = json.loads(script_data)
    #
    # # Extract the list of videos from the JSON data and store it in the 'videos_container' variable
    # videos_container = \
    # json_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']['richGridRenderer'][
    #     'contents']
    #
    # print(f"Total videos: {len(videos_container) - 1}")
    #
    # # Loop through the video list and print the URLs of the videos
    # for video in videos_container[:-1]:
    #     # print(video)
    #     video_id = video['richItemRenderer']['content']['videoRenderer']['videoId']
    #     video_url = f"https://www.youtube.com/watch?v={video_id}"
    #     print(video_url)
    #


def search_results_scraper(search):
    pass


def youtube_scraper():
    return


if __name__ == "__main__":
    channel_videos_scraper("@aiexplained-official")

