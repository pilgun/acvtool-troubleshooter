
import os
import subprocess
import math
import argparse

import config

def main(apk_path):
    MAX_METHODS = 150000

    left = 0
    right_failed =  MAX_METHODS
    right = right_failed
    successfull = False
    while left is not right or (left == right and successfull):
        print("Instrumenting the methods from {0} to {1} ...".format(left, right))
        successfull = try_repack(left, right, apk_path)

        if not successfull:
            if right == left:
                print("Incorrect instrumentations is in the method {0}. Compare the instrumented code.".format(left))
                return
            print("Failed.")
            right_failed = right
            right = math.floor( (right_failed + left) / 2)
            # here if left == right then we expect that instrumenting faild either in left or left+1?

        if successfull:
            if left == 0 and end_instrumented == MAX_METHODS:
                print("The full app was instrumented and repackaged properly. Exit.")
                return
            print("Success.")
            left = right + 1
            right = left + math.floor((left + right_failed) / 2)
        
def try_repack(left, right, apk_path):
    folder, apk_name = os.path.split(apk_path)
    generated_apk_path = os.path.join(config.ACVTOOL_PATH, "smiler", "acvtool_working_dir", "instr_{0}".format(apk_name))
    if os.path.exists(generated_apk_path):
        os.remove(generated_apk_path)

    acvtool_call(left, right, apk_path)
    try:
        result = request_pipe(cmd)
        is_apk_generated = os.path.exists(generated_apk_path)
        return is_apk_generated
    except Exception:
        return False

def request_pipe(cmd):
    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = pipe.communicate()

    res = out
    if not out:
        res = err
    
    if pipe.returncode > 0:
        raise Exception("----------------------------------------------------\n\
Out: %s\nError: %s" % (out, err))

    return res

def acvtool_call(left, right, apk_path):
    cmd = "{0} {1} instrument -dbgstart {2} -dbgend {3} {4}".format(config.PYTHON, 
        os.path.join(config.ACVTOOL_PATH, 'smiler', 'acvtool.py'),
        left, right, apk_path)
    result = request_pipe(cmd)
    return result

def get_parser():
    parser = argparse.ArgumentParser(prog='main.py', 
        description='This script is designed to help in finding the method \
        that is bad instrumented by acvtool.')
    parser.add_argument("apk_path", metavar="<path_to_apk>", 
            help="Path to apk file")
    return parser

def run_actions(args):
    if not os.path.exists(args.apk_path):
        print("Can't find apk by the path provided.")
        return
    main(args.apk_path)


if __name__ == "__main__":
    parser = get_parser()
    #args = parser.parse_args()
    args = parser.parse_args([r"C:\apks\originalapk\FDroid.apk"])
    print(args.apk_path)
    run_actions(args)
