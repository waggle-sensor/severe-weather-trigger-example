import os
import requests


def main():
    token = os.environ["WAGGLE_TOKEN"]
    # cmd = CommandRunner(token, "https://es.sagecontinuum.org")

    r = requests.get("https://api.weather.gov/alerts/active?area=IL")
    r.raise_for_status()
    data = r.json()

    severe_events = [
        f
        for f in data["features"]
        if f["properties"].get("@type") == "wx:Alert"
        and f["properties"].get("severity") == "Severe"
    ]

    if len(severe_events) == 0:
        print("stopping severe weather event job...")
    else:
        print("starting severe weather event job...")


if __name__ == "__main__":
    main()
