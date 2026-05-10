import os
from pathlib import Path
import sys
import shutil
import platform



class FileManager:

    def __init__(self):
        ##отчищаем терминал
        self.clear_screen()
        #берем путь где пользователь открыл терминал
        self.root = Path.cwd().resolve()
        self.current_path = self.root
       

    def clear_screen(self):
        #под платформу разные кманды
        cmd = 'cls' if platform.system() == "Windows" else 'clear'
        os.system(cmd)


    def get_relative_path(self):
            #возвращаем короткий путь относительно корня
            return self.current_path.relative_to(self.root)


    def _safe_path(self, user_path):
        """Проверка безопасности: не дает выйти за пределы root"""
        target = (self.current_path / user_path).resolve()
        if self.root in target.parents or target == self.root:
            return target
        raise PermissionError("Error: You cannot leave this environment")


    def list_dir(self):
        return list(self.current_path.iterdir())


    def move_to(self, folder_name):
        target = self._safe_path(folder_name)
        if target.is_dir():
            self.current_path = target
        else:
            print("not a directory")


    def create_dir(self, name):
        self._safe_path(name).mkdir(exist_ok=True)
        

    def delete(self, name):
        target = self._safe_path(name)
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()


if __name__ == "__main__":
    fileman = FileManager()
    fileman.show_path_and_input()
