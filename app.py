\
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from pathlib import Path
from datetime import datetime
import subprocess
import os
import shutil
import re

app = Flask(__name__)

ROOT = Path(__file__).parent
JOBS = ROOT / "app" / "data" / "jobs"
JOBS.mkdir(parents=True, exist_ok=True)

GPTS_URL = "https://chatgpt.com/g/g-69ef95c18ff081918a267dcbd722305f-sseuredeu-ni-daeboni-nae-daebonida"
GOOGLE_LENS_URL = "https://lens.google.com/"

def safe_job_name():
    return datetime.now().strftime("%Y%m%d_%H%M%S") + "_tiktok"

def make_job_dirs(job_dir: Path):
    for name in ["video", "frames", "links", "notes"]:
        (job_dir / name).mkdir(parents=True, exist_ok=True)

def run(cmd):
    return subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

@app.route("/")
def index():
    jobs = sorted([p.name for p in JOBS.iterdir() if p.is_dir()], reverse=True)
    return render_template("index.html", jobs=jobs, gpts_url=GPTS_URL, lens_url=GOOGLE_LENS_URL)

@app.route("/create", methods=["POST"])
def create():
    tiktok_url = request.form.get("tiktok_url", "").strip()
    if not tiktok_url:
        return redirect(url_for("index"))

    job_name = safe_job_name()
    job_dir = JOBS / job_name
    make_job_dirs(job_dir)

    (job_dir / "links" / "source_tiktok.txt").write_text(tiktok_url, encoding="utf-8")

    video_path = job_dir / "video" / "source.mp4"

    # Download TikTok video with simple safe filename
    cmd = f'python -m yt_dlp -o "{video_path}" "{tiktok_url}"'
    result = run(cmd)
    (job_dir / "notes" / "download_log.txt").write_text(result.stdout, encoding="utf-8", errors="ignore")

    # Extract 6 frames. Requires ffmpeg available in yt-dlp environment or system PATH.
    frames_dir = job_dir / "frames"
    ffmpeg_cmd = f'ffmpeg -y -i "{video_path}" -vf "fps=1" -vframes 6 "{frames_dir / "frame%d.jpg"}"'
    frame_result = run(ffmpeg_cmd)
    (job_dir / "notes" / "frames_log.txt").write_text(frame_result.stdout, encoding="utf-8", errors="ignore")

    return redirect(url_for("job", job=job_name))

@app.route("/job/<job>")
def job(job):
    job_dir = JOBS / job
    frames = []
    frames_dir = job_dir / "frames"
    if frames_dir.exists():
        frames = sorted([p.name for p in frames_dir.glob("*.jpg")])
    coupang = (job_dir / "links" / "coupang.txt").read_text(encoding="utf-8") if (job_dir / "links" / "coupang.txt").exists() else ""
    coupas = (job_dir / "links" / "coupas.txt").read_text(encoding="utf-8") if (job_dir / "links" / "coupas.txt").exists() else ""
    memo = (job_dir / "notes" / "memo.txt").read_text(encoding="utf-8") if (job_dir / "notes" / "memo.txt").exists() else ""
    return render_template("job.html", job=job, frames=frames, coupang=coupang, coupas=coupas, memo=memo, gpts_url=GPTS_URL, lens_url=GOOGLE_LENS_URL)

@app.route("/job/<job>/save_links", methods=["POST"])
def save_links(job):
    job_dir = JOBS / job
    make_job_dirs(job_dir)
    (job_dir / "links" / "coupang.txt").write_text(request.form.get("coupang", "").strip(), encoding="utf-8")
    (job_dir / "links" / "coupas.txt").write_text(request.form.get("coupas", "").strip(), encoding="utf-8")
    (job_dir / "notes" / "memo.txt").write_text(request.form.get("memo", "").strip(), encoding="utf-8")
    return redirect(url_for("job", job=job))

@app.route("/data/jobs/<job>/frames/<filename>")
def frame_file(job, filename):
    return send_from_directory(JOBS / job / "frames", filename)

if __name__ == "__main__":
    # 0.0.0.0 lets phones on the same Wi-Fi access it through the PC IP.
    app.run(host="0.0.0.0", port=5000, debug=False)
