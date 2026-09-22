from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import time

print("=" * 50)
print("IMDb Movie Rating Scraper")
print("=" * 50)

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://www.imdb.com/chart/top/")
    time.sleep(5)

    if "Human Verification" in driver.title:
        print("Human Verification detected.")
        input("Complete verification, then press ENTER...")

    time.sleep(3) 
    movies = driver.find_elements(
        By.CSS_SELECTOR,
        "li.ipc-metadata-list-summary-item"
    )
    print("Movies found:", len(movies))
    movie_data = []
    for movie in movies:
        lines = [
            line.strip()
            for line in movie.text.split("\n")
            if line.strip()
        ]
        rank = None
        title = None
        year = None
        rating = None
        for line in lines:
            match = re.match(r"#(\d+)", line)
            if match:
                rank = int(match.group(1))
                break
        for line in lines:
            match = re.search(r"(19\d{2}|20\d{2})", line)
            if match:
                year = int(match.group(1))
                break
        for line in lines:
            match = re.fullmatch(r"(\d+\.\d)", line)
            if match:
                rating = float(match.group(1))
                break
        if rank is not None:
            rank_index = None

            for i, line in enumerate(lines):
                if line == f"#{rank}":
                    rank_index = i
                    break

            if rank_index is not None and rank_index + 1 < len(lines):
                title = lines[rank_index + 1]
        if rank is not None and title and year is not None and rating is not None:

            movie_data.append({
                "Rank": rank,
                "Title": title,
                "Year": year,
                "Rating": rating
            })
    df = pd.DataFrame(movie_data)
    if not df.empty:
        df = df.drop_duplicates(subset="Rank")
        df = df.sort_values("Rank").reset_index(drop=True)

    print("\n" + "=" * 50)
    print("Extracted Movie Data")
    print("=" * 50)

    if not df.empty:
        print(df.to_string(index=False))

        df.to_csv("imdb_top250.csv", index=False)

        print("\n" + "=" * 50)
        print("CSV SAVED SUCCESSFULLY")
        print("=" * 50)

        print("Total movies saved:", len(df))
        print("CSV file: imdb_top250.csv")

    else:
        print("No movie data extracted.")
        print("CSV file was not overwritten.")

finally:
    driver.quit()