import random

def random_star_map_generator():
    return [(random.randint(-590, 590), random.randint(-590, 590)) for star in range(300)]

def parsed_data_to_string(data):
    return '|'.join([','.join([str(x)] + [str(y)] + [str(random.randint(1, 6))]) for x, y in data]) + ':'

################################################################################

class star_map:

    def __init__(self, name, string):
        self.name = name
        self.original_string = string
        self.original_cords = self.parse_string(string)
        self.star_set = set(self.original_cords)

    def parse_string(self, data_string):
        no_colon = data_string[:-1]
        stars = no_colon.split('|')
        star_sets = [star.split(',') for star in stars]
        star_cords = [(int(x), int(y)) for x, y, color in star_sets]
        return star_cords

    # finds self in another map
    def find_self_in(self, another_map, min_stars):
        master_list = another_map.original_cords
        master_set = another_map.star_set
        answers = []
        for current_master_star in master_list:
            for current_selected_star in self.original_cords:
                x_diff = current_master_star[0] - current_selected_star[0]
                y_diff = current_master_star[1] - current_selected_star[1]
                new_self = [(x + x_diff, y + y_diff) for x, y in self.original_cords]
                new_set = set(new_self)
                in_both = master_set & new_set
                # were there at least the minimum number of stars?
                if len(in_both) >= min_stars:
                    answer = []
                    answer.append(list(in_both))
                    # calculate self's cords
                    in_self = [(x - x_diff, y - y_diff) for x, y in in_both]
                    answer.append(in_self)
                    answers.append(answer)
        # answers has all constellations with at least min_stars (number of stars)
        def sort_help(list_x, list_y):
            if len(list_x[0]) < len(list_y[0]):
                return -1
            elif len(list_x[0]) > len(list_y[0]):
                return 1
            else:
                return 0
        answers.sort(sort_help)
        # now that answers is sorted, remove duplicate answers
        duplicates = 0
        index = 0
        while index < len(answers):
            star = answers[index][0][0]
            delete_these = []
            for constellation_pointer in range(index + 1, len(answers)):
                if len(answers[index][0]) != len(answers[constellation_pointer][0]):
                    break
                if self.is_in(star, answers[constellation_pointer][0]):
                    delete_these.append(constellation_pointer)
            duplicates += len(delete_these)
            delete_these.reverse()
            for constellation_pointer in delete_these:
                del answers[constellation_pointer]
            index += 1
        print # a break
        if duplicates:
            print 'Engine sorted out', duplicates, 'duplicate solutions from', self.name, 'and', another_map.name + '.'
        # print results
        wrong_answers = 0
        for answer in answers:
            if self.correct_answer(answer):
                print len(answer[0]), 'STARS:'
                print ' ' * 2 + 'In', self.name + ':'
                print ' ' * 4 + str(answer[1])[1:-1]
                print ' ' * 2 + 'In', another_map.name + ':'
                print ' ' * 4 + str(answer[0])[1:-1]
            else:
                wrong_answers += 1
        # note information regarding the results
        if wrong_answers:
            print 'Engine sorted out', wrong_answers, 'invalid solutions from', self.name, 'and', another_map.name + '.'
        if len(answers) == wrong_answers:
            print 'No constellations with at least', min_stars, 'stars could be found in', self.name, 'and', another_map.name + '.'

    # find out if a star is in a constellation
    def is_in(self, star, constellation):
        for point in constellation:
            if self.equal(star, point):
                return True
        return False

    # find out if two stars are the same
    def equal(self, x, y):
        return x[0] == y[0] and x[1] == y[1]

    # verify the numerical validity of the answer
    def correct_answer(self, answer):
        if len(answer[0]) < 2:
            return True
        x_diff = answer[0][0][0] - answer[1][0][0]
        y_diff = answer[0][0][1] - answer[1][0][1]
        for index in range(1, len(answer[0])):
            if answer[0][index][0] - answer[1][index][0] !=  x_diff:
                return False
            if answer[0][index][1] - answer[1][index][1] !=  y_diff:
                return False
        return True

################################################################################

if __name__ == '__main__':
    # test the star_map class
    a = star_map('Sky A', parsed_data_to_string(random_star_map_generator()))
    b = star_map('Sky B', parsed_data_to_string(random_star_map_generator()))
    a.find_self_in(b, 3)
    # most likely, no constellations will be found
    c = star_map('Sky C', parsed_data_to_string(random_star_map_generator()))
    d = star_map('Sky D', parsed_data_to_string(random_star_map_generator()))
    c.find_self_in(d, 4)
    # the following should yield one answer of 300 stars
    e = star_map('Sky E', parsed_data_to_string(random_star_map_generator()))
    e.find_self_in(e, 300)
