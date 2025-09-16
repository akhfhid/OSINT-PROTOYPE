#!/usr/bin/env python3
"""
DarkCrawler 2.2 – Ethical dark-web OSINT through Tor
Author: you
Licence: MIT
Usage: python/python3 osin.py  [--gui] [--urls u1.onion,u2.onion]
"""

import argparse, base64, csv, json, os, random, re, socket, sys, time, datetime
import requests, socks, csv, json, os, random, re, socket, time, datetime
from bs4 import BeautifulSoup
from fpdf import FPDF
from stem import Signal
from stem.control import Controller
import nltk, tkinter as tk, threading, queue
from tkhtmlview import HTMLLabel
from tkinter import ttk, scrolledtext
import pandas as pd
from tqdm import tqdm

TOR_PROXY = ("127.0.0.1", 9150)
TOR_CTRL = ("127.0.0.1", 9051)
TOR_CTRL_PWD = None  # set below if you enabled HashedControlPassword

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
]

KEYWOARDS = {
    "high": [
        "credit card fraud",
        "stolen data",
        "cvv",
        "fullz",
        "dump",
        "carding",
        "ransomware",
        "malware",
        "exploit kit",
        "zero-day",
        "database leak",
    ],
    "medium": [
        "fake passport",
        "fake id",
        "counterfeit",
        "bank logs",
        "paypal transfer",
        "weed",
        "cocaine",
        "amphetamine",
        "pills",
        "guns",
        "ammo",
    ],
    "low": ["premium accounts", "cracking", "hacking tutorial", "config", "combolist"],
}

MARKETPLACE_CATEGORIES = {
    "digital_goods": [
        "credit cards",
        "accounts",
        "paypal",
        "bank logs",
        "cvv",
        "fullz",
    ],
    "fraud": ["fake documents", "counterfeit", "passport", "id"],
    "drugs": ["weed", "cocaine", "mdma", "pills", "heroin", "meth"],
    "weapons": ["gun", "rifle", "pistol", "ammo", "firearm"],
    "services": ["hacking", "ransomware", "ddos", "malware", "exploit"],
}

MAX_DEPTH = 2
MAX_PAGES = 50
CRAWL_DELAY = (1, 4)
RETRY = 3
TIMEOUT = 20

# Safe onion example
DEFAULT_ONION_URLS = [
    "http://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion",
    "http://www.nytimes3xbfgragh.onion",
    "http://facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion",
]


def new_tor_identity():
    """Renew Tor circuit via control port"""
    try:
        with Controller.from_port(port=TOR_CTRL[1]) as c:
            c.authenticate(password=TOR_CTRL_PWD or "")
            c.signal(Signal.NEWNYM)
            time.sleep(2)
    except Exception as e:
        print("[!] Failed to renew Tor circuit:", e)


def tor_session():
    """Return a requests session routed through Tor"""
    sess = requests.Session()
    sess.proxies = {
        "http": f"socks5h://{TOR_PROXY[0]}:{TOR_PROXY[1]}",
        "https": f"socks5h://{TOR_PROXY[0]}:{TOR_PROXY[1]}",
    }
    sess.headers.update({"User-Agent": random.choice(USER_AGENTS)})
    return sess


def normalize_link(base, link):
    """Convert relative onion links to absolute"""
    if link.startswith("http"):
        return link
    if link.startswith("/"):
        return base.split("/")[0] + "//" + base.split("/")[2] + link
    return base.rsplit("/", 1)[0] + "/" + link


def classify_threats(text):
    """Return dict with high/medium/low lists"""
    text_lower = text.lower()
    res = {"high": [], "medium": [], "low": []}
    for level, kws in KEYWOARDS.items():
        res[level] = [kw for kw in kws if kw in text_lower]
    return res


