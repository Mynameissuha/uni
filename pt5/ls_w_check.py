import subprocess as sb
try:
    output = sb.check_output("ls",shell = True,text = True, encoding = 'cp866')
    print(output)
    files = output.strip().split('\n')
    print(f"Количество элементов :{len(files)}")
except sb.CalledProcessError as e:
    print(f"Ошибка выполнения команды: {e}")

