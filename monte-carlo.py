#!/usr/bin/env python
from scipy import stats
import json
import optparse
import os

class ticket(object):
    def __init__(self, name=None, mindays=0, maxdays=0, parallelizable=0):
        self.mindays = mindays
        self.maxdays = maxdays
        self.name = name
        self.mediandays = (float(self.maxdays) + float(self.mindays))/2
        self.parallelizable = 1/float(1+parallelizable)
        self.guesses = []

    def random_guesses(self, size=100000, stddevs=3.29):
        """make size random guesses from median out to stddevs
           
        Keyword args:
        size -- number of iterations for this simulation
        stddevs -- distance to include from median in standard deviations
        """
        self.guesses = stats.norm.rvs(loc=self.mediandays, scale=stddevs, size=size)
        return self.guesses

    def negatives_to_zero(self,list):
        """convert negative numbers to zero for a given list"""
        # outliers are sometimes negative.  I am torn on whether to remove
        # them.  hubbard says leave them.
        for index, item in enumerate(list):
            if item < 0:
                list[index] = 0
        return list

    def __str__(self):
        return self.name

class project(object):
    def __init__(self, file=file):
        self.name = None
        self.tickets = []
        self.totals = []
        self.file = file
        self.read_project()

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

        for tick in d["tickets"]:
            # fix - check that each exists and set sane defaults
            t = ticket( name=tick["name"], mindays=tick["mindays"], maxdays=tick["maxdays"], parallelizable=tick["parallelizable"])
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
        print "Day\tGuesses where project completed on that day"
        hist = self.histogram()
        range = self.range_of_ints(self.totals)
        for index, item in enumerate(hist):
            print "%d\t%d" % (range[index],hist[index])

    def histogram(self):
        """histogram of days to guesses"""
        range = self.range_of_ints(self.totals)
        return stats.histogram2(self.totals,range)

    def range_of_ints(self,alist):
        """return range of integers for a given unordered list"""
        return range(int(min(alist)),int(max(alist))+1)

    def __str__(self):
        return self.name

if __name__== "__main__":
    parser = optparse.OptionParser("usage: monte-carlo.py --file filename")
    parser.add_option("-f", "--file", dest="filename",
        type="string", help="json project file")
    (options, args) = parser.parse_args()

    if options.filename:
        if not os.path.isfile(options.filename):
            raise Exception("%s is not a file" % options.filename)
    else:
        parser.error("-f or --file is required")

    #import pdb; pdb.set_trace()

    p = project(file=options.filename)
    p.get_totals(iterations=100000)
    p.google_histogram()
    print "OK %d percent chance %s will be done in %d days" % (85,p,p.n_percentile(percentile=85))
    # want to get total man days at 85% is 458 man days for this project
    #print "mindays = %d, maxdays = %d" % (p.mindays(),p.maxdays())
