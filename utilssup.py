"""Python Utilities Support Module

   Provides functions and classes used by all the utilities.
"""
import argparse, configparser, os
from pathlib import Path

class NewFileAction(argparse.Action): 
    """Sets the arg value as a writable file object."""
    def __call__(self, parser, namespace, values, option_string= None) -> None:
        if values is None:
            setattr(namespace,self.dest, None)
            return
        p = Path(values)
        f = p.open(mode="w")
        setattr(namespace,self.dest,f)
    
class ExistFileAction(argparse.Action): 
    """Set the arg value as a readable file.
    
       If the file does not exist print and error and exit
    """
    def __call__(self, parser, namespace, values, option_string= None) -> None:
        p = Path(values)
        if not (p.is_file() and p.exists()):
            print("File {0} does not exist!".format(values))
            exit()
        f = p.open(mode="r")
        setattr(namespace,self.dest,f)

def get_config(): 
    """Get Utilities Configuration

       Load configuration from 
           1) defaults.cfg and 
           2) pyutils.cfg in current dir and 
           3) pytils in user home dir
    """
    config = configparser.ConfigParser(allow_no_value=True)
    config.read([
      os.curdir + os.sep + '.pyutils.cfg',
      os.path.expanduser('~') + os.sep + '.pyutils.cfg'
    ])