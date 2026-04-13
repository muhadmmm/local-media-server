# 🎬 Local Media Server

Lightweight Flask-based local media server with fast video streaming and instant seeking support over LAN.

---

## 🚀 Features

* 📡 Stream videos over local network (WiFi/LAN)
* ⏩ Instant seeking (HTTP Range Requests)
* ⚡ Fast and minimal single-file backend (`app.py`)
* 🖼️ Automatic thumbnail generation
* 📱 Works on mobile and desktop browsers

---

## 🛠️ Requirements

* Python 3.x
* Flask

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/muhadmmm/local-media-server.git
cd local-media-server
```

### 2. (Optional) Create virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Server

```bash
python app.py
```

---

## 🌐 Access

* On your PC:

```
http://127.0.0.1:8000
```

* On your mobile (same WiFi):

```
http://YOUR-IP:8000
```

---

## 📁 Project Structure

```
app.py        → Main server (backend + UI)
```

---

## 🖼️ Thumbnails

* The `thumps/` folder is **automatically created**
* Thumbnails are generated during runtime
* This folder is not included in the repository

---

## ⚙️ How It Works

* Flask serves video files over HTTP
* Uses **HTTP Range Requests** for smooth streaming and instant seeking
* UI (HTML, CSS, JS) is embedded inside `app.py`

---

## ⚠️ Notes

* Designed for **local network use only**
* No authentication or security implemented
* Not intended for public deployment

---

## 🚧 Future Improvements

* Better UI (grid layout)
* Authentication system
* Upload support
* Separate frontend (HTML/CSS/JS files)

---

## 📄 License

MIT License
