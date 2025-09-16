# DarkCrawler 2.2 – Ethical Dark-Web OSINT Tool

## Overview
DarkCrawler is an open-source Python tool designed for ethical open-source intelligence (OSINT) gathering on dark-web (.onion) sites via the Tor network. It crawls specified .onion URLs, extracts content, classifies threats, and categorizes marketplace goods, generating detailed reports in JSON, CSV, and PDF formats. The tool supports both command-line and GUI modes for flexibility.

- **Version**: 2.2
- **Author**: [Your Name]
- **License**: MIT
- **Purpose**: To assist security researchers and analysts in ethically collecting and analyzing data from dark-web sites for threat intelligence.

**Note**: This tool is intended for ethical and legal use only. Ensure compliance with all applicable laws and regulations.

## Features
- Crawls .onion sites with configurable depth and page limits.
- Classifies threats into high, medium, and low severity based on predefined keywords.
- Categorizes marketplace goods (e.g., digital goods, drugs, weapons).
- Generates reports in JSON, CSV, and PDF formats.
- Optional GUI for interactive crawling and report preview.
- Tor integration for anonymous browsing with circuit renewal.

## Prerequisites
- **Tor**: Install and configure the Tor service to enable access to .onion sites.
- **Python**: Version 3.6 or higher.
- **Dependencies**: Listed in `requirements.txt`.

## Installation
1. **Install Tor**:
   - On Linux: `sudo apt-get install tor`
   - On macOS: `brew install tor`
   - On Windows: Download and install from [Tor Project](https://www.torproject.org/download/).
   - Start Tor and ensure it’s running on `127.0.0.1:9050` (default proxy port) and `127.0.0.1:9051` (default control port).
   - Optionally, configure `HashedControlPassword` in `torrc` for control port authentication.

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/darkcrawler.git
   cd darkcrawler
   ```

3. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK Data**:
   ```python
   import nltk
   nltk.download('punkt')
   ```

## Usage
DarkCrawler can be run in two modes: command-line or GUI.

### Command-Line Mode
Run the script with default settings (crawls safe example .onion URLs):
```bash
python3 darkcrawler.py
```

Crawl specific .onion URLs:
```bash
python3 darkcrawler.py --urls http://example1.onion,http://example2.onion
```

Launch the GUI:
```bash
python3 darkcrawler.py --gui
```

### GUI Mode
- Launch the GUI with `--gui`.
- Enter .onion URLs in the text box (one per line).
- Click "Start Crawl" to begin.
- View progress in the log and a summary in the "Report Preview" tab.

### Output Files
- `darkweb_crawl_results.json`: Detailed crawl results in JSON format.
- `darkweb_crawl_results.csv`: Summary table of crawled pages.
- `darkweb_threat_report.pdf`: Threat intelligence report with summary statistics.

### Sample Output
**JSON Output** (`darkweb_crawl_results.json`):
```json
[
  {
    "url": "http://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion",
    "title": "DuckDuckGo Search Engine",
    "text": "DuckDuckGo — Privacy, simplified. Search the web without being tracked...",
    "threats": {
      "high": [],
      "medium": [],
      "low": []
    },
    "marketplace_goods": {
      "digital_goods": {},
      "fraud": {},
      "drugs": {},
      "weapons": {},
      "services": {}
    },
    "crawl_time": "2025-09-16T11:56:00.123456"
  }
]
```

**CSV Output** (`darkweb_crawl_results.csv`):
```csv
URL,Title,Content,Threats,Marketplace Goods
http://example.onion,Example Page,Example content snippet...,"{""high"": [], ""medium"": [], ""low"": []}","{""digital_goods"": {}, ""fraud"": {}, ""drugs"": {}, ""weapons"": {}, ""services"": {}}"
```

**PDF Output** (`darkweb_threat_report.pdf`):
```
DARKWEB THREAT INTELLIGENCE REPORT
Generated: 2025-09-16 11:56:00
Pages crawled: 1
High threats: 0
Medium threats: 0
Low threats: 0

URL: http://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion
Title: DuckDuckGo Search Engine
Threats: {"high": [], "medium": [], "low": []}
```

## Ethical Use
DarkCrawler is designed for ethical OSINT purposes, such as security research and threat intelligence. Users must:
- Comply with all applicable laws and regulations.
- Avoid accessing or collecting data from sites without permission.
- Use the tool responsibly to avoid harm or disruption.

## Contributing
Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.
