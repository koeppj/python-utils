import argparse
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
