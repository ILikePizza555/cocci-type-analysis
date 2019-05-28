from collections import namedtuple
import subprocess
import re
import sys

Location = namedtuple("Location", [
    "file", "current_element", "ce_line", "ce_column", "ce_line_end",
    "ce_column_end", "line", "column", "line_end", "column_end"
])

varRe = re.compile(r"(?P<param_name>.+?)='(?P<param_value>.+?)',?")

def parse_line(line):
    loc_begin = line.find("(Location(")

    location_params = {}
    for match in varRe.finditer(line[loc_begin + 10:]):
        param_name = match.group("param_name").strip()
        location_params[param_name] = match.group("param_value")

    return (line[5:loc_begin], Location(**location_params))

if __name__ == "__main__":
    output_lines = subprocess.run(["spatch", 
        "--python", sys.executable, 
        "--sp-file", "type-printer.smpl",
        "test.c"], stdout=subprocess.PIPE).stdout.decode("utf-8").splitlines()
    
    output_data = [parse_line(l) for l in output_lines]
    print(output_data)