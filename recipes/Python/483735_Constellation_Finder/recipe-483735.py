class stars:

    def __init__(self, owner, star_data):
        self.__owner = owner
        self.__star_data = star_data
        self.__stars = self.__parse()
        self.__set = set(self.__stars)

    def __parse(self):
        colon_index = self.__star_data.index(':')
        before_colon = self.__star_data[:colon_index]
        star_definitions = before_colon.split('|')
        split_definitions = [star_definition.split(',') for star_definition in star_definitions]
        star_coordinates = [(int(x), int(y)) for x, y, color in split_definitions]
        return star_coordinates

    def unlock(self, key_object):
        assert key_object.__class__ is key
        owner, constellations = key_object.get_data()
        master_list = self.__stars
        master_set = self.__set
        answers = []
        print 'Stars Owner =', self.__owner
        print ' Key Owner =', owner
        found = 0
        for number, current_constellation in enumerate(constellations):
            answers = self.__find_constellations(current_constellation, master_list)
            for answer in answers:
                print '  Constellation', number + 1, 'was found at the following coordinates:'
                print '   ' + str(answer)[1:-1]
                found += 1
        if not found:
            print '   No constellations could be found.'

    def __find_constellations(self, constellation, sky):
        answers = []
        for star in sky:
            x_diff = star[0] - constellation[0][0]
            y_diff = star[1] - constellation[0][1]
            new_constellation = set([(x + x_diff, y + y_diff) for x, y in constellation])
            same = self.__set & new_constellation
            if len(same) == len(constellation):
                answers.append(list(same))
        return answers

class key:

    def __init__(self, owner, star_data):
        self.__owner = owner
        self.__star_data = star_data
        self.__constellations = self.__parse()

    def __parse(self):
        colon_index = self.__star_data.index(':')
        after_colon = self.__star_data[colon_index + 1:]
        constellation_definitions = after_colon.split('|')
        parsed_definitions = [self.__parse_definition(constellation_definition) for constellation_definition in constellation_definitions]
        pruned_definitions = [self.__prune_definition(parsed_definition) for parsed_definition in parsed_definitions]
        return pruned_definitions

    def __parse_definition(self, constellation_definition):
        bang_index = constellation_definition.index('!')
        after_bang = constellation_definition[bang_index + 1:]
        segment_definitions = after_bang.split('#')
        star_definitions = [star_definition for segment_definition in segment_definitions for star_definition in segment_definition.split(';')]
        split_definitions = [star_definition.split(',') for star_definition in star_definitions]
        star_coordinates = [(int(x), int(y)) for x, y in split_definitions]
        return star_coordinates

    def __prune_definition(self, parsed_definition):
        stars = parsed_definition
        index = 0
        while index < len(stars):
            delete = []
            for pointer in range(index + 1, len(stars)):
                if self.__equals(stars[index], stars[pointer]):
                    delete.append(pointer)
            delete.reverse()
            for pointer in delete:
                del stars[pointer]
            index += 1
        return stars

    def __equals(self, star1, star2):
        return star1[0] == star2[0] and star1[1] == star2[1]

    def get_data(self):
        return self.__owner, self.__constellations
