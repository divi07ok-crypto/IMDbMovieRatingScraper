from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Chrome browser settings
options = webdriver.ChromeOptions()

# Browser visible-ah open aagum
options.add_argument("--start-maximized")

# Chrome WebDriver
service = Service(
    ChromeDriverManager().install()
)

driver = webdriver.Chrome(
    service=service,
    options=options
)

try:

    print("========================================")
    print("     IMDb Live Movie Rating Scraper")
    print("========================================")

    # Open IMDb Top 250
    driver.get(
        "https://www.imdb.com/chart/top/"
    )

    print("\nIMDb Top 250 page opened.")

    print(
        "If Human Verification appears, "
        "complete it manually."
    )

    input(
        "\nAfter the IMDb page is fully loaded, "
        "press ENTER here..."
    )

    time.sleep(3)

    print("\nPage Title:")
    print(driver.title)

    # Find movie items
    movies = driver.find_elements(
        "css selector",
        "li.ipc-metadata-list-summary-item"
    )

    print(
        "\nMovies found:",
        len(movies)
    )

    movie_data = []

    for movie in movies:

        try:

            text = movie.text.strip()

            print("\n--------------------")
            print(text)

            movie_data.append({
                "Movie Details": text
            })

        except Exception as error:

            print(
                "Error extracting movie:",
                error
            )

    # Create DataFrame
    df = pd.DataFrame(movie_data)

    print("\n========================================")
    print("Extracted Movie Data")
    print("========================================")

    print(
        df.head(10).to_string(
            index=False
        )
    )

    # Save CSV
    output_file = "imdb_top250.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print("\n========================================")
    print("Scraping completed!")
    print(
        "Total movies:",
        len(df)
    )
    print(
        "CSV file:",
        output_file
    )
    print("========================================")

finally:

    driver.quit()

    print(
        "\nChrome WebDriver closed."
    )