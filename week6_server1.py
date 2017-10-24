"""версия сервера, в которой метрики хранятся на сервере в scope
сервер не в виде класса, отсутствует метод run(host, port)"""

import asyncio

def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ClientServerProtocol(asyncio.Protocol):
    store = []
    #def __init__(self):
    #    self.store = []

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def process_data(self, data):
        if data.split(" ")[0] == "put":
            try:
                method = data.split(" ")[0]
                key = data.split(" ")[1]
                value = data.split(" ")[2]
                timestamp = data.split(" ")[3]
                data_put = f"{key} {value} {timestamp}"
                if data_put not in self.store:
                    self.store.append(data_put)
                print(self.store)
                message = "ok\n\n"
            except ValueError:
                message = "error\nwrong command\n\n"
        elif data.split(" ")[0] == "get":
            data_get = []
            key = data.split(" ")[1]
            key = key[:-1]
            if key != "*":
                for item in self.store:
                    print(item)
                    for it in item.split(" "):
                        if it == key:
                            data_get.append(item[:-1]+"\n")
                message = "ok\n" + "".join(data_get) + "\n"
            else:
                try:
                    message = "ok\n" + "".join(self.store) +"\n"
                except ValueError:
                    message = "error\nwrong command\n\n"
        else:
            message = "error\nwrong command\n\n"
        return message

if __name__ == "__main__":
    run_server("127.0.0.1", 10001)
#
#
# async def myserver(reader, writer):
#     data_in = await reader.read(1024)
#     data = data_in.decode()
#     message = processing(data).encode()
#     print('send {}'.format(message))
#     writer.write(message)
#     await writer.drain()
#     writer.close()
#
#
# loop = asyncio.get_event_loop()
# coro = asyncio.start_server(myserver, "127.0.0.1", 10001, loop=loop)
# server = loop.run_until_complete(coro)
# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass
#
# server.close()
# loop.run_until_complete(server.wait_closed())
# loop.close()