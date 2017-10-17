#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Recipe calculator.
"""
import re
import click
import yaml

FORMAT = "%20s  %4s  %5s  %5s  %5s  %5s"


@click.command()
@click.option('--yml-food', default="", help="Yaml file with food details")
@click.option('--yml-recipe', default="", help="Yaml file with recipe details")
def main(yml_food, yml_recipe):
    food = yaml.load(open(yml_food).read())
    recipe = yaml.load(open(yml_recipe).read())

    persons = int(recipe['persons'])
    print("\nRezept: %s für %d Person(en)" % (recipe['name'], persons))

    separator = FORMAT % ("_"*20, "_"*4, "_"*5, "_"*5, "_"*5, "_"*5)

    print(separator)
    print(FORMAT % ("Name", "#", "kcal", "KH", "E", "F"))
    print(separator)

    sum_large_calories = 0.0
    sum_carb = 0.0
    sum_protein = 0.0
    sum_fat = 0.0

    for rentry in recipe['food']:
        for fentry in food:
            if re.match(rentry['name'], fentry['name']):
                name = fentry['name']
                quantity = int(rentry['quantity'])
                large_calories = round(quantity * fentry['large_calories'] / 100.0, 1)
                carb = round(quantity * fentry['carb'] / 100.0, 1)
                protein = round(quantity * fentry['protein'] / 100.0, 1)
                fat = round(quantity * fentry['fat'] / 100.0, 1)

                print(FORMAT % (name, quantity, large_calories, carb, protein, fat))

                sum_large_calories += large_calories
                sum_carb += carb
                sum_protein += protein
                sum_fat += fat
                break

    sum_ingredients = sum_carb + sum_protein + sum_fat
    percentage_carb = round(sum_carb * 100.0 / sum_ingredients, 1)
    percentage_protein = round(sum_protein * 100.0 / sum_ingredients, 1)
    percentage_fat = round(sum_fat * 100.0 / sum_ingredients, 1)

    print(separator)
    print(FORMAT % ("Summe", "",
                    sum_large_calories,
                    sum_carb,
                    sum_protein,
                    sum_fat))

    print(FORMAT % ("Pro Person", "",
                    round(sum_large_calories / persons, 1),
                    round(sum_carb / persons, 1),
                    round(sum_protein / persons, 1),
                    round(sum_fat / persons, 1)))

    print(FORMAT % ("Anteil %", "", "",
                    percentage_carb,
                    percentage_protein,
                    percentage_fat))
    print("")


if __name__ == "__main__":
    main()
