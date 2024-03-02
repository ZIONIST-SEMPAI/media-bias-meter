# NYT scraper

This Python script is designed to scrape articles from The New York Times (NYT) and store them in a MySQL database. It automates the collection of articles, efficiently gathering data without manual intervention.

## Features

- Automated scraping of NYT articles.
- Efficient storage of articles in a MySQL database.
- Configurable for specific sections or topics.
- Easy to set up and run on any system with Python and MySQL.
- Provides a foundation for further data analysis and research.

## Getting Started

### Prerequisites
- Python 3.10.0 or greater
- MySQL instance 
- New York Times(NYT) API-KEY follow this [link](https://developer.nytimes.com/get-started) to get started 
- .env file under the scripts directory with the following secrets 

```yaml
API_KEY: GQ2x8SmP1UgAd3UMQV6saK96xUrbrSL6
begin_date: [2024, 01 ,29]
end_date: [2024, 02, 11]
filter_query: Gaza AND Palestine AND Israel AND Palestinian AND Israeli
```

### Installation

A step-by-step series of examples that tell you how to get a development environment running.

#### Setting Up a Virtual Environment

To isolate the project dependencies, it's recommended to use a virtual environment. Run the following command in your terminal to create a virtual environment in the current directory:

```bash
python -m venv venv
```

#### Activating the Virtual Environment

After creating the virtual environment, you need to activate it. Use the appropriate command for your operating system.

**Windows:**

```bash
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

#### Installing Dependencies

Install all dependencies that are required for the project to run.

```bash
pip install -r requirements.txt
```

### Running the Script

Explain how to run your script, including any command-line arguments you can use.

```bash
python your_script.py
```
