# Schritt 0 : Einstellung und definition  aller  Parameter,  Classen und funktionen für die optimitation

# Durch das Kalibrierungsprogramm erstellte Matrix ,
# mit Schwerpunkte der gitter und breite des messberreich um den SP 
matrix_sp_messbreite= [[615.3756038647343, 865.2252415458937, 18], [615.6591619762352, 824.7116948092557, 15], [615.8033088235294, 783.1850490196078, 16], [615.8986810551559, 742.068345323741, 17], [615.4225609756097, 701.3396341463415, 18], [615.7853907134768, 660.3737259343148, 19], [615.7416619559073, 619.2589033352176, 19], [615.9786301369863, 577.841095890411, 19], [616.2704333516182, 536.8869994514537, 19], [616.7010928961748, 495.87158469945354, 18], [616.6470911086718, 454.7365532381998, 19], [616.8727858293075, 413.8217928073, 19], [616.4873903508771, 373.2998903508772, -1], [616.3637339055794, 331.94957081545067, 19], [616.3268625393495, 291.1579223504722, 20], [616.9497409326425, 248.89844559585492, 19], [618.158024691358, 205.01086419753085, 20], [618.9689880304679, 162.04406964091405, 19], [618.8880846325167, 121.37193763919822, 19], [618.6595622119816, 80.90783410138249, 18], [569.8849332485696, 864.9796567069294, 6], [570.1013767209012, 824.6182728410513, -1], [570.436004784689, 782.9413875598086, 16], [570.696261682243, 741.6571261682243, 18], [570.7545977011495, 700.7919540229885, 18], [570.7955555555556, 659.7716666666666, 19], [570.7969009407858, 618.7183176535694, 19], [570.8208791208791, 577.895054945055, 19], [571.188689217759, 536.8292811839324, 20], [571.3521505376344, 495.41182795698927, 20], [571.4215686274509, 454.3278867102396, 20], [571.2629609834313, 413.29396044895776, 20], [570.9492332099418, 372.246430460074, 20], [570.8037037037037, 331.44867724867726, 20], [570.9392, 290.65226666666666, 19], [570.988770053476, 249.55347593582889, 20], [571.3678220382825, 206.15623383341955, 20], [572.5376344086021, 162.3783922171019, 21], [573.4187192118227, 120.60864805692393, 19], [573.3159955257271, 80.3579418344519, 19], [524.0891803278688, 864.3940983606558, -1], [524.6053268765133, 823.7602905569007, -1], [524.4666254635353, 782.4202719406675, -1], [524.5879602571596, 741.583869082408, 18], [524.9230769230769, 700.5075757575758, 18], [525.1335963923337, 659.5, 19], [525.1531728665208, 618.3490153172867, 19], [525.4741707449701, 577.516041326808, 19], [525.7800851970181, 536.3184238551651, 20], [525.9858416360776, 495.00157315154695, 20], [526.3817427385892, 453.38641078838174, 20], [525.7843137254902, 412.3518812930578, 20], [525.3870967741935, 371.7059139784946, 19], [525.3951871657754, 330.9374331550802, 19], [525.3709591944886, 290.1494435612083, 20], [525.3016877637131, 249.01476793248946, 20], [525.5937984496124, 206.57364341085272, 20], [526.2912474849095, 163.07997987927564, 21], [527.2956243329776, 120.534151547492, 20], [527.4642058165548, 80.07606263982103, 19], [479.1939840392879, 863.8354818907305, 8], [478.9385687143762, 822.8809373020899, -1], [479.0852994555354, 782.0810647307925, 18], [479.3661075766339, 741.5164835164835, 19], [479.1430219146482, 700.0732410611304, 19], [479.30056179775283, 658.9775280898876, 18], [479.2433774834437, 618.1280353200883, 19], [479.27371273712737, 577.3289972899729, 19], [479.65711252653927, 536.2266454352441, 20], [480.0068493150685, 494.9067439409905, 19], [480.28850102669406, 452.3752566735113, 20], [479.95299145299145, 411.2986111111111, 20], [479.92841765339074, 370.79278794402586, 19], [479.8868126001068, 330.6097170315003, 19], [479.9957582184517, 289.84623541887595, 19], [479.75819451907574, 248.57872111767867, 19], [479.7102657634184, 206.62480458572173, 19], [480.0815407703852, 164.0015007503752, 21], [481.1975116640746, 120.85225505443235, 20], [481.1991223258365, 79.51508502468458, 19], [432.77059569074777, 863.5836501901141, 9], [433.3181008902077, 822.7341246290802, 8], [433.7618203309693, 781.7021276595744, 17], [433.52389380530974, 740.7705014749263, 18], [433.59450171821305, 699.4054982817869, -1], [433.731884057971, 658.5189520624303, 19], [433.7505617977528, 617.5544943820224, 19], [433.72095608671486, 576.8010005558643, 19], [433.62615803814714, 535.9051771117166, 19], [433.87293729372936, 494.93949394939494, 18], [434.3100414078675, 452.13923395445136, 20], [433.9570815450644, 411.0402360515021, 20], [434.33988316516195, 370.5326606479023, 20], [434.3816503800217, 329.8061889250814, 8], [434.1232076473712, 289.1147105682422, 20], [434.0784421283598, 247.73230938014262, 19], [434.04421949920084, 206.62067128396376, 19], [434.3600620796689, 164.36368339368858, 20], [434.78607983623334, 120.2906857727738, 20], [434.9400665926748, 79.21032186459489, 19], [387.26809314033983, 863.3612334801762, 18], [387.2650221378874, 822.5173940543959, -1], [387.5045153521975, 781.2450331125827, 6], [387.8211009174312, 740.1095183486239, 19], [387.94379521424594, 699.0946021146354, 19], [387.8568281938326, 658.0616740088105, 19], [388.2665553700612, 617.0940456316082, 19], [388.1651634723788, 576.272266065389, 19], [388.54471101417664, 535.7889858233369, 19], [388.25823591923483, 494.58979808714133, 18], [388.19838056680163, 451.62854251012146, 20], [388.5298826040555, 410.7241195304162, 19], [388.26954620010935, 369.901585565883, 19], [388.3962678375412, 329.3781558726674, 20], [388.15587918015103, 288.6084142394822, 19], [388.4327077747989, 247.30723860589814, 20], [388.5550755939525, 206.43196544276458, 19], [388.39858012170384, 164.16683569979716, 21], [388.6238670694864, 120.09264853977845, 21], [388.95235487404165, 78.46440306681271, 19], [341.37120211360633, 862.9009247027741, -1], [341.39403758911214, 821.7109526895658, -1], [341.81669585522474, 780.6497373029772, -1], [341.94076655052265, 739.7090592334495, 18], [342.0402722631878, 698.7702779353375, 18], [342.0060840707965, 657.6216814159292, 19], [341.7494419642857, 616.6897321428571, 19], [342.22434497816596, 575.9918122270742, 18], [342.2217391304348, 535.2983695652174, 20], [341.9388739946381, 493.857908847185, 19], [341.93985355648533, 451.3342050209205, 20], [342.56902002107483, 409.949947312961, 19], [342.5172786177106, 369.3768898488121, 19], [342.6225619399051, 328.8671586715867, 19], [342.74297827239, 288.1600423953365, 20], [342.7968421052632, 247.07368421052632, 20], [342.8684070324987, 205.92488012786362, 19], [342.51947368421054, 163.6357894736842, 19], [342.5246406570842, 120.17967145790554, 21], [342.89473684210526, 78.42317916002126, 20], [295.0700416088766, 862.5561719833564, -1], [295.078431372549, 821.5287792536369, -1], [295.47435897435895, 780.310606060606, 19], [295.2836363636364, 739.150303030303, -1], [295.44607566346696, 697.9785431959345, 18], [295.67690557451647, 656.8577929465301, 18], [295.8887640449438, 616.5775280898877, 19], [295.8791507893304, 575.6374523679913, 19], [296.0512682137075, 534.5402050728549, 19], [296.0793901156677, 493.2397476340694, 20], [295.8712606837607, 451.19070512820514, 20], [296.372654155496, 409.56300268096516, 19], [296.69586243954865, 368.7587318645889, 19], [296.97047772410093, 328.50670960815887, 20], [297.0693703308431, 287.6654215581644, 19], [296.80021482277124, 247.16326530612244, 12], [296.9405204460966, 205.29580456718003, 20], [296.79501525941, 163.03458799593082, 21], [296.7662141779789, 120.24484665661136, 21], [296.7735341581495, 78.43141473910704, 19], [249.15107913669064, 862.1164159581426, -1], [249.52715070164734, 821.3770591824283, 8], [249.14873035066506, 779.8917775090689, 13], [249.1837223219629, 738.7450628366248, 18], [249.4012702078522, 697.8487297921478, 18], [249.69006176305447, 656.7259966311061, 19], [249.57756696428572, 616.1194196428571, 19], [249.6, 574.9606557377049, 19], [249.54778809393773, 534.2151829601311, 19], [249.96209016393442, 492.5983606557377, 20], [249.72471324296143, 451.1475495307612, 20], [250.06210191082803, 409.6656050955414, 20], [250.55448201825013, 368.64573268921094, 19], [250.86608122941823, 328.1322722283205, 19], [250.80519480519482, 287.44534632034635, 19], [250.86787426744806, 246.39318060735215, 19], [250.97360248447205, 204.83695652173913, 20], [250.94008056394765, 162.3585095669688, 21], [250.47058823529412, 119.75577731092437, 19], [250.51942522618415, 78.38797232570516, 19], [203.7084917617237, 861.8795944233207, 6], [203.87061668681983, 820.6106408706166, -1], [204.13656114214774, 779.1800124146492, 6], [204.30251071647274, 738.4170238824249, 18], [204.25678119349004, 697.4406268836649, 18], [204.34635879218473, 656.2125518058023, 19], [204.3450292397661, 615.2216374269005, 19], [204.43651753325273, 574.3821039903265, 10], [204.06578947368422, 533.8323798627002, 19], [204.06291390728478, 492.4635761589404, 19], [204.38711423930698, 451.06767731456415, 20], [204.49267498643516, 409.55561584373305, 20], [204.75635359116023, 368.59889502762434, 19], [204.8064343163539, 327.8134048257373, 19], [205.06412382531786, 286.92371475953564, 19], [205.4340909090909, 245.57329545454544, 12], [205.64309031556039, 204.6088139281828, 19], [205.0021052631579, 161.89736842105262, 19], [204.23214285714286, 119.07773109243698, 20], [204.52730192719486, 77.57012847965738, 20]]

