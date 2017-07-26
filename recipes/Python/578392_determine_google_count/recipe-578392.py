import autopy
from time import sleep

import subprocess
import re

m = autopy.mouse
k = autopy.key


class count_detector:

    CORRECTED_MSG = 'Showing results for'
    #a comma seperated number
    NUMBER = re.compile(r'^[\d]{1,3}(,[\d]{3})*$')

    def calibrate(self):
        #determine position of search field:
        raw_input('please move cursor over search field and press enter.')
        self.search_field = m.get_pos()

        #determine position of result count
        print("Search something google will find.")
        raw_input('Then move the cursor over the count and press enter.')
        self.result = m.get_pos()

        #Google might autocorrect the query foo to ba.
        #In this case we need to press 'Search instead for foo'
        #in order to get the right count
        print("Search something google will autocorrect.")
        raw_input("Move cursor slightly left to 'Showing results for ' and press enter.")
        self.autocorrect_indicator_left = m.get_pos()

        raw_input("Move cursor to the right of whole 'Showing results for '-thing and press enter.")
        self.autocorrect_indicator_right = m.get_pos()

        #adjust right point. we need about same y-value and the one from left point is death sure
        self.autocorrect_indicator_right = (self.autocorrect_indicator_right[0],
                                            self.autocorrect_indicator_left[1])

        raw_input("Move cursor over 'Search instead for '-link and press enter")
        self.deautocorrect = m.get_pos()

    def get_count(self, word):
        #get focus
        m.move(*self.search_field)

        #select old
        m.click()
        m.click()
        m.click()

        sleep(5)

        #enter new
        k.type_string(word, 100)
        k.tap(k.K_RETURN)

        #get result count
        count = self.__fetch_results(1, 2)

        if not self.__is_count(count):  # if field is blank -> no entrys
            count = '0'
        else:

            #check for possible autocorrect
            #select possible 'Showing results for' message and examine
            m.move(*self.autocorrect_indicator_left)
            sleep(1)
            m.toggle(True)
            m.move(*self.autocorrect_indicator_right)
            m.toggle(False)

            string = self.__get_clipboard(2)

            if string.find(self.CORRECTED_MSG) == 0:
                #if query was autocorrected, deautocorrect
                m.move(*self.deautocorrect)
                m.click()
                count = self.__fetch_results(2, 2)

        return count

    def __fetch_results(self, waiting_time, waiting_time2):
        sleep(waiting_time)
        m.move(*self.result)
        m.click()
        m.click()
        return self.__get_clipboard(waiting_time2)

    def __get_clipboard(self, waiting_time):
        sleep(waiting_time)

        child = subprocess.Popen('xsel', stdout=subprocess.PIPE)
        count = child.communicate()
        return count[0]

    #determine if scrapped count is valid to sort out 'nothing found' and stuff
    def __is_count(self, number_to_test):
        return self.NUMBER.match(number_to_test)
