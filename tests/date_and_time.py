from datetime import datetime
import time

"""Gets a valid start date and time from the user"""
	
#Prompts user to enter date. Repeat until vaild entry.
while True:
	startdate = raw_input("Enter start date (mm/dd/yyyy): ")
	try:
	  valid_date = time.strptime(startdate, '%m/%d/%Y')
	  break
	except ValueError:
	  print "Invalid date!"
		
#Prompts user to enter time. Repeat until vaild entry.
while True:
	starttime = raw_input("Enter start time (hh:mm AM/PM): ")
	try:
	  valid_time = time.strptime(starttime, '%I:%M %p')
	  break
	except ValueError:
	  print "Invalid time!"

#Creates datetime string
startdatetime = str(startdate + " " + starttime)
print startdatetime

"""Uses start date to get end date --> One day after start at 12AM"""

month, day = startdatetime.split("/",1)
day, year = day.split("/",1)
year, time = year.split(" ", 1)

day = int(day) + 1
day = str(day)

enddate = month + "/" + day + "/" + year

endtime = "12:00:00 AM"

print enddate

enddatetime = str(enddate + " " + endtime)

print enddatetime