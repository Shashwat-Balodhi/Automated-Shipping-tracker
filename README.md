# 📦 HMM Booking Info Tracker

This project automates the process of retrieving **Voyage Number** and **Arrival Date** for any HMM booking ID like `SINI25432400` by simulating browser actions.

## ✅ Features

- Accepts natural language prompt like:
  `"Track SINI25432400 on HMM and get voyage and arrival date"`
- Extracts the booking ID
- Fills the HMM website form
- Clicks **Retrieve**
- Extracts the **Vessel/Voyage** and **Arrival Date**
- Stores steps to `steps.json` so they can be **reused** for other IDs

---

## 🧪 Environment Setup

### 🔧 Prerequisites
- Windows 10/11
- Python 3.8 or higher
- Google Chrome (latest version)

### 🐍 Create virtual environment (optional but recommended)
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 📦 Install dependencies
```bash
pip install -r requirements.txt
```

### 💡 Required Python package:
- `undetected-chromedriver`

---

## 🚀 How to Run

### ▶️ First Time (to create steps.json)
```bash
python app.py
```
Then enter:
```
Track SINI25432400 on HMM and get voyage and arrival date
```

### 🔁 Reuse for Future IDs
```bash
python runner.py
```
Then enter:
```
Track SINI25432400 on HMM and get voyage and arrival date
```

You’ll see:
```json
{
  "voyage": "YM MANDATE 0096W",
  "arrival": "2025-03-28 10:38",
  "booking_id": "SINI25881234"
}
```

---

## ⚙️ File Descriptions

| File                | Purpose                                         |
|---------------------|-------------------------------------------------|
| `app.py`            | Main script to record steps and get info        |
| `tracker.py`        | Core logic and persistence step logger          |
| `runner.py`         | Replays saved steps using any future booking ID |
| `steps.json`        | Saved interaction blueprint                     |
| `requirements.txt`  | Required Python packages                        |
| `run.bat`           | One-click launcher                              |

---

## 💬 Notes
- Make sure Chrome is installed and updated.
- If you face SSL or certificate warnings, they're automatically ignored.
- `WinError 6` can be safely ignored (Chrome closes fine).

---

## 📍 Author & Acknowledgment
Created for the AI-based automation assignment for HMM shipping line container tracking.
