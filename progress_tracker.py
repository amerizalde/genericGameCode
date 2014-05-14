import datetime


def report(starttime):
    t = datetime.datetime.now()
    print "Time elapsed: {} seconds".format(t - starttime)


if __name__ == "__main__":
    start = datetime.datetime.now()
    n = 100
    while n:
        report(start)
        n -= 1
