from typing import List, Dict
import requests
import datetime
import pandas as pd

# Set up logging
import logging
FORMAT="[%(asctime)s] [%(levelname)s] <%(funcName)s> %(message)s"
logging.basicConfig(format=FORMAT, encoding='utf-8')
logger = logging.getLogger('messari_log')
#logger.setLevel(logging.INFO) # Uncomment for more prints

# API KEY
API_KEY='c97a02e4-4073-4eb4-b449-412cafa15247'

def get_metrics() -> List[str]:
    """Returns a list of metrics available as messari endpoints"""

    # Get response from messari metrics endpoint
    logger.info("retriving metrics")
    metrics_url=f"https://data.messari.io/api/v1/assets/metrics"
    headers = {'x-messari-api-key' : API_KEY}
    response=requests.get(metrics_url, data=headers).json()

    # Check for data
    if "data" not in response.keys():
        logger.error("Error in endpoint, data not found in response, printing response")
        print(response)
        return None

    # Grab metrics from resposne
    messari_metrics=response["data"]["metrics"]
    metrics = []
    for metric in messari_metrics:
        metrics.append(metric["metric_id"])
    return metrics

def get_historical_data(assets: List[str], metric: str, start_date: str, end_date: str, parameter: str=None) -> pd.DataFrame:
    """Returns a DataFrame of historical data for:
        assets: list of assets to retrieve data for
        metric: metric to get historical data for
        start_date: desired start date for data, format "YYYY-MM-DD"
        end_date: desired end date for data, format "YYYY-MM-DD"
        parameter (optional): Most metrics have multiple parameters (eg price can be high, low, open, close, or volume) this optional arg can be used to specify the parameter"""

    # Scrub input incase it is a single asset as a string not a list 
    assets = [assets] if type(assets) == str else assets

    # Loop through assets
    asset_data = {} # dict for data of each asset
    index=None
    for asset in assets:

        # Get data from endpoint
        logger.info("getting historical {} data for {}".format(metric, asset)) #NOTE, have to do oldschool formating inside of logger
        url=f"https://data.messari.io/api/v1/assets/{asset}/metrics/{metric}/time-series?end={end_date}&start={start_date}&interval=1d&timestamp-format=unix-milliseconds&x-messari-api-key={API_KEY}"
        response = requests.get(url).json()


        # Check for data
        if "data" not in response.keys():
            logger.error("Error in endpoint, data not found in response, printing response")
            print(response)
            return None

        data=response["data"]

        # Get index for finding relevant parameter inside of return data
        parameters=data["parameters"]["columns"]
        if index == None:
            if parameter != None: # 
                if parameter in parameters:
                    index = parameters.index(parameter)
                    logger.info("found parameter " + parameter + " at index " + str(index) + " of values")
                else:
                    index=1
                    logger.warning("Parameter " + parameter + " not found in available parameters, reading return values at index 1")
                    logger.info("Available parameters are {}".format(parameters)) #NOTE, getting wild with formatting but it had to be done
            else:
                index=1
                logger.info("No parameter specificed, reading return values at index 1")


        val = []
        dates = []
        values=data["values"]
        if values != None: # Check if empty data
            for value in values: # Get each value from the lists

                # Get timestamp and relevant parameter from value
                unix_milliseconds = value[0]
                val.append(value[index])
                dates.append(datetime.datetime.fromtimestamp(unix_milliseconds/1000).date()) # Convert from unix_milliseconds to date

            asset_data[asset] = val
            asset_data['date'] = dates
        else:
            logger.warning("Empty set of values returned for {}, skipping".format(asset))


    # Create & format dataframe
    df = pd.DataFrame(data=asset_data)
    df = df.set_index('date')
    df.index.name = None

    return df

if __name__ == "__main__":
    print(get_metrics())
