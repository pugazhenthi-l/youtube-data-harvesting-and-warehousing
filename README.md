<h1 align="center">YouTube Data Harvesting and Warehousing</h1>

![Alt text](youtube_project.png)


## Problem Statement
The primary objective of this system is to create a robust tool that facilitates the extraction, analysis, and management of data from various YouTube channels. 
This involves fetching comprehensive data such as channel information, video details, and user comments using the YouTube API, and efficiently handling this data through storage, analysis, and migration processes.

## Solution Overview
This Python script is designed for extracting, processing, and managing data from YouTube using the YouTube API. It includes functionalities for connecting to the YouTube API, retrieving channel and video information, and managing data in databases.

## Features
- **YouTube API Integration**: The script interacts with the YouTube API. This is evident from the use of the `build` function with parameters related to the YouTube API service.
- **Database Connectivity**: Supports operations with MySQL, PyMySQL, and MongoDB for data storage and management.
- **Data Processing**:  The script uses `pandas`, a powerful data analysis and manipulation library, indicating that it processes data, possibly YouTube data fetched via the API.
- **Visualization**: The presence of `streamlit` and `PIL` (Python Imaging Library) suggests that the script might be creating visualizations or a web interface to display data.


## Dependencies
- `googleapiclient`
- `mysql.connector`
- `pymysql`
- `pymongo`
- `pandas`
- `datetime`
- `re`
- `streamlit`
- `PIL`

## Functions
- `api_connect()`: Establishes connection to the YouTube API.
- `get_channel_info(channel_id)`: Retrieves information about a specified YouTube channel.
- `get_video_ids(channel_id)`: Fetches video IDs for a given channel.
- `get_video_info(video_ids)`: Gathers information about specific videos.
- `get_comment_info(video_ids)`: Extracts comments from specified videos.

## Usage
1. **API Connection**: Set up the YouTube API key and establish a connection.
2. **Data Retrieval**: Use provided functions to fetch data about channels, videos, and comments.
3. **Data Storage and Management**: Store and manage the retrieved data in MySQL, PyMySQL, or MongoDB databases.
4. **Data Processing and Analysis**: Process and analyze the data using Pandas.
5. **Web Interface and Image Processing**: Utilize Streamlit for web deployment and PIL for image processing tasks.

## Notes
- Ensure you have a valid YouTube API key before attempting to connect.
- Database credentials and configurations need to be set up prior to running database-related operations.
- The script may require additional setup for Streamlit if used for web deployment.