def count_marketplace_goods(text):
    """Count occurrences per marketplace category"""
    text_lower = text.lower()
    counts = {cat: {} for cat in MARKETPLACE_CATEGORIES}
    for cat, kws in MARKETPLACE_CATEGORIES.items():
        for kw in kws:
            cnt = len(re.findall(r"\b" + re.escape(kw) + r"\b", text_lower))
            if cnt:
                counts[cat][kw] = cnt
    return counts


def crawl(urls, max_depth=MAX_DEPTH, max_pages=MAX_PAGES, gui_queue=None):
    """Crawl list of onion urls; return list of result dicts"""
    session = tor_session()
    visited = set()
    to_visit = [(u, 0) for u in urls]
    results = []
    pbar = tqdm(total=max_pages, desc="Pages crawled") if not gui_queue else None

    def update_pbar():
        if pbar:
            pbar.update(1)
        elif gui_queue:
            gui_queue.put(("pbar",))

    while to_visit and len(results) < max_pages:
        url, depth = to_visit.pop(0)
        if url in visited or depth > max_depth:
            continue
        visited.add(url)
        for attempt in range(1, RETRY + 1):
            try:
                time.sleep(random.uniform(*CRAWL_DELAY))
                resp = session.get(url, timeout=TIMEOUT)
                if resp.status_code != 200:
                    raise ValueError(f"status {resp.status_code}")
                break
            except Exception as e:
                if attempt == RETRY:
                    print(f"[!] Failed {url} – {e}")
                    continue
                new_tor_identity()
                session = tor_session()
                time.sleep(2**attempt)

        soup = BeautifulSoup(resp.text, "lxml")
        title = soup.title.string.strip() if soup.title else url
        text = soup.get_text(" ", strip=True)

        threats = classify_threats(text)
        goods = count_marketplace_goods(text)

        results.append(
            {
                "url": url,
                "title": title,
                "text": text[:2000],
                "threats": threats,
                "marketplace_goods": goods,
                "crawl_time": datetime.datetime.utcnow().isoformat(),
            }
        )
        update_pbar()

        if depth < max_depth:
            for link in soup.find_all("a", href=True):
                href = normalize_link(url, link["href"])
                if ".onion" in href and href not in visited:
                    to_visit.append((href, depth + 1))

    if pbar:
        pbar.close()
    return results

def save_json(results, fname="darkweb_crawl_results.json"):
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def save_csv(results, fname="darkweb_crawl_results.csv"):
    rows = []
    for r in results:
        rows.append(
            {
                "URL": r["url"],
                "Title": r["title"],
                "Content": r["text"][:200],
                "Threats": json.dumps(r["threats"]),
                "Marketplace Goods": json.dumps(r["marketplace_goods"]),
            }
        )
    pd.DataFrame(rows).to_csv(fname, index=False)


def save_pdf(results, fname="darkweb_threat_report.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Courier", size=12)

    pdf.set_font(size=16)
    pdf.cell(0, 10, "DARKWEB THREAT INTELLIGENCE REPORT", ln=1, align="C")
    pdf.ln(10)
    pdf.set_font(size=12)
    meta = f"Generated: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\nPages crawled: {len(results)}"
    pdf.multi_cell(0, 6, meta)
    pdf.ln(10)

    high = sum(len(r["threats"]["high"]) for r in results)
    med = sum(len(r["threats"]["medium"]) for r in results)
    low = sum(len(r["threats"]["low"]) for r in results)
    pdf.multi_cell(
        0, 6, f"High threats: {high}\nMedium threats: {med}\nLow threats: {low}"
    )
    pdf.ln(10)

    for r in results:
        pdf.set_font(style="B", size=11)
        pdf.multi_cell(0, 5, f"URL: {r['url']}")
        pdf.set_font(style="")
        pdf.multi_cell(0, 5, f"Title: {r['title']}")
        pdf.multi_cell(0, 5, f"Threats: {json.dumps(r['threats'])}")
        pdf.ln(5)

    pdf.output(fname)


