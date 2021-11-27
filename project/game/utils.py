"""This module contains general utility functions for ease of calculation.
"""

def is_between(target, begin, end):
    return target >= begin and target <= end

def px_to_pt(pixels):
    return pixels / 3 * 4

def pt_to_px(points):
    return points / 4 * 3

def get_smallest(*values):
    return sorted(values)[0]
