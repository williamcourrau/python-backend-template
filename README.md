# Candidate Filtering CLI – User Guide

This script allows you to **retrieve candidate profiles**, **apply filters**, and **store filtered results** in a MongoDB database.  
It is designed to be **simple, safe, and HR-friendly**, without exposing technical details.

---

## Prerequisites

Before running the script, make sure you have:

- Python **3.11+**
- MongoDB running locally or accessible remotely
- Required Python dependencies installed

### Step 1: Create Virtual Environment

Create and activate a Python virtual environment:

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 2: Install Dependencies

Install required packages:
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Create a `.env` file in the project root directory:
```bash
touch .env
```
Create a `.env` file in the project root directory by copying the example:

**On macOS/Linux:**
```bash
cp .env.example .env
```

**On Windows (Command Prompt):**
```cmd
copy .env.example .env
```

**On Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

Add the following configuration to `.env`:
```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB=candidates
LOG_LEVEL=INFO
```

> **Note:** The `.env.example` file contains template values. Make sure to update them with your actual configuration.

### Step 4: Start MongoDB

Ensure MongoDB is running:

**Using MongoDB locally:**
```bash
mongod
```


## Running Commands

All commands are executed from the project root directory.
```bash
python -m app.main  [options]
```

## Available Commands

### 1. Get All Candidates

Retrieves candidates from the external data source and prints a readable summary for each one.
```bash
python -m app.main get-candidates
```

**What this does:**
- Connects to the candidate data source
- Displays candidate experience history and gaps
- Does not store data in the database

---

### 2. Filter Candidates (Main Use Case)

Filters candidates based on criteria and saves the results to MongoDB.
```bash
python -m app.main filter-candidates --industry "Real Estate" --skills "general ledger" --min-experience 10
```

#### Supported Filters

| Option | Description |
|--------|-------------|
| `--industry` | Industry to match (case-insensitive) |
| `--skills` | One or more skills (space-separated) |
| `--min-experience` | Minimum years of experience |

> **Note:** You can omit any filter if not needed.

---

## Example Output (User-Friendly)
```
Candidate filtering completed successfully.

Filters applied:
- Industry: Real Estate
- Skills: general ledger
- Minimum experience: 10 years

Results:
- Candidates matched: 3
- Candidates saved: 3
- Candidates skipped: 12
```

> **Privacy:** No candidate names or personal details are shown during filtering.

---

## Where Filtered Data Is Stored

Filtered candidates are saved in MongoDB under:

- **Database:** `candidates`
- **Collection:** `filtered_candidates`

Each candidate is stored idempotently (re-running the command will not create duplicates).

---

__Thanks for reading my code 😊__