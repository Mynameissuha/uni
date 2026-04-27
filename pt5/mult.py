#несколько потоков для выполнения функции, которая симулирует длительную задачу (в нашем случае ожидание с использованием time.sleep())

import threading, time
import asyncio
def task(name):
    print(f"Задача {name}  началась\n")
    time.sleep(2)
    print(f"\nЗадача {name} завершена")

for i in range(5):
    t = threading.Thread(target = task,args = (f"Поток {i+1}",))
    t.start()

async def async_task(name):
    print(f"Асинхронная задача {name} началась")
    await asyncio.sleep(2)
    print(f"Асинхронная задача {name} завершилась")

#tasks = [asyncio.create_task(async_task(f"Задача {i+1}")) for i in range(5)]

#gather() является агрегатором и принимает на вход произвольное количество объектов, поддерживающих ожидание, которые передаются через запятую как позиционные аргументы. Чтобы передать в gather() заранее подготовленный список задач или корутин, необходимо использовать оператор распаковки *, который превращает элементы списка в отдельные аргументы функции.
#Другой способ 
async def main():
    await asyncio.gather(*(async_task(f"Задача {i+1}") for i in range(5)))

asyncio.run(main())

