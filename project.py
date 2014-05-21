from ticket import Ticket
from scipy import stats
from datetime import datetime, timedelta
import json
import os

class Project(object):
    def __init__(self, file=None):
        self.name = None
        self.tickets = []
        self.totals = []
        self._start = datetime.now()
        self.file = file
        if self.file:
            self.read_project()

    @property
    def startdate(self):
       return self._start.strftime("%Y-%m-%d")
    @startdate.setter
    def startdate(self,d):
        self._start = d

    def enddate(self,days):
       d = self._start + timedelta(days=days) 
       return d.strftime("%Y-%m-%d")

    def mindays(self):
        """sum of ticket mindays"""
        total = 0
        for t in self.tickets:
            total = total + t.mindays
        return total

    def maxdays(self):
        """sum of ticket maxdays"""
        total = 0
        for t in self.tickets:
            total = total + t.maxdays
        return total

    def add_ticket(self,t):
        """add a ticket to the project"""
        self.tickets.append(t)

    def read_project(self):
        """read a project from a json file"""
        with open(self.file) as json_file:
            d = json.load(json_file)
            json_file.close()

        self.name = d["name"]
        if "start" in d:
            blah = datetime.strptime(d["start"], '%Y-%m-%d')
            self.startdate = blah

        for tick in d["tickets"]:
            # fix - check that each exists and set sane defaults
            t = Ticket( name=tick["name"], mindays=tick["mindays"], maxdays=tick["maxdays"], parallelizable=tick["parallelizable"])
            self.add_ticket(t);

    def num_tickets(self):
        """number of tickets in this project"""
        return len(self.tickets)

    def get_totals(self,iterations=100000):
        """make random guesses for each ticket range and total them

        Keyword args:
        iterations -- number of iterations for this simulation
        """
        self.totals = [0] * iterations
        self.unparallelized_totals = [0] * iterations
        for t in self.tickets:
            t.random_guesses(size=iterations)
            print "OK %d guesses for %s between %d and %d days" % (iterations, t, t.mindays, t.maxdays)
            for index,guess in enumerate(t.guesses):
                self.totals[index] = self.totals[index] + float(t.guesses[index]) * t.parallelizable
                # this could be used to get a raw estimate (without parallelization of the number of man days for a project
                #self.unparallelized_totals[index] = self.unparallelized_totals[index] + float(t.guesses[index])

    def n_percentile(self,percentile=85):
        """return the number of days at N percent
   
        Keyword args:
        percentile -- percent at which you'd like day returned
        """
        hist = self.histogram()
        total = 0
        for item in hist:
            total = total + item

        npercent = float(total) * (float(percentile)/100)
        total = 0
        range = self.range_of_ints(self.totals)
        for index,item in enumerate(hist):
            total = total + item
            if total >= npercent:
                return range[index]

    def google_histogram(self):
        """tab separated histogram of days to guesses"""
        print "OK printing histogram"
        print "Day\tGuesses\tLikelyhood of completion on that day"
        hist = self.histogram()
        total = 0
        for item in hist:
            total = total + item
        totalsofar = 0
        range = self.range_of_ints(self.totals)
        for index, item in enumerate(hist):
            totalsofar = totalsofar + hist[index]
            print "%d\t%d\t%d" % (range[index],hist[index],(float(totalsofar)/total)*100)

    def histogram(self):
        """histogram of days to guesses"""
        range = self.range_of_ints(self.totals)
        return stats.histogram2(self.totals,range)

    def range_of_ints(self,alist):
        """return range of integers for a given unordered list"""
        return range(int(min(alist)),int(max(alist))+1)

    def __str__(self):
        return self.name

class TestProject:
    def test_range_of_ints(self):
        alist = [-2,7,3,6]
        correct = [-2,-1,0,1,2,3,4,5,6,7]
        p = Project()
        answer = p.range_of_ints(alist)
        assert answer == correct

    def test_num_tickets(self):
        p = Project()
        assert p.num_tickets() == 0
        t = Ticket()
        p.add_ticket(t)
        assert p.num_tickets() == 1
        p.add_ticket(t)
        assert p.num_tickets() == 2

    def test_mindays(self):
        p = Project()
        assert p.mindays() == 0 
        t = Ticket(mindays=2)
        p.add_ticket(t)
        t = Ticket(mindays=3)
        p.add_ticket(t)
        assert p.mindays() == 5 

    def test_maxdays(self):
        p = Project()
        assert p.maxdays() == 0
        t = Ticket(maxdays=11)
        p.add_ticket(t)
        t = Ticket(maxdays=3)
        p.add_ticket(t)
        assert p.maxdays() == 14 
