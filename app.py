from flask import Flask, send_from_directory, render_template_string
import os
import cv2


app = Flask(__name__)

FOLDER = "<your-media-path>" #replace with your path
THUMB_FOLDER = "thumbs"

os.makedirs(FOLDER, exist_ok=True)
os.makedirs(THUMB_FOLDER, exist_ok=True)

# -------------------------
# 🎬 Thumbnail Generator
# -------------------------
def generate_thumbnail(video_path, thumb_path):
    try:
        if os.path.exists(thumb_path):
            return

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("❌ Cannot open:", video_path)
            return

        # Get total frames
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if total_frames == 0:
            print("❌ No frames:", video_path)
            return

        # Take frame at ~20% of video
        frame_no = int(total_frames * 0.2)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)

        success, frame = cap.read()

        if success and frame is not None:
            cv2.imwrite(thumb_path, frame)
        else:
            print("❌ Frame read failed:", video_path)

        cap.release()

    except Exception as e:
        print("Thumbnail error:", e)


# -------------------------
# 📂 Category Detection
# -------------------------
def get_category(name):
    name = name.lower()

    if "malayalam" in name:
        return "Malayalam"
    elif "anime" in name:
        return "Anime"
    elif "hindi" in name :
        return "Hindi"
    else:
        return "English"


# -------------------------
# 🏠 Home Page
# -------------------------
@app.route("/")
def index():
    files = os.listdir(FOLDER)

    categories = {"Malayalam": [], "English": [], "Anime": [], "Hindi": []}

    for file in files:
        if file.endswith((".mp4", ".mkv", ".avi")):

            video_path = os.path.join(FOLDER, file)
            thumb_path = os.path.join(THUMB_FOLDER, file + ".jpg")

            generate_thumbnail(video_path, thumb_path)

            cat = get_category(file)

            categories[cat].append({
                "name": file,
                "thumb": "/thumbs/" + file + ".jpg"
            })

    return render_template_string(HOME_HTML, categories=categories)


# -------------------------
# ▶ Player Page
# -------------------------
@app.route("/watch/<filename>")
def watch(filename):
    files = [f for f in os.listdir(FOLDER) if f.endswith((".mp4", ".mkv", ".avi"))]

    return render_template_string(PLAYER_HTML, file=filename, files=files)


# -------------------------
# 📁 Serve files
# -------------------------
@app.route("/files/<filename>")
def files(filename):
    return send_from_directory(FOLDER, filename)


# -------------------------
# 🖼️ Serve thumbnails
# -------------------------
@app.route("/thumbs/<filename>")
def thumbs(filename):
    return send_from_directory(THUMB_FOLDER, filename)


# -------------------------
# 🎨 HOME UI (Netflix style)
# -------------------------
HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
:root {
  --bg: #0f0f0f;
  --card: #1c1c1c;
  --text: #fff;
  --accent: #00e5ff;
}

.light {
  --bg: #f5f5f5;
  --card: #fff;
  --text: #111;
  --accent: #0077ff;
}

body {
  margin: 0;
  font-family: system-ui;
  background: var(--bg);
  color: var(--text);
}

.header {
  display: flex;
  justify-content: space-between;
  padding: 15px;
}

.row {
  display: flex;
  overflow-x: auto;
  padding: 10px;
}

.card {
  min-width: 140px;
  margin-right: 10px;
  background: var(--card);
  border-radius: 10px;
  padding: 8px;
}

.thumb {
  width: 100%;
  height: 90px;
  object-fit: cover;
  border-radius: 6px;
}

.name {
  font-size: 12px;
  height: 30px;
  overflow: hidden;
}

a {
  color: var(--accent);
  text-decoration: none;
}

h2 {
  margin-left: 10px;
}
</style>
</head>

<body>

<div class="header">
  <b>🎬 Media Server</b>
  <button onclick="toggleTheme()">🌓</button>
</div>

{% for cat, items in categories.items() %}
<h2>{{cat}}</h2>
<div class="row">
  {% for item in items %}
    <div class="card">
      <img src="{{item.thumb}}" class="thumb">
      <div class="name">{{item.name}}</div>
      <a href="/watch/{{item.name}}">▶ Play</a>
    </div>
  {% endfor %}
</div>
{% endfor %}

<script>
function toggleTheme() {
  document.body.classList.toggle("light");
}
</script>

</body>
</html>
"""


# -------------------------
# ▶ PLAYER UI
# -------------------------
PLAYER_HTML = """
<!DOCTYPE html>
<html>
<body style="margin:0;background:black;">

<video id="player" controls autoplay style="width:100%;height:100%;">
  <source src="/files/{{file}}">
</video>

<script>
let list = {{files|tojson}};
let current = "{{file}}";

let index = list.indexOf(current);
let video = document.getElementById("player");

video.onended = () => {
    if(index + 1 < list.length){
        window.location = "/watch/" + list[index + 1];
    }
};
</script>

</body>
</html>
"""


# -------------------------
# 🚀 RUN SERVER
# -------------------------
app.run(host="0.0.0.0", port=8000)
