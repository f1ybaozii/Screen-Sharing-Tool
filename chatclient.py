import socket
import threading

class ChatClient:
    def __init__(self, mainwindow:None,nickname:str=None,host='127.0.0.1', port=12345):
        self.nickname = nickname
        self.mainwindow=mainwindow
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                self.mainwindow.on_message_received(message)
            except:
                print("An error occured!")
                self.client.close()
                break

    def write(self):
        while True:
            message = f'{self.nickname}: {input("")}'
            self.client.send(message.encode('ascii'))

    def run(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

if __name__ == "__main__":
    client = ChatClient()
    client.run()