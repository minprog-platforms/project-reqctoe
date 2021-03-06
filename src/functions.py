"""
functions.py
Programmeerproject
Eline van de Lagemaat (11892900)

Assisting functions for calculating distance and normalized direction vector between two points.
"""

from math import sqrt


def get_distance(pos1, pos2):
    """ Calculate distance between two points on grid."""
    return sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def get_normed_diff(pos1, pos2):
    """ Calculate normalized direction vector between two points on grid."""
    d = get_distance(pos1,pos2)
    # account for when pos1 and pos2 are the same
    if d == 0:
        return (0,0)
    return (pos2[0] - pos1[0])/d, (pos2[1] - pos1[1])/d