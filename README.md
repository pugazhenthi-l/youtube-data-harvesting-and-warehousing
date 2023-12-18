# youtube-data-harvesting-and-warehousing

## Overview:
This Python script is designed for extracting, processing, and managing data from YouTube using the YouTube API. 
It includes functionalities for connecting to the YouTube API, retrieving channel and video information, and managing data in databases.

## Features:
YouTube API Integration: Connects to the YouTube API to fetch data about channels, videos, and comments.
Database Interaction: Supports operations with MySQL, PyMySQL, and MongoDB for data storage and management.
Data Processing: Utilizes Pandas for efficient data manipulation and analysis.
Web Interface: Includes Streamlit integration for potential web application deployment.
Image Processing: Uses PIL for image-related operations, possibly for thumbnails or other media from YouTube.

## Dependencies:
googleapiclient
mysql.connector
pymysql
pymongo
pandas
datetime
re
streamlit
PIL

## Functions:
api_connect(): Establishes connection to the YouTube API.
get_channel_info(channel_id): Retrieves information about a specified YouTube channel.
get_video_ids(channel_id): Fetches video IDs for a given channel.
get_video_info(video_ids): Gathers information about specific videos.
get_comment_info(video_ids): Extracts comments from specified videos.

## Usage:
API Connection: Set up the YouTube API key and establish a connection.
Data Retrieval: Use provided functions to fetch data about channels, videos, and comments.
Data Storage and Management: Store and manage the retrieved data in MySQL, PyMySQL, or MongoDB databases.
Data Processing and Analysis: Process and analyze the data using Pandas.
Web Interface and Image Processing: Utilize Streamlit for web deployment and PIL for image processing tasks.

## Notes:
Ensure you have a valid YouTube API key before attempting to connect.
Database credentials and configurations need to be set up prior to running database-related operations.
The script may require additional setup for Streamlit if used for web deployment.
