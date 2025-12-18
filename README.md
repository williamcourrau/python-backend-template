✅ Simple Steps to Run the Script
1️⃣ Create and activate a virtual environment
python -m venv venv


Windows

venv\Scripts\activate


Mac / Linux

source venv/bin/activate

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Start MongoDB

Make sure MongoDB is running locally:

mongodb://localhost:27017


Or via Docker:

docker run -d -p 27017:27017 mongo

4️⃣ Create .env file (project root)
MONGO_URI=mongodb://localhost:27017
MONGO_DB=rankings_db
LOG_LEVEL=INFO

5️⃣ Run Exercise 1 – Load candidates
python -m app.main get-candidates

6️⃣ Run Exercise 2 – Filter candidates
python -m app.main filter-candidates \
  --industry "Real Estate" \
  --skills "general ledger" \
  --min-experience 3

🧪 Other examples

Filter by skills only:

python -m app.main filter-candidates --skills python sql


Filter by experience only:

python -m app.main filter-candidates --min-experience 10

❗ If something fails

Check MongoDB is running

Check .env values

Run with logs:

LOG_LEVEL=DEBUG python -m app.main get-candidates