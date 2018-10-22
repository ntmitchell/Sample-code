#!/usr/bin/env python

"""
Python 2.7

Problem: A directory contains ZIP files, each of which holds several files of that can be either a Postscript file or an AFP file. (The extensions were previously changed and no longer match the file type.)

Goal: Create a spreadsheet that list all of the files, their folder structure, and identify the file type.
1) Locate the directory in the system (through user input).
2) List all of the ZIP files in the directory.
3) For each file, peek at first ~500 bytes. If header contains string "%!PS-Adobe " then file is postscript
4) You can assume all other files are afp, but you can validate this by checking if first byte of file is hex 5A control character
"""

import argparse
from os import path, walk
from csv import DictWriter
from zipfile import ZipFile


def find_zip_files(directory):
    """
    Find all zip files in the target directory.
    Input: directory to search
    Output: list, file paths for zip files
    """
    zip_file_list = list()
    for directory_path, directory_name, file_names in walk(directory):
        for file in file_names:
            if file.endswith('.zip'):
                file_path = path.join(directory_path, file)
                zip_file_list.append(path.abspath(file_path))
    return zip_file_list


# IN PROGRESS
# IMPROVE TO HANDLE NESTED ZIP FILES
def inspect_zip_file(zip_file_path):
    """
    Given a zip file's path, analyze it's contents and classify the files.
    Input: list of file paths
    Output: dictionary, keys = [file_path, file_type, zip_file_path]
    """
    result_list = list()
    with ZipFile(zip_file_path, 'r') as zip_archive:
        file_list = zip_archive.namelist()
        for file in file_list:
            file_type = None
            if file.endswith('.zip'):
                print file + ' is a zip file and needs further analysis.'
            else:
                file_type = categorize_file(zip_archive, file)
                print file, file_type  # DEBUGGING
            if file_type != None:
                file_dictionary = {
                    'zip_file_path': zip_file_path,
                    'file_name': file,
                    'file_type': file_type
                }
                result_list.append(file_dictionary)
    return result_list


def categorize_file(archive, file_name):
    """
    Determine if file is a Postscript or AFP file.
    Input: file path
    Output: strings, "Postscript" or "AFP"
    """
    with archive.open(file_name, 'r') as archived_file:
        line = archived_file.readline()
        if line.startswith('Z'.format('x')):  # Tests if first line begins with hex. 5A character
            return 'AFP'
        file_buffer = archived_file.read(1000)  # Read first 1000 bytes. Sometimes the PS marker is several lines inside the file
        if '%!PS-Adobe' in file_buffer:
            return 'Postscript'
        return None


def create_csv_output(result_list, output_filename="spool_file_list", output_directory='./'):
    """
    Return inspection results to CSV for later conversion to Excel.
    Input: list of dictionary-type values and the location for output file
    Output: write CSV to output directory
    """
    output_path = path.join(output_directory, "{0}.csv".format(output_filename))
    output_path = path.abspath(output_path)
    with open(output_path, 'w') as output_file:
        fieldnames = ['file_name', 'zip_file_path', 'file_type']
        csv_writer = DictWriter(output_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(result_list)


def run(target_directory, output_directory):
    inspection_result_list = list()
    zip_file_list = find_zip_files(target_directory)
    for zip_file in zip_file_list:
        inspection_results = inspect_zip_file(zip_file)
        inspection_result_list.extend(inspection_results)
    create_csv_output(inspection_result_list, output_directory=output_directory)


if __name__ == '__main__':
    # Get command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_directory')
    parser.add_argument('-o', dest='output_directory', default='./')
    args = parser.parse_args()

    run(target_directory=args.input_directory, output_directory=args.output_directory)
