import requests
import sys
import csv
import json
import os
from datetime import datetime
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo
from collections import deque
from cleaner import clean, weekly_checker, change_limit #functions from cleaner.py 
from typing import Any as any


class Collect_data():

    
    def __init__(self, city, temp, windspeed, date):

        self.city = city
        self.temp = temp
        self.windspeed = windspeed
        self.date = date


    def turn_dict(self) -> dict[str, any]:

        return {
            'city': self.city,
            'temperature': self.temp,
            'windspeed': self.windspeed,
            'date-time': self.date
        }

class Returner:
    
    def finder(self) -> None:
        lst =  []
        while True:
            
            if ' '.join(sys.argv[1:]) in ('forecast', 'average -s', 'weekly -n', 'average -d'): 
                
                if not lst:
                    self.c = input('Enter the city/country name: ').lower()

                    if self.c == 'q':
                        sys.exit()
                    lst.append(self.c)
            elif ' '.join(sys.argv[1:]) == "average":
                print('The average function must be followed by -d (days) or -s (searches)!')
                sys.exit()
            else:
                self.c = " ".join(sys.argv[1:]).lower()
                if not lst:
                    lst.append(self.c)
            
            api_1 = f'https://geocoding-api.open-meteo.com/v1/search?name={lst[0]}'
            if self.c == 'q' or self.c == 'quit':
                sys.exit('Successfully quit!')

            try:

                r = requests.get(api_1)
                j = r.json()

                try:
                    
                    for index, i in enumerate(j['results']):#list all the available cities/countries with the given name
                        print(f"{index+1}){i['name']}, {i['country']}")
                        
                except KeyError:

                    self.c = input('Invalid city/country name!\nEnter the city/country name: ')

                    if self.c != 'q':
                        sys.exit()

                    lst.pop(0)
                    lst.append(self.c)
                    continue

                while True:

                    try:
                        user: str = input("Enter the number of the intended city/country: ").lower()

                        if int(user) < 1 or int(user) > len(j['results']):#if the user chooses a number that does not match the index start the loop again
                            print('Input out of range!')
                            continue
                        break

                    except ValueError:

                        if user == "quit": sys.exit('You successfully quit the program!')
                        else:
                            print("Invalid input!")
                            continue

                self.longitude = j['results'][int(user) - 1]['longitude']#if the user chooses a number it subtract one to match everything (1 == 0, 2 == 1 and etc.)
                self.latitude = j['results'][int(user) -1]['latitude']
                return
            except requests.exceptions.RequestException:
                print("Check your connection sir!")

returner = Returner()

WEEK = [
    'Monday','Tuesday','Wednesday',
    'Thursday','Friday','Saturday',
    'Sunday'
]

MONTHS = {
        '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
        '05': 'May','06': 'Jun', '07': 'Jul','08': 'Aug',
        '09': 'Sep','10': 'Oct','11': 'Nov','12': 'Dec'
}



def forecast() -> None:
    returner.finder()
    try:
        api3 = f"https://api.open-meteo.com/v1/forecast?latitude={returner.latitude}&longitude={returner.longitude}&current_weather=true&hourly=temperature_2m,precipitation_probability&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=auto"

        r2 = requests.get(api3)
        j2 = r2.json()
        units = j2['daily']
        ind = range(1,8)
        maxt: list[float] = units['temperature_2m_max']#highest temperature
        mint: list[float] = units['temperature_2m_min']#lowest temperature

        tf = TimezoneFinder()
        zone: str|None = tf.timezone_at(
            lng=returner.longitude,
            lat=returner.latitude
        )


        current = datetime.now(ZoneInfo(zone))
        day = current.strftime('%A')#finding the day of the week with a given city/country name

        ind_day = [inde for inde,i in enumerate(WEEK) if i == day][0]#[0] at the end cuz inde returns a list and to extract a value from it we just specify the item we want    
        dates = j2['daily']['time'] 


        dict_ = {
            '01': 'st', '02': 'nd', '03': 'rd'
        }
        for k in range(4,32):
            if k < 10: dict_[f'0{k}'] = 'th'
            dict_[f'{k}'] = 'th'


        print(f'{'-'*37}\n{'Highest-Lowest'} | country -> {returner.c.capitalize()}\n{'-'*37}')

        for z,i,x,y,t in zip(ind,maxt, mint, range(7), dates):

            month: str = MONTHS[str(t[5:7])]
            day: str = t[8:10]

            y = (ind_day+y)%7#the remainder is the day of the week in sequence, if it is wednesday the ind_day is 3 and it will be added 0 first and wednesday will be given, then 1 will be added and index 4 and thursday
            if 0 < i < 10.0: i = f"0{i}"
            if 0 < x < 10.0: x = f"0{x}"


            print(f'{z}){i}°C|{x}°C || {month} {day}{dict_[day]} | {WEEK[y]}')


        print(f'{'-'*24}\nHighest-Lowest (average)\n{'-'*24}')
        print(f"{round(sum(maxt)/len(maxt), 1)}°C || {round(sum(mint)/len(mint), 1)}°C\n{'-'*24}")

    except (requests.exceptions.RequestException):
        sys.exit('Connection error!')


