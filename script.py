# COPYRIGHT Théo BASTY - 2022

import sys
import time

import pikepdf
import re
from glob import glob

INST_PATTERN = re.compile("^\w+")
COMMENT_PATTERN = re.compile("#.*")

operations = {}
pdf_cache = {}


def inst_open(instruction_line):
    global staging
    filename = re.match("OPEN (.*)", instruction_line).group(1)
    print("Opening " + filename)
    staging = pikepdf.open(filename, allow_overwriting_input=True)
operations["OPEN"] = inst_open


def inst_merge(instruction_line):
    global staging
    filenames = re.match("^MERGE (.*)$", instruction_line).group(1).split(" ")
    print("Merging files:", end='')
    for pattern in filenames:
        for file in glob(pattern):
            src = pikepdf.open(file)
            print(" " + file, end='')
            staging.pages.extend(src.pages)
    print(" - Done!")
operations["MERGE"] = inst_merge


def inst_swap(instruction_line):
    global staging
    pages = re.match("SWAP (\d+) (\d+)", instruction_line)
    p1, p2 = staging.pages[int(pages.group(1)) - 1], staging.pages[int(pages.group(2)) - 1]
    print("Swapping pages " + pages.group(1) + " and " + pages.group(2))
    staging.pages.append(p1)
    p1.emplace(p2)
    p2.emplace(staging.pages[-1])
    del staging.pages[-1]
operations["SWAP"] = inst_swap


def inst_remove(instruction_line):
    global staging
    pages = re.match("REMOVE ([0-9 ]+)", instruction_line).group(1).split(" ")
    pages = list(map(int, pages))
    pages.sort(reverse=True)
    print("Removing pages:", end='')
    for page in pages:
        print(" " + str(page), end='')
        del staging.pages[int(page) - 1]
    print(" - Done!")
operations["REMOVE"] = inst_remove


def inst_save(instruction_line):
    global staging
    filename = re.match("SAVE (.*)", instruction_line).group(1)
    print("Saving buffer as '" + filename + "'")
    staging.save(filename)
operations["SAVE"] = inst_save


def inst_keep(instruction_line):
    global staging
    pages = re.match("KEEP ([0-9 ]+)", instruction_line).group(1).split(" ")
    pages = list(map(int, pages))
    pages.sort(reverse=False)
    dst = pikepdf.new()
    print("Keeping some page in buffer:", end='')
    for page in pages:
        print(" " + str(page), end='')
        dst.pages.append(staging.pages[page - 1])
    staging.close()
    staging = dst
    print(" - Done!")
operations["KEEP"] = inst_keep


def inst_cache(instruction_line):
    global staging
    cache_name = re.match("CACHE (.*)", instruction_line).group(1)
    print("Placing buffer in cache entry '" + cache_name + "'")
    pdf_cache[cache_name] = staging
operations["CACHE"] = inst_cache


def inst_load(instruction_line):
    global staging
    cache_name = re.match("LOAD (.*)", instruction_line).group(1)
    print("Loading cache entry '" + cache_name + "' in buffer")
    staging = pdf_cache[cache_name]
operations["LOAD"] = inst_load

instructions = open("instructions.txt")
staging = pikepdf.new()
startingAt = time.time()
for i, line in enumerate(instructions, start=1):
    line = COMMENT_PATTERN.sub("", line).strip()
    if not line:
        print("")
        continue
    regexLine = INST_PATTERN.match(line)
    if regexLine is None:
        print("No instructions found on line " + str(i), file=sys.stderr)
        break
    inst = regexLine.group(0)

    if inst in operations.keys():
        operations[inst](line)
    else:
        print("Instruction " + str(inst) + " on line " + str(i) + " is not a valid instruction", file=sys.stderr)
        break
print("==========================================")
print("Instructions ran in " + str(round((time.time() - startingAt) * 1000)) + "ms")
