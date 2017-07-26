# this is an example to demonstrate the programming technique

DATA = """
# data souce: http://www.mongabay.com/igapo/world_statistics_by_pop.htm
# Country / Captial / Area [sq. km] / 2002 Population Estimate
China / Beijing / 9,596,960 / 1,284,303,705
India / New Delhi / 3,287,590 / 1,045,845,226
United States / Washington DC / 9,629,091 / 280,562,489
Indonesia / Jakarta / 1,919,440 / 231,328,092
Russia / Moscow / 17,075,200 / 144,978,573
"""

def initData():
    """ parse and return a country list of (name, captial, area, population) """

    countries = []
    for line in DATA.splitlines():

        # filter out blank lines/comment lines
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # 4 fields separated by '/'
        parts = map(string.strip, line.split('/'))
        country, captial, area, population = parts

        # remove commas in numbers
        area = int(area.replace(',',''))
        population = int(population.replace(',',''))

        countries.append((country, captial, area, population))

    return countries


def findLargestCountry(countries):
    # your algorithm here


def main():
    countries = initData()
    print findLargestCountry(countries)
