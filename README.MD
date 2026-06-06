# Weather App
A command-line weather application that provides current weather, forecasts, and historical data retrieval using the Open-Meteo API.
 
## Features
*   Fetches current temperature and wind speed for any city worldwide.
*   Displays a full 7-day forecast with daily high/low temperatures.
*   Includes a weekly tracker that automatically updates each week. You only need to set the country once.
*   Calculates the average temperature and wind speed from a specified number of recent searches for a city.
*   Calculates the average temperature and wind speed from a given number of days by the user for a city/country. 
*   Logs all searches to `kregg.csv`, which is automatically cleaned to retain only the last certain number of entries set by the user in the `configs.json`.
## Usage
 
**Get current weather:**
```sh
python app.py <city_name>
```
```
--------------------------
   Current temperature
--------------------------
The temperature is 16.0°C
The windspeed is 8.1 km/h
Night time
--------------------------
```
 
---
 
**Get a 7-day forecast:**
```sh
python app.py forecast
```
```
-------------------------------------
Highest-Lowest | country -> Samarkand
-------------------------------------
1)24.4°C|12.9°C || May 01st | Friday
2)19.3°C|13.2°C || May 02nd | Saturday
3)20.0°C|11.1°C || May 03rd | Sunday
4)22.6°C|10.9°C || May 04th | Monday
5)24.9°C|12.0°C || May 05th | Tuesday
6)27.8°C|13.4°C || May 06th | Wednesday
7)29.8°C|14.7°C || May 07th | Thursday
------------------------
Highest-Lowest (average)
------------------------
24.1°C || 12.6°C
------------------------
```
 
---
 
**View the weekly tracker:**
```sh
python app.py weekly
```
```
---------------------------------------
Highest-Lowest | Country -> Samarkand
---------------------------------------
1)26.1°C || 14.6°C | Monday
2)21.8°C || 11.5°C | Tuesday
3)26.0°C || 13.4°C | Wednesday
4)26.6°C || 14.2°C | Thursday
5)27.6°C || 14.3°C | Friday <- today
6)24.0°C || 13.6°C | Saturday
7)20.7°C || 12.6°C | Sunday
---------------------------------------
Highest-Lowest (average)
---------------------------------------
24.7°C || 13.5°C | Number of weeks -> 4
---------------------------------------
```
 
---
 
**See the average temperature of the last N days:**
```sh
python app.py average -d
```
```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                 How many days?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
> 3
========================
        Average
========================
    23.4°C || 12.1°C
========================
        Each day
========================
 1. 22.2°C || 11.1°C
 2. 22.7°C || 12.4°C
 3. 25.4°C || 12.9°C
========================
    Num of days -> 3
========================
```
 
---
 
**Calculate average from past searches of a certain city or country:**
```sh
python app.py average -s
```
```
Enter the number of searches you wanna see the average of: 3
-----------------------------
  Number of search(es) -> 3
-----------------------------
Temperature: 18.3°C (average)
Windspeed: 9.7 km/h (average)
-----------------------------
```
 
---
 
**Change the search log limit:**
```sh
python app.py limit -c
```
 
---
 
**View all commands:**
```sh
python app.py -h
```

---

**Set a new city for the weekly tracker:**
```sh
python app.py weekly -n
```
