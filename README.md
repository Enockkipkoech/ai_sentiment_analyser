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

## FEATURES
- Sentiment Analysis: Analyze text data and determine its sentiment (positive, negative, or neutral).
- FastAPI Backend: Provides a robust and efficient backend API for handling requests and processing sentiment analysis
- Streamlit Frontend: Offers a user-friendly interface for inputting text and viewing sentiment analysis results.
- SQLite Database: Stores sentiment analysis results for future reference and analysis.

## SCREENSHOTS
- Sentiment Analysis UI [UI Screenshot](./UI_screenshot.png)