def index_id(a_list, elem):
    return (index for index, item in enumerate(a_list) if item is elem).next()
