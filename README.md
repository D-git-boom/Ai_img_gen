# SYNTHIA - Smart AI Image Generator

SYNTHIA is an AI-powered image generation web application built as a final-year academic project. It allows users to generate images from text prompts, edit existing images using natural language instructions, and manage a personal gallery of generated content. The project is designed to run entirely without a local GPU by leveraging the HuggingFace Inference API for all model inference.

---

## Features

- Text-to-image generation using FLUX.1-schnell via HuggingFace Inference API
- Image-to-image editing using instruct-pix2pix (describe what to change in plain English)
- Prompt expansion engine that automatically enriches short prompts into detailed ones
- Six style presets that modify prompts to match different visual aesthetics
- Keyword-based safety filtering to block inappropriate content before inference
- Before/after comparison view for image edits
- Gallery with grouped edit chains, allowing you to trace the history of an image through multiple edits
- Animated particle background UI with a fake generation stats loader for visual feedback
- No frontend server required — runs directly in the browser by opening `index.html`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Uvicorn |
| Frontend | Vanilla HTML, CSS, JavaScript |
| Database | MongoDB (local instance) |
| AI Inference | HuggingFace Inference API |
| Models | FLUX.1-schnell (text-to-image), instruct-pix2pix (image-to-image) |

---

## Project Structure

```
Ai_img_gen/
├── backend/
│   ├── main.py                  # FastAPI app, all API routes
│   ├── image_generator.py       # HuggingFace API calls, image generation logic
│   ├── prompt_intelligence.py   # Prompt expansion and style modifier logic
│   ├── safety_filter.py         # Keyword-based content filtering
│   ├── database.py              # MongoDB connection and gallery operations
│   └── outputs/                 # Generated images saved here (gitignored)
├── frontend/
│   └── index.html               # Complete frontend, open directly in browser
├── .env                         # API keys (not committed, create manually)
├── .env.example                 # Template showing required environment variables
├── requirements.txt             # Python dependencies
└── start_synthia.sh             # One-click dev startup script (Linux/Ubuntu only)
```

---

## Prerequisites

Before setting up, make sure the following are installed on your machine:

- Python 3.10 or higher
- pip (comes with Python)
- MongoDB Community Edition (local instance)
- A HuggingFace account with a valid User Access Token

---

## Setup Instructions (Windows 11)

### Step 1: Clone the Repository

Open Command Prompt or PowerShell and run:

```bash
git clone https://github.com/D-git-boom/Ai_img_gen.git
cd Ai_img_gen
```

### Step 2: Create and Activate a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` appear at the beginning of your terminal prompt. This confirms the virtual environment is active.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs FastAPI, Uvicorn, pymongo, httpx, Pillow, python-dotenv, and all other required libraries in one shot.

### Step 4: Set Up the Environment File

Create a file named `.env` in the project root (same level as the `backend/` folder). Add the following line:

```
HF_API_KEY=your_huggingface_token_here
```

Replace `your_huggingface_token_here` with your actual HuggingFace User Access Token. You can generate one at https://huggingface.co/settings/tokens. Make sure the token has at least read access.

### Step 5: Start MongoDB

Make sure your local MongoDB instance is running. If you installed MongoDB Community Edition with default settings, it usually starts automatically as a Windows service. You can verify by opening Task Manager and checking for `mongod.exe`, or by running:

```bash
mongosh
```

If it connects, MongoDB is running. If not, start it manually:

```bash
net start MongoDB
```

### Step 6: Run the Backend

```bash
cd backend
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. You should see Uvicorn startup logs in the terminal. Keep this terminal open — closing it stops the server.

### Step 7: Open the Frontend

Navigate to the `frontend/` folder and open `index.html` directly in your browser. No additional server is needed.

```
Ai_img_gen/
└── frontend/
    └── index.html   <-- open this in Chrome or Firefox
```

The app connects to the FastAPI backend running on `http://127.0.0.1:8000` by default.

---

## Setup Instructions (Ubuntu / Linux)

### Step 1: Clone and Navigate

```bash
git clone https://github.com/D-git-boom/Ai_img_gen.git
cd Ai_img_gen
```

### Step 2: Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up the Environment File

Create `.env` in the project root:

```bash
echo "HF_API_KEY=your_huggingface_token_here" > .env
```

### Step 5: Start MongoDB

```bash
sudo systemctl start mongod
```

### Step 6: Run the Backend

```bash
cd backend
uvicorn main:app --reload
```

### Step 7: Open the Frontend

Open `frontend/index.html` directly in your browser, or from the terminal:

```bash
xdg-open frontend/index.html
```

### One-Click Startup (Ubuntu with GNOME only)

A shell script `start_synthia.sh` is included in the project root. It opens VS Code in the project directory and launches the backend in a new terminal window automatically. Make it executable and run it:

```bash
chmod +x start_synthia.sh
./start_synthia.sh
```

---

## Common Issues

**Port 8000 already in use**

This usually happens if a previous Uvicorn process was suspended with Ctrl+Z instead of stopped with Ctrl+C. Find and kill the process:

```bash
# Linux
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**MongoDB connection refused**

Make sure MongoDB is running before starting the backend. The app expects a local MongoDB instance on the default port 27017 with no authentication required.

**HuggingFace API returning errors**

Check that your `HF_API_KEY` in `.env` is valid and has not expired. Regenerate it at https://huggingface.co/settings/tokens if needed. Also note that HuggingFace free tier inference can be slow or temporarily unavailable during peak hours.

**Images not generating, no error shown**

Open your browser's developer console (F12) and check the network tab for failed requests to `http://127.0.0.1:8000`. This usually points to the backend not running or a CORS issue.

---

## Notes

- This project uses the HuggingFace Inference API exclusively. No local GPU is required.
- Generated images are saved to `backend/outputs/` which is gitignored and will not appear in the repository.
- The `.env` file is gitignored. Never commit it. Share API keys privately.
- MongoDB data is stored locally and is also gitignored.

---

## Author

Dharmesh — MIT Final Year Project, Ahmedabad