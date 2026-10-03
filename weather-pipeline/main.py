import json
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

from retry import retry


BASE_URL = "https://api.open-meteo.com/v1/forecast"

RAW_DIR = Path("raw")
OUTPUT_DIR = Path("output")

RAW_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


def load_config():
    with open("config.json", "r") as file:
        return json.load(file)


@retry(max_attempts=3, delay=2)
def fetch(city, latitude, longitude, settings):
    today = date.today().isoformat()
    cache_file = RAW_DIR / f"{city}_{today}.json"

    if cache_file.exists():
        print(f"{city}: using cached data")
        with open(cache_file, "r") as file:
            return json.load(file)

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation",
        "forecast_days": settings["forecast_days"],
        "timezone": settings["timezone"]
    }

    print(f"{city}: fetching data from API")

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    with open(cache_file, "w") as file:
        json.dump(data, file, indent=4)

    print(f"{city}: raw data saved")

    return data


def transform(city_data):
    rows = []

    for city, data in city_data.items():
        hourly = data["hourly"]

        times = hourly["time"]
        temperatures = hourly["temperature_2m"]
        precipitation = hourly["precipitation"]

        for time_value, temperature, rain in zip(
            times,
            temperatures,
            precipitation
        ):
            rows.append({
                "city": city,
                "time": time_value,
                "temperature": temperature,
                "precipitation": rain
            })

    df = pd.DataFrame(rows)

    df["time"] = pd.to_datetime(df["time"])

    return df


def analyse(df):
    analysis_df = df.copy()

    analysis_df["date"] = analysis_df["time"].dt.date

    summary = (
        analysis_df
        .groupby(["city", "date"], as_index=False)
        .agg(
            min_temperature=("temperature", "min"),
            max_temperature=("temperature", "max"),
            mean_temperature=("temperature", "mean"),
            total_rain=("precipitation", "sum")
        )
    )

    hottest_index = df["temperature"].idxmax()
    hottest_hour = df.loc[hottest_index]

    rain_by_day = (
        analysis_df
        .groupby(["city", "date"], as_index=False)
        ["precipitation"]
        .sum()
        .rename(columns={"precipitation": "total_rain"})
    )

    rainiest_indices = (
        rain_by_day
        .groupby("city")["total_rain"]
        .idxmax()
    )

    rainiest_days = rain_by_day.loc[rainiest_indices].reset_index(drop=True)

    return summary, hottest_hour, rainiest_days


def save(df, summary):
    forecast_path = OUTPUT_DIR / "forecast.csv"
    summary_path = OUTPUT_DIR / "summary.csv"
    plot_path = OUTPUT_DIR / "temperature.png"

    df.to_csv(forecast_path, index=False)
    summary.to_csv(summary_path, index=False)

    plt.figure(figsize=(12, 6))

    for city, city_df in df.groupby("city"):
        plt.plot(
            city_df["time"],
            city_df["temperature"],
            label=city
        )

    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.title("7-Day Temperature Forecast")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(plot_path)
    plt.close()

    print(f"\nSaved: {forecast_path}")
    print(f"Saved: {summary_path}")
    print(f"Saved: {plot_path}")


def main():
    try:
        config = load_config()

        settings = config["settings"]
        cities = config["cities"]

        city_data = {}

        for city, coordinates in cities.items():
            city_data[city] = fetch(
                city,
                coordinates["latitude"],
                coordinates["longitude"],
                settings
            )

        df = transform(city_data)

        summary, hottest_hour, rainiest_days = analyse(df)

        save(df, summary)

        print("\nHottest hour overall:")
        print(
            f"{hottest_hour['city']} | "
            f"{hottest_hour['time']} | "
            f"{hottest_hour['temperature']} °C"
        )

        print("\nRainiest day per city:")

        for _, row in rainiest_days.iterrows():
            print(
                f"{row['city']} | "
                f"{row['date']} | "
                f"{row['total_rain']:.2f} mm"
            )

        print("\nPipeline completed successfully.")

    except requests.exceptions.Timeout:
        print(
            "\nWeather API request timed out. "
            "Please check your internet connection and try again."
        )

    except requests.exceptions.ConnectionError:
        print(
            "\nCould not connect to the weather API. "
            "Please check your internet connection."
        )

    except requests.exceptions.HTTPError as error:
        print(
            f"\nWeather API returned an HTTP error: {error}"
        )

    except (KeyError, ValueError, TypeError) as error:
        print(
            f"\nData processing error: {error}"
        )

    except Exception as error:
        print(
            f"\nPipeline failed: {error}"
        )


if __name__ == "__main__":
    main()