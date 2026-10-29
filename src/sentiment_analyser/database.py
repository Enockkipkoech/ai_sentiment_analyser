import sqlite3

DB_NAME = "sentiment_analyser.db"

def initialize_database():
    """Initializes the SQLite database and creates the necessary tables."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create a table for storing sentiment analysis results
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentiment_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review TEXT,
            sentiment TEXT,
            score INTEGER,
            theme TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def save_analysis_result(results):
    """Saves the sentiment analysis result to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for result in results:
        cursor.execute('''
            INSERT INTO sentiment_feedback (review, sentiment, score, theme)
            VALUES (?, ?, ?, ?)
        ''', (result['review'], result['sentiment'], result['score'], result['theme']))    

    conn.commit()
    conn.close()
    return "Analysis results saved successfully."

def load_analysis_results():
    """Loads all sentiment analysis results from the database."""
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute('SELECT * FROM sentiment_feedback').fetchall()

    conn.close()
    return rows