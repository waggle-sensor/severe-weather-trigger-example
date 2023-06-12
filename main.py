import os
import requests
import subprocess
import re


WAGGLE_TOKEN = os.environ["WAGGLE_TOKEN"]


def main():
    events = get_severe_weather_events()

    # NOTE we assume the user has created this job ahead of time and that this examples simple suspends / resumes it based on events
    jobs = find_jobs_with_name("severe-weather-trigger-example")

    if len(events) == 0:
        suspend_all_jobs(jobs)
    else:
        submit_all_jobs(jobs)


def suspend_all_jobs(jobs):
    print("stopping severe weather event job...")
    for job in jobs:
        suspend_job(job["id"])


def submit_all_jobs(jobs):
    print("starting severe weather event job...")
    for job in jobs:
        submit_job(job["id"])


def find_jobs_with_name(name):
    output = subprocess.check_output(
        [
            "./sesctl",
            "--token",
            WAGGLE_TOKEN,
            "--server",
            "https://es.sagecontinuum.org",
            "stat",
            "-A",
        ],
        text=True,
    )

    # example output data:
    # JOB_ID NAME                           USER           STATUS    AGE
    # 17     test-pipeline                  seanshahkarami Removed   -
    # 23     test-pipeline                  seanshahkarami Removed   -
    # 634    severe-weather-trigger-example seanshahkarami Created   -
    # 25     test-pipeline                  seanshahkarami Removed   -
    # 635    severe-weather-trigger-example seanshahkarami Suspended   -
    # 636    severe-weather-trigger-example seanshahkarami Removed   -
    matches = re.findall(r"(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)", output)

    # read and filter data
    jobs = [{"id": m[0], "name": m[1], "status": m[3]} for m in matches]
    jobs = [
        job for job in jobs if job["name"] == name and job["status"] not in ["Removed"]
    ]
    return jobs


def submit_job(job_id):
    output = subprocess.check_output(
        [
            "./sesctl",
            "--token",
            WAGGLE_TOKEN,
            "--server",
            "https://es.sagecontinuum.org",
            "submit",
            "-j",
            job_id,
        ],
        text=True,
    )
    print(output)


def suspend_job(job_id):
    output = subprocess.check_output(
        [
            "./sesctl",
            "--token",
            WAGGLE_TOKEN,
            "--server",
            "https://es.sagecontinuum.org",
            "rm",
            "--suspend",
            job_id,
        ],
        text=True,
    )
    print(output)


def get_severe_weather_events():
    r = requests.get("https://api.weather.gov/alerts/active?area=IL")
    r.raise_for_status()
    data = r.json()

    return [
        f
        for f in data["features"]
        if f["properties"].get("@type") == "wx:Alert"
        and f["properties"].get("severity") == "Severe"
    ]


if __name__ == "__main__":
    main()
