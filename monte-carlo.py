#!/usr/bin/env python
from project import Project
import optparse
import os

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

    # create the project from a file
    p = Project(file=options.filename)

    # do simulation
    p.get_totals(iterations=100000)
#    import pdb; pdb.set_trace()

    # print a pretty histogram of the sim
    p.google_histogram()

    # get the important stuff - what day are we 85% likely we'll finish
    days = p.n_percentile(percentile=85)

    # get the total man days required for the project
    mandays = p.man_days()

    # get the start and end date
    start_date = p.startdate
    end_date = p.enddate(days)

    print "OK %d percent chance %s will be done in %d days" % (85,p,days)
    if(end_date):
        print "OK start date is %s and end date is %s" % (start_date,end_date)
    print "OK %d percent chance %s has %d total man days of work" % (85,p,mandays)