#...............................................................Parameter..................................................
periode, orientations =5,180                  #Parameter Hologram
generationen_anzahl=100                                             #anzah der generationen
cooling_param=0.95                                                     #cooling von 0 bis 0.99
uberlebende=75                                                          #survivors von 0 bis 200
mutation_rate=0.9                                                     # mutation rate von 0 bis 1

gen_one=0                     #Chromosomen der Erste generation
#falls gen_one=0=test mit nur eine Chromosom kombination 
chrom0,chrom1,chrom2,chrom3,chrom4,chrom5=0,0.5,0,0,0,0
#fall gen_one=1= zufaellige erstellte chromosome im bereich min/max
a0min,a0max=-0.5,1.0
a1min,a1max=-1.0,1.0
a2min,a2max=-1.0,1.0
a3min,a3max=-1.0,1.0
a4min,a4max=-0.5,0.5
a5min,a5max=-0.2,0.2

#------ Für Protokolierung & Auswertung sind wichtige  Ausgabe erförderlich,
#  wie z.b Bilder und optimisierte Chromosome.  Hier befinden sich die wichtigste
#  mögliche Ausgabe mit ihrem True/False Schalter 
#...............................................................Am Anfang der Optimierung..........................................

prnt0=0         #plot Bild des Hintergrunds und für der Normierung der Intensitaetsverteilung 
prnt1=0       #Ausgabe der Hintergrunds intesnsitaets liste
prnt2=0       #Ausgabe der Brutto & Netto intensitaeten bei  der Normierung
prnt3=0       #Ausgabe er Koeffizienten der  Normierung
# .................................................................. Nach jede Generation..........................................
prnt4=0                                        #Ausgabe Chromosome Aller individuen
prnt5=0                                        #Ausgabe Kennlinie Aller individuen
prnt6=0                                        #Plot Bild jede neue generation
plt_gen=[0,99]               #Plot Bild bestimmte Generationen
prnt7=0                                        #Ausgabe der individuelle Brutto.intensitäten 
prnt8=0                                        #Ausgabe  gesamt Brutto & Netto intensitaet
prnt9=0                                        #Ausgabe der individuelle Netto.intensitaeten
#................................................................. Am Ende der Optimierung..................................................
prnt10=0       #Ausgabe liste mit alle die Gesammt Brutto & Netto  aller individuen in  jede generation
prnt11=1       #Ausgabe Wert Brutto & Netto intensität bestes individuum jeder Gen 
prnt12=1       #Ausgabe Chromosome Beste Ergebnis
prnt13=1       #Ausgabe Wert Netto intensitaet
# Referenz: "Bruto"= Intensität direckt aus Kamera Aufnahme
#                 "Netto"= Hintergrund intensitaet abgezogen von "Brutto" ,
#                                 und mit normalkoefient dividiert 






