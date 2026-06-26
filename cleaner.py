from timezonefinder import TimezoneFinder
from datetime import datetime
from zoneinfo import ZoneInfo
from constants import WEEK
import csv
import json
import requests
import calendar


def return_lst():
    with open('kregg.csv') as f:
        lst = []
        reader = csv.DictReader(f)
        
        for i in reader:
            lst.append(i)

        return lst

lst = return_lst()
columns = ['city', 'temperature', 'windspeed', 'date-time']


def change_limit():
    with open('configs.json') as f:
        r = json.load(f)

    current_limit = r['user']['limit']
    user = int(input(f'Enter the new limit (current limit -> {current_limit}): '))

    if user < current_limit and len(lst) > user:
        del lst[0:len(lst)-user]

    r = {
        'user': {'limit': user}
    }

    with open('configs.json', 'w') as f:
        json.dump(r,f,indent=3)

    with open('kregg.csv', 'w', newline='') as f:#writing over the csv after storing everything to a list and modifying it
        
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()

        for i in lst:
            writer.writerow(i)

def clean():
    lines = []

    with open('kregg.csv') as f:

        reader = csv.DictReader(f)
        for i in reader:
            lines.append(i)
        
        with open('configs.json') as f:
            reader = json.load(f)
            user_limit = reader['user']['limit']

        if len(lines) > user_limit:#if the number of searches exceed 30 delete one from the top of csv file
            lines.pop(0)#remove the first item

    with open('kregg.csv', 'w', newline='') as f:#writing over the csv after storing everything to a list and modifying it
        
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()

        for i in lines:
            writer.writerow(i)

def weekly_checker():
    with open('weekly.json') as f:
        reader = json.load(f)
        
        tf = TimezoneFinder()
        zone = tf.timezone_at(
            lng=reader['configs']['longitude'],
            lat=reader['configs']['latitude']
        )

        current = datetime.now(ZoneInfo(zone))

        day = current.strftime('%A')#finding the day of the week with a given city/country name
        inde = [inde for inde,h in enumerate(WEEK) if h == day][0]
        y = len(WEEK[0:inde+1])

        api3 = f"https://api.open-meteo.com/v1/forecast?latitude={reader['configs']['latitude']}&longitude={reader['configs']['longitude']}&current_weather=true&hourly=temperature_2m,precipitation_probability&daily=weathercode,temperature_2m_max,temperature_2m_min&past_days=7&timezone=auto"
        r = requests.get(api3)
        j = r.json()
        starter = j['daily']['time']

        year = int(starter[7-y][0:4])
        month = current.month - 1 if current.month != 1 else 12
        days = calendar.monthrange(year, month)[1]

        end_month_dict = {
            '28':5,
            '29':6,
            '30':7,
            '31':8
        }
        
        starting_date = starter[end_month_dict[str(days)] - y]

        try:

            if reader['configs']['starting_date'] not in j['daily']['time']:   

                maxt: list[float] = j['daily']['temperature_2m_max']
                mint: list[float] = j['daily']['temperature_2m_min']
                
                week_num = 1 if current.month != int(reader['configs']['starting_date'][5:7]) else reader['week_data']['week_num'] + 1
                
                dict_ = {"configs":{
                            "country": reader['configs']['country'],
                            'longitude': reader['configs']['longitude'],
                            'latitude': reader['configs']['latitude'],
                            'starting_date': starting_date}}

                for x,y,z, in zip(maxt[7-y:7+(7-y)], mint[7-y:7+(7-y)], range(len(WEEK))):
                        total1, total2 = 0,0
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
                      
        except KeyError:
            pass