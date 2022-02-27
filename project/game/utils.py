"""This module contains general utility functions for ease of calculation.
"""


def is_between(target, begin, end):
    """Check if a target is between a beginning and end point.

    WARNING: this function should be depreciated in favor of
        chaining, a python feature. It works as follows:

        begin <= target <= end

    Args:
        target (int, float): target value
        begin (int, float): beginning value
        end (int, float): ending value
    """
    raise DeprecationWarning('Use a chain comparison instead.\n'
                             f'Example: begin ({begin}) <= target '
                             f'({target}) <= end ({end})')


def px_to_pt(pixels):
    """Convert pixels to point values.

    This is for dynamically determining a font size.

    Args:
        pixels (int, float): size in pixels

    Returns:
        float: size in points
    """
    return pixels / 3 * 4


def pt_to_px(points):
    """Convert points to pixel values.

    This is for dynamically determining a pixel size from a font size.

    Args:
        points (int, float): size in points

    Returns:
        float: size in pixels
    """
    return points / 4 * 3


def get_smallest(*values):
    """Get the smallest value.

    Returns:
        any: smallest value determined by sorted.
    """
    return sorted(values)[0]

def article_selector(noun):
    """Select an article to use based on a given noun.

    Args:
        noun (str): noun in a sentence

    Returns:
        str: article
    """
    noun = noun.lower()
    vowels = ('a', 'e', 'i', 'o', 'u')
    if noun[0] in vowels:
        return 'an'
    return 'a'