class CrawlerGUI(tk.Tk):
    def __init__(self, urls):
        super().__init__()
        self.urls = urls
        self.queue = queue.Queue()
        self.title("DarkCrawler 2.2 – GUI")
        self.geometry("900x600")
        self.build_ui()
        self.after(100, self.queue_listener)

    def build_ui(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True)
        self.tab1 = ttk.Frame(nb)
        self.tab2 = ttk.Frame(nb)
        nb.add(self.tab1, text="Dashboard")
        nb.add(self.tab2, text="Report Preview")

        ttk.Label(self.tab1, text="Target URLs:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.url_box = scrolledtext.ScrolledText(self.tab1, width=80, height=6)
        self.url_box.grid(row=1, column=0, padx=5, pady=5)
        self.url_box.insert("1.0", "\n".join(self.urls))

        self.start_btn = ttk.Button(
            self.tab1, text="Start Crawl", command=self.start_thread
        )
        self.start_btn.grid(row=2, column=0, pady=8)

        self.pbar = ttk.Progressbar(self.tab1, length=400, mode="determinate")
        self.pbar.grid(row=3, column=0, pady=5)

        self.log = scrolledtext.ScrolledText(self.tab1, width=100, height=15)
        self.log.grid(row=4, column=0, padx=5, pady=5)

        self.html = HTMLLabel(self.tab2, html="<h3>Report will appear here…</h3>")
        self.html.pack(fill="both", expand=True)

    def log_msg(self, msg):
        self.log.insert("end", msg + "\n")
        self.log.see("end")

    def queue_listener(self):
        try:
            while True:
                typ, *rest = self.queue.get_nowait()
                if typ == "pbar":
                    self.pbar.step(1)
                elif typ == "log":
                    self.log_msg(rest[0])
                elif typ == "done":
                    self.show_report(rest[0])
        except queue.Empty:
            pass
        self.after(100, self.queue_listener)

    def start_thread(self):
        self.start_btn.config(state="disabled")
        urls = [
            u.strip() for u in self.url_box.get("1.0", "end").splitlines() if u.strip()
        ]
        threading.Thread(target=self.run_crawl, args=(urls,), daemon=True).start()

    def run_crawl(self, urls):
        self.queue.put(("log", "Crawl started…"))
        results = crawl(urls, gui_queue=self.queue)
        save_json(results)
        save_csv(results)
        save_pdf(results)
        self.queue.put(("done", results))
        self.queue.put(("log", "Crawl finished – files saved."))

    def show_report(self, results):
        html = "<h2>Quick Summary</h2><ul>"
        high = sum(len(r["threats"]["high"]) for r in results)
        med = sum(len(r["threats"]["medium"]) for r in results)
        low = sum(len(r["threats"]["low"]) for r in results)
        html += f"<li>High: {high}</li><li>Medium: {med}</li><li>Low: {low}</li></ul>"
        html += "<h3>Pages</h3><ol>"
        for r in results:
            html += f"<li><b>{r['title']}</b> – <a href='{r['url']}'>{r['url']}</a><br/>Threats: {json.dumps(r['threats'])}</li>"
        html += "</ol>"
        self.html.set_html(html)


def main():
    parser = argparse.ArgumentParser(
        description="DarkCrawler 2.2 – Ethical dark-web crawler"
    )
    parser.add_argument("--gui", action="store_true", help="launch GUI")
    parser.add_argument(
        "--urls", help="comma-separated .onion URLs (default: safe examples)"
    )
    args = parser.parse_args()

    urls = args.urls.split(",") if args.urls else DEFAULT_ONION_URLS

    if args.gui:
        root = CrawlerGUI(urls)
        root.mainloop()
    else:
        print("[*] Starting crawl…")
        results = crawl(urls)
        save_json(results)
        save_csv(results)
        save_pdf(results)
        print("[+] Done – check darkweb_crawl_results.{json,csv,pdf}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\n[!] Successfully interrupted.")
