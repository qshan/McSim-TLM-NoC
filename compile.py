#! /usr/bin/env python2

import argparse
import os
import subprocess
import shutil

def main():
    ''' Compile the cycle accurate simulator '''

    # Configure parameters parser
    parser = argparse.ArgumentParser(description='Abstract simulator compiler script')
    parser.add_argument('-v',  '--verbose', action='store_true', help='enable verbose output')
    subparsers = parser.add_subparsers(title='valid subcommands', dest='command')
    parser_cp = subparsers.add_parser('build')
    parser_cp.add_argument('-nc',  '--noClean', action='store_true', help='don\'t clean before compiling')
    parser_cp.add_argument('-j',  '--jobs', type=int, help='perform parallel compilation using the specified number of threads')
    parser_cl = subparsers.add_parser('clean')
    args = parser.parse_args()

    # Clean if required
    work_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'obj')
    if args.command == 'clean' or not args.noClean:
        print ('Cleaning')
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir)
        os.makedirs(work_dir)

    # Build if needed
    if args.command == 'build':
        print ('Running cmake')
        cmd = ['cmake', '..']
        if not args.verbose:
            cmake = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=work_dir)
        else:
            print (cmd)
            cmake = subprocess.Popen(cmd, cwd=work_dir)
        if cmake.wait() != 0:
            print ('cmake FAILED')
            exit(-1)
        print ('cmake done')
        print ('Running make')
        cmd = ['make']
        if args.jobs:
            cmd.append('-j' + str(args.jobs))
        if not args.verbose:
             build = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=work_dir)
        else:
            print (cmd)
            build = subprocess.Popen(cmd, cwd=work_dir)
        if build.wait() != 0:
            print ('Bulding FAILED')
            exit(-1)
        print ('Building done')

# This script runs the main
if __name__ == "__main__":
    main()
