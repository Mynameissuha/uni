import socket

host = 'google.com'
port = 80

request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

#socket.AF_INET - обозначение Adress Family - innternet (тоесть обозначение что мы хотим подключится к определенному адресу по языковому стандарту для IPv4) и socket.SOCK_STREAM - обозначаем тип сокета для протокола TCP 
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((host,port))
    s.sendall(request.encode())# по сети передаются байты поэтму испльзуем преобразование
    response = ""
    while True:
        part = s.recv(4096).decode()# метод recv(4096) читает данные из сокета частями по 4096 байт за раз
        if not part:
            break
        response += part

headers,_,body = response.partition('\r\n\r\n')
status_line = headers.splitlines()[0]
status_code = status_line.split(' ')[1]
print(f"Статус-код: {status_code}")
print("Заголовки ответа:")
print('\n'.join(headers.splitlines()[1:]))
