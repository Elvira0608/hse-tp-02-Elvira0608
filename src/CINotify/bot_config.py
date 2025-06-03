from pathlib import Path
import json

def get_report_when_failed():
    temp = ""
    if(Path("report.json").is_file()):
        with open("report.json", 'r') as file:
            data = json.load(file)

    if("failed" in data):
        failed_tests = int(data["report"]["summary"]["failed"])
    else:
        failed_tests = 0
    if(failed_tests > 0):
        for test in data["report"]["tests"]:
            if(test["outcome"] == "failed"):
                temp += "*TEST NAME*: " + test["name"] + "\n"  
                temp += test["call"]["longrepr"] + "\n"  
        res = "*Feiled tests (%d)*\n" % failed_tests + temp
    else:
        res = "All passed"    
    return res

token = '7705354270:AAGKM_nf8lN12S7SZ90jcCkRl1Cr5bMzzC0'
chat_id = '1331277451'
message_when_passed = 'Tests complited succesfully'
message_when_failed = get_report_when_failed()