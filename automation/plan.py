"""List posts that are due to be scheduled now. Usage: python3 plan.py [fb|tk]
fb: posts from now until now+28 days (Meta allows ~29 days ahead).  tk: posts in the next 30 days (TikTok also caps the queue at 30 posts)."""
import json, sys, os, datetime as dt
H = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(H, 'schedule.json')))
SAST = dt.timezone(dt.timedelta(hours=2)); now = dt.datetime.now(SAST)
days = 28.7 if (sys.argv[1:] or ['fb'])[0] == 'fb' else 29
for i, e in enumerate(E):
    t = dt.datetime.fromisoformat(e['date'] + 'T' + e['time']).replace(tzinfo=SAST)
    if now + dt.timedelta(minutes=30) < t <= now + dt.timedelta(days=days):
        print(i, e['date'], e['time'], e['id'], e['aud'], (e['tk'][:60]))
