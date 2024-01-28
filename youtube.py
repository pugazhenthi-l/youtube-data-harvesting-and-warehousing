# YOUTUBE DATA HARVESTING AND WAREHOUSING SCRIPT

# Setup and Initial Imports
# Imports necessary libraries for API connections, database operations, data manipulation, and creating a web interface.

from googleapiclient.discovery import build
import mysql.connector
import pymysql
import pymongo
import pandas as pd
import re
from datetime import datetime
import streamlit as st
import numpy as np
from PIL import Image

# YouTube API Connection
# Establishes a connection to the YouTube API using a developer key.
def api_connect():
    api_id="AIzaSyCkUV169hHVuT0jd8kmaKvDsQu8yWARM5w"
    api_service_name="youtube"
    api_version="v3"

# `build` function from `googleapiclient.discovery` is used to create a YouTube service object.
    youtube=build(api_service_name,api_version,developerKey=api_id)

    return youtube

youtube=api_connect()


# DATA RETRIEVAL FUNCTIONS:

# Fetching Channel Information:
    # Retrieves information about a specific YouTube channel like name, ID, subscriber count, etc.
def get_channel_info(channel_id):
    request=youtube.channels().list(
                            part="snippet,ContentDetails,statistics",
                            id=channel_id
    )
    response=request.execute()

    for i in response['items']:
        data=dict(Channel_Name=i["snippet"]["title"],
                  Channel_Id=i["id"],
                  Subscribers=i["statistics"]["subscriberCount"],
                  Views=i["statistics"]["viewCount"],
                  Total_Videos=i["statistics"]["videoCount"],
                  Channel_Description=i["snippet"]["description"],
                  Playlist_Id=i["contentDetails"]["relatedPlaylists"]["uploads"])
    return data


# Extracting Video IDs:
    # Obtains a list of video IDs from the specified channel's playlist.
def get_video_ids(channel_id):
    video_ids=[]
    response=youtube.channels().list(id=channel_id,
                                    part='ContentDetails').execute()
    playlist_id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    next_page_token=None

    while True:
        response1=youtube.playlistItems().list(
                                            part='snippet',
                                            playlistId=playlist_id,
                                            maxResults=50,
                                            pageToken=next_page_token).execute()
        for i in range(len(response1['items'])):
            video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token=response1.get('nextPageToken')

        if next_page_token is None:
            break
    return video_ids


# Gathering Video Information:
    # Collects detailed information about each video using their IDs.
def get_video_info(video_ids):
    video_data=[]
    for video_id in video_ids:
        request=youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=video_id)
        response=request.execute()

        for item in response["items"]:
            data=dict(Channel_Name=item["snippet"]["channelTitle"],
                    Channel_id=item["snippet"]["channelId"],
                    Video_id=item["id"],
                    Title=item["snippet"]["title"],
                    Tags=item["snippet"].get("tags"),
                    Thumbnail=item["snippet"]["thumbnails"]["default"]["url"],
                    Description=item["snippet"]["localized"].get("description"),
                    Published_Date=item["snippet"]["publishedAt"],
                    Duration=item["contentDetails"]["duration"],
                    Views=item["statistics"].get("viewCount"),
                    Likes=item["statistics"].get("likeCount"),
                    Comments=item["statistics"].get("commentCount"),
                    Favorite_count=item["statistics"]["favoriteCount"],
                    Definition=item["contentDetails"]["definition"],
                    Caption_status=item["contentDetails"]["caption"]
                    )
            video_data.append(data)
    return video_data


# Extracting Comment Data:
    # Gathers comments from specific videos.
