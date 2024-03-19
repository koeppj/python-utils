"""Generate genenic scripts from templates and input data.

   For usage datails run "scriptgen --help"
"""
from io import TextIOWrapper
from string import Template
import csv 
import ast
import argparse
import os
from typing import Any
import utilssup

def get_template(template_file:TextIOWrapper) -> list[str]: 
    """Loads the template file (may be one or more lines)."""
    return template_file.readlines()

def proc_line(input_line: TextIOWrapper,values: dict,outfile: TextIOWrapper | None):
    """Processes each line in the template.
    
    For each line in the template replace all tokens with values and 
    output the result to specified output target.
    """
    t = Template(input_line)
    s = t.safe_substitute(values)
    print(s,file=outfile,end='')

def proc_inputs(values:csv.DictReader,templates:list[str],output:TextIOWrapper | None):
    """Process each row in the input file

        Process each row in the input csv against the template source.  
        Note that all occurances of a single qoute ("'") in the input 
        data will be replaed with two single qoutes ("''")
    """
    for row in values:
        proc_value_inputs(values=row,templates=templates,output=output)
        # Replace all the single qoute strings in values with 'double' single qoute
        #for key in row.__iter__():
        #    row[key] = row[key].replace("'","''")
        #for template in templates:
        #    proc_line(input_line=template,values=row,outfile=output)
        #print('',file=output)

def proc_value_inputs(values:dict[Any, str | Any] | Any,templates:list[str],output:TextIOWrapper | None):
    """ Use the provided dictionary values to process the template file 

        Process the provided key/value pairs against the template source.  
        Note that all occurances of a single qoute ("'") in the input 
        data will be replaed with two single qoutes ("''")
    """
    for key in values.__iter__():
        values[key] = values[key].replace("'","''")
    for template in templates:
        proc_line(input_line=template,values=values,outfile=output)
    print('',file=output)

def get_parser(): 
    """Builds the command line argument parser"""
    parser = argparse.ArgumentParser(
        prog='scriptgen',
        description='Use an input CSV and a template file with placeholders to generate an output file',
        epilog="Great for generating scripts based on a set of input values")
    parser.add_argument('-t','--template',
                        type=str,
                        required=True,
                        action=utilssup.ExistFileAction,
                        help='The [path]/name of the template file')
    parser.add_argument('-v','--values',
                        type=str,
                        required=False,
                        help='The values (in dict format) to apply to template')
    parser.add_argument('-o','--output',
                        type=str,
                        required=False,
                        help='The [path]/name of the output (or sysout of not provided)',
                        action=utilssup.NewFileAction,
                        default=None)
    parser.add_argument('-i','--input',
                        type=str,
                        required=False, 
                        action=utilssup.ExistFileAction,
                        help='The [path]/name of the input csv file')
    parser.add_argument('-d','--delimitter',
                        type=str,
                        required=False,
                        help='The character to use as a csv field delimitter (default is comma)',
                        default=",")
    return parser

if __name__ == "__main__":
    args = get_parser().parse_args()
    if (args.input):
        proc_inputs(values=csv.DictReader(args.input,delimiter=args.delimitter),
                    templates=get_template(args.template),
                    output=args.output)
    elif (args.values):
        values = ast.literal_eval(args.values)
        proc_value_inputs(values=values,
                    templates=get_template(args.template),
                    output=args.output)
    else:
        templateStr = TextIOWrapper.read(args.template)
        template = Template(templateStr)
        tokens = template.get_identifiers()
        values = dict()
        for token in tokens:
            tokenVal = input('Enter value of {token}:'.format(token=token))
            values[token]=tokenVal
        # 
        # Reset to the beginning
        args.template.seek(0,os.SEEK_SET)
        proc_value_inputs(values=values,
                    templates=get_template(args.template),
                    output=args.output)

