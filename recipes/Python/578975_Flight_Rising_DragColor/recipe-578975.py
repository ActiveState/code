reds = ["coral", "carmine", "red", "maroon", "blood", "crimson", "tomato", "rust"]
browns = ["chocolate", "brown", "soil"]
grays = ["slate", "stone", "beige"]
oranges = ["sand", "tangerine", "fire", "orange", "sunshine"]
yellows = ["gold", "ivory", "banana", "lemon", "goldenrod", "yellow"]
greens = ["leaf", "green", "avocado", "swamp", "forest", "jungle", "emerald", "jade"]
blues = ["seafoam", "aqua", "teal", "carribean", "azure", "denim"]
steel = ["steel"]
blues2 = ["stonewash", "sky", "splash", "blue", "navy", "storm"]
purples = ["royal", "violet", "purple", "lavender"]
thistle = ["thistle"]
mulberry = ["mulberry"]
blacks = ["shadow", "midnight", "obsidian", "black", "coal"]
grays2 = ["charcoal", "gray", "silver", "platinum"]
whites = ["ice", "white", "maize"]
pinks = ["rose", "pink", "magenta"]
colorwheel = []
colorwheel.append(reds)
colorwheel.append(browns)
colorwheel.append(grays)
colorwheel.append(oranges)
colorwheel.append(yellows)
colorwheel.append(greens)
colorwheel.append(blues)
colorwheel.append(steel)
colorwheel.append(blues2)
colorwheel.append(purples)
colorwheel.append(thistle)
colorwheel.append(mulberry)
colorwheel.append(blacks)
colorwheel.append(grays2)
colorwheel.append(whites)
colorwheel.append(pinks)
colors = []
coral = "coral"
carmine = "carmine"
red = "red"
maroon = "maroon"
magenta = "magenta"
pink = "pink"
rose = "rose"
maize = "maize"
white = "white"
ice = "ice"
platinum = "platinum"
silver = "silver"
gray = "gray"
charcoal = "charcoal"
coal = "coal"
black = "black"
obsidian = "obsidian"
midnight = "midnight"
shadow = "shadow"
mulberry = "mulberry"
thistle = "thistle"
lavender = "lavender"
purple = "purple"
violet = "violet"
royal = "royal"
storm = "storm"
navy = "navy"
blood = "blood"
crimson = "crimson"
tomato = "tomato"
stonewash = "stonewash"
sky = "sky"
splash = "splash"
blue = "blue"
rust = "rust"
chocolate = "chocolate"
brown = "brown"
soil = "soil"
slate = "slate"
stone = "stone"
beige = "beige"
sand = "sand"
tangerine = "tangerine"
fire = "fire"
orange = "orange"
sunshine = "sunshine"
gold = "gold"
ivory = "ivory"
banana = "banana"
lemon = "lemon"
goldenrod = "goldenrod"
yellow = "yellow"
leaf = "leaf"
green = "green"
avocado = "avocado"
swamp = "swamp"
forest = "forest"
jungle = "jungle"
emerald = "emerald"
jade = "jade"
seafoam = "seafoam"
aqua = "aqua"
teal = "teal"
carribean = "carribean"
azure = "azure"
denim = "denim"
for i in range(len(colorwheel)):
    for j in range(len(colorwheel[i])):
        colors.append(colorwheel[i][j])
done = False
while not done:
    color1 = input("Enter the color of the first dragon: ").lower()
    color2 = input("Enter the color of the second dragon: ").lower()
    colorlistFound = False
    colorlist = []
    colorlistIndex = []
    colorlistGet = False
    invalid = False
    i = 0
    while not colorlistGet and not invalid:
        if colors[i] == color1 or colors[i] == color2:
            colorlistFound = True
            colorlist.append(colors[i])
            colorlistIndex.append(i)
            if len(colorlist) == 2:
                colorlistGet = True
        i += 1
        if i == len(colors):
            if not colorlistGet:
                print("One or both colors was invalid. Try again.")
                print("Make sure you do not add any extra spaces.")
                invalid = True
    if not invalid:
        if colorlistIndex[0] > colorlistIndex[1]:
            colorlistIndex.append(colorlistIndex[0])
            colorlistIndex.pop(0)
        complete = False
        relevantList = []
        if colorlistIndex[1] - colorlistIndex[0] > (len(colors) / 2):
            index = colorlistIndex[1]
            while not complete:
                relevantList.append(colors[index])
                if index == colorlistIndex[0]:
                    complete = True
                index += 1
                if index == len(colors):
                    index = 0
        else:
            index = colorlistIndex[0]
            while not complete:
                relevantList.append(colors[index])
                if index == colorlistIndex[1]:
                    complete = True
                index += 1
                if index == len(colors) and color2 != "magenta" and color1 != "magenta":
                    print("Something went wrong in cataloguing.")
        print("There are", len(relevantList), "possible color outcomes.")
        print("They are: ", relevantList)
        goOn = input("Would you like to enter another combination?").lower()
        for letter in goOn:
            if letter == "n":
                done = True
