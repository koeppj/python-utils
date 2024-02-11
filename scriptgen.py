"""Generate genenic scripts from templates and inpupt data.

   For usage datails run "scriptgen --help"
"""
from io import TextIOWrapper
from string import Template
import csv 
import argparse
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
        # Replace all the single qoute strings in values with 'double' single qoute
        for key in row.__iter__():
            row[key] = row[key].replace("'","''")
        for template in templates:
            proc_line(input_line=template,values=row,outfile=output)
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
    parser.add_argument('-o','--output',
                        type=str,
                        required=False,
                        help='The [path]/name of the output (or sysout of not provided)',
                        action=utilssup.NewFileAction,
                        default=None)
    parser.add_argument('-i','--input',
                        type=str,
                        required=True, 
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
    proc_inputs(values=csv.DictReader(args.input,delimiter=args.delimitter),
                templates=get_template(args.template),
                output=args.output)
