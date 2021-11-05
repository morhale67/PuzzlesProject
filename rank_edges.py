def rank_edges(self, e1, e2):
    rank = sum(abs(e1 - e2)) / len(e1)
    return rank