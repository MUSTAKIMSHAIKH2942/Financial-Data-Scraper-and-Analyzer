from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import sqlite3
import threading
import re

app = Flask(__name__)

# Regular expression for detecting financial data (e.g., dollars, rupees)
financial_data_regex = r'\$[\d,]+(?:\.\d{1,2})?|\₹[\d,]+(?:\.\d{1,2})?|\d+(?:,\d{3})*(?:\.\d+)?'

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract paragraphs and filter those containing financial data
        paragraphs = soup.find_all('p')
        text = ' '.join([p.text for p in paragraphs if re.search(financial_data_regex, p.text)])
        
        return text
    except Exception as e:
        return str(e)

def standardize_name(url):
    name = re.sub(r'[^a-zA-Z0-9]', '_', url)
    return name[:50]  # Limit name length

def store_data(url, name, content):
    conn = sqlite3.connect("scraped_data.db")
    cursor = conn.cursor()
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS stock_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            name TEXT,
            content TEXT
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO stock_data (url, name, content) VALUES (?, ?, ?)", (url, name, content))
    conn.commit()
    conn.close()

def analyze_data():
    conn = sqlite3.connect("scraped_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM stock_data")
    data = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    if not data:
        return {"error": "No data to analyze"}
    
    # Here you can apply more ML analysis, clustering, or NER as needed
    return {"message": "Analysis complete"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    urls = data.get("urls")
    if not urls or not isinstance(urls, list):
        return jsonify({"error": "Please provide a list of URLs"}), 400
    
    results = []
    threads = []
    for url in urls:
        name = standardize_name(url)
        thread = threading.Thread(target=lambda u, n: results.append({"url": u, "name": n, "content": scrape_website(u)}), args=(url, name))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    for result in results:
        store_data(result["url"], result["name"], result["content"])
    
    return jsonify({"message": "Data scraped and stored successfully!", "results": results})

@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect("scraped_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, url, name, SUBSTR(content, 1, 500) AS summary FROM stock_data")
    data = [{"id": row[0], "url": row[1], "name": row[2], "summary": row[3]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(data)

@app.route('/delete/<int:data_id>', methods=['DELETE'])
def delete_data(data_id):
    conn = sqlite3.connect("scraped_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM stock_data WHERE id = ?", (data_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Data deleted successfully"})

@app.route('/analyze', methods=['GET'])
def analyze():
    result = analyze_data()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
