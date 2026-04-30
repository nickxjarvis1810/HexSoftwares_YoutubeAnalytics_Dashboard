import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
import numpy as np

# ---------------- API KEY ----------------
import os
API_KEY = os.getenv("YOUTUBE_API_KEY") # ENTER YOUR API KEY

youtube = build('youtube', 'v3', developerKey=API_KEY)

# ---------------- FUNCTIONS ----------------
def get_channel_stats(channel_id):
    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    return request.execute()

def get_videos(channel_id):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=30,   # ✅ increased from 10 → 30
        order="date"
    )
    response = request.execute()

    video_ids = []
    for item in response['items']:
        if item['id']['kind'] == "youtube#video":
            video_ids.append(item['id']['videoId'])

    return video_ids

def get_video_details(video_ids):
    request = youtube.videos().list(
        part="statistics,snippet",
        id=",".join(video_ids)
    )
    response = request.execute()
    return response['items']

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "About"])

st.sidebar.markdown("---")
st.sidebar.write("Made by Nikunj")

# ---------------- MAIN ----------------
if page == "Dashboard":

    st.markdown("<h1 style='text-align:center;'>📊 YouTube Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Analyze channel performance in real-time</p>", unsafe_allow_html=True)

    st.markdown("###")

    channel_id = st.text_input("Enter Channel ID")

    if not channel_id:
        st.info("Enter a Channel ID to start analysis")

    if channel_id:
        with st.spinner("Fetching data..."):
            data = get_channel_stats(channel_id)

        stats = data['items'][0]['statistics']
        snippet = data['items'][0]['snippet']

        # ---------------- CHANNEL STATS ----------------
        st.markdown("---")
        st.subheader("📊 Channel Overview")

        col1, col2, col3 = st.columns(3)
        col1.metric("Subscribers", stats['subscriberCount'])
        col2.metric("Views", stats['viewCount'])
        col3.metric("Videos", stats['videoCount'])

        # ---------------- SUBSCRIBER GROWTH ----------------
        st.markdown("---")
        st.subheader("📈 Subscriber Growth (Estimated)")

        subs = int(stats['subscriberCount'])

        days = ["Day 1","Day 2","Day 3","Day 4","Day 5","Day 6","Day 7"]
        growth = np.linspace(subs * 0.9, subs, 7)

        growth_df = pd.DataFrame({
            "Day": days,
            "Subscribers": growth
        })

        st.line_chart(growth_df.set_index("Day"))

        # ---------------- VIDEO DATA ----------------
        video_ids = get_videos(channel_id)
        videos = get_video_details(video_ids)

        data_list = []

        for video in videos:
            title = video['snippet']['title']
            views = int(video['statistics'].get('viewCount', 0))
            likes = int(video['statistics'].get('likeCount', 0))

            engagement = (likes / views) if views != 0 else 0

            data_list.append({
                "Title": title,
                "Views": views,
                "Likes": likes,
                "Engagement Rate": round(engagement, 3)
            })

        df = pd.DataFrame(data_list)

        # ---------------- SIDEBAR FILTERS ----------------
        st.sidebar.header("Filters")

        search = st.sidebar.text_input("Search video")
        if search:
            df = df[df["Title"].str.contains(search, case=False)]

        sort_option = st.sidebar.selectbox(
            "Sort by",
            ["Views", "Likes", "Engagement Rate"]
        )

        df = df.sort_values(by=sort_option, ascending=False)

        # ✅ FIXED SLIDER
        max_videos = len(df)

        if max_videos > 1:
            top_n = st.sidebar.slider(
                "Top N Videos",
                1,
                max_videos,
                min(5, max_videos)
            )
        else:
            top_n = 1
            st.sidebar.warning("Only 1 video available")

        df = df.head(top_n)

        # ---------------- TOP VIDEO ----------------
        if not df.empty:
            top_video = df.iloc[0]
            st.success(f"🔥 Top Video: {top_video['Title']} ({top_video['Views']} views)")

        # ---------------- TABLE ----------------
        st.markdown("---")
        st.subheader("🎥 Top Videos")
        st.dataframe(df)

        # ---------------- CHARTS ----------------
        st.markdown("---")
        st.subheader("📈 Views Chart")

        df["Title"] = df["Title"].apply(lambda x: x[:40] + "..." if len(x) > 40 else x)
        st.bar_chart(df.set_index("Title")["Views"])

        st.markdown("---")
        st.subheader("👍 Likes Chart")

        likes_df = df[df["Likes"] > 0]

        if not likes_df.empty:
            st.bar_chart(likes_df.set_index("Title")["Likes"])
        else:
            st.info("Likes data is not available for these videos.")

        st.markdown("---")
        st.subheader("📊 Engagement Rate")

        eng_df = df[df["Engagement Rate"] > 0]

        if not eng_df.empty:
            st.line_chart(eng_df.set_index("Title")["Engagement Rate"])
        else:
            st.info("Engagement data not available for these videos.")

        st.info("Watch time data is not publicly available via YouTube API. Engagement rate is used as an alternative metric.")

        # ---------------- DOWNLOAD ----------------
        csv = df.to_csv(index=False)
        st.download_button(
            "Download Data",
            csv,
            "youtube_data.csv",
            "text/csv"
        )

# ---------------- ABOUT PAGE ----------------
elif page == "About":
    st.title("About This Project")

    st.write("""
    This YouTube Analytics Dashboard allows users to:
    - Analyze channel statistics
    - View top-performing videos
    - Measure engagement rates
    - Visualize trends using charts

    Built using:
    - Python
    - Streamlit
    - YouTube Data API
    """)