#...............................................................Classen & Functions..................................................


# Simple straight forward Genetic Optimization based on a fixed
# Chromosome Length. The genes are just numbers (integers)
#
# Please see the example sample_geneticOptimization.py for a 
# very simple example
# and sample_geneticOptimization.py for nearly as simple example using
# inheritance. 
# T. Haist, November 2012
#


import random                   # for  random numbers
import copy                       # for the deep copy

gGenDebug =False                # set to True for some debugging

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class Individual:
    """
    Implements one individual in the population

    """
    # ----------------------------------------
    # ctor
    # maxlength gives the chromosome length
    def __init__(self, maxlength):
        # ------ The class variables --------------------------------
        self.mChromosome = []               # the chromosome itself (a list of integers)
        self.mChromosomeMin = []            # Minimum value of integers of the chromosome
        self.mChromosomeMax = []            # Maximum value of integers of the chromosome
        self.mChromosomeSize = maxlength    # The length of the chromosome (numbers)

        for x in range(maxlength):        
            self.mChromosome.append(0)       # Default Value = 0
            self.mChromosomeMin.append(0)    # Default Value Range: 0 ... 255
            self.mChromosomeMax.append(255)  
   

    def setValue(self,Chromosome,value):
        self.mChromosome[Chromosome]=value


    # ----------------------------------------
    # Mutate the Chromosome at position "position"
    # If delta = True then strength will give the CHANGE compared to the fully
    # allowed range of values. 0.5 means e.g. that the change will be allowed
    # to be in maximually 0.5 of the whole range of values.
    def mutate(self, position, strength, delta):
        bereich = self.mChromosomeMax[position] - self.mChromosomeMin[position]

        if delta:
            bereich *= strength
            change =(bereich * 2*(random.random()-0.5)*strength)
            self.mChromosome[position] += change
        else:                   # completely random change
            change = (bereich * random.random() * strength)
            self.mChromosome[position] = change + self.mChromosomeMin[position] +bereich/2

        # Check the boundaries and correct if necessary
        if self.mChromosome[position] < self.mChromosomeMin[position]:
            self.mChromosome[position] = self.mChromosomeMin[position]
        if self.mChromosome[position] > self.mChromosomeMax[position]:
            self.mChromosome[position] = self.mChromosomeMax[position]

    # ----------------------------------------
    # Define the minimum and maximum value of the Chromosome-entry/Gene at
    # position "position"
    def setMinMax(self, position, mini, maxi):
        self.mChromosomeMin[position] = mini;
        self.mChromosomeMax[position] = maxi;

    # ----------------------------------------
    # Print out the whole Chromosome
    def show(self):
        print(self.mChromosome)
    
    # ----------------------------------------
    # Set the entry/gene "number"  of the Chromosome to "number"
    def erase(self, number):
        for t in range(self.mChromosomeSize):        
            self.mChromosome[t] = number


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class Population:
    """
    Implements a population (consiting of several Individuals)

    """
    # ----------------------------------------
    # ctor
    def __init__(self):
    # ------ The class variables --------------------------------
        self.mIndividual = []               # the list of individuals
        self.mPopulationSize =  0           # The size of the population
        
    # ----------------------------------------
    # Append one individual to the population
    def append(self, indi):
        self.mIndividual.append(indi)     
        self.mPopulationSize +=1

    # ---------------------------------------
    #  one of the individuals (which) with strength and Delta
    def mutate (self, which, strength, delta):
        for u in range(self.mIndividual[which].mChromosomeSize):
            self.mIndividual[which].mutate(u, strength, delta)

    # ----------------------------------------
    # show all individuals of the population
    def show(self):
        for t in range(self.mPopulationSize):
            self.mIndividual[t].show()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

