""""
script amount file -> file with fix 4.2 messages

It generates 'amount' random fix 4.2 messages and
records them in 'file'.
Exceptions could be raised mainly related to IO interaction
"""
import os
import sys
from libs.fileLib import write_messages
from libs import fixLib
import random


def main(argv):
    if len(argv) != 3 or not argv[1].isdigit():
        print "Expected: " + sys.argv[0] + " amount_of_fix_4.2_messages output_file_name"
        exit(1)
    amount = int(argv[1])
    file_full_path = os.path.abspath(argv[2])
    fix42_objects = []
    messages = []

    for count in range(0, amount):
        messages.append(fixLib.FixObject(
            random.randint(1, 5),  # 5 products
            random.choice(fixLib.T54_VALUES),
            random.randint(1, 100),  # quantity to buy or sell
            random.choice(fixLib.T40_VALUES),
            random.choice(fixLib.T59_VALUES),
            random.choice(fixLib.T167_VALUES),
            random.randint(1, 10),  # 10 clients
            float(random.randint(1, 10000))  # price max set to 10000
        ).get_fix_message())

    write_messages(file_full_path, messages)


if __name__ == "__main__": main(sys.argv)
