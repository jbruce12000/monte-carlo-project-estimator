monte-carlo-project-estimator
=============================
Monte Carlo simulator to estimate how many days a project will take

Getting Started
---------------
::

  git clone git://github.com/jbruce12000/monte-carlo-project-estimator.git
  cd monte-carlo-project-estimator
  virtualenv mcpe
  source mcpe/bin/activate
  # on ubuntu only...
  # sudo apt-get install gfortran libopenblas-dev liblapack-dev build-essential
  pip install -r requirements.txt
  ./monte-carlo.py -f sample-project.json

Background
----------
I am a programmer turned manager.  This project is based on ideas from How to Measure Anything: Finding the Value of "Intangibles" in Business by Doug Hubbard.  The goal is to create a fast monte carlo project estimation tool that can be used on the command line.  It takes a series of tasks with ranges and runs thousands of guesses when each task will be finished.  The results are combined and displayed.

JSON Input File
---------------
The JSON input file consists of an array of tickets/tasks.  Each task has the following keys/values...
::

  "name" : "TASK 1",
  "mindays" : 10,
  "maxdays" : 21,
  "parallelizable" : 6

where:
::

  name = string, a unique name for this ticket/task.
  mindays = integer, the minimum number of days to complete the task
  maxdays = integer, the maximum number of days to complete the task
  parallelizable = integer, 0 to N, how many other tasks could be done in parallel with this task on this project.  this is how team size and task dependencies are accounted for. 

.. note:: The MOST IMPORTANT THING to the accuracy of this estimation is that you're 90% sure every task can be completed within the range you specify.  If you are not 90% sure, fix that.  Either make the range bigger or learn more about the task so you are sure.  Make sure to factor in weekends, holidays and sick time into each range.


Running Tests
-------------
py.test is installed with the requirements so if you followed the Getting Started instructions, run tests like so...
::

  source mcpe/bin/activate
  py.test *.py

Output
------
Here is the output from running ./monte-carlo.py -f sample-project.json.  It completes 700,000 guesses against 7 tasks and prints out a histogram in a little over a second.
::

  OK 100000 guesses for TASK1 between 10 and 21 days
  OK 100000 guesses for TASK2 between 10 and 30 days
  OK 100000 guesses for TASK3 between 2 and 15 days
  OK 100000 guesses for TASK4 between 2 and 15 days
  OK 100000 guesses for TASK5 between 2 and 4 days
  OK 100000 guesses for TASK6 between 2 and 4 days
  OK 100000 guesses for TASK7 between 3 and 10 days
  OK printing histogram
  Day	Guesses	Likelyhood of completion on that day
  8	1	0
  9	2	0
  10	2	0
  11	5	0
  12	10	0
  13	29	0
  14	56	0
  15	125	0
  16	185	0
  17	332	0
  18	604	1
  19	860	2
  20	1344	3
  21	1933	5
  22	2599	8
  23	3482	11
  24	4504	16
  25	5479	21
  26	6497	28
  27	7327	35
  28	7782	43
  29	8072	51
  30	8059	59
  31	7480	66
  32	7091	73
  33	6149	80
  34	5243	85
  35	4191	89
  36	3260	92
  37	2421	95
  38	1717	96
  39	1242	98
  40	758	98
  41	482	99
  42	300	99
  43	178	99
  44	98	99
  45	54	99
  46	28	99
  47	8	99
  48	8	99
  49	1	99
  50	2	100
  OK 85 percent chance sample project will be done in 34 days
  OK start date is 2014-10-15 and end date is 2014-11-18
  OK 85 percent chance sample project has 74 total man days of work