class GeneticOptimization:
    """
    Implements simple Genetic Optimization

    """
    # ----------------------------------------
    def __init__(self, population, coolingParameter):
        # ------ The class variables --------------------------------
        self.mTime = 0                # Time stamp
        self.mPopulation = population# The population of individuals
        self.mGenerations = 0         # The current generation number
        self.mCoolingParameter = coolingParameter  # 0 -> linear cooling, 1 -> exp.
        self.mMutationRate =mutation_rate    # Cooling parameter for cooling 
        self.mDeltaMutation = True # False -> Random Mutation, True -> Delta
        self.mEvaluations = []        # Array of the Evaluations
        self.mDeltaModulation = True  # True -> Delta when doing a mutation
        self.mBestMerrit = 0          # Best Merrit Value (Individual[0] after optimiz.
        self.mBestIndividual = 0      # Best Found Solution after optimization

    # ----------------------------------------
    # Evaluate the fitness of Individual with number index. 
    # THIS IS JUST AN EXAMPLE (optimization of sum of para1, para2 and para3
    def evaluateIndividual(self, index):   # Example 
        para1 = self.mPopulation.mIndividual[index].mChromosome[0]
        para2 = self.mPopulation.mIndividual[index].mChromosome[1]
        para3 = self.mPopulation.mIndividual[index].mChromosome[2]
        return para1 + para2 + para3

    # ----------------------------------------
    # Evaluate the fitness of the whole population and save the result in
    # the array mEvaluations. Beware: The array stores them as Tuples with
    # (fitness, number). This is necessary to be later able to sort the array
    # easily. ( A version using dictionaries lead to problems)
    def evaluateFitness(self):   # Defualt Implementierung
        self.mEvaluations = []   # set the start array to empty
        for t in range(self.mPopulation.mPopulationSize): # go through all Individuals
            self.mEvaluations.append((self.evaluateIndividual(t), t)) 

    # ----------------------------------------

    # Exponential or Linear Decrease of the 
    def cooling(self, type):
        self.mTime += 1;      # Increase the time stamp
        if type == 0:
            self.mMutationRate *= self.mCoolingParameter # exponential decrease
        else:
            self.mMutationRate -= self.mCoolingParameter # linear decrease 

    # ----------------------------------------
    # Mutate all but the best "survivors" individuals
    def mutateAll(self,survivors):
        for t in range(self.mPopulation.mPopulationSize-survivors):
            self.mPopulation.mutate(t+survivors, self.mMutationRate/4, self.mDeltaMutation)

    # ----------------------------------------
    # Genetic selection based on the fitness. 
    # MIGHT BE OVERRIDDEN !
    # Currently, just the best "survivors" Individuals will survive to the
    # next generation and might get descendents
    def selection(self, survivors):
        # Step 1: Sort the array of Evaluations based on Fitness
        self.mEvaluations = sorted(self.mEvaluations)
        # Step 2: Put the best "survivors" Individuals to the array sortiert
        sortiert = []
        for t in range(self.mPopulation.mPopulationSize):
            number = self.mEvaluations[t][1]
            sortiert.append(self.mPopulation.mIndividual[number])
        # Step 3: Copy (beware: Deepcopy is mandatory !) the best Individuals
        # to the front of the Population
        for t in range(self.mPopulation.mPopulationSize):        
            self.mPopulation.mIndividual[t] = copy.deepcopy(sortiert[t])
            if gGenDebug:    
                print(self.mEvaluations[t], \
                      self.mPopulation.mIndividual[t].mChromosome[0], \
                      self.mPopulation.mIndividual[t].mChromosome[1], \
                      self.mPopulation.mIndividual[t].mChromosome[2])

        if gGenDebug:    
            print("best ",self.mEvaluations[0], \
                      self.mPopulation.mIndividual[0].mChromosome[0], \
                      self.mPopulation.mIndividual[0].mChromosome[1], \
                      self.mPopulation.mIndividual[0].mChromosome[2])
        self.mBestMerrit = self.mEvaluations[0][0]
        self.mBestIndividual = copy.deepcopy(self.mPopulation.mIndividual[0])

    # ----------------------------------------
    # Create the descendents of the survivors.
    # Mating as well as asexual reproduction is possible
    # the prop. of mating is given bei propCrossover (0...1)
    def mating(self, survivors, propCrossover):
        children = self.mPopulation.mPopulationSize - survivors
        for t in range(children):
            mama = int(random.random()*survivors)
            papa = int(random.random()*survivors)
            child = survivors + t
            if(random.random() < propCrossover):
                self.crossover(mama,papa,child)
            else:
                self.mPopulation.mIndividual[child] =  \
                    copy.deepcopy(self.mPopulation.mIndividual[papa])

    # ----------------------------------------
    # Crossover between two parents (mama, papa) to create the child            
    # The crossoverposition is randomly chosen.
    def crossover(self, mama, papa, child):
        size = self.mPopulation.mIndividual[0].mChromosomeSize
        pos = int(random.random() *  size)
        for t in range(pos):
            self.mPopulation.mIndividual[child].mChromosome[t] = \
                self.mPopulation.mIndividual[papa].mChromosome[t]

        for t in range(size-pos):
            self.mPopulation.mIndividual[child].mChromosome[pos + t] =  \
                self.mPopulation.mIndividual[mama].mChromosome[t+pos]


    # ----------------------------------------
    # Show the whole population (all individuals)
    def show(self):
        for t in range(self.mPopulation.mPopulationSize):        
            self.mPopulation.mIndividual[t].show()


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

