import math


def comment_rating(upvotes, downvotes):
    total = upvotes + downvotes

    if total <= 0:
        return 0

    if upvotes == 0 and downvotes == 1:
        return -0.01

    Z = 1.6 # Zindex Assumes .95 confidence
    phat = 1.0 * upvotes / total
    WilsonScore = (phat + Z*Z/(2*total) - Z * math.sqrt(phat*(1-phat) + Z*Z/(4*total))) / (1+Z*Z/total)

    return WilsonScore