def get_country() -> None:
    returner.finder()
    try:
        api_2 = f'https://api.open-meteo.com/v1/forecast?latitude={returner.latitude}&longitude={returner.longitude}&current_weather=true'


        r_2 = requests.get(api_2)
        j = r_2.json()


        j = j['current_weather']
        temp = j['temperature']
        w_S = j['windspeed']
        day = j['is_day']
        date = j['time']
        
        l = '-'*26
        print(f'{l}\n{" "*3}Current temperature')
        print(f"{l}\nThe temperature is {temp}°C")
        print(f"The windspeed is {w_S} km/h")

        if day == 1: print(f'Day time\n{l}')
        else: print(f'Night time\n{l}')


        with open('kregg.csv', 'a', newline='') as f:
            columns = ['city', 'temperature', 'windspeed' ,'date-time']
            writer = csv.DictWriter(f, fieldnames=columns)
            form = Collect_data(returner.c, temp, w_S, date)
            writer.writerow(form.turn_dict())


    except requests.exceptions.RequestException:
        print("Check your connection sir!")
    except(KeyError, ValueError):
        print('City/country not found check the spelling!')



def average_search_func(directory: str, num_of_days: int, c_name: str) -> None:#an average temperature and windspeed calculator in a given number of searches from the user input
    nm = []
    tem = []
    w__s = []

    with open(directory) as f:

        reader = csv.DictReader(f)
        for i in reader:
            if i['city'] == c_name:
                nm.append(i)

        last_lines = deque(nm, maxlen=num_of_days)
        for x in last_lines:
            temp = x['temperature']
            ws = x['windspeed']
            tem.append(float(temp))
            w__s.append(float(ws))


        avgt = sum(tem)/len(tem)
        avgw = sum(w__s)/len(w__s)
        last_days = len(nm)

        if num_of_days > last_days: 
            raise ValueError #if the user input is higher than the available number of searches in csv it will raise a ValueError
        
        print(f'{'-'*29}\n{" "*2}Number of search(es) -> {num_of_days}\n{'-'*29}\nTemperature: {round(avgt,1)}°C (average)\nWindspeed: {round(avgw,1)} km/h (average)\n{'-'*29}')

def average_search_output():  
        lst = []
        while True:
            try:
                with open('kregg.csv') as f:
                    reader = csv.DictReader(f)

                    country_name = input('Enter the city/country name: ')

                    for i in reader:
                        lst.append(i['city'])

                    if country_name not in lst:
                        print('The given country does not exist!')
                        continue

                    days = input('Enter the number of searches you wanna see the average of: ').lower()
                    average_search_func('kregg.csv', int(days), country_name)

                sys.exit()
            except (ValueError,ZeroDivisionError):
                if average_search_func != 'quit':#if the user does not quit or chooses a number this error will be raised
                    print('The given city/country has not been searched this many times!')
                    continue