#-------------------------------------------------Program-----------------------------------------------
# Schritt 1 : Ausführung des Programms



import time     #Für die Kamera Aufnahme 



# Schritt 1.1 : Kamara aufnahme und  messung der Hintergrundsintensitaet 

cam = dataIO('Vistek')                                                  
cam.setParam("exposure",0.08)
cam.startDevice()
cam. acquire()
time.sleep(0.3)
img = dataObject()
cam.getVal(img)
if (prnt0):
    plot(img)
cam.stopDevice()

hintergrundliste = []
for o in range(200):
    sume=0
    for w in range (matrix_sp_messbreite[o][2]*2+1):
        for q in range (matrix_sp_messbreite[o][2]*2+1):
            pixel=img[int(matrix_sp_messbreite[o][0]-matrix_sp_messbreite[o][2]+q), 			int(matrix_sp_messbreite[o][1]-matrix_sp_messbreite[o][2]+w)]
            sume+=pixel
    total=(-sume/((2*matrix_sp_messbreite[o][2]+1)**2))
    hintergrundliste.append(total)
    
if(prnt1):
    print("hintergrundsliste",hintergrundliste)
del cam


# Schritt 1.2  : Ausrechnug einer Kennlinie für alle Gitter, die im SLM  Geschrieben werden
#                       zum berechnen der Normierungskoeffizienten 


