import json
import re
from collections import defaultdict

#####

# This file is a template only

#####
with open('InputFileName.json') as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

new_list = []
count = 0
for product in jsonObject:
    attribute_list = defaultdict(list)
    category_list = defaultdict(list)
    count += 1

# split out the categories from their groups
    category_split = product["Category"].split("| ")
    for category in category_split:
        # split again to each individual level
        category_name_split = category.split(" > ")

        # add the category to the first, second, or third category level
        # check if the category exists already, only append if it doesn't exist
        for idx, category in enumerate(category_name_split):
            if category not in category_list[f"category_L{idx+1}"]:
                category_list[f"category_L{idx+1}"].append(category)

    # merge the list of category dicts into product
    product.update(category_list)

    product["SKU_list"] = product["SKU"].split("| ")
    product.pop("SKU")

    # split price
    price_split = product["price"].split(" | ")
    price_list = []
    for price in price_split:
        # extract price only with regex and convert to float
        price_value = re.search(r"\d.+", price)
        price_list.append(float(price_value.group()))
    product["price_list"] = price_list

    # check if there is more than one price, if so add to low/high fields
    if len(price_list) > 1:
        product["price_low"] = price_list[0]
        product["price_high"] = price_list[1]

    # rename price field to price string
    product["price_string"] = product["price"]
    product["price"] = price_list[0]

    # create a dynamic list for each attribute field
    if "Json" in product:
        for idx, val in enumerate(json.loads(product["Json"])):
            for k, v in val.items():
                attribute_list[f"{k}_list"].append(v)
        product.update(attribute_list)
        product.pop("Json")
    new_list.append(product)


print(json.dumps(new_list[2], indent=4))
# print(count)  # print the total number of products to the console

# write a new json file with the file name specified when the command is run in the terminal
with open('OutputFileName.json', "w") as jsonFile:
    json.dump(new_list, jsonFile)
    jsonFile.close()
