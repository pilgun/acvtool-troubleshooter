
import os
import subprocess
import math

import config

def main():
    apk_path = ""

    MAX_METHODS = 150000

    left = 0
    right_failed =  MAX_METHODS
    right = right_failed
    while is_exception and not is_apk_generated:
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

    instrument_app(left, right, apk_path)
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

def instrument_app(start_instrumented, end_instrumented, apk_path):
    cmd = "{0} {1} instrument -dbgstart {2} -dbgend {3} {4}".format(config.PYTHON, 
        os.path.join(config.ACVTOOL_PATH, 'smiler', 'acvtool.py'),
        right_current, right_current, apk_path)
    result = request_pipe(cmd)
    return result

if __name__ == "__main__":
    main()