holo = dataIO('CGHWindow')              # initialisierung des Holograms 
time.sleep(1)
holo.setParam('yholos',10)
holo.setParam('xholos',20)


brutergliste = []
nettergliste = []
brutbestresults=[]
netbestresults=[]



z=0.0                                                       #Ausrechnung der Kennlinie mit dem Chromosom
probkl=[]                                                 # (0,0.5,0,0,0,0)
while z<1:
    if z==0.0:
        Wert=0
    else:
        Wert=(0+0.5*z+0*z**2 +0*z**3)*z**0+0
    if Wert>1:
        Wert=1
    if Wert<0:
        Wert=0
    Wert=int(Wert*255)
    probkl.append(Wert)
    z=z+0.003921569
for t in range(200):
    holo.setParam('activeholo',t)
    holo.setParam('period',periode)
    holo.setParam('orientation',orientations)
    holo.setParam('maxvalue',255)
    holo.setParam('curve',probkl)
holo.setParam('redraw',0)


cam = dataIO('Vistek')                              # Bild aufnahme
cam.setParam("exposure",0.08)
cam.startDevice()
cam. acquire()
time.sleep(0.3)
cam. acquire()
time.sleep(0.3)
cam. acquire()
time.sleep(0.3)
time.sleep(0.3)
img = dataObject()
cam.getVal(img)
if(prnt0):
    plot(img)
cam.stopDevice()


normliste = []

for o in range(200):                                            #Ausrechnung der Intensitaetswerte 
    sume=0
    for w in range (matrix_sp_messbreite[o][2]*2+1):
        for q in range (matrix_sp_messbreite[o][2]*2+1):
            pixel=img[int(matrix_sp_messbreite[o][0]-matrix_sp_messbreite[o][2]+q),int(matrix_sp_messbreite[o][1]-matrix_sp_messbreite[o][2]+w)]
            sume+=pixel
    total=(sume/((2*matrix_sp_messbreite[o][2]+1)**2))
    if (total==0.0):
        total=10
    normliste.append(total)

totalnormliste=[i+j for i,j in zip(normliste,hintergrundliste)]     # Substraktion der  
normkoeff=[]                                                                             #Hintergrundsintensitaeten
for h in range (200):                                                                  
    wertkoeff=totalnormliste[h]/max(totalnormliste)  #Normierungs koefizient jedes Gitter 
    normkoeff.append(wertkoeff)                            #=(Intensitaet je Gitter)/max gitter intensitaet


