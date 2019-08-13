import cPickle


def write_messages(output_file, messages):
    """"Function will write the messages array to the file using pickle
    :rtype:
    """
    output = open(output_file, 'wb')
    cPickle.dump(messages, output)
    output.close()


def read_messages(input_file):
    """"Function will read the file using pickle to get a array of messages"""
    file_pointer = open(input_file, 'rb')
    messages = cPickle.load(file_pointer)
    file_pointer.close()
    return messages

