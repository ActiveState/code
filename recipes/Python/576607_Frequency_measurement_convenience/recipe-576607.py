import unittest, time

class FrequencyMeasure(object):
    """
    Convenience class to measure the average frequency of arbitrary events.
    """

    def __init__(self, time_window):
        """
        :Parameters:

          time_window : time in seconds
            Over this period the average frequency is measured
            
        """
        self.time_window = time_window
        self.tick_times = []

    def tick(self, time_step=None):
        """
        Provide a new time tick and return the current frequency
        """
        if time_step is None:
            time_step = time.time()

        self.tick_times.append(time_step)

        # only consider the ticks in the most recent time_window
        while time_step - self.tick_times[0] > self.time_window:
            del self.tick_times[0]
            
        if len(self.tick_times)<2:
            return 0

        return (len(self.tick_times)-1)/(time_step-self.tick_times[0])


class FrequencyMeasureTestCase(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.fm = FrequencyMeasure(3)

    def test_1(self):
        fm = self.fm
        t = fm.tick(0.0)
        self.assertEqual(t, 0.0)
        t = fm.tick(1.0)
        self.assertEqual(t, 1.0)
        t = fm.tick(2.0)
        self.assertEqual(t, 1.0)
        t = fm.tick(3.0)
        self.assertEqual(t, 1.0)
        t = fm.tick(4.0)
        self.assertEqual(t, 1.0)        
        
def suite():
    s = unittest.TestSuite()
    s.addTests(unittest.defaultTestLoader.loadTestsFromName(__name__))
    return s
    
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
    
