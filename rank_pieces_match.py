from rank_edges import rank_edges

def rank_pieces_match(self, p1, p2, direction):
    """direction ex: connect p2 up from p1 or left from P1"""
    if direction == 'up':
        e1, e2 = p1[0, :], p2[-1, :]
    elif direction == 'down':
        e1, e2 = p1[-1, :], p2[0, :]
    elif direction == 'left':
        e1, e2 = p1[:, 1], p2[:, -1]
    elif direction == 'right':
        e1, e2 = p1[:, -1], p2[:, 1]
    else:
        print('the direction is not valid, please choose another direction')
        return -10
    rank = rank_edges(e1, e2)
    return rank