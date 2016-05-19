# countdown_to_from_any_date
Displays a percentage of a way between two dates, or count down to a date, or a count since a certain date


#### count(startlist=None, endlist=None, kind="percentage", pdec=8, cunit="days"):

    Displays a percentage of a way between two dates, or count down to a date, or a count since a certain date

    :param startlist: list of integers [year, month, day, hour, minute, second]
                      defining the start of the count down

    :param endlist: list of integers [year, month, day, hour, minute, second]
                    defining the start of the count down

    :param kind: string, kind of count down, kinds are:
                    - "percentage"
                    - "count down"
                    - "count since"

    :param pdec: integer, number of decimal places to use in result

    :param cunit: string, units to use in count downs:
                    - "years"
                    - "months"
                    - "days"
                    - "hours"
                    - "minutes"
                    - "seconds"
