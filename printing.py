import os, sys

class HiddenPrints:
    def __init__(self, off=False) -> None:
        self.off = off
    
    def __enter__(self):
        if self.off == False:
            self._original_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.off == False:
            sys.stdout.close()
            sys.stdout = self._original_stdout