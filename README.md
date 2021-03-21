## Time Code Tracker

TOL 2: Electric Boogaloo


## My Stuff

Models:
- Event:
	- id
	- name
	- start
	- end
	- charge code
		- A foreign key to ChargeCode


Views:
- Holidays
	- Prepopulate “Event” at start of every month
- Pay Period

Event
Charge Code
User

Note charge codes that contribute to billability:
- B
- F
- T
- M (some)
- Make the above checked by default

## Aarons Stuff

Table Labor
- Description
- Charge Number

Table Hours Per Month
- Hours (manually update)
- Start date
- end date

Table Task Authorization
- Allocated hours
- Start date
- end date
- charge number
	- A foreign key to table labor

Table Tax Location
- Abbreviation (HAWA)
- State

Table Time Entry
- Charge number
	- foreign key to labor
- entry date
- start time
- end time
- tol time (work time)
- telework
- tax location
	- foreign key to Tax Location
- notes


Notes:
- Add time off, holiday, and placeholder
- Mid month for separating pay periods
