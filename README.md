##

### Start

1. Backend API
```bash
uv run uvicorn sentiment_analyser.api:app --reload --app-dir src
``` 

2. Frontend UI (Streamlit)
```bash
uv run streamlit run src/sentiment_analyser/app.py
```

## ABOUT PROJECT
- sentiment-analyser is a Python-based application that utilizes FastAPI for backend API development and Streamlit for frontend UI. 
It leverages the Google GenAI library for sentiment analysis, allowing users to analyze text data and determine its sentiment.

