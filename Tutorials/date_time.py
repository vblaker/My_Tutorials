# This example explains date manipulations
import datetime
import calendar

# Create new object
now = datetime.datetime.now()
CurrentDate = datetime.date.today()

print("Today is: %s" % datetime.datetime.today())
print("Today is: {}: ".format(datetime.datetime.today()))

print("Current date and time using str method of datetime object: {}".format(now))

print('Current date and time using instance attributes:')
print('Current year: %d' % now.year)
print("Current month: %d" % now.month)
print("Current day: %d" % now.day)
print("Current hour: %d" % now.hour)
print("Current minute: %d" % now.minute)
print("Current second: %d" % now.second)
print("Current microsecond: %d" % now.microsecond)

print("Current date and time using strftime:")
print(now.strftime("%Y-%b-%d %H:%M:%S:%f"))
print(now.strftime("%Y-%m-%d %H:%M"))

print(calendar.isleap(now.year))
