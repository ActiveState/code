from types import TypeType

class Pizza(object):
    @staticmethod
    def containsIngredient(ingredient):
        return False
    def getPrice(self):
        return 0

class PizzaHamAndMushroom(Pizza):
    @staticmethod
    def containsIngredient(ingredient):
        return ingredient in ["ham", "mushroom"]
    def getPrice(self):
        return 8.50

class PizzaHawaiian(Pizza):
    @staticmethod
    def containsIngredient(ingredient):
        return ingredient in ["pineapple", "curry"]
    def getPrice(self):
        return 11.50

class PizzaFactory(object):
    @staticmethod
    def newPizza(ingredient):
        # Walk through all Pizza classes 
        pizzaClasses = [j for (i,j) in globals().iteritems() if isinstance(j, TypeType) and issubclass(j, Pizza)]
        for pizzaClass in pizzaClasses :
            if pizzaClass.containsIngredient(ingredient):
                return pizzaClass()
        #if research was unsuccessful, raise an error
        raise ValueError('No pizza containing "%s".' % ingredient)

def main():
    myPizza = PizzaFactory().newPizza("ham")
    print(myPizza.getPrice())
    myPizza2 = PizzaFactory().newPizza("curry")
    print(myPizza2.getPrice())
    myPizza3 = PizzaFactory().newPizza("beef")

if __name__ == "__main__":
    main()
