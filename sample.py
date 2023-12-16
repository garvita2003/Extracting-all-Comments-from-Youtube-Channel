# import the libraries
# for interacting with Google APIs
import googleapiclient.discovery
# to store the output - {comments, replies} in json file
import json
# to format the output properly in a clean manner use pprint
from pprint import pprint

CHANNEL_ID = "REPLACE_ME_WITH_CHANNEL_ID_BY_USER"  # channel id user input

def build_youtube(API_KEY): # building youtube data api
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY)
    return youtube

youtube = build_youtube("REPLACE_ME_WITH_API_KEY") # api key of the user creted from the google cloud platform credentials

# search youtube data api
request = youtube.search().list(
    part="snippet",
    type="video",
    channelId="REPLACE_ME_WITH_CHANNEL_ID_BY_USER", # channel id of the user provided video
    maxResults=50
)
response = request.execute()

# to store the outputs in a list
videos_ids = [] # to store the number of videos and their id in a provided channel
comments=[] # to store all the comments in that channel
comment_reply=[] # to store all the replies to the comment in the channel

for item in response['items']:
    title = item['snippet']['title']
    videoId = item['id']['videoId']
    videos_ids.append(videoId)

    # comments youtube data api
    request = youtube.commentThreads().list(
        part="snippet, replies",
        videoId=videoId,
        maxResults=50
    )
    response = request.execute()
    for item in response["items"]:
        print("Comments: ")
        comment = item["snippet"]["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]
        comment_text = comment["snippet"]["textDisplay"]
        date_time = comment["snippet"]["publishedAt"]
        comments.append(f"Video Id: {videoId}")
        comments.append(f"Author Name: {author}")
        comments.append(f"Comment: {comment_text}")
        comments.append(f"Date and Time: {date_time}")
        comments.append(" ")

        # adding or writing to the comment json file the output fetched for comments
        with open('all_comments.json', 'w', encoding='utf-8') as f:
            json.dump(comments, f, indent = 4)
        pprint(author)
        pprint(comment_text)
        pprint(date_time)

        # if replies exits then execute the following commands
        if "replies" in item:
            print("Replies: ")
            for reply_item in item["replies"]["comments"]:
                reply = reply_item["snippet"]["textDisplay"]
                replier = reply_item["snippet"]["authorDisplayName"]
                duration = reply_item["snippet"]["publishedAt"]
                comment_reply.append(f"Video Id: {videoId}")
                comment_reply.append(f"Replier Name: {replier}")
                comment_reply.append(f"Reply: {reply}")
                comment_reply.append(f"Date and Time: {duration}")
                comment_reply.append(" ")

                # adding or writing to the reply comment json file the output fetched for replies
                with open('all_replies.json', 'w', encoding='utf-8') as f:
                    json.dump(comment_reply, f, indent=4)
                pprint(reply)
                pprint(replier)
                pprint(duration)
