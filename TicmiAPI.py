import requests

class TICMIDataAPI:
    def __init__(self, api_key):
        self.base_url = "https://api.ticmidata.co.id"
        self.headers = {
            'x-Auth-key': api_key
        }
        self.endpoints = {
            "trading_data": "/direct/v1/saham/dp/eq/",
            "index": "/direct/v1/saham/dp/ix/",
            "index_weight": "/direct/v1/saham/dp/iw/",
            "stock_news": "/direct/v1/news/eq",
            "corporate_action": "/direct/v1/saham/ca/eq/",
            "income_statement": "direct/v1/saham/lk/is/",
            "balance_sheet": "direct/v1/saham/lk/bs/",
            "cash_flow": "direct/v1/saham/lk/cf/",
            "financial_ratios": "direct/v1/saham/fdr/rk/",
            "market_information": "direct/v1/saham/fdr/ip/",
            "board_of_commissioners": "/direct/v1/saham/cp/boc/",
            "board_of_directors": "/direct/v1/saham/cp/bod/",
            "company_profile": "/direct/v1/saham/cp/pr/",
            "company_address": "/direct/v1/saham/cp/add/",
            "holding_composition": "/direct/v1/saham/cp/hc/",
            "share_holders": "/direct/v1/saham/cp/sh/"
        }

    def make_request(self, endpoint, params):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code, response.text

    def index(self, startDate, endDate, indexCode):
        params = {
            "indexCode": indexCode,
            "startDate": startDate,
            "endDate": endDate,
            "granularity": "daily"
        }
        return self.make_request(self.endpoints["index"], params)

    def index_weight(self, startDate, endDate, indexCode):
        params = {
            "indexCode": indexCode,
            "startDate": startDate,
            "endDate": endDate
        }
        return self.make_request(self.endpoints["index_weight"], params)

    def trading(self, startDate, endDate, stock):
        params = {
            "secCode": stock,
            "startDate": startDate,
            "endDate": endDate,
            "granularity": "daily"
        }
        return self.make_request(self.endpoints["trading_data"], params)

    def corporate_action(self, startDate, endDate, stock, action_type):
        action_types = ['ipo', 'public_expose', 'rups', 'rupslb', 'dividen', 'stock-bonus', 'stock_split', 'right', 'waran', 'konversi-waran']
        if action_type not in action_types:
            print(f"recognized action_type: {action_types}")
        else:
            params = {
                "secCode": stock,
                "startDate": startDate,
                "endDate": endDate,
                "tipeCalendar": action_type
            }
            return self.make_request(self.endpoints["corporate_action"], params)

    def stock_news(self, startDate, endDate, stock):
        params = {
            "secCode": stock,
            "startDate": startDate,
            "endDate": endDate,
            "page": "1",
            "pageSize": "20",
        } 
        return self.make_request(self.endpoints["stock_news"], params)

    def financial_report(self, stock, year, quarter, report_type):
        report_types = ["income_statement", "balance_sheet", "cash_flow", "financial_ratios"]
        if report_type not in report_types:
            print(f"recognized action_type: {report_types}")
        else:
            params = {
                "secCode": stock,
                "granularity": "Quarterly",
                "periode": str(year),
                "q": str(quarter),
            }
            return self.make_request(self.endpoints[report_type], params)

    def market_information(self, stock, year, quarter):
        params = {
            "secCode": stock,
            "granularity": "Quarterly",
            "periode": str(year),
            "q": str(quarter),
        }
        return self.make_request(self.endpoints["market_information"], params)

    def static_data(self, stock):
        results = {}
        param = {
            "secCode": stock
        }
        params_holding_composition = {
            "secCode": stock,
            "granularity": "1"
        }
        all_params_static = {
            "board_of_commissioners": param,
            "board_of_directors": param,
            "company_profile": param,
            "company_address": param,
            "holding_composition": params_holding_composition,
            "share_holders": param,
        }
        for key, params in all_params_static.items():
            results[key] = self.make_request(self.endpoints[key], params)
        return results