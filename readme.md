# DarkCrawler 2.2 – Ethical Dark-Web OSINT Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.6+](https://img.shields.io/badge/Python-3.6%2B-blue)](https://www.python.org/downloads/)
[![Version: 2.2](https://img.shields.io/badge/Version-2.2-green)](https://github.com/akhfhid/osint-prototype/releases)

## Overview

DarkCrawler is a robust, open-source Python tool engineered for ethical open-source intelligence (OSINT) gathering on dark-web (.onion) sites via the Tor network. It systematically crawls specified .onion URLs, extracts textual content, classifies threats by severity, and categorizes marketplace goods, producing comprehensive reports in JSON, CSV, and PDF formats. Designed for flexibility, DarkCrawler supports both command-line and graphical user interface (GUI) modes, catering to security researchers, analysts, and threat intelligence professionals.

- **Version**: 2.2
- **Author**: Akhfhid
- **License**: MIT
- **Purpose**: To enable ethical analysis of dark-web content for threat intelligence and security research.

---

## Ethical and Legal Considerations

DarkCrawler is strictly intended for lawful and ethical OSINT activities, such as academic research, cybersecurity analysis, or authorized threat intelligence operations. Users are responsible for ensuring compliance with all applicable local, national, and international laws, including those governing data access and privacy. Unauthorized access to websites, collection of sensitive data without permission, or any misuse of this tool is expressly prohibited and may result in legal consequences. Always obtain explicit authorization from site owners before crawling.

---

## Features

- **Configurable Crawling**: Supports user-defined crawl depth (default: 2) and page limits (default: 50).
- **Threat Classification**: Identifies high, medium, and low-severity threats using predefined keyword lists.
- **Marketplace Analysis**: Categorizes goods into digital goods, fraud, drugs, weapons, and services.
- **Multi-Format Reporting**: Generates detailed outputs in JSON, CSV, and PDF formats.
- **Graphical Interface**: Provides an optional GUI for interactive URL input, real-time progress tracking, and report previews.
- **Tor Integration**: Ensures anonymous crawling with automated circuit renewal via Tor’s control port.

---

## Prerequisites

To operate DarkCrawler, ensure the following are installed and configured:
- **Tor**: Required for accessing .onion sites.
- **Python**: Version 3.6 or higher.
- **Dependencies**: Python libraries specified in `requirements.txt`.
- **NLTK Data**: Required for text processing.

---

## Installation

1. **Install Tor**:
   - **Linux**: Execute `sudo apt-get install tor`.
   - **macOS**: Execute `brew install tor`.
   - **Windows**: Download and install from the [Tor Project website](https://www.torproject.org/download/).
   - Start the Tor service (e.g., `tor` on Linux/macOS or launch Tor Browser on Windows).
   - Verify Tor is running on `127.0.0.1:9050` (proxy port) and `127.0.0.1:9051` (control port).
   - Optional: Configure `HashedControlPassword` in the `torrc` file for enhanced control port security.

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/akhfhid/osint-prototype.git
   cd osint-prototype
   ```

3. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK Data**:
   ```python
   python3 -c "import nltk; nltk.download('punkt')"
   ```

---

## Usage

DarkCrawler supports two operational modes: command-line and GUI. The script is named `osin.py`.

### Command-Line Mode

Run with default settings (crawls predefined safe .onion URLs, e.g., DuckDuckGo’s .onion site):
```bash
python3 osin.py
```

Crawl specific .onion URLs (comma-separated):
```bash
python3 osin.py --urls http://example1.onion,http://example2.onion
```

Launch the GUI:
```bash
python3 osin.py --gui
```

**Command-Line Options**:
| Option | Description | Example |
|--------|-------------|---------|
| `--gui` | Launches the graphical interface | `python3 osin.py --gui` |
| `--urls` | Specifies comma-separated .onion URLs | `python3 osin.py --urls http://example1.onion,http://example2.onion` |

### GUI Mode

- Execute `python3 osin.py --gui`.
- Input .onion URLs in the provided text box (one URL per line).
- Click **Start Crawl** to initiate the crawling process.
- Monitor real-time progress in the log panel and view results in the **Report Preview** tab.

### Output Files

DarkCrawler generates three output files:
- `darkweb_crawl_results.json`: Comprehensive crawl data in JSON format.
- `darkweb_crawl_results.csv`: Tabular summary of crawled pages.
- `darkweb_threat_report.pdf`: Formatted threat intelligence report with summary statistics.

---

### Sample Output

Below are illustrative outputs showcasing a page with detected threats and marketplace goods.

**JSON Output** (`darkweb_crawl_results.json`):
```json
[
  {
    "url": "http://marketxyz.onion",
    "title": "DarkWeb Marketplace",
    "text": "Secure marketplace for credit cards, fullz, fake passports, and bank logs. Contact for CVV deals...",
    "threats": {
      "high": ["credit card fraud", "fullz", "cvv"],
      "medium": ["fake passport", "bank logs"],
      "low": []
    },
    "marketplace_goods": {
      "digital_goods": {"credit cards": 5, "cvv": 3, "fullz": 2, "bank logs": 1},
      "fraud": {"fake passports": 4},
      "drugs": {},
      "weapons": {},
      "services": {}
    },
    "crawl_time": "2025-09-16T19:00:00.123456"
  }
]
```

**CSV Output** (`darkweb_crawl_results.csv`):
```csv
URL,Title,Content,Threats,Marketplace Goods
http://marketxyz.onion,DarkWeb Marketplace,Secure marketplace for credit cards, fullz, fake passports...,"{""high"": [""credit card fraud"", ""fullz"", ""cvv""], ""medium"": [""fake passport"", ""bank logs""], ""low"": []}","{""digital_goods"": {""credit cards"": 5, ""cvv"": 3, ""fullz"": 2, ""bank logs"": 1}, ""fraud"": {""fake passports"": 4}, ""drugs"": {}, ""weapons"": {}, ""services"": {}}"
```

**PDF Output** (`darkweb_threat_report.pdf`):
```
DARKWEB THREAT INTELLIGENCE REPORT
Generated: 2025-09-16 19:00:00 UTC
Pages Crawled: 1
High Threats: 3
Medium Threats: 2
Low Threats: 0

URL: http://marketxyz.onion
Title: DarkWeb Marketplace
Threats: {"high": ["credit card fraud", "fullz", "cvv"], "medium": ["fake passport", "bank logs"], "low": []}
```

**GUI Preview** (Description):
The GUI’s **Report Preview** tab renders an HTML summary, including:
- Aggregate statistics: “High Threats: 3, Medium Threats: 2, Low Threats: 0”.
- A clickable list of crawled pages, displaying titles, URLs, and associated threats.

---

## Contributing

Contributions to DarkCrawler are encouraged. To contribute:
1. Fork the repository: `https://github.com/akhfhid/osint-prototype`.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/) coding standards.
4. Test changes locally with Tor running.
5. Commit changes: `git commit -m "Add your feature"`.
6. Push to the branch: `git push origin feature/your-feature`.
7. Submit a pull request with a detailed description of changes.

Please include unit tests for new features and update documentation as needed.

---

## License

DarkCrawler is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.