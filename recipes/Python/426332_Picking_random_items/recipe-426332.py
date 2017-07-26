def random_items(iterator, items_wanted=1):
    selected_items = [None] * items_wanted

    for item_index, item in enumerate(iterator):
        for selected_item_index in xrange(items_wanted):
            if not random.randint(0, item_index):
                selected_items[selected_item_index] = item

    return selected_items
