import os
import datetime

from config import production_config

email_file = 'result.html'


def parse_day(days: list):
    today = datetime.datetime.today()
    print('today:', today)
    for day in days:
        remind_day = datetime.datetime.strptime(day['date'], '%Y-%m-%d')
        this_year_remind_day = datetime.datetime(today.year, remind_day.month, remind_day.day)
        timedelta = this_year_remind_day - datetime.datetime.today()
        day['timedelta'] = timedelta.days
        if day['offset'] >= timedelta.days >= 0:
            result.append(day)


def write_mail(content: list):
    with open(email_file, 'w') as f:
        f.write('NOTICE:\n')
        for item in content:
            if item['timedelta']:
                text = '%s(%s) is coming in %d days!\n' % (item['title'], item['date'], item['timedelta'])
            else:
                text = 'Today is %s(%s)!\n' % (item['title'], item['date'])
            f.write(text)


if __name__ == '__main__':
    result = []
    print("days", production_config.days)
    parse_day(production_config.days)
    print('result', result)
    if result:
        print('send email')
        write_mail(result)
    else:
        print('if no notification, remove email_file')
        if os.path.exists(email_file):
            os.remove(email_file)
