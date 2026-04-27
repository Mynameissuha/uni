#Упражнение 1. Работта с файловой системой
import os
directory = input("Введите путь для создания директории: ")
if os.path.exists(directory):
    print("Такая директория уже существует")
else:
    os.makedirs(directory)
    print(f"Директория {directory} создана")

# Вывод всех файлов в директории и ее поддиректориях
def list_files(direcrory):
    for root,dirs,files in os.walk(directory):
        for file in files:
            print(os.path.join(root,file))
dr= ('Введите путь к директории для перечисления всех файлов в ней: ')            
list_files(directory)