def get_comment_info(video_ids):
    comment_data=[]
    try:
        for video_id in video_ids:
            request=youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=50
            )
            response=request.execute()

            for item in response["items"]:
                data=dict(Comment_id=item["snippet"]["topLevelComment"]["id"],
                        Video_id=item["snippet"]["topLevelComment"]["snippet"]["videoId"],
                        Comment_text=item["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                        Comment_author=item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                        Comment_Published=item["snippet"]["topLevelComment"]["snippet"]["publishedAt"])
                
                comment_data.append(data)

    except:
        pass

    return comment_data


# Getting Playlist Details:
    # Fetches details about playlists within a channel.
def get_playlist_details(channel_id):

    next_page_token=None
    playlist_data=[]

    while True:
        request=youtube.playlists().list(
                    part="snippet, contentDetails",
                    channelId=channel_id,
                    maxResults=50,
                    pageToken=next_page_token
        )
        response=request.execute()

        for items in response['items']:
            data=dict(Playlist_id=items["id"],
                    Title=items['snippet']['title'],
                    Channel_id=items['snippet']['channelId'],
                    Channel_name=items['snippet']['channelTitle'],
                    Published_on=items['snippet']['publishedAt'],
                    Video_count=items['contentDetails']['itemCount'])
            
            playlist_data.append(data)

        next_page_token=response.get('nextPageToken')

        if next_page_token is None:
            break

    return playlist_data


# MongoDB Integration:
    # Connects to MongoDB and defines operations for storing YouTube data.
client=pymongo.MongoClient("mongodb://localhost:27017")
db=client["YouTube_data"]


def channel_details(channel_id):
    ch_details=get_channel_info(channel_id)
    pl_details=get_playlist_details(channel_id)
    vi_ids=get_video_ids(channel_id)
    vi_details=get_video_info(vi_ids)
    com_details=get_comment_info(vi_ids)
    
    coll1=db["channel_details"]
    coll1.insert_one({"channel_information":ch_details,"playlist_information":pl_details,
                      "video_information":vi_details,"comment_information":com_details})
    
    return "The data has been successfully imported into MongoDB."

# MYSQL DATABASE OPERATIONS:

#Creating Channels Table:
    # Sets up a MySQL table for storing channel details
def channels_table():

    mydb=pymysql.connect(host="127.0.0.1",
                        user="root",
                        password="root",
                        database="youtube_data")
    cursor=mydb.cursor()

    drop_query='''drop table if exists channels'''
    cursor.execute(drop_query)
    mydb.commit()


    try:
        create_query='''create table if not exists channels(Channel_Name varchar(100), 
                                                            Channel_Id varchar(80) primary key,
                                                            Subscribers bigint,
                                                            Views bigint,
                                                            Total_Videos int,
                                                            Channel_Description text,
                                                            Playlist_Id varchar(80))'''
        cursor.execute(create_query)  
        mydb.commit()

    except:
        print("channel's table already created")


    ch_list=[]

    db=client["YouTube_data"]
    coll1=db["channel_details"]

    for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
        ch_list.append(ch_data["channel_information"])

    df=pd.DataFrame(ch_list)    


    for index,row in df.iterrows():
        insert_query='''insert into channels(Channel_Name,
                                            Channel_Id,
                                            Subscribers,
                                            Views,
                                            Total_Videos,
                                            Channel_Description,
                                            Playlist_Id)
                                            
                                            values(%s,%s,%s,%s,%s,%s,%s)'''
        values=(row["Channel_Name"],
                row["Channel_Id"],
                row["Subscribers"],
                row["Views"],
                row["Total_Videos"],
                row["Channel_Description"],
                row["Playlist_Id"])
        
        try:
            cursor.execute(insert_query,values)
            mydb.commit()

        except:
            print("Channels values are already inserted")


#Creating Playlists Table:
    # Creates a MySQL table for playlist information.

def playlists_table():

    mydb=pymysql.connect(host="127.0.0.1",
                    user="root",
                    password="root",
                    database="youtube_data")
    cursor=mydb.cursor()

    drop_query='''drop table if exists playlists'''
    cursor.execute(drop_query)
    mydb.commit()

    create_query='''create table if not exists playlists(   Playlist_id varchar(100) primary key, 
                                                            Title varchar(100),
                                                            Channel_id varchar(100),
                                                            Channel_name varchar(100),
                                                            Published_on datetime,
                                                            Video_count int)'''

    cursor.execute(create_query)  
    mydb.commit()

    pl_list=[]

    db=client["YouTube_data"]
    coll1=db["channel_details"]

    for pl_data in coll1.find({},{"_id":0,"playlist_information":1}):
        for i in range(len(pl_data["playlist_information"])):
            pl_list.append(pl_data["playlist_information"][i])

    df1=pd.DataFrame(pl_list)

    for index, row in df1.iterrows():
        insert_query = '''insert into playlists(Playlist_id,
                                                Title,
                                                Channel_id,
                                                Channel_name,
                                                Published_on,
                                                Video_count)
                        values(%s,%s,%s,%s,%s,%s)'''

        # Convert the 'Published_on' value to the correct datetime format
        published_on = datetime.strptime(row["Published_on"], "%Y-%m-%dT%H:%M:%SZ")

        values = (row["Playlist_id"],
                row["Title"],
                row["Channel_id"],
                row["Channel_name"],
                published_on,  # Use the converted datetime value
                row["Video_count"])

        cursor.execute(insert_query, values)
        mydb.commit()


# Creating Videos Table:
    # Establishes a MySQL table for video details.
def videos_table():
    mydb=pymysql.connect(host="127.0.0.1",
                    user="root",
                    password="root",
                    database="youtube_data")
    cursor=mydb.cursor()

    drop_query='''drop table if exists videos'''
    cursor.execute(drop_query)
    mydb.commit()

    create_query='''create table if not exists videos(Channel_Name varchar(100),
                                                    Channel_id varchar(100),
                                                    Video_id varchar(50) primary key,
                                                    Title varchar(200),
                                                    Tags text,
                                                    Thumbnail varchar(100),
                                                    Description text,
                                                    Published_Date datetime,
                                                    Duration time,
                                                    Views bigint,
                                                    Likes bigint,
                                                    Comments int,
                                                    Favorite_count int,
                                                    Definition varchar(10),
                                                    Caption_status varchar(10)
                                                    )'''

    cursor.execute(create_query)
    mydb.commit()


    vi_list=[]

    db=client["YouTube_data"]
    coll1=db["channel_details"]

    for vi_data in coll1.find({},{"_id":0,"video_information":1}):
            for i in range(len(vi_data["video_information"])):
                    vi_list.append(vi_data["video_information"][i])

    df2=pd.DataFrame(vi_list)



    def convert_duration(duration):
            """Convert ISO 8601 duration format to HH:MM:SS format."""
            match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration)
            hours, minutes, seconds = 0, 0, 0
            if match:
                    hours = int(match.group(1)[:-1]) if match.group(1) else 0
                    minutes = int(match.group(2)[:-1]) if match.group(2) else 0
                    seconds = int(match.group(3)[:-1]) if match.group(3) else 0
            return f"{hours:02}:{minutes:02}:{seconds:02}"

    # Assuming 'df2' is your DataFrame and 'cursor' and 'mydb' are your database cursor and connection objects

    for index, row in df2.iterrows():
            # Convert Tags list to a string
            tags_str = ','.join(row["Tags"]) if isinstance(row["Tags"], list) else row["Tags"]
            
            # Convert the 'Published_on' value to the correct datetime format
            published_date = datetime.strptime(row["Published_Date"], "%Y-%m-%dT%H:%M:%SZ")

            # Convert the 'Duration' value to the correct time format
            duration_str = convert_duration(row["Duration"])

            insert_query = '''INSERT INTO videos (
                                    Channel_Name,
                                    Channel_id,
                                    Video_id,
                                    Title,
                                    Tags,
                                    Thumbnail,
                                    Description,
                                    Published_Date,
                                    Duration,
                                    Views,
                                    Likes,
                                    Comments,
                                    Favorite_count,
                                    Definition,
                                    Caption_status)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

            values = (row["Channel_Name"],
                    row["Channel_id"],
                    row["Video_id"],
                    row["Title"],
                    tags_str,
                    row["Thumbnail"],
                    row["Description"],
                    published_date,
                    duration_str,
                    row["Views"],
                    row["Likes"],
                    row["Comments"],
                    row["Favorite_count"],
                    row["Definition"],
                    row["Caption_status"])

            cursor.execute(insert_query, values)
            mydb.commit()


#Creating Comments Table:
    # Sets up a MySQL table for comments data.
def comments_table():

    mydb=pymysql.connect(host="127.0.0.1",
                    user="root",
                    password="root",
                    database="youtube_data")
    cursor=mydb.cursor()

    drop_query='''drop table if exists comments'''
    cursor.execute(drop_query)
    mydb.commit()

    create_query='''create table if not exists comments(Comment_id varchar(100) primary key,
                                                        Video_id varchar(100),
                                                        Comment_text text,
                                                        Comment_author varchar(100),
                                                        Comment_Published datetime)'''
    

    cursor.execute(create_query)  
    mydb.commit()


    cmt_list=[]

    db=client["YouTube_data"]
    coll1=db["channel_details"]

    for cmt_data in coll1.find({},{"_id":0,"comment_information":1}):
        for i in range(len(cmt_data["comment_information"])):
            cmt_list.append(cmt_data["comment_information"][i])

    df3=pd.DataFrame(cmt_list)

    for index, row in df3.iterrows():
        insert_query = '''insert into comments(Comment_id,
                                                Video_id,
                                                Comment_text,
                                                Comment_author,
                                                Comment_Published)
                        values(%s,%s,%s,%s,%s)'''

        # Convert the 'Published_on' value to the correct datetime format
        published_on = datetime.strptime(row["Comment_Published"], "%Y-%m-%dT%H:%M:%SZ")

        values = (row["Comment_id"],
                row["Video_id"],
                row["Comment_text"],
                row["Comment_author"],
                published_on)  # Use the converted datetime value

        cursor.execute(insert_query, values)
        mydb.commit()


# Function to Create Database Tables
def tables():
    channels_table()
    playlists_table()
    videos_table()
    comments_table()

    return "SQL table creation: Done    "


# Retrieves channel information from the "channel_details" collection in MongoDB, converts it into a DataFrame.
def show_channels_tables():
    ch_list=[]

    db=client["YouTube_data"]
    coll1=db["channel_details"]

    for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
        ch_list.append(ch_data["channel_information"])

    df=st.dataframe(ch_list)  

    return df


# Retrieves playlist information from the "channel_details" collection in MongoDB, converts it into a DataFrame.
def show_playlists_tables():
    pl_list=[]

    db=client["YouTube_data"]
    coll1=db["channel_details"]

    for pl_data in coll1.find({},{"_id":0,"playlist_information":1}):
        for i in range(len(pl_data["playlist_information"])):
            pl_list.append(pl_data["playlist_information"][i])

    df1=st.dataframe(pl_list)

    return df1


# Retrieves video information from the "channel_details" collection in MongoDB, converts it into a DataFrame.
def show_videos_tables():
    vi_list=[]

    db=client["YouTube_data"]
    coll1=db["channel_details"]

    for vi_data in coll1.find({},{"_id":0,"video_information":1}):
            for i in range(len(vi_data["video_information"])):
                    vi_list.append(vi_data["video_information"][i])

    df2=st.dataframe(vi_list)

    return df2


# Retrieves comment information from the "channel_details" collection in MongoDB, converts it into a DataFrame.
def show_comments_tables():
    cmt_list=[]

    db=client["YouTube_data"]
    coll1=db["channel_details"]

    for cmt_data in coll1.find({},{"_id":0,"comment_information":1}):
        for i in range(len(cmt_data["comment_information"])):
            cmt_list.append(cmt_data["comment_information"][i])

    df3=st.dataframe(cmt_list)

    return df3


#STREAMLIT WEB INTERFACE:
    # Utilizes Streamlit to create a user-friendly web interface for data collection and visualization.

# Set page configuration
st.set_page_config(layout="wide")

# Column layout for logos
col1, col2, col3 = st.columns([1,6,1])

# Load and display YouTube logo
with col1:
    image = Image.open("guvi_logo.png")

    new_size = (100, 40) 
    resized_image = image.resize(new_size)
    st.image(resized_image)

# Load and display YouTube logo
with col3:
    image = Image.open("youtube_logo.png")

    new_size = (100, 40)
    resized_image = image.resize(new_size)
    st.image(resized_image)


# Display the main header: Using Markdown with HTML for center alignment
st.markdown("<h1 style='text-align: center;'>YouTube Data Harvesting & Warehousing</h1>", unsafe_allow_html=True)
st.markdown("##")

# Database connection
mydb=pymysql.connect(host="127.0.0.1",
                user="root",
                password="root",
                database="youtube_data")
cursor=mydb.cursor()

# Data display section
col1, col2, col3 = st.columns([2, 3, 2])

with col2:

    with st.container():  
        query1='''SELECT Channel_Name, Subscribers, Views, Total_Videos FROM channels; '''
        cursor.execute(query1)
        mydb.commit()
        t1=cursor.fetchall()
        st.write(pd.DataFrame(t1, columns=["Channel Name","Subscribers", "Total Views", "Total Videos"]))

# Channel ID input
channel_id = st.text_input(("Enter the Channel ID here 👇🏻"), key="channel_id")

# Data import and migration buttons
if st.button("Click and Import data to MangoDB",help="The data of the YouTube channel will be collected and stored in MangoDB"):
    ch_ids=[]
    db=client["YouTube_data"]
    coll1=db["channel_details"]
    for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
        ch_ids.append(ch_data["channel_information"]["Channel_Id"])

    if channel_id in ch_ids:
        st.success("Provide a different channel ID: the current one has existing details")

    else:
        insert=channel_details(channel_id)
        st.success(insert)

if st.button("Click and add the data to MySQL",help="The extracted data will be migrated to SQL database"):
    Table=tables()
    st.success(Table)

# Data overview with tabs
st.markdown("<h2 style='text-align: center;'>🗄 Overview of Data Set</h2>", unsafe_allow_html=True, help="Select a tab to view detailed data on Channels, Playlists, Videos, or Comments.")

with st.container():
    tab0, tab1, tab2, tab3, tab4 = st.tabs(["❄️","CHANNELS", "PLAYLISTS", "VIDEOS", "COMMENTS"])

    with tab0:
        st.caption("👆🏼Select a tab to view detailed data")

    with tab1:
        st.header("CHANNELS")
        show_channels_tables()

    with tab2:
        st.header("PLAYLISTS")
        show_playlists_tables()

    with tab3:
        st.header("VIDEOS")
        show_videos_tables()

    with tab4:
        st.header("COMMENTS")
        show_comments_tables()


    #SQL Queries for Analysis:
        # Provides a selection of SQL queries for data analysis and displays the results in the Streamlit interface.

    question=st.selectbox("SELECT YOUR QUESTION",("",
                                                "1. What are the names of all the videos and their corresponding channels?",
                                                "2. Which channels have the most number of videos, and how many videos do they have?",
                                                "3. What are the top 10 most viewed videos and their respective channels?",
                                                "4. How many comments were made on each video, and what are their corresponding video names?",
                                                "5. Which videos have the highest number of likes, and what are their corresponding channel names?",
                                                "6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
                                                "7. What is the total number of views for each channel, and what are their corresponding channel names?",
                                                "8. What are the names of all the channels that have published videos in the year 2022?",
                                                "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                                                "10. Which videos have the highest number of comments, and what are their corresponding channel names?"))


    if question=="1. What are the names of all the videos and their corresponding channels?":
        query1='''select title as videos, channel_name as channelname from videos '''
        cursor.execute(query1)
        mydb.commit()
        t1=cursor.fetchall()
        st.write(pd.DataFrame(t1, columns=["video title","channel name"]))

    elif question=="2. Which channels have the most number of videos, and how many videos do they have?":
        query2=query2='''select channel_name as channelname, Total_Videos as totalvideos from channels order by Total_Videos desc'''
        cursor.execute(query2)
        mydb.commit()
        t2=cursor.fetchall()
        st.write(pd.DataFrame(t2, columns=["channel name","total videos"]))


    elif question=="3. What are the top 10 most viewed videos and their respective channels?":
        query3='''select channel_name as channelname, Title as videoname, views from videos order by views desc limit 10'''
        cursor.execute(query3)
        mydb.commit()
        t3=cursor.fetchall()
        st.write(pd.DataFrame(t3, columns=["channel name","video name","views"]))


    elif question=="4. How many comments were made on each video, and what are their corresponding video names?":
        query4='''select Title as videoname, Comments from videos where Comments is not null order by Comments desc'''
        cursor.execute(query4)
        mydb.commit()
        t4=cursor.fetchall()
        st.write(pd.DataFrame(t4, columns=["video name","comment count"]))


    elif question=="5. Which videos have the highest number of likes, and what are their corresponding channel names?":
        query5='''select channel_name as channelname, Title as videoname, likes from videos where likes is not null order by likes desc'''
        cursor.execute(query5)
        mydb.commit()
        t5=cursor.fetchall()
        st.write(pd.DataFrame(t5, columns=["channel name","video name","likes count"]))


    elif question=="6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?":
        query6='''select channel_name as channelname, Title as videoname, likes from videos where likes is not null'''
        cursor.execute(query6)
        mydb.commit()
        t6=cursor.fetchall()
        st.write(pd.DataFrame(t6, columns=["channel name","video name","likes count"]))


    elif question=="7. What is the total number of views for each channel, and what are their corresponding channel names?":
        query7='''select channel_name as channelname, views from channels'''
        cursor.execute(query7)
        mydb.commit()
        t7=cursor.fetchall()
        st.write(pd.DataFrame(t7, columns=["channel name","total views"]))


    elif question=="8. What are the names of all the channels that have published videos in the year 2022?":
        query8='''select distinct(channel_name) as channelname from videos where year(Published_Date)=2022'''
        cursor.execute(query8)
        mydb.commit()
        t8=cursor.fetchall()
        st.write(pd.DataFrame(t8, columns=["channel name"]))


    elif question=="9. What is the average duration of all videos in each channel, and what are their corresponding channel names?":
        query9='''SELECT Channel_Name, avg(Duration) as average_duration FROM youtube_data.videos group by Channel_Name'''
        cursor.execute(query9)
        mydb.commit()
        t9=cursor.fetchall()
        st.write(pd.DataFrame(t9, columns=["channel name", "average duration"]))


    elif question=="10. Which videos have the highest number of comments, and what are their corresponding channel names?":
        query10='''SELECT Channel_Name, Title, Comments FROM youtube_data.videos order by comments desc'''
        cursor.execute(query10)
        mydb.commit()
        t10=cursor.fetchall()
        st.write(pd.DataFrame(t10, columns=["channel name", "video name", "total comments"]))
