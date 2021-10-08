# Messari API

## Instructions
You should be able to get any needed packages with this. I used python3.9 for this but you can probably get this to work with any python >= 3.5
```
$> python3.9 -m pip install -r requirments.txt
```
Then you can run a short demo I created
```
$> python3.9 demo.py
```

## Playing with the code
To demonstrate this code I tried to recreate the end user experience. All of the code needed to get historical data for any messari metric is contained in messari.py

The end user can enter the following lines into their python work and have access to the two functions I've made
```
import messari

# Get a list of available messari metrics
messari.get_metrics()

# Get historical data for any metric and parameter
messari.get_historical_data(...)
```
Feel free to mess with demo.py to try different things

## Notes
Maybe my code is wrong but i've noticed that start date and end date for the messari end points are shifted by one day? In demo.py I define the range of dates from the 25th to the 29th and get data returned from the 24th to the 28th. I could add a day to the user inputs but I'm not sure if I would be missing some nuance to the API.

There is also a typo in the messari API docs [here](https://messari.io/api/docs#operation/Get%20Asset%20timeseries). The timestamp-format specifies "unix-millisecond". The real API endpoint is acutally "unix-milliseconds".
