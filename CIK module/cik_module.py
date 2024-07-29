import requests
import json

class CIKLookup:
    COMPANY_TICKERS_URL = 'https://www.sec.gov/files/company_tickers.json'
    COMPANY_TICKERS_EXCHANGE_URL = 'https://www.sec.gov/files/company_tickers_exchange.json'
    COMPANY_TICKERS_MF_URL = 'https://www.sec.gov/files/company_tickers_mf.json'

    def __init__(self):
        self.name_to_cik_map = {}
        self.ticker_to_cik_map = {}
        self._fetch_data()

    def _fetch_data(self):
        headers = {
            'User-Agent': 'YourCompanyName AdminContact@yourcompany.com',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.sec.gov'
        }

        # Fetch data from the URLs
        company_tickers_response = requests.get(self.COMPANY_TICKERS_URL, headers=headers)
        company_tickers_exchange_response = requests.get(self.COMPANY_TICKERS_EXCHANGE_URL, headers=headers)
        company_tickers_mf_response = requests.get(self.COMPANY_TICKERS_MF_URL, headers=headers)

        company_tickers = company_tickers_response.json()
        company_tickers_exchange = company_tickers_exchange_response.json()
        company_tickers_mf = company_tickers_mf_response.json()

        # Helper function to process each ticker info
        def process_ticker_info(ticker_info):
            if isinstance(ticker_info, dict):
                cik = ticker_info.get('cik_str')
                name = ticker_info.get('title')
                ticker = ticker_info.get('ticker')
                exchange = ticker_info.get('exchange', None)  # Some entries may not have 'exchange'
                series = ticker_info.get('series', None)      # Some entries may not have 'series'
                class_info = ticker_info.get('class', None)   # Some entries may not have 'class'
                
                if cik and name and ticker:
                    if exchange:
                        self.name_to_cik_map[name.lower()] = (cik, name, ticker, exchange)
                        self.ticker_to_cik_map[ticker.lower()] = (cik, name, ticker, exchange)
                    elif series and class_info:
                        self.name_to_cik_map[series.lower()] = (cik, series, class_info, ticker)
                        self.ticker_to_cik_map[ticker.lower()] = (cik, series, class_info, ticker)
                    else:
                        self.name_to_cik_map[name.lower()] = (cik, name, ticker)
                        self.ticker_to_cik_map[ticker.lower()] = (cik, name, ticker)

        # Process each ticker info in the fetched data
        for ticker_info in company_tickers.values():
            process_ticker_info(ticker_info)

        for ticker_info in company_tickers_exchange.values():
            process_ticker_info(ticker_info)

        for ticker_info in company_tickers_mf.values():
            process_ticker_info(ticker_info)

    def name_to_cik(self, name):
        return self.name_to_cik_map.get(name.lower(), None)

    def ticker_to_cik(self, ticker):
        return self.ticker_to_cik_map.get(ticker.lower(), None)

# Example usage
if __name__ == "__main__":
    cik_lookup = CIKLookup()
    print(cik_lookup.name_to_cik('Apple Inc.'))  # Replace 'Apple Inc.' with the company name you want to look up
    print(cik_lookup.ticker_to_cik('AAPL'))  # Replace 'AAPL' with the ticker you want to look up
