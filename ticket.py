from scipy import stats
class Ticket(object):
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

class TestTicket:
    def test_negatives_to_zero(self):
        alist = [-1,0,1]
        correct = [0,0,1]
        t = Ticket()
        answer = t.negatives_to_zero(alist)
        assert answer == correct