def set_week() -> None:

    while True:
        
        if os.path.getsize('weekly.json') == 0 or ' '.join(sys.argv[1:]) == 'weekly -n':
            returner.finder()
            try:
                api3 = f"https://api.open-meteo.com/v1/forecast?latitude={returner.latitude}&longitude={returner.longitude}&current_weather=true&hourly=temperature_2m,precipitation_probability&daily=weathercode,temperature_2m_max,temperature_2m_min&past_days=7&timezone=auto"
                r = requests.get(api3)
                j = r.json()

                tf = TimezoneFinder()
                zone: str = tf.timezone_at(
                    lng=returner.longitude,
                    lat=returner.latitude
                )

                current = datetime.now(ZoneInfo(zone))
                day: str = current.strftime('%A')#finding the day of the week with a given city/country name

                inde = [inde for inde,h in enumerate(WEEK) if h == day][0]
                maxt: list[float] = j['daily']['temperature_2m_max']
                mint: list[float] = j['daily']['temperature_2m_min']

                with open('weekly.json') as f:
                    reader = json.load(f)
                    if current.month != int(reader['configs']['starting_date'][5:7]):
                        week_num = 1
                    else:
                        week_num = reader['week_data']['week_num'] + 1

                y = len(WEEK[0:inde+1])
                starting_date = j['daily']['time'][8-y]#the date of the monday of the current week

                dict_ = {"configs":{
                            "country": returner.c,   
                            'longitude': returner.longitude,
                            'latitude': returner.latitude,
                            'starting_date': starting_date}}
                
                total1, total2 = 0,0
                for x,y,z, in zip(maxt[7-y:7+(7-y)], mint[7-y:7+(7-y)], range(len(WEEK))):#the calculation here defines the starting point on a list of temperatures and end the point of it
                    
                    total1 += x
                    total2 += y

                    dict_['week_data'] = {
                        'week_num': week_num,
                        'average_temp_max': round(total1/7, 1),
                        'average_temp_min': round(total2/7, 1)
                    }
                    dict_[WEEK[z]] = {'max': x, 'min': y}
                    
                with open('weekly.json', 'w') as f:
                    json.dump(dict_,f,indent=1)
                    break
            except requests.exceptions.RequestException:
                print("Check your connection sir!")
                break
        else:   
            with open('weekly.json') as f:
                reader = json.load(f)
                tf = TimezoneFinder()
                zone: str = tf.timezone_at(
                    lng=reader['configs']['longitude'],
                    lat=reader['configs']['latitude']
                )

                current = datetime.now(ZoneInfo(zone))
                day: str = current.strftime('%A')

            total1,total2,divider = 0,0,0   
            country = reader['configs']['country']

            print(f'{'-'*39}\n{'Highest-Lowest'} | Country -> {country.capitalize()}\n{'-'*39}')
            for g in range(len(WEEK)):

                if WEEK[g] == day:
                    is_today = "<- today"
                else:
                    is_today = ''

                i = reader[WEEK[g]]['max']
                x = reader[WEEK[g]]['min']
                total1 += i
                total2 += x
                divider += 1
                if 0 < i < 10.0: i = f'0{i}'
                if 0 < x < 10.0: x = f"0{x}"
                
                print(f'{g+1}){i}°C || {x}°C | {WEEK[g]} {is_today}')

            print(f'{'-'*39}\n{'Highest-Lowest (average)'}\n{'-'*39}')
            print(f'{round(total1/divider, 1)}°C || {round(total2/divider, 1)}°C | Number of weeks -> {reader['week_data']['week_num']}\n{'-'*39}')
            break


def average_day_func() -> None:
    returner.finder()

    print(f'{'~'*48}\n{' '*17}How many days?\n{'~'*48}')
    num_days = int(input(f"> "))

    api = f"https://api.open-meteo.com/v1/forecast?latitude={returner.latitude}&longitude={returner.longitude}&current_weather=true&hourly=temperature_2m,precipitation_probability&daily=weathercode,temperature_2m_max,temperature_2m_min&past_days={num_days}&timezone=auto&forecast_days=0"
    r = requests.get(api)
    j = r.json()

    maxt: list[float] = j['daily']['temperature_2m_max']
    mint: list[float] = j['daily']['temperature_2m_min']

    average_max = round(sum(maxt)/len(maxt), 1)
    average_min = round(sum(mint)/len(mint), 1)

    print(f'{"="*24}\n{" "*8}Average\n{"="*24}\n{" "*4}{average_max}°C || {average_min}°C\n{"="*24}\n{' '*8}Each day\n{"="*24}')
    for i,x,y in zip(maxt,mint, range(0,7)):
        print(f"{' '}{y+1}. {i}°C || {x}°C")
    print(f'{'='*24}\n{' '*4}Num of days -> {num_days}\n{'='*24}')

def display_saved():#a function to read the csv file without having to go inside of the file 
    with open('kregg.csv') as f:
        for i in f:
            print(i, end='')

command_lst = [
               'forecast - to see the projected temperature and the windspeed in the upcoming 7 days',
               'weekly - set weekly tracker if not set yet, if set already returns the set weekly with data',
               '<name of country/city> - to see the current temperature of the searched city/country, saves the info to .csv',
               'average -s - to see the average temperature and the windspeed in a certain number of searches',
               'average -d - to see the average temperature and the windspeed in a certain number of days',
               'weekly -n - set a new city/country for the weekly function',
               'limit -c - change the limit of the csv searches',
               'saved - to see the csv file from the terminal',
               '-h - to list all the functions'
               ]

funcs = {
    'average -s': average_search_output,
    'saved': display_saved,
    'forecast': forecast,
    'weekly': set_week,
    'limit -c': change_limit,
    'average -d': average_day_func,
    '-h': lambda : [print('*',i) for i in command_lst]
}

def main():
    if len(sys.argv) < 2:
        sys.exit("Not enough arguments on the terminal!\n-h for for help")
    command = funcs.get(" ".join(sys.argv[1:]))
    if command:
        command()
    else:
        get_country()

if __name__ == "__main__":
    weekly_checker()
    main()
    clean()