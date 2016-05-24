
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
startmonth = 3
startday = 1
starthour = 12
startminute = 0
startsecond = 0
# define end date
endyear = 2018
endmonth = 9
endday = 1
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
    # deal with start and end (i.e. set to "NOW" if none else set 
    # to the time defined in startlist/endlist)
    if startlist is None:
        start = unix_time()
    else:
        start = unix_time(datetime(*startlist))
    if endlist is None:
        end = unix_time()
    else:
        end = unix_time(datetime(*endlist))
    # set up dictionary for conversion between units and seconds
    convert = dict(years=365.25 * 24 * 3600.0,
                   months=365.25 * 24 * 3600 / 12.0,
                   days=24 * 3600.0,
                   hours=3600.0,
                   minutes=60.0,
                   seconds=1.0)
    # set up the date and time format string
    fmt = '{0:02.0f}-{1:02.0f}-{2:02.0f} '
    fmt += '{3:02.0f}:{4:02.0f}:{5:02.2f}'
    # run code to produce count down
    os.system("clear")
    # if we want a percentage display percentage
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
    # if we want a count down display a count down
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
    # else assume a count up is wanted
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
    """
    GUI to display count down/ count up /percentage in a pop up graphical 
    user interface
    """
    def __init__(self, master=None):
        """
        Constructor for the app create app, window, canvas and widgets
        """
        # start display
        tk.Frame.__init__(self, master)
        self.parent = master
        # set width and height
        self.width = 640
        self.height = 360
        # apply width and height
        self.parent.minsize(width=self.width, height=self.height)
        # create a red canvas and fill the window with it 
        self.can = tk.Canvas(self.parent, bg='red', height=self.height,
                             width=self.width)
        # place the canvas in the window at 0, 0 
        # (North West corner of canvas)
        self.can.place(x=0, y=0, anchor=tk.NW)
        # call the create_widgets function to populate the canvas
        self.create_widgets()

    def create_widgets(self):
        """
        Populate the canvas with these widjets
        """
        # extract and save variables internally
        # Note these should be read in, through the __init__???
        self.kind = countdowntype
        self.cunit = countdown_units
        self.pdec = percent_decimals
        startlist, endlist = startl, endl
        # deal with start and end (as in count function)
        if startlist is None:
            self.start = unix_time()
        else:
            self.start = unix_time(datetime(*startlist))
        if endlist is None:
            self.end = unix_time()
        else:
            self.end = unix_time(datetime(*endlist))
        # set up dictionary for conversion between units and seconds
        self.convert = dict(years=365.25 * 24 * 3600.0,
                       months=365.25 * 24 * 3600 / 12.0,
                       days=24 * 3600.0,
                       hours=3600.0,
                       minutes=60.0,
                       seconds=1.0)
        # set up the date and time format string
        fmt = '{0:02.0f}-{1:02.0f}-{2:02.0f} '
        fmt += '{3:02.0f}:{4:02.0f}:{5:02.2f}'
        # sort out the title
        if self.kind in ["percentage", "pc", r"%"]:
            title = "Percentage"
            title1 = ' Percentage From ' + fmt.format(*startlist)
            title1 += ' To ' + fmt.format(*endlist)
        elif self.kind == "count down":
            title = 'Count Down'
            title1 = ' Count down to ' + fmt.format(*endlist)
        else:
            title = "Time since"
            title1 = ' Time since ' + fmt.format(*startlist)
        # set the title of the window
        self.parent.title(title)
        # make a label widget to display more information (see title1)
        self.title = tk.Label(self.can, text=title1, font=('Helvetica', 16))
        # place the title in the canvas
        self.title.place(x=self.width/2.0, y=self.height/3.0, anchor=tk.CENTER)
        # create a quit button to close the window when clicked
        self.QUIT = tk.Button(self.can, text="QUIT", fg="red",
                              command=root.destroy)
        # place the quit button in the canvas
        self.QUIT.place(x=self.width/2.0, y=self.height, anchor=tk.S)
        # create a string variable and clock to display the count down
        self.msg = tk.StringVar()
        self.clock = tk.Label(self.can, font=('Helvetica', 24))
        # place the clock in the canvas
        self.clock.place(x=self.width/2.0, y=self.height/2.0,
                         anchor=tk.CENTER)
        # set the clocks text to the string variable
        self.clock["textvariable"] = self.msg
        # now call update clock
        self.update_clock()

    def update_clock(self, interval=10):
        """
        Method to update the clock (count down) every "interval" milliseconds
        
        :param interval: integer, time in milliseconds to call this function again 
        """
        # as with count function if percentage display a percentage
        # (NOW - start)/(end - start) x 100%
        if self.kind in ["percentage", "pc", r"%"]:
            tick1 = unix_time()
            # display percentage
            num = float(tick1 - self.start)
            denom = float(self.end - self.start)
            percent = (num/denom) * 100.0
            msg = r'{0:.8f} %'.format(percent)
        # else if a count down display the count down (end - NOW)
        elif self.kind == "count down":
            units = self.convert[self.cunit]
            self.start = unix_time()
            diff = self.end - self.start
            msg = '\t{0:,.8f} {1}'.format(diff / units, self.cunit)
        # else count up from the start (NOW - start)
        else:
            units = self.convert[self.cunit]
            self.end = unix_time()
            diff = self.end - self.start
            msg = '\t{0:,.8f} {1}'.format(diff / units, self.cunit)
        # update the message to be displayed on the clock widget
        self.msg.set(msg)
        # after interval milliseconds recall this method
        self.after(interval, self.update_clock)


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
