
""""
script file -> Prints to stdout stats related to the fix 4.2 messages in the file

It generates statistics to stdout regarding fix 4.2
messages stored at file
Exceptions could be raised mainly related to IO interaction
"""
import os
import sys
from libs.fileLib import read_messages
from libs import fixLib


def main(argv):
    if len(sys.argv) != 2:
        print "Expected: " + sys.argv[0] + " input_file_name"
        exit(1)
    file_full_path = os.path.abspath(sys.argv[1])

    fix_objects = []
    for message in read_messages(file_full_path):
        fix_objects.append(fixLib.FixObject.get_fix_instance(message))

    t54stats = {'1': 0, '2': 0}
    t40stats = {}
    for i in fixLib.T40_VALUES:
        t40stats[i] = 0
    t59stats = {}
    for i in fixLib.T59_VALUES:
        t59stats[i] = 0
    t167stats = {}
    for i in fixLib.T167_VALUES:
        t167stats[i] = 0

    for fix_object in fix_objects:
        t54stats[fix_object.t54] += 1
        t40stats[fix_object.t40] += 1
        t59stats[fix_object.t59] += 1
        t167stats[fix_object.t167] += 1

    print "Nr of transactions: {0}\n".format(len(fix_objects))
    print "Sell transactions: {0}".format(t54stats['1'])
    print "Buy transactions: {0}".format(t54stats['2'])
    print

    print "By order type\n"
    keys = t40stats.keys()
    keys.sort()
    for i in keys:
        print "Type {0}: {1}".format(i, t40stats[i])
    print

    print "By all in force orders\n"
    keys = t59stats.keys()
    keys.sort()
    for i in keys:
        print "Type {0}: {1}".format(i, t59stats[i])
    print

    print "By 167 tag\n"
    keys = t167stats.keys()
    keys.sort()
    for i in keys:
        print "Type {0}: {1}".format(i, t167stats[i])
    print

    # This will be the most complex
    # We will find the average price per product per buy / sell
    t44avg_per55_per54 = {}
    t55keys = []
    for fix_object in fix_objects:
        if fix_object.t55 not in t44avg_per55_per54:
            t44avg_per55_per54[fix_object.t55] = {}
            t55keys.append(fix_object.t55)
        if fix_object.t54 not in t44avg_per55_per54[fix_object.t55]:
            t44avg_per55_per54[fix_object.t55][fix_object.t54] = []
        t44avg_per55_per54[fix_object.t55][fix_object.t54].append(fix_object.t44)

    t55keys.sort()
    t54_values = fixLib.T54_VALUES[:]
    t54_values.sort()
    print "Average price per product per buy / sell\n"
    for t55 in t55keys:
        for t54 in t54_values:
            if t54 in t44avg_per55_per54[t55]:
                print "Average price of {0} {1} product is {2:.2f}".format(
                    fixLib.T54_MEANING[t54],
                    t55,
                    average(t44avg_per55_per54[t55][t54])
                )


def average(lst):
    """"Average value of the list"""
    acc = 0.0
    for i in lst:
        acc += float(i)
    return acc / len(lst)


if __name__ == "__main__": main(sys.argv)
