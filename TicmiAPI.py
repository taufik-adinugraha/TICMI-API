import requests

class TICMIDataAPI:
    def __init__(self, api_key):
        self.base_url = "https://api.ticmidata.co.id"
        self.headers = {
            'x-Auth-key': api_key
        }
        self.endpoints = {
            "index_weight": "/direct/v1/saham/dp/iw/",
            "public_expose": "/direct/v1/saham/ca/eq/",
            "board_of_commissioners": "/direct/v1/saham/cp/boc/",
            "board_of_directors": "/direct/v1/saham/cp/bod/",
            "trading_data": "/direct/v1/saham/dp/eq/",
            "market_information": "/direct/v1/saham/fdr/ip/",
            "company_profile": "/direct/v1/saham/cp/pr/",
            "company_address": "/direct/v1/saham/cp/add/",
            "holding_composition": "/direct/v1/saham/cp/hc/",
            "stock_news": "/direct/v1/news/"
        }

    def make_request(self, endpoint, params):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code, response.text

    def request_index_weight(self, startDate, endDate, indexCode):
        params_index_weight = {
            "indexCode": indexCode,
            "startDate": startDate,
            "endDate": endDate
        }
        return self.make_request(self.endpoints["index_weight"], params_index_weight)

    def request_data_by_date(self, startDate, endDate, stock, category):
        results = {}

        params_public_expose = {
            "secCode": stock,
            "startDate": startDate,
            "endDate": endDate,
            "tipeCalendar": "public-expose"
        }
        params_trading_data = {
            "secCode": stock,
            "startDate": startDate,
            "endDate": endDate,
            "granularity": "daily"
        }
        params_stock_news = {
            "filter": "emiten",
            "sort": "terbaru",
            "page": "1",
            "pageSize": "5",
            "startDate": startDate,
            "endDate": endDate
        }

        all_params_by_date = {
            "public_expose": params_public_expose,
            "trading_data": params_trading_data,
            "stock_news": params_stock_news
        }

        if category not in all_params_by_date:
            raise ValueError(f"Unrecognized category: '{category}'. Recognized categories: 'trading_data', 'stock_news', 'public_expose'")
        
        endpoint = all_params_by_date[category]
        results[category] = self.make_request(self.endpoints[category], endpoint)

        return results

    def request_static_data(self, stock, year):
        results = {}

        params_board_of_commissioners = {
            "secCode": stock
        }
        params_board_of_directors = {
            "secCode": stock
        }
        params_market_information = {
            "secCode": stock,
            "granularity": "quarterly",
            "periode": year,
            "q": "1"
        }
        params_company_profile = {
            "secCode": stock
        }
        params_company_address = {
            "secCode": stock
        }
        params_holding_composition = {
            "secCode": stock,
            "granularity": "1"
        }

        all_params_static = {
            "board_of_commissioners": params_board_of_commissioners,
            "board_of_directors": params_board_of_directors,
            "market_information": params_market_information,
            "company_profile": params_company_profile,
            "company_address": params_company_address,
            "holding_composition": params_holding_composition
        }

        for key, endpoint in all_params_static.items():
            results[key] = self.make_request(self.endpoints[key], endpoint)

        return results