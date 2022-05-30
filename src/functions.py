from math import sqrt


def get_distance(pos1, pos2):
    return sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def get_normed_diff(pos1, pos2):
    d = get_distance(pos1,pos2)
    if d == 0:
        return (0,0)
    return (pos2[0] - pos1[0])/d, (pos2[1] - pos1[1])/d