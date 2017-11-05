
import os
import subprocess
import math

import config

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

if __name__ == "__main__":
    apk_path = ""

    correct_instrumented = 0
    failed_instrumented = 150000
    current_instrumented = 500

    start_instrumented = 0
    end_instrumented = 150000
    is_exception = True
    is_apk_generated =False
    result = None
    while is_exception:
        cmd = "py {0}/smiler/acvtool.py instrument -dbgstart {0} -dbgend {1} {2}".format(config.ACVTOOL_PATH, start_instrumented, end_instrumented, apk_path)
        try:
            result = request_pipe(cmd)
            is_apk_generated = os.path.exists(generated_apk)
            if is_apk_generated:
                correct_instrumented = current_instrumented


        except Exception:
            is_exception = True
        
        if not is_exception and is_apk_generated:
            start_instrumented = end_instrumented + 
            correct_instrumented = current_instrumented
        if not is_apk_generated or is_exception:
            failed_instrumented = current_instrumented

        if failed_instrumented - correct_instrumented > 1:
            pass
    
    left = 0
    right_failed =  15000
    right_current = right_failed
    while is_exception and not is_apk_generated:
        successfull = try_repack(left_success, right_success)

        if successfull:
            left = right_current
            right_current = math.ceil((left + right_failed) / 2)
            if left == right_current:
                print("app is fine?")
                return
        else: # failed
            right_failed = right_current
            right_current = math.ceil((left + right_current) / 2)
            if right_current == right_failed:
                break

    cmd = "py {0}/smiler/acvtool.py instrument -dbgstart {0} -dbgend {1} {2}".format(config.ACVTOOL_PATH, right_current, right_current, apk_path)
    result = request_pipe(cmd)
    
    print("hello")