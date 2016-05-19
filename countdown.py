
from datetime import datetime
from calendar import timegm
import time
import os
import sys
import Tkinter as tk

# ==============================================================================
# Define variables
# ==============================================================================
# define starting date
startyear = 2015
startmonth = 03
startday = 01
starthour = 12
startminute = 0
startsecond = 0
# define end date
endyear = 2018
endmonth = 9
endday = 01
endhour = 12
endminute = 0
endsecond = 0
# kind of count down
# kinds are:
#           - "percentage"
#           - "count down"
#           - "count since"
countdowntype = "count down"
# define the number of decimal places for percent
percent_decimals = 8
# define whether we want the count down in years, months, days, hours,
# minutes or seconds
countdown_units = "days"
# use gui
gui = True


# ==============================================================================
# Define functions
# ==============================================================================
def percentage(it1, total, message, ptype=None):
    """
    ===========================================================================
    Displays percentage bar
    ===========================================================================
    Displays a simple message followed by a updating percentage
    bar, for use inside a loop, variables are as follows:

     - Format:
        percentage(it1, total, message, ptype)

            it1 (INT) is the iteration number of the loops

            total (INT) is the total number of iterations of the loop

            message (STRING) is displayed as follows:
                "[message] ...0%"
                "[message] ...50%"
                "[message] ...100%"

            ptype (STRING) is the format in which to return the percentage.
                Current accepted formats are:

                'i'         - returns percentage in integer form

                    message ...12%

                'f0'         - returns percentage in integer form

                    message ...12%

                'f2'         - returns percentage to two decimal places

                    message ...12.34%

                'f4'         - returns percentage to four decimal places

                    message ...12.3456%

                'bar'      - returns a loading percentage bar:

                    Loading =================================================

                None/Other  - returns percentage to six decimal places
    """
    percent = (float(it1) / float(total)) * 100.0
    if ptype == 'i':
        sys.stdout.write("\r" + message + "...%d%%" % percent)
        sys.stdout.flush()
    elif ptype == 'f0':
        sys.stdout.write("\r" + message + "...%.0f%%" % percent)
        sys.stdout.flush()
    elif ptype == 'f2':
        sys.stdout.write("\r" + message + "...%.2f%%" % percent)
        sys.stdout.flush()
    elif ptype == 'f4':
        sys.stdout.write("\r" + message + "...%.4f%%" % percent)
        sys.stdout.flush()
    elif ptype == 'bar':
        for j1 in range(1, 50):
            if round(percent) == float(j1 * 2.0):
                sys.stdout.write("\r" + "Loading (%.2f%%)" % percent + "=" * j1)
                sys.stdout.flush()
    else:
        sys.stdout.write("\r" + message + "...%.6f%%" % percent)
        sys.stdout.flush()


def unix_time(dttm=None):
    """
    converts date time objects to unix times
    taken from http://stackoverflow.com/a/22918717

    Note: if you pass in a naive dttm object it's assumed to already be in UTC

    :param dttm: date time object (see from datetime import datetime)
    :return:
    """
    if dttm is None:
       dttm = datetime.utcnow()
    return timegm(dttm.utctimetuple())


def count(startlist=None, endlist=None, kind="percentage",
          pdec=8, cunit="days"):
    """
    Displays a percentage of a way between two dates, or count down to a date,
    or a count since a certain date

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

    :return:
    """
    # deal with start and end
    if startlist is None:
        start = unix_time()
    else:
        start = unix_time(datetime(*startlist))
    if endlist is None:
        end = unix_time()
    else:
        end = unix_time(datetime(*endlist))

    convert = dict(years=365.25 * 24 * 3600.0,
                   months=365.25 * 24 * 3600 / 12.0,
                   days=24 * 3600.0,
                   hours=3600.0,
                   minutes=60.0,
                   seconds=1.0)

    fmt = '{0:02.0f}-{1:02.0f}-{2:02.0f} '
    fmt += '{3:02.0f}:{4:02.0f}:{5:02.2f}'
    # run code to produce count down
    os.system("clear")

    if kind in ["percentage", "pc", r"%"]:
        title = '\tPercentage From ' + fmt.format(*startlist)
        title += ' To ' + fmt.format(*endlist)
        print ('\n{0}\n{1}\n{0}\n\n'.format('=' * 50, title))
        while 1:
            tick1 = unix_time()
            # display percentage
            percentage(tick1 - start, end - start, "\t",
                       ptype="f{0}".format(pdec))
            # wait 0.1 seconds to go again
            time.sleep(0.1)
    elif kind == "count down":
        units = convert[cunit]
        title = '\tCount down to ' + fmt.format(*endlist)
        print ('\n{0}\n{1}\n{0}\n\n'.format('=' * 50, title))
        while 1:
            start = unix_time()
            msg = '\t{0:,.8f} {1}'.format((end - start)/units, cunit)
            sys.stdout.write("\r" + msg)
            sys.stdout.flush()
            # wait 0.1 seconds to go again
            time.sleep(0.1)
    else:
        units = convert[cunit]
        title = '\tTime since ' + fmt.format(*startlist)
        print ('\n{0}\n{1}\n{0}\n\n'.format('=' * 50, title))
        while 1:
            end = unix_time()
            msg = '\t{0:,.8f} {1}'.format((end - start) / units, cunit)
            sys.stdout.write("\r" + msg)
            sys.stdout.flush()
            # wait 0.1 seconds to go again
            time.sleep(0.1)


