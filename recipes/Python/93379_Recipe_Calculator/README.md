# Welcome to the simple recipe calculator

## Quickstart

The example yml files you will find in the repository (no guarantee for food values; fetch your own):
  - [food.yml](food.yml)
  - [fruit_cocktail.yml](fruit_cocktail.yml)

```
python pyfood.py --yml-food=food.yml --yml-recipe=fruit_cocktail.yml

Rezept: Frucht Cocktail für 3 Person(en)
____________________  ____  _____  _____  _____  _____
                Name     #   kcal     KH      E      F
____________________  ____  _____  _____  _____  _____
                Kiwi   200  124.0   18.2    2.0    1.2
              Orange   300  141.0   24.9    3.0    0.6
               Apfel   400  260.0   57.6    1.2    0.4
           Himbeeren   350  150.5   16.8    4.5    1.1
        Heidelbeeren   250   97.5   15.0    2.5    0.0
             Zitrone   200   66.0    6.0    2.8    1.2
____________________  ____  _____  _____  _____  _____
               Summe        839.0  138.5   16.0    4.5
          Pro Person        279.7   46.2    5.3    1.5
            Anteil %                87.1   10.1    2.8

```

You can see the name and the quantity of each food and 
the calculated ingredients. As an example for the Kiwi
the double of the ingredient values is shown as specified
in the food yml file.

At the end you can see the sum per ingredient and the 
sum per ingredient value calculated for one person.

Finally you see the percentages. Obviously the example is
not really low carb :)

Hint: there are a lot of online locations to find those
food ingredients but usually buying food you often have
such information available on the article somewhere with
some exceptions of course.

My personal rules I try to follow:
 - at least 50% protein for a recipe (in most cases)
 - avoid to eat more large calories as you should (can be roughly calculated -> internet)
 - avoid fast food; buying fresh things
 - do some sport (no athletic; just a litte bit does help; you can do it at home)
 - we (my wife and me) are making our own low carb bread (as an example)

## The structure of the food file

Quite simple it's a list of entries like following:

```
- name: Some Food
  large_calories: 1.1
  fat: 2.2
  carb:3.3
  protein: 3.3
```

It's always the ingredients related to 100 gram or
100 millilitre of a concrete food. The tool does
not check that the sum of fat, carb and protein
is less or equal that limit.

You can find an example file in the repository.
Please note: no guarantee on the value there;
I fetched them from somewhere for testing purpose only.

## The structure of one recipe file

You would have to organise one recipe per file and
one file looks like following:

```
---
name: Frucht Cocktail
persons: 3
food:
    - { name: Kiwi, quantity: 200 }
    - { name: .*nge, quantity: 300 }
    - { name: Ap.*, quantity: 400 }
    - { name: Him.*, quantity: 350 }
    - { name: Heid.*, quantity: 250 }
    - { name: Zi.*, quantity: 200 }
```

Of course you have name (title) and you specify
for how many person the recipe is. Finally
you have a food list where you specify the food
and how many gram/millilitre you take.

The name is a Python compatible regular expression
so that you do not have to specify the full name.

