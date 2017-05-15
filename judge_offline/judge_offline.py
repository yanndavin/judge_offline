import unittest
import sys
import filecmp
import os
import re
import difflib
from functools import partial


# Show full diff in unittest
unittest.util._MAX_LENGTH=2000

def create_test_class(module):
    exec('from ' + module + ' import *')
    problems = []
    splits = module.split(".")
    class_name = splits[-1]

    test_class = type(class_name,(unittest.TestCase,),{})
    test_class.__module__ = splits[-2] if len(splits)>1 else 'tests'
    for subdir, dirs, files in os.walk('./'):
        for file in files:
            m = re.search('([[aA-zZ|_|\d]+)_in.txt',file)
            if m:
                problems.append(m.group(1))

    for problem in problems:
        test_name = 'test_' + problem
        setattr(test_class, test_name, judge(module,problem))

    return test_class


def judge_problem(module,problem_to_judge,self):
    exec_problem_solution(module, problem_to_judge)
    cmp = cmp_problem_result(problem_to_judge)
    if not cmp:
        diff = diff_problem_result(problem_to_judge)
        print_problem_result_diff(diff)
    self.assertTrue(cmp)

def judge(module, problem):
    test_func = partial(judge_problem, module, problem)
    test_func.__doc__ = problem
    return lambda cls: test_func(cls)

def problem_filename(problem,type):
    return problem + '_' + type + '.txt'

def check_problem_files_existance(problem):
    fin = problem_filename(problem, 'in')
    fout = problem_filename(problem, 'out')
    fres = problem_filename(problem, 'res')
    return fin and fout and fres

def exec_problem_solution(module,problem):
    sout = sys.stdout
    sin = sys.stdin
    f_in = open(problem_filename(problem, 'in'), 'r')
    f_out = open(problem_filename(problem, 'out'), 'w')
    f_res = open(problem_filename(problem, 'res'), 'r')
    sys.stdin = f_in
    sys.stdout = f_out
    try:
        filename = module.split(".")[-1] + '.py'
        code_block = compile(open(filename).read(),filename,'exec')
        blob = {}
        exec(code_block,blob)
    finally:
        f_in.close()
        f_res.close()
        f_out.close()

        sys.stdout = sout
        sys.stdin = sin

def cmp_problem_result(problem):
    return filecmp.cmp(problem_filename(problem, 'res'),
                       problem_filename(problem, 'out'))


def diff_problem_result(problem):
    filename_out = problem_filename(problem, 'out')
    filename_res = problem_filename(problem, 'res')
    f_out = open(filename_out, 'r')
    f_res = open(filename_res, 'r')
    diff = difflib.unified_diff(
        f_res.readlines(),
        f_out.readlines(),
        fromfile=filename_out,
        tofile=filename_res,
    )
    return diff

def print_problem_result_diff(diff):
    for i,line in enumerate(diff):
        sys.stdout.write(line)
        if i>unittest.util._MAX_LENGTH:
            print("Too many differences...")
            break;