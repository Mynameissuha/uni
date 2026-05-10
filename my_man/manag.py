import os
from pathlib import Path
import sys
import platform

class FileManager:
    def __init__(self):
        self.path_abs = Path.cwd()
    
    def show_path_and_input(self):
        shortened = self.path_abs.parts
        print('ЧАСТИ',shortened)
        #inpt = input(f"{}")

if __name__ == "__main__":
    fileman = FileManager()
    fileman.show_path_and_input()
