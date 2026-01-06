## What system lets me talk to 10 qualified business owners per day with minimal effort?

## Instructions

1. Start server
```bash
python web/server.py
```
2. Run smtp server
```bash
python -m smtpd -c DebuggingServer -n localhost:1025
```
3. Run watch
```bash
python -m notifier.watch
```

## Top-level repository layout

```bash
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
```
