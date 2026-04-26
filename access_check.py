#Расширенная проверка доступности веб-сайта 
import requests as req
import time

st_t = time.time()
resp = req.get("http://www.google.com")
end_t = time.time()


print(f"Статус-код: {resp.status_code}")
print(f"Тип содержимого: {resp.headers.get('Content-Type')}")
print(f"Размер контента: {resp.headers.get('Content-Length')} байт")
print(f"Время ответа: {end_t - st_t} секунд")
