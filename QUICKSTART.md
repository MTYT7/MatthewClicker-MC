# Mathew Clicker Web - Quick Start Guide

## Option 1: Play Online (Easiest)

### Deploy to Render (Free)
1. Go to https://render.com and sign up with GitHub
2. Click "New +" and select "Web Service"
3. Connect your GitHub repo (MTYT7/MatthewClicker-MC)
4. Select the `web-idle-game` branch
5. Fill in:
   - **Name**: mathew-clicker
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. Click "Create Web Service"
7. Wait ~2 minutes and your game will be live at `https://mathew-clicker.onrender.com`

**That's it!** No coding needed. Share the link with friends.

---

## Option 2: Run Locally (If You Want to Test)

### Windows
1. Download and install Python from https://www.python.org/downloads/
2. Open Command Prompt
3. Navigate to the repo folder:
   ```
   cd path/to/MatthewClicker-MC
   ```
4. Run these commands:
   ```
   pip install -r requirements.txt
   python app.py
   ```
5. Open http://localhost:5000 in your browser

### Mac
1. Open Terminal
2. Navigate to the repo folder:
   ```
   cd path/to/MatthewClicker-MC
   ```
3. Run:
   ```
   pip3 install -r requirements.txt
   python3 app.py
   ```
4. Open http://localhost:5000 in your browser

### Linux
```bash
cd path/to/MatthewClicker-MC
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000 in your browser

---

## Game Features

- **Click to earn** Mathew Points
- **Buy upgrades** to increase power
- **Auto-generate** passive income per second
- **Rebirth system** for permanent bonuses
- **Save automatically** every 15 seconds
- **Quest system** for bonus rewards

---

## Troubleshooting

**"pip: command not found"**
- On Mac/Linux, use `pip3` instead of `pip`
- On Windows, make sure Python is installed and in PATH

**Port 5000 already in use**
- Change the last line in `app.py` from `port=5000` to `port=5001`

**Game won't load**
- Make sure you're on the `web-idle-game` branch
- Try a different browser (Chrome, Firefox, Safari)

---

## Next Steps

Once it's running, you can:
1. Test the gameplay
2. Ask for features (daily chests, golden Mathew, rush mode, etc.)
3. Customize colors, names, or upgrade descriptions
4. Share with friends

Enjoy! 🎮
