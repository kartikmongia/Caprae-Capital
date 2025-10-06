# Caprae-Capital

# Caprae Lead Enricher (Demo)


A small Streamlit demo to enrich and deduplicate leads for sales outreach. Built as a 5-hour focused feature for the Caprae Capital Developer Intern Pre-Work.


## Features
- Upload CSV with columns: company, email, phone, country
- Infer company domain (heuristic)
- Basic email quality scoring
- Deduplication by normalized company+email/phone
- Filter and download enriched CSV


## Run locally
1. Create virtualenv: `python -m venv venv && source venv/bin/activate` (or Windows equivalent)
2. Install requirements: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`


## Notes
- This is a demo; for production integrate with enrichment APIs and add proxy/crawling safeguards.
