from flask import Flask, request, jsonify
from flask_cors import CORS
from core.db.crud import save_job, get_results
from core.crawler import fetch
from sqlalchemy.orm import Session
from core.db.session import get_db

app = Flask(__name__)
CORS(app)


@app.route("/crawl", methods=["POST"])
def crawl():
    data = request.get_json()
    urls = data.get("urls", [])
    job_id = save_job(get_db(), urls)
    for url in urls:
        fetch(url, get_db(), job_id)
    return jsonify({"job_id": job_id, "status": "started"})


@app.route("/results/<job_id>", methods=["GET"])
def results(job_id):
    return jsonify(get_results(get_db(), job_id))