#-------Ausgaben zur Normierung--------
if(prnt2):
    print("Brutto inten der Normierung",normliste )
if(prnt2):
    print ("Netto inten der Normierung",totalnormliste)
if(prnt3):
    print (" normierungs koeff",normkoeff)
del cam





"""
Still very simple demo for optimizing something but this time
it is demonstrated how to add your own MerritFunction by deriving a
class from GeneticOptimization
"""


# Schritt 1.2:
#Optimisation mit der Evaluationsfunktion bei ableiten einer Klasse aus GeneticOptimization 

#-----------------------------------------------------------------------
# Here comes the derived class

class MyOptimization(GeneticOptimization):
    """
    Simple example
    """
    # ----------------------------------------
    # Evaluate the fitness of Individual with number index. 
    #def evaluateIndividual(self, index):   # Example methode
    
    def evaluatefitness(self,bulean):   
        for v in range(200):
            poli1=self.mPopulation.mIndividual[v].mChromosome[0]
            poli2=self.mPopulation.mIndividual[v].mChromosome[1]
            poli3=self.mPopulation.mIndividual[v].mChromosome[2]
            poli4=self.mPopulation.mIndividual[v].mChromosome[3]
            poli5=self.mPopulation.mIndividual[v].mChromosome[4]
            poli6=self.mPopulation.mIndividual[v].mChromosome[5]
            if(prnt4):
                print ("Chromo aller indiv",poli1,poli2,poli3,poli4,poli5,poli6)

            z=0.0                               #Ausrechnung der Kennlinie für jedem Individuum  
            kl=[]                                 #aus seine  Chromosomen
            while z<1:
                if z==0.0:
                    Wert=0
                else:
                    Wert=(poli1+poli2*z+poli3*z**2 +poli4*z**3)*z**poli5+poli6
                if Wert>1:
                    Wert=1
                if Wert<0:
                    Wert=0
                Wert=int(Wert*255)
                kl.append(Wert)
                z=z+0.003921569
            holo.setParam('activeholo',v)
            holo.setParam('period',periode)
            holo.setParam('orientation',orientations)
            holo.setParam('maxvalue',255)
            holo.setParam('curve',kl)
            if(prnt5):
                print("kennlinie aller indiv", kl)
            
        holo.setParam('redraw',0)

     





 
        cam = dataIO('Vistek')                      # Bild Aufnahme
        cam.setParam("exposure",0.08)
        cam.startDevice()
        cam. acquire()
        time.sleep(0.3)
        img = dataObject()
        cam.getVal(img)
        if(prnt6):
            plot(img)
        elif(bulean):
            plot(img)
        cam.stopDevice()


        intensitaetliste = []
        for o in range(200):                                    #Ausrechnung der Intensitaetswerte 
            sume=0
            for w in range (2*matrix_sp_messbreite[o][2]+1):
                for q in range (2*matrix_sp_messbreite[o][2]+1):
                    pixel=img[int(matrix_sp_messbreite[o][0]-matrix_sp_messbreite[o][2]+q),int(matrix_sp_messbreite[o][1]-matrix_sp_messbreite[o][2]+w)]
                    sume+=pixel
            total=(-sume/((2*matrix_sp_messbreite[o][2]+1)**2))
            intensitaetliste.append(total)


        #Ausrechnung der Gitter intensitaeten mit Substraktion der
        # Hintergrundsintensitaetenund division der normierungskoefizient
        totalintenliste=[i-j for i,j in zip(intensitaetliste,hintergrundliste)]
        total_int_liste_mit_koeff=[]                                                     
        for c,d in zip(totalintenliste,normkoeff):                                  
            total_int_liste_mit_koeff.append(c/d)                                
        enumObj = enumerate(total_int_liste_mit_koeff)
        self.mEvaluations = [ [value,idx] for [idx,value] in enumObj ]
        brutergliste.append(sum(intensitaetliste)/200)
        nettergliste.append(sum(total_int_liste_mit_koeff)/200)
        netbestresults.append(min(total_int_liste_mit_koeff))
        brutbestresults.append(min(intensitaetliste))
        #-------Ausgaben zur Evaluation -----

        if(prnt7):
            print("individuelle Brutto intensitäten ",intensitaetliste)
        if(prnt8):
            print("gesamt bruto inten",sum(intensitaetliste)/200)
        if(prnt8):
            print("gesamt netto inten",total_int_liste_mit_koeff)
        if(prnt9):
            print("nummerierte indiv Netto intensitäten",self.mEvaluations)
        if(prnt11):
            print(" Brutto Best Result in generation",min(intensitaetliste) )
            print(" Netto Best Result in  generation", min(total_int_liste_mit_koeff))
        del cam
        return self.mEvaluations

