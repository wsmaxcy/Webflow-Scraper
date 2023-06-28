# Webflow Wishlist Scraper

The Webflow Wishlist Scraper is a Python script that allows you to scrape information from the Webflow Wishlist website (https://wishlist.webflow.com/). The script gathers data about ideas posted on the wishlist, including idea details, votes, descriptions, dates, statuses, and comments. The scraped data is saved in a CSV file for further analysis or processing.

## Prerequisites

Before running the script, make sure you have the following installed:

- Python 3 (https://www.python.org/downloads/)
- `requests` library (install using `pip install requests`)
- `BeautifulSoup` library (install using `pip install beautifulsoup4`)

## Getting Started

1. Clone the repository or download the `webflow_wishlist_scraper.py` file to your local machine.
2. Open a terminal or command prompt and navigate to the directory containing the script.

## Usage

To use the Webflow Wishlist Scraper, follow these steps:

1. Open the `webflow_wishlist_scraper.py` file in a text editor or integrated development environment (IDE).
2. Customize the script if needed. You can modify the URL, adjust the number of pages to scrape, or change the output file name.
3. Run the script by executing the command `python webflow_wishlist_scraper.py` in the terminal or command prompt.

## Output

The script generates two files:

- `output.csv`: This file contains the scraped data, including idea IDs, names, vote counts, descriptions, dates, statuses, and URLs. The data is appended to any existing data in the file.
- `comments/{id}_comments.csv`: For each idea, a separate CSV file is created in the `comments` directory. These files contain comments associated with each idea, including the comment date, name, and text.

Please note that if you rerun the script, it will not duplicate existing data in `output.csv` based on the idea ID. The script checks if an ID already exists in the file before appending new data.

## Customization

The script provides several customization options:

- `url`: The base URL of the Webflow Wishlist website. You can modify this URL if necessary.
- `max_retries`: The maximum number of retries the script attempts to retrieve a webpage in case of errors. You can adjust this value as needed.
- `retry_delay`: The delay (in seconds) between retries when encountering errors. Increase this value if you experience connection issues.
- `write_comment_csv(comment_list, id)`: Customize this function if you want to change the format or destination of the comment CSV files.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Disclaimer

This script is provided as-is and is intended for educational and informational purposes only. The usage of this script is your responsibility, and any actions you take with the scraped data should comply with the terms and policies of the Webflow Wishlist website.

Please use this script responsibly and respect the website's usage guidelines and limitations.

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## Support

If you encounter any problems or have questions regarding the Webflow Wishlist Scraper, please open an issue in the project repository.
