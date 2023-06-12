import os
import requests


def main():
    token = os.environ["WAGGLE_TOKEN"]
    # cmd = CommandRunner(token, "https://es.sagecontinuum.org")

    events = get_severe_weather_events()

    if len(events) == 0:
        print("stopping severe weather event job...")
        # TODO stop job with sesctl
    else:
        print("starting severe weather event job...")
        # TODO start job with sesctl


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
