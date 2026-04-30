# YouTube Analytics Dashboard

## Overview

This project is a web-based YouTube Analytics Dashboard built using Streamlit. It uses the YouTube Data API v3 to fetch and analyze channel and video-level data. The application provides interactive visualizations and insights into channel performance.

---

## Features

* Displays channel statistics including total subscribers, total views, and number of videos
* Fetches recent videos from a given YouTube channel
* Calculates and visualizes engagement rate (likes per view)
* Interactive filtering options:

  * Search videos by title
  * Sort by views, likes, or engagement rate
  * Select number of top videos
* Visualizations:

  * Bar chart for video views
  * Bar chart for likes
  * Line chart for engagement rate
  * Line chart for estimated subscriber growth
* Data export functionality (download as CSV)
* Handles edge cases such as missing likes data and limited video availability

---

## Technologies Used

* Python
* Streamlit
* YouTube Data API v3
* Pandas
* NumPy

---

## Project Structure

```text
youtube-analytics-dashboard/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/youtube-analytics-dashboard.git
cd youtube-analytics-dashboard
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your YouTube API key in `app.py`:

```python
API_KEY = "YOUR_API_KEY"
```

4. Run the application:

```bash
streamlit run app.py
```

---

## Usage

1. Enter a valid YouTube Channel ID in the input field
2. The dashboard will automatically fetch and display:

   * Channel statistics
   * Video data
   * Charts and insights
3. Use sidebar filters to refine results

---

## Limitations

* Watch time and audience retention data are not available through the YouTube Data API
* Subscriber growth is estimated for visualization purposes
* Data depends on availability and limitations of the YouTube API

---

## Future Improvements

* Implement pagination to fetch more videos
* Integrate YouTube Analytics API for advanced metrics
* Improve UI/UX design and layout
* Add caching for faster performance

---

## Conclusion

This project demonstrates how APIs can be used to collect real-time data and build interactive dashboards. It highlights data processing, visualization, and handling of real-world API limitations.

---

## Author

Nikunj Sinha
