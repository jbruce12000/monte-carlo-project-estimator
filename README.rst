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
  pip install -r requirements.txt
  ./monte-carlo.py -f sample-project.json

Background
----------
I am a manager, not a programmer.  This project is based on ideas from
How to Measure Anything: Finding the Value of "Intangibles" in Business by Doug Hubbard.  The goal is to create a fast monte-carlo project estimation tool that can be used on the command line.  It takes a series of tasks with ranges and runs thousands of guesses when each task will be finished.  The results are combined and displayed.

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

.. note:: The MOST IMPORTANT THING to the accuracy of this estimation is that you're 90% sure every task can be completed within the range you specify.  If you are not 90% sure, fix that.  Either make the range bigger or learn more about the task so you are sure.
