"""
FRONTEND : A streamlit dashboard for User to input text and get sentiment analysis results.
BACKEND : A FastAPI backend that receives the text input, processes it using a sentiment analysis model, and returns the sentiment label, score, and theme.
DATABASE : An SQLite database to store the sentiment analysis results for future reference and analysis.
RUN: uv run streamlit run src/sentiment_analyser/app.py

"""

from collections import Counter
import streamlit as st
import requests

from sentiment_analyser.database import (initialize_database, save_analysis_result, load_analysis_results, DB_NAME)

BASE_API_URL = "http://localhost:8000"

initialize_database()


# Streamlit app
st.title("📝 Sentiment Analysis Dashboard")
st.write("Enter your customerreview below, one review per line.")

reviews_text = st.text_area("Customer Reviews", height=200, placeholder="Enter your customer reviews here...")

if st.button("Analyze Sentiment"):
    reviews = [line.strip() for line in reviews_text.strip().split("\n") if line.strip()]

    if not reviews:
        st.warning("Please enter at least one review.")
    else:
        results = []
        for review in reviews:
            try:
                response = requests.post(f"{BASE_API_URL}/analyze", json={"text": review})
                data = response.json()

                results.append({
                    "review": review,
                    "sentiment": data.get("sentiment"),
                    "score": data.get("score"),
                    "theme": data.get("theme")
                })
            except Exception as e:

                results.append({
                    "review": review,
                    "sentiment": "Error",
                    "score": None,
                    "theme": "Error"
                })
                print(f"Error analyzing review: {review}. Error: {dir(e)}")
                st.error(f"Error analyzing review. Error: {dir(e.args)}")
               
        # save the results to a session state to persist them.    
        st.session_state.results = results

# show results if they exist in session state
if "results" in st.session_state:
    results = st.session_state.results

    st.subheader("Analysis Results")
    st.dataframe(results)

    # ---- STATS & SUMMARY----

    scores = [result['score'] for result in results if result['sentiment'] != "Error" ]
    positive=[result for result in results if result['sentiment'] == "positive"]
    negative=[result for result in results if result['sentiment'] == "negative"]
    neutral=[result for result in results if result['sentiment'] == "neutral"]
    themes = [result['theme'] for result in results if result['theme'] != "Error" ]

    st.subheader("Summary") 
    col1, col2, col3, col4 = st.columns(4)   

    col1.metric("Reviews Analyzed", len(results))

    if scores:
        col2.metric("Average Score", round(sum(scores) / len(scores), 1))
        col3.metric("% Positive", f"{round(len(positive) / len(results) * 100, 1)}%")
        col4.metric("% Negative", f"{round(len(negative) / len(results) * 100, 1)}%")
        col4.metric("% Neutral", f"{round(len(neutral) / len(results) * 100, 1)}%")

    if themes:
        top_theme = Counter(themes).most_common(1)[0][0]   
        st.info(f"Most Common Theme: **{top_theme}**") 

    # save full results to db as Report
    if st.button(" 💾 Save Results"):
        save_analysis_result(results)
        st.success(f"Saved {len(results)} analysis results to {DB_NAME} datastore.")

# SHOW SAVED REPORTS
with st.expander(" 📚 View Saved Reports"):
    saved_results = load_analysis_results()
    if saved_results:
        st.write(f"Total Saved Reports: {len(saved_results)}")
        st.dataframe([{"review": row[0], "sentiment": row[1], "score": row[2], "theme": row[3], "created_at": row[4]} for row in saved_results])
    else:
        st.info("No saved reports saved yet.Analyze some reviews and save them to see them here.")