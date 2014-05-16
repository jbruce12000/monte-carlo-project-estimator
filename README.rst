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

Background
----------
I am a manager, not a programmer.  This project is based on ideas from
How to Measure Anything: Finding the Value of "Intangibles" in Business by Doug Hubbard.  The goal is to create a fast monte-carlo project estimation tool that can be used on the command line.  It takes a series of tasks with ranges and runs thousands of guesses when each task will be finished.  The results are combined and displayed.
