<h1 align="center">YouTube Data Harvesting and Warehousing</h1>

![Alt text](project_thumbnail_1.png)


This repository contains the source code and documentation for the "YouTube Data Harvesting and Warehousing" project, which is designed to efficiently harvest and warehouse data from YouTube for analytical and business purposes.

## Overview
The project involves extracting data using YouTube's API, storing it in databases, and presenting it through a user-friendly web interface. It aims to provide a comprehensive solution for businesses to leverage YouTube data for market analysis and decision-making.es.

## Features
- **YouTube API Integration**: The script interacts with the YouTube API. This is evident from the use of the `build` function with parameters related to the YouTube API service.
- **Database Connectivity**: Supports operations with MySQL and MongoDB for data storage and management.
- **Data Processing**:  The script uses `pandas`, a powerful data analysis and manipulation library, indicating that it processes data, possibly YouTube data fetched via the API.
- **Visualization**: The presence of `streamlit` for visualizations and a web interface to display data.

## YouTube Video Explanation
For a detailed explanation of this project and a walkthrough of the code, check out our YouTube video. This video is ideal for understanding the project's real-world applications and getting a visual insight into the functionality.
<p align="center">🎥 [Watch the Video Here](https://youtu.be/ebwOZcAo9PA). </p>

## Dependencies
- `googleapiclient`
- `mysql.connector`
- `pymysql`
- `pymongo`
- `pandas`
- `datetime`
- `streamlit`

## Functions
- `api_connect()`: Establishes connection to the YouTube API.
- `get_channel_info(channel_id)`: Retrieves information about a specified YouTube channel.
- `get_video_ids(channel_id)`: Fetches video IDs for a given channel.
- `get_video_info(video_ids)`: Gathers information about specific videos.
- `get_comment_info(video_ids)`: Extracts comments from specified videos.
- `tables()`: Creates database tables of channels, videos, comments and playlist.

## Usage
1. **API Connection**: Set up the YouTube API key and establish a connection.
2. **Data Retrieval**: Use provided functions to fetch data about channels, videos, and comments.
3. **Data Storage and Management**: Store and manage the retrieved data in MySQL and MongoDB databases.
4. **Data Processing and Analysis**: Process and analyze the data using Pandas.
5. **Web Interface and Image Processing**: Utilize Streamlit for web deployment and PIL for image processing tasks.

## Notes
- Ensure you have a valid YouTube API key before attempting to connect.
- Database credentials and configurations need to be set up prior to running database-related operations.
- The script may require additional setup for Streamlit if used for web deployment.

# Project Title

This is an example of adding a hyperlink to a README file on GitHub.

For more information, visit [GitHub's official website](https://github.com).

You can also link to other sections within the README, like [this section](#section-title).

## Section Title

More content here.


