# ShowTime — BookMyShow-style Flask App (Step 1)

## Folder Structure

```
bookmyshow/
├── app.py                  ← Flask backend (routes + mock data)
├── requirements.txt        ← Python dependencies
├── README.md               ← This file
└── templates/
    └── index.html          ← Homepage (dark theme, all 5 sections)
```

## Setup & Run

```bash
# 1. Create & activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the development server
python app.py

# 4. Open in browser
#    http://127.0.0.1:5000
```

## What's Included (Step 1)

| Section         | Content                                              |
|-----------------|------------------------------------------------------|
| 🎬 Movies        | 6 cards — poster, rating, timings, book button       |
| 🎭 Live Plays    | 4 cards — artist, venue, date/time, price            |
| 🎪 Live Events   | 4 cards — category, venue, price                     |
| 🏆 Sports        | 4 cards — sport, match, venue, price                 |
| 🎤 Comedy        | 4 cards — comedian, show name, venue, price          |

## API Endpoints (JSON)

```
GET /api/movies
GET /api/plays
GET /api/events
GET /api/sports
GET /api/comedy
```

## Next Steps (Steps 2+)
- Step 2: Movie detail page + seat selection UI
- Step 3: User auth (Flask-Login)
- Step 4: Booking flow + order summary
- Step 5: Admin panel / CMS
- Step 6: Database (SQLAlchemy + SQLite/PostgreSQL)
