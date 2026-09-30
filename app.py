from flask import Flask, render_template, request
from urllib.parse import quote_plus

app = Flask(__name__)

# --------------------------------
# VIRAT KOHLI CENTURY RECORDS
# --------------------------------
# Sample records only.
# Add additional verified records as needed.

centuries_data = [
    {
        "format": "ODI",
        "score": "183",
        "opponent": "Pakistan",
        "venue": "Sher-e-Bangla Stadium, Dhaka",
        "date": "2012-03-18"
    },
    {
        "format": "Test",
        "score": "254*",
        "opponent": "South Africa",
        "venue": "MCA Stadium, Pune",
        "date": "2019-10-10"
    },
    {
        "format": "T20I",
        "score": "122*",
        "opponent": "Afghanistan",
        "venue": "Dubai International Stadium",
        "date": "2022-09-08"
    }
]


# --------------------------------
# YOUTUBE VIDEO DATA
# --------------------------------

videos_data = [
    {
        "title": "Virat Kohli - ICC Shot of the Century",
        "category": "Batting Highlights",
        "video_id": "HW6umBCDv9c",
        "search": "Virat Kohli ICC Shot of the Century"
    },
    {
        "title": "Virat Kohli 103* vs Bangladesh",
        "category": "World Cup",
        "video_id": "A8CeBfu37ok",
        "search": "Virat Kohli 103 Bangladesh World Cup 2023"
    },
    {
        "title": "Virat Kohli ODI Century Highlights",
        "category": "Centuries",
        "video_id": None,
        "search": "Virat Kohli ODI century highlights"
    },
    {
        "title": "Virat Kohli Test Batting",
        "category": "Test Cricket",
        "video_id": None,
        "search": "Virat Kohli Test batting highlights"
    },
    {
        "title": "Virat Kohli IPL Highlights",
        "category": "IPL",
        "video_id": None,
        "search": "Virat Kohli IPL batting highlights"
    },
    {
        "title": "Virat Kohli Interviews",
        "category": "Interviews",
        "video_id": None,
        "search": "Virat Kohli interview"
    },
    {
        "title": "Virat Kohli Best Innings",
        "category": "Best Innings",
        "video_id": None,
        "search": "Virat Kohli best innings"
    },
    {
        "title": "Virat Kohli Cover Drives",
        "category": "Batting Skills",
        "video_id": None,
        "search": "Virat Kohli cover drive highlights"
    },
    {
        "title": "Virat Kohli World Cup Moments",
        "category": "World Cup",
        "video_id": None,
        "search": "Virat Kohli world cup moments"
    }
]


# --------------------------------
# HOME PAGE
# --------------------------------

@app.route("/")
def home():

    formats = ["Test", "ODI", "T20I"]

    summary = {
        fmt: sum(
            1 for item in centuries_data
            if item["format"] == fmt
        )
        for fmt in formats
    }

    return render_template(
        "index.html",
        total=len(centuries_data),
        formats=summary
    )


# --------------------------------
# BIOGRAPHY PAGE
# --------------------------------

@app.route("/bio")
def bio():

    return render_template("bio.html")


# --------------------------------
# RECORDS PAGE
# --------------------------------

@app.route("/records")
def records():

    summary = []

    for fmt in ["Test", "ODI", "T20I"]:

        entries = [
            item for item in centuries_data
            if item["format"] == fmt
        ]

        highest = max(
            (
                int(item["score"].replace("*", ""))
                for item in entries
            ),
            default=0
        )

        summary.append({
            "format": fmt,
            "centuries": len(entries),
            "highest_score": highest
        })

    return render_template(
        "records.html",
        records=summary
    )


# --------------------------------
# CENTURIES PAGE
# --------------------------------

@app.route("/centuries")
def centuries():

    selected_format = request.args.get(
        "format", "All"
    )

    if selected_format == "All":
        data = centuries_data
    else:
        data = [
            item for item in centuries_data
            if item["format"] == selected_format
        ]

    data = sorted(
        data,
        key=lambda item: item["date"],
        reverse=True
    )

    return render_template(
        "centuries.html",
        centuries=data,
        selected_format=selected_format
    )


# --------------------------------
# YOUTUBE VIDEOS PAGE
# --------------------------------

@app.route("/videos")
def videos():

    search = request.args.get("q", "").strip()

    if search:
        filtered_videos = [
            video for video in videos_data
            if search.lower() in (
                video["title"] + " " +
                video["category"] + " " +
                video["search"]
            ).lower()
        ]
    else:
        filtered_videos = videos_data

    video_list = []

    for video in filtered_videos:

        item = video.copy()

        if item["video_id"]:
            item["youtube_url"] = (
                "https://www.youtube.com/watch?v="
                + item["video_id"]
            )
        else:
            item["youtube_url"] = (
                "https://www.youtube.com/results?search_query="
                + quote_plus(item["search"])
            )

        video_list.append(item)

    return render_template(
        "videos.html",
        videos=video_list,
        search=search
    )


# --------------------------------
# RUN APPLICATION
# --------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

