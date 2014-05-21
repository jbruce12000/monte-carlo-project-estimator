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

    #import pdb; pdb.set_trace()

    p = Project(file=options.filename)
    p.get_totals(iterations=100000)
    p.google_histogram()
    days = p.n_percentile(percentile=85)
    # fix - print start date too
    start_date = p.startdate
    end_date = p.enddate(days)
    print "OK %d percent chance %s will be done in %d days" % (85,p,days)
    if(end_date):
        print "OK start date is %s and end date is %s" % (start_date,end_date)
    # want to get total man days at 85% is 458 man days for this project
    #print "mindays = %d, maxdays = %d" % (p.mindays(),p.maxdays())
