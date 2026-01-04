## What system lets me talk to 10 qualified business owners per day with minimal effort?
```bash
docker run outreach python assist.py --lead "Plumbing Co"
```

## Top-level repository layout

client_hunter/
├── docker-compose.yml
├── .env
├── README.md
│
├── data/
│   ├── leads_raw.csv
│   ├── leads_qualified.csv
│   ├── contacts.csv
│   └── call_logs.csv
│
├── scraper/
│   ├── Dockerfile
│   ├── scrape.py
│   ├── sources/
│   │   ├── google_maps.py
│   │   ├── yellow_pages.py
│   │   └── static_sites.py
│   └── utils.py
│
├── scorer/
│   ├── Dockerfile
│   ├── score.py
│   ├── prompts/
│   │   └── lead_score.txt
│   └── llm/
│       └── llama.cpp   (or local runner wrapper)
│
├── outreach/
│   ├── Dockerfile
│   ├── scripts/
│   │   ├── voicemail.txt
│   │   ├── call_guide.txt
│   │   └── followup.txt
│   └── assist.py
│
├── web/
│   ├── Dockerfile
│   ├── server.py
│   ├── templates/
│   │   └── landing.html
│   └── static/
│       └── style.css
│
└── notifier/
    ├── Dockerfile
    └── whatsapp_web.py