#-----------------------------------------------------------------------
def main():
    try:
# --------------------------------------------------------------
#  Referenz zu Schritt 0:  Alle wichtige Parameter 
        ChromosomeLength=6        # Length of the Chromosome
        PopulationSize = 200       # Number of Individuals per Generation
        CntGenerations =generationen_anzahl      # Number of Generations
        Survivors = uberlebende           # Survivors per Generation
        Crossover = False         # No Crossover
        CoolingParameter =cooling_param   # Exponential Decrease per Generation of Mutation Rate

# --------------------------------------------------------------
# Schritt 2 : Now we generate a population and initialize them with some individuals
        popu = Population()  


        for t in range(PopulationSize):
            indi = Individual(ChromosomeLength)  # The allowed range for all genes
            indi.setMinMax(0,a0min,a0max)                                 
            indi.setMinMax(1,a1min,a1max)
            indi.setMinMax(2,a2min,a2max)
            indi.setMinMax(3,a3min,a3max)
            indi.setMinMax(4,a4min,a4max)
            indi.setMinMax(5,a5min,a5max)

            # erstellung zufaellige Chromosome fur den Zufällig erstellte gitter u=0 bis 200
            va=[]                                    
            vb=[]
            vc=[]
            vd=[]
            ve=[]
            vg=[]
            for u in range(200):					 		
                va.append(random.uniform(a0min,a0max))
                vb.append(random.uniform(a1min,a1max))
                vc.append(random.uniform(a2min,a2max))
                vd.append(random.uniform(a3min,a3max))
                ve.append(random.uniform(a4min,a4max))
                vg.append(random.uniform(a5min,a5max))

            if(gen_one):                                # Erstellung der erste Generation 
                indi.setValue(0,va[t])              # entweder Zufällig oder predeterminiert
                indi.setValue(1,vb[t])              # 
                indi.setValue(2,vc[t])
                indi.setValue(3,vd[t])
                indi.setValue(4,ve[t])
                indi.setValue(5,vg[t])
            else:
                indi.setValue(0,chrom0)
                indi.setValue(1,chrom1)
                indi.setValue(2,chrom2)
                indi.setValue(3,chrom3)
                indi.setValue(4,chrom4)
                indi.setValue(5,chrom5)
            popu.append(indi)

# Step 3: Optimize  ------------------------------------------------------------
        optimizer = MyOptimization(popu, CoolingParameter) # 0 -> Exp.Cooling 
        for generations in range(CntGenerations):
            bulean=generations in plt_gen
            optimizer.evaluatefitness(bulean)        # Evaluate the Fitness of all Individuals
            optimizer.selection(Survivors)     # Decide who is surviving
            optimizer.mating(Survivors,0.5)    # Mating of the Survivors         
            optimizer.mutateAll(Survivors)     # Mutate the Children
            optimizer.cooling(0)               # 0 -> Exponential Cooling  
            print("Generation:", generations,"MutationRate:" , optimizer.mMutationRate)
            if(prnt11):
                print("Liste Beste Results Netto je gen",netbestresults)
                print("Liste Beste Results Brutto je gen" ,brutbestresults)
        #-------Ausgaben zur Optimisation -----

        
        if(prnt10): 
            print ("Gesamt Brutto Intensitaeten",brutergliste)
            print("Gesamt Netto Intensitaeten",nettergliste)
        #popu.show()
        print("evaluating")
        for q in range (5):
            print("...")
        if(prnt13):
            print("Netto Best Result:",optimizer.mBestMerrit)
            print("Verbesserung von:", ((netbestresults[29]-netbestresults[0])/netbestresults[0])*100, "%")
        if(prnt12):
            print("Chromosome Best individual")
            optimizer.mBestIndividual.show()
        if(prnt10):
            print ("Gesamt Brutto Intensitaeten",brutergliste)
            print("Gesamt Netto Intensitaeten",nettergliste)
        if(prnt11):
            print("Liste Beste Results Netto je gen",netbestresults)
            #print("Liste Beste Results Brutto je gen" ,brutbestresults)
# --------------------------------------------------------------
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()

del holo
