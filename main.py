from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from remote_pdb import set_trace
import threading
import socket
import io
import traceback
from contextlib import redirect_stdout

class PyRun:
    def __init__(self):    
        self.local_vars = {}
        self.global_vars = {"__name__":"__main__"}
    
    def execute_code(self, code_str):
        print("running code", code_str)
        output_buffer = io.StringIO()

        try:
            with redirect_stdout(output_buffer):
                exec(code_str, self.global_vars, self.local_vars)
        except Exception:
            trace_str = traceback.format_exc()
            return f"Error during execution:\n{trace_str}"
        return output_buffer.getvalue()

    def handle_client(self, client_socket, address):
        """Handles communication with a single client."""
        print(f"Connection from {address}")
        try:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break  
                try:
                    code_str = data.decode("utf-8")
                except UnicodeDecodeError:
                    output_str = "Error: Invalid UTF-8 input"
                else:
                    output_str = self.execute_code(code_str)
                    client_socket.sendall(output_str.encode('utf-8'))

        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            print(f"Closed connection from {address}")


    def main(self):
        """Sets up the socket server and listens for incoming connections."""
        host = '0.0.0.0'
        port = 8022

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((host, port))
            server_socket.listen(5)         
            print(f"Server listening on {host}:{port}")

            while True:
                client_socket, address = server_socket.accept()
                self.handle_client(client_socket, address)
        except KeyboardInterrupt:
            print("Server shutting down.")
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            server_socket.close()

class SocketListenerApp(App):
    
    
    def build(self):
        # Create an empty screen layout
        layout = BoxLayout(orientation='vertical')
        py = PyRun()
        # Thread to handle socket communication in the background
        # set_trace(host="0.0.0.0",port=8022)
        threading.Thread(target=py.main).start()
        return layout

if __name__ == '__main__':
    SocketListenerApp().run()
