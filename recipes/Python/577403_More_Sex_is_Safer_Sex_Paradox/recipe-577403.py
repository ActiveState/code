import random

HIGH_ACTIVITY_RATE = 0.10
HIGH_ACTIVITY_INITIAL_INFECTION = 0.5
CONDOM_FAILURE_RATE = 0.01

class Player(object):
    def __init__(self, id, activity, use_condom=False):
        self.id = id
        self.activity = activity
        self.use_condom = use_condom
        self.infected = False
        self.history = []
        self.conversion_day = None
        
class LowActivityPlayer(Player):
    def __init__(self, id, activity, use_condom):
        Player.__init__(self, id, activity, use_condom)
        self.infected = False
        
class HighActivityPlayer(Player):
    def __init__(self, id, activity, use_condom, infected):
        Player.__init__(self, id, activity, False)
        self.infected = infected

class Manager():
    def __init__(self, low_activity, high_activity, transmission, players_count, days, use_condom):
        self.low_activity = low_activity
        self.high_activity = high_activity
        self.transmission = transmission
        self.players_count = players_count
        self.days = days
        self.use_condom = use_condom
        random.seed()
        self.pool = {}
        self.hookup_queue = []
        
        for id in range(self.players_count):
            if id < self.players_count * HIGH_ACTIVITY_RATE:
                infected = False
                if id < self.players_count * HIGH_ACTIVITY_RATE * HIGH_ACTIVITY_INITIAL_INFECTION:
                    infected = True
                player = HighActivityPlayer(id, self.high_activity, use_condom, infected)
            else:
                player = LowActivityPlayer(id, self.low_activity, use_condom)
            self.pool[id] = player
                
    def run(self):
        for day in range(self.days):
            self.hookup_queue = []
            for player in self.pool.values():
                if random.random() < player.activity:
                    self.hookup_queue.append(player)
            
            while self.hookup_queue:
                player_1 = player_2 = None
                player_1 = random.choice(self.hookup_queue)
                self.hookup_queue.remove(player_1)
                if self.hookup_queue:
                    player_2 = random.choice(self.hookup_queue)
                    self.hookup_queue.remove(player_2)
                if player_1 and player_2:
                    self.expose(player_1, player_2, day)
        return self
            
    def expose(self, player_1, player_2, day):
        transmission = self.transmission
        player_1.history.append(day)
        player_2.history.append(day)
        if player_1.infected or player_2.infected:
            if player_1.use_condom or player_2.use_condom:
                transmission *= CONDOM_FAILURE_RATE
            infection = (random.random() < transmission)
            if infection:
                if not player_1.infected:
                    player_1.infected = True
                    player_1.conversion_day = day
                if not player_2.infected:
                    player_2.infected = True
                    player_2.conversion_day = day

def trial(max_runs, low_activity, high_activity, transmission, players_count, days, use_condom):                    
    new_infections = 0.0
    new_low_infections = 0.0
    new_high_infections = 0.0
    contacts = 0.0
    low_contacts = 0.0
    high_contacts = 0.0
    
    for i in range(max_runs):
        mgr = Manager(low_activity, high_activity, transmission, players_count, days, use_condom).run()
        for player in mgr.pool.values():
            if isinstance(player, LowActivityPlayer):
                if player.conversion_day:
                    new_low_infections += 1
                low_contacts += len(player.history)
            elif isinstance(player, HighActivityPlayer):
                if player.conversion_day:
                    new_high_infections += 1
                high_contacts += len(player.history)
            else:
                raise Exception("trial: invalid player %d", player.id)
            contacts += len(player.history)
    
    new_infections = new_low_infections + new_high_infections
    avg_new_infections = new_infections/max_runs
    avg_new_low_infections = new_low_infections/max_runs
    avg_new_high_infections = new_high_infections/max_runs
    
    avg_contacts = contacts/max_runs
    avg_low_contacts = low_contacts/max_runs
    avg_high_contacts = high_contacts/max_runs
    risk_per_contact = avg_new_infections / avg_contacts
    
    print "\t%-15.2f%-15.2f%-15.2f%-15.2f%-15.1f%-15.2f%-15.5f" %(low_activity, high_activity, \
            avg_new_low_infections, avg_new_high_infections, avg_contacts, avg_new_infections, risk_per_contact)


def print_heading():
    print "\t%-15s%-15s%-15s%-15s%-15s%-15s%-15s" %\
    ("Low_Activity", "High_Activity", "Low_Infects", "High_Infects", "Contacts", "New_Infects", "Risk" )
    
def test_landsburg(max_runs, low_activity, high_activity, transmission, players_count, days, use_condom):
    print "\t%s" % ("Landsburg: increase activity of low-activity players")
    print
    print_heading()
    for i in range(6):
        trial(max_runs, low_activity, high_activity, transmission, players_count, days, use_condom)
        low_activity += 0.01
    print
    print
                        
def test_landsburg_condom(max_runs, low_activity, high_activity, transmission, players_count, days, use_condom):
    print "\t%s" % ("Landsburg w/ condoms: increase activity of low-activity players, use condoms")
    print
    print_heading()
    for i in range(6):
        trial(max_runs, low_activity, high_activity, transmission, players_count, days, use_condom)
        low_activity += 0.01
    print
    print
                        
def test_kremer(max_runs, low_activity, high_activity, transmission, players_count, days, use_condom):
    print "\t%s" % ("Kremer: increase activity of low-activity players, decrease activity of high-activity players")
    print
    print_heading()
    for i in range(6):
        trial(max_runs, low_activity, high_activity, transmission, players_count, days, use_condom)
        low_activity += 0.01
        high_activity -= 0.01
    print
    print
                        
def test_commonsense(max_runs, low_activity, high_activity, transmission, players_count, days, use_condom):
    print "\t%s" % ("Commonsense: decrease activity of high-activity players")
    print
    print_heading()
    for i in range(6):
        trial(max_runs, low_activity, high_activity, transmission, players_count, days, use_condom)
        high_activity -= 0.01
    print
    print
                        
def main():
    max_runs = 100
    low_activity = 0.01
    high_activity = 0.1
    transmission = 0.01
    players_count = 1000
    days = 1000
    use_condom = False
    test_landsburg(max_runs, low_activity, high_activity, transmission, players_count, days, use_condom)
    test_landsburg_condom(max_runs, low_activity, high_activity, transmission, players_count, days, True)
    test_kremer(max_runs, low_activity, high_activity, transmission, players_count, days, use_condom)
    test_commonsense(max_runs, low_activity, high_activity, transmission, players_count, days, use_condom)

if __name__ == "__main__":
    main()
