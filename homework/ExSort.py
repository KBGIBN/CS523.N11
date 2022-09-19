import os
import time
import random
import string
import logging

#!rm -r /content/tmp/

BUFFER_DIR = 'tmp'
BUFFER_SIZE = 100_000


def dump_buffer(data: list) -> str:
    """Dump array of lines to text file.
    All files will be saved into temporary directory.
    :param data: Input list
    :return: Filename
    """
    buffer_filename = BUFFER_DIR + '/' + str(time.time())

    with open(buffer_filename, 'w+') as f:
        for line in data:
            f.write(str(line) + '\n')

    return buffer_filename


def prepare_buffers(file_to_sort: str) -> list:
    """Split big text file into limited size buffers.
    Simply read big file line by line.
    Single file contains BUFFER_SIZE lines.
    :param file_to_sort: large text file name
    :return: list of buffer file names
    """
    count = 0
    buffers = []
    buffer_data = []

    with open(file_to_sort, 'r') as f:
        while True:
            count += 1

            line = f.readline()
            if not line:
                break

            buffer_data.append(float(line))

            if count % BUFFER_SIZE == 0:
                buffer_data.sort()
                buffer_filename = dump_buffer(buffer_data)
                buffer_data = []
                buffers.append(buffer_filename)

        if buffer_data:
            buffer_data.sort()
            buffer_filename = dump_buffer(buffer_data)
            buffers.append(buffer_filename)

    return buffers


def merge_files(file1: str, file2: str) -> str:
    """Merge 2 sorted buffer files into one.
    :param file1:
    :param file2:
    :return:
    """
    output = BUFFER_DIR + '/' + str(time.time())
    res = open(output, 'w+')
    buffer1 = open(file1, 'r')
    buffer2 = open(file2, 'r')
    line1 = ''
    line2 = ''

    while True:
        line1 = buffer1.readline() if not line1 else line1
        line2 = buffer2.readline() if not line2 else line2

        if not line1 and not line2:
            break
        elif not line1:
            res.write(str(line2))
            line2 = ''
            continue
        elif not line2:
            res.write(str(line1))
            line1 = ''
            continue

        if line1 < line2:
            res.write(str(line1))
            line1 = ''
        else:
            res.write(str(line2))
            line2 = ''

    buffer1.close()
    buffer2.close()
    res.close()

    os.remove(file1)
    os.remove(file2)
    return output


def external_merge_sort(file_to_sort: str) -> str:
    """Main sorting method.
    Merge prepared buffers into single text file.
    :param file_to_sort:
    :return:
    """
    if not os.path.exists(BUFFER_DIR):
        os.makedirs(BUFFER_DIR)

    sorted_file = 'ExSort.OUT'
    buffers = prepare_buffers(file_to_sort)

    start_buff_cnt = len(buffers)

    for i in range(0, (start_buff_cnt - 1) * 2, 2):
        file1 = buffers[i]
        file2 = buffers[i + 1]
        buffers.append(merge_files(file1, file2))

    os.rename(buffers[-1], sorted_file)

    if os.path.exists(BUFFER_DIR):
        os.rmdir(BUFFER_DIR)

    return sorted_file


class FileHandler:
    filename: str

    def __init__(self, filename: str = 'ExSort.IN'):
        self.filename = filename

    def generate_file(self, num_lines: int = 50, force: bool = False) -> str:
        """Generate float numbers by number of lines and save as input file
        :param num_lines:
        :param force:
        :return: generated file name
        """
        if os.path.isfile(self.filename) and not force:
            logging.warning('File %s already exist. Generation skipped.', self.filename)
            return self.filename

        with open(self.filename, 'w+') as f:
            for _ in range(num_lines):
                x = random.uniform(-5,5)
                f.write(str(x) + '\n')

        return self.filename

    def sort(self) -> str:
        """Sort large text file.
        In this current case external merge sort used.
        :return: sorted file name
        """
        return external_merge_sort(self.filename)


if __name__ == '__main__':
    file = FileHandler('/content/ExSort.IN') # Directory to input file and the "ExSort.OUT" output file too
    #file.generate_file(num_lines=100, max_len=100) # Generate a sample text file for testing

    start = time.time()
    sorted_filepath = file.sort() # Perform external sorting
    end = time.time()

    print("SORTING COMPLETED!")
