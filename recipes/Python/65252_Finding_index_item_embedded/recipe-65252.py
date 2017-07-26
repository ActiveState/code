from __future__ import nested_scopes
import types

found='found'

def deepindex(sequence, goal):
    """deepindex(sequence,goal) -> index list"""
    def helper(sequence,index_list):
        for item in sequence:
            if item==goal:
                index_list.append(sequence.index(item))
                raise found,index_list
            elif isinstance(item,types.ListType) or isinstance(item,types.TupleType):
                index_list.append(sequence.index(item))
                index_list=helper(item,index_list)
        else: return index_list[:-1]

    try: helper(sequence,[])
    except found,index_list: return index_list
    else: return -1
