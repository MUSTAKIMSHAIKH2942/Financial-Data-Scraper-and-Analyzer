# Financial Data Scraper and Analyzer

This project provides a Flask-based web application that scrapes financial data from given URLs, stores the data in an SQLite database, and provides analysis functionalities. It uses BeautifulSoup for web scraping, SQLite for data storage, and threading for concurrent scraping of multiple URLs.

## Features
- **Scrape financial data**: Extracts paragraphs containing financial data (e.g., USD, INR) from the provided URLs.
- **Store data**: Stores scraped data in an SQLite database.
- **View data**: Retrieve stored data with a summary of the content.
- **Delete data**: Delete specific records from the database.
- **Analyze data**: Placeholder for further data analysis or ML-based analysis.

## Technologies Used
- **Flask**: Web framework for building the application.
- **BeautifulSoup**: Library for parsing HTML and extracting relevant data.
- **SQLite**: Lightweight database for storing scraped data.
- **Threading**: Used for concurrent scraping of multiple URLs.

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/<username>/financial-data-scraper.git
   cd financial-data-scraper
Install the required dependencies:

pip install -r requirements.txt
Run the application:

python app.py
The app will be accessible at http://127.0.0.1:5000.

API Endpoints
GET /
Returns the home page (renders index.html).
POST /scrape
Scrapes financial data from the provided list of URLs.
Request Body:

{
  "urls": ["http://example.com", "http://another-example.com"]
}
Response:

{
  "message": "Data scraped and stored successfully!",
  "results": [
    {
      "url": "http://example.com",
      "name": "example_com",
      "content": "Some scraped financial data..."
    }
  ]
}
GET /data
Retrieves all stored data with a summary of the content.
Response:
json
Copy
Edit
[
  {
    "id": 1,
    "url": "http://example.com",
    "name": "example_com",
    "summary": "Some scraped financial data..."
  }
]
DELETE /delete/<int:data_id>
Deletes the record with the specified ID from the database.
Response:
json
Copy
Edit
{
  "message": "Data deleted successfully"
}
GET /analyze
Performs analysis on the stored data.
Response:

{
  "message": "Analysis complete"
}


Database
The application uses an SQLite database to store scraped data. The database file is named scraped_data.db and is created automatically if it doesn't already exist.
