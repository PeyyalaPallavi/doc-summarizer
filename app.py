from flask import Flask, render_template, request
from utils.extractor import extract_text_from_pdf
from utils.summarizer import summarize_text
import sqlite3, os

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("database.db")
    conn.execute('CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, filename TEXT, content TEXT)')
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    summary = ""
    if request.method == "POST":
        file = request.files["document"]
        if file and file.filename.endswith(".pdf"):
            filepath = os.path.join("uploads", file.filename)
            os.makedirs("uploads", exist_ok=True)
            file.save(filepath)

            text = extract_text_from_pdf(filepath)
            summary = summarize_text(text)

            # save to database
            conn = sqlite3.connect("database.db")
            conn.execute("INSERT INTO documents (filename, content) VALUES (?, ?)", (file.filename, text))
            conn.commit()
            conn.close()

    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
