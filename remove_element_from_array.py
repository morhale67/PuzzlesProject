def remove_element_from_array(self, list_pieces, arr):
    ind = 0
    size = len(list_pieces)
    while ind != size and not np.array_equal(list_pieces[ind], arr):
        ind += 1
    if ind != size:
        list_pieces.pop(ind)
        return list_pieces, ind
    else:
        raise ValueError('array not found in list.')
