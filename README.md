
# KupujemProdajem Ad Scraper & Notifier

A small web scraping project built for hands-on practice, designed around a real-world use case.

Resellers who look for underpriced second-hand items need to act fast, since the best deals disappear within minutes. This scraper monitors a marketplace category and sends an instant notification the moment a new listing goes up, giving the user a head start over other buyers. This example targets **KupujemProdajem**, the largest marketplace in Serbia, tracking iPhone devices and accessories. The approach generalizes easily to other categories or platforms with minor changes to the search parameters and parsing logic.

## How it works

1. Scrapes the first few pages of search results (sorted by newest) every 2 minutes
2. Compares newly scraped listings against a locally stored database of known ads
3. Sends a Telegram message for each newly detected listing, including title, price, and link
4. Updates the local database to prevent duplicate notifications

## Tech stack

- **Python**: core application logic
- **Requests**: HTTP requests and session handling
- **BeautifulSoup**: HTML parsing and data extraction
- **Telegram Bot API**: real-time push notifications
- **JSON**: lightweight local persistence for tracked listings

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install requests beautifulsoup4 pandas python-dotenv
   ```
3. Create a `.env` file in the project root with your Telegram bot credentials:
   ```
   TELEGRAM_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```
   (Create a bot via [@BotFather](https://t.me/BotFather) on Telegram to obtain a token.)
4. Run the script:
   ```bash
   python scraper.py
   ```
## Example

New listing on KupujemProdajem:

![New ad](ss/ad.jpeg)

Instant Telegram notification:

![Telegram notification](ss/message.jpg)

## Configuration

The search keyword, category filters, and number of pages scraped per cycle can be adjusted directly in the script to target different products or marketplaces.

## Notes

This script runs continuously (`while True`) and checks for new listings every 2 minutes by default. The interval can be tuned depending on how time-sensitive the target category is, while keeping request frequency reasonable.
