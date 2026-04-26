import os,platform,psutil

print(f"OS: {platform.system()} {platform.release()}")
print(f"Версия Python: {platform.python_version()}")
print(f"Свободно на диске: {psutil.disk_usage('/').free / (1024**3):.2f} GB")

print(f"Текущий рабочий каталог:{os.getcwd()}")

#os.chdir(r'/content/dir')
#pirnt(f"Новый рабочий каталог: {os.getcwd()}")

print("Переменные окружения:")
for key,value in os.environ.items():
    print(f"{key}: {value}")



