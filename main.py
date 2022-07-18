#!/usr/bin/env python3

import sys
import requests
import os
import subprocess
from urllib.request import urlopen, URLError

def redditDownloader(url):
    if not urlopen(url):
       raise Exception("invalid url:" + url)

    print("Processing URL: " + url)

    # User Agent headers to prevent 429 error response
    headers = {
        'User-Agent': 'reddit-video-downloader',
        'From': 'reddit-video-downloader@example.com'
    }

    metadata_url = url + ".json"
    data = requests.get(metadata_url, headers=headers).json()
    submission_data = data[0]["data"]["children"][0]["data"]
    media_data = submission_data["media"]

    title = submission_data["title"]
    video_url = media_data["reddit_video"]["fallback_url"]
    audio_url = video_url.split("DASH_")[0] + "DASH_audio.mp4"
    video_output_path = os.path.join(".", title) + ".mp4"

    print("Title: " + title)
    print("Video URL: " + video_url)
    print("Audio URL: " + audio_url)
    print("Destination: " + video_output_path)

    tmp_dir = "/tmp/reddit-video-downloader"
    os.system("mkdir " + tmp_dir)

    video_temp_path = tmp_dir + "/video.mp4"
    audio_temp_path = tmp_dir + "/audio.mp4"

    os.system("curl -o " + video_temp_path + " {}".format(video_url))
    os.system("curl -o " + audio_temp_path + " {}".format(audio_url))

    os.system("ffmpeg -y -i " + video_temp_path + " -i " + audio_temp_path + " -c:v copy -c:a copy '" + video_output_path + "'")

def main():
    url = sys.argv[1]
    redditDownloader(url)

main()