class App(tk.Frame):
    def __init__(self, master=None):
        # start display
        tk.Frame.__init__(self, master)
        self.parent = master

        self.width = 640
        self.height = 360

        self.parent.minsize(width=self.width, height=self.height)

        self.can = tk.Canvas(self.parent, bg='red', height=self.height,
                             width=self.width)
        self.can.place(x=0, y=0, anchor=tk.NW)

        self.create_widgets()


    def create_widgets(self):
        self.kind = countdowntype
        self.cunit = countdown_units
        self.pdec = percent_decimals
        startlist, endlist = startl, endl
        # deal with start and end
        if startlist is None:
            self.start = unix_time()
        else:
            self.start = unix_time(datetime(*startlist))
        if endlist is None:
            self.end = unix_time()
        else:
            self.end = unix_time(datetime(*endlist))

        self.convert = dict(years=365.25 * 24 * 3600.0,
                            months=365.25 * 24 * 3600 / 12.0,
                            days=24 * 3600.0,
                            hours=3600.0,
                            minutes=60.0,
                            seconds=1.0)
        fmt = '{0:02.0f}-{1:02.0f}-{2:02.0f} '
        fmt += '{3:02.0f}:{4:02.0f}:{5:02.2f}'

        # sort out the title
        if self.kind in ["percentage", "pc", r"%"]:
            title = '\tPercentage From ' + fmt.format(*startlist)
            title += ' To ' + fmt.format(*endlist)
        elif self.kind == "count down":
            title = '\tCount down to ' + fmt.format(*endlist)
        else:
            title = '\tTime since ' + fmt.format(*startlist)

        self.parent.title(title)

        self.QUIT = tk.Button(self.can, text="QUIT", fg="red",
                              command=root.destroy)
        self.QUIT.place(x=self.width/2.0, y=self.height, anchor=tk.S)

        self.msg = tk.StringVar()
        self.clock = tk.Label(self.can, font=('Helvetica', 24))
        # self.clock.pack(side="top")
        self.clock.place(x=self.width/2.0, y=self.height/2.0,
                         anchor=tk.CENTER)
        self.clock["textvariable"] = self.msg

        # now call update clock
        self.update_clock()



    def update_clock(self):
        if self.kind in ["percentage", "pc", r"%"]:
            tick1 = unix_time()
            # display percentage
            num = float(tick1 - self.start)
            denom = float(self.end - self.start)
            percent = (num/denom) * 100.0
            msg = r'{0:.8f} %'.format(percent)
        elif self.kind == "count down":
            units = self.convert[self.cunit]
            self.start = unix_time()
            diff = self.end - self.start
            msg = '\t{0:,.8f} {1}'.format(diff / units, self.cunit)
        else:
            units = self.convert[self.cunit]
            self.end = unix_time()
            diff = self.end - self.start
            msg = '\t{0:,.8f} {1}'.format(diff / units, self.cunit)
        self.msg.set(msg)

        self.after(10, self.update_clock)


# ==============================================================================
# Start of code
# ==============================================================================
if __name__ == '__main__':

    # set up starting parameters as list of integers
    # [year, month, day, hour, minute, second] defining the start of
    # the count down
    startl = [startyear, startmonth, startday,
              starthour, startminute, startsecond]
    # set up ending parameters as list of integers
    # [year, month, day, hour, minute, second] defining the start of
    # the count down
    endl = [endyear, endmonth, endday, endhour, endminute, endsecond]

    # run the count
    if not gui:
        count(startl, endl, countdowntype, percent_decimals, countdown_units)
    else:
        root = tk.Tk()
        app = App(master=root)
        root.mainloop()

# =============================================================================
# End of code
# =============================================================================
