import messari


messari.get_metrics()

##############################
# case 1: getting close price data
assets = ["uni", "aave", "luna", "cake", "mkr"]
start_date = "2020-12-25"
end_date = "2020-12-29"
metric = 'price'
parameter='close'
print("function call as intended")
print(f"metic: '{metric}' parameter: '{parameter}'")
df = messari.get_historical_data(assets=assets, metric=metric, start_date=start_date, end_date=end_date, parameter=parameter)
print(df)
print()

##############################
# case 2: getting volume price data
assets = ["uni", "luna", "cake"] # less assets to avoid rate limit
parameter='volume'
print("function call intended with new parameter")
print(f"metic: '{metric}' parameter: '{parameter}'")
df = messari.get_historical_data(assets=assets, metric=metric, start_date=start_date, end_date=end_date, parameter=parameter)
print(df)
print()

##############################
# case 3: getting price data w/ a bad parameter specified
parameter='whoops'
print("function call with a bad parameter")
print(f"metic: '{metric}' parameter: '{parameter}'")
df = messari.get_historical_data(assets=assets, metric=metric, start_date=start_date, end_date=end_date, parameter=parameter)
print(df)
print()

##############################
# case 4: getting data w/ a bad metric specified
metric = 'whoops'
print("function call with a bad metric")
print(f"metic: '{metric}' parameter: '{parameter}'")
df = messari.get_historical_data(assets=assets, metric=metric, start_date=start_date, end_date=end_date, parameter=parameter)
print(df)
print()

##############################
# case 5: getting data w/ a new metric
# NOTE: this metric doesn't exist for cake and the code will skip cake appropriately
metric = 'mcap.circ'
parameter = 'circulating_marketcap'
print("function call with new metric & parameter, skips asset which metric doesn't apply to (cake)")
print(f"metic: '{metric}' parameter: '{parameter}'")
df = messari.get_historical_data(assets=assets, metric=metric, start_date=start_date, end_date=end_date, parameter=parameter)
print(df)
print()
