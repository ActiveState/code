'''
@author: Elazar Gershuni
@version: 0.1

Input: two text files in the following formats
    votes.txt: {name} {votes}
    agreements.txt: {party a} {party b}
(Without actual braces)
'''
qualifying_threshold_percentage = 0.02


def read_data():
    def read_pairs(filename):
        '''(This is not the right way to handle resources - we should use a `with` statement.
         But who cares.)'''
        yield from (line.strip().split() for line in open(filename, encoding='utf-8'))

    party_pairs = [(name, int(votes.replace(',', '')))
                    for name, votes in read_pairs('votes.txt')]
    return party_pairs, read_pairs('agreements.txt')


def prepare_data(party_pairs, agreement_pairs):
    class Party:
        def __init__(self, name, votes):
            self.name = name
            self.agreement = Agreement([self])
            self.votes = votes
    
    class Agreement:
        seats = 0
        def __init__(self, parties):
            self.parties = parties
    
    parties = {name:Party(name, votes) for name, votes in party_pairs}

    for name1, name2 in agreement_pairs:
        p1, p2 = parties[name1], parties[name2]
        p1.agreement = p2.agreement = Agreement({p2, p1})
    return list(parties.values())

def sum_votes(parties):
    return sum(p.votes for p in parties)


def list_indicator(x):
    '''The reason for adding 1 is for determining what the indicator would be 
    if the pair would receive that additional seat.'''
    return x.votes // (x.seats + 1)


def filter_parties(parties):
    total_votes = sum_votes(parties)
    passed_parties = [p for p in parties
                      if p.votes > total_votes * qualifying_threshold_percentage]
    for p in passed_parties:
        p.agreement.parties = [x for x in p.agreement.parties if x in passed_parties]
    return passed_parties


def get_shares(passed_parties):
    # first phase
    general_indicator = sum_votes(passed_parties) // 120
    for p in passed_parties:
        p.agreement.seats += p.votes // general_indicator
    return {p.agreement for p in passed_parties}


def mandate_splitting(agreements_list):
    # second phase
    seats_so_far = sum(s.seats for s in agreements_list)
    for s in agreements_list:
        s.votes = sum_votes(s.parties)
    for _ in range(seats_so_far, 120):
        max(agreements_list, key=list_indicator).seats += 1
    return agreements_list


def split_share(excess_votes_list):
    for s in excess_votes_list:
        if len(s.parties) == 1:
            s.parties[0].seats = s.seats
        else:
            # split between sharing parties
            indicator = s.votes // s.seats
            for p in s.parties:
                p.seats = p.votes // indicator
            max(s.parties, key=list_indicator).seats += 1
        

def calculate():
    parties = filter_parties(prepare_data(*read_data()))
    split_share(mandate_splitting(get_shares(parties)))
    return {p.name:p.seats for p in parties}

def print_parties(parties):
    for name, seats in sorted(parties.items(), key=lambda x: x[1], reverse=True):
        print(name, '=', seats)

if __name__ == '__main__':
    parties = calculate()
    print_parties(parties)
