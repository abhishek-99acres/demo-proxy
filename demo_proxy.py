# import socket
# import threading
# import sys
# import time
# from urllib.parse import urlparse
# import keyboard


# class Proxy:
#     def __init__(self, host="0.0.0.0", port=8080):
#         self.host = host
#         self.port = port
#         self.buffer_size = 1024
#         self.running = True
#         self.server_socket = None

#     def start(self):
#         """Start the proxy server."""

#         try:
#             # Create a TCP socket
#             self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#             #   Bind the server to a specific address and port
#             self.server_socket.bind((self.host, self.port))

#             #   Listen for incoming connections
#             self.server_socket.listen(50)
#             print("=" * 50)
#             print(
#                 f"[*] Proxy server running on {'http://' if 'http' or 'https' in self.host else 'https://'}{self.host}:{self.port}"
#             )
#             print(f"[*] Configure your browser to use this proxy")
#             print(f"[*] Press Ctrl+C to stop")
#             print("=" * 50)

#             while True:
#                 # Accept client connection
#                 client_socket, client_address = self.server_socket.accept()
#                 print(
#                     f"[+] Accepted connection from {client_address[0]}:{client_address[1]}"
#                 )
#                 # Handle each client in a separate thread

#                 client_thread = threading.Thread(
#                     target=self.handle_client, args=(client_socket, client_address)
#                 )

#                 client_thread.daemon = True
#                 client_thread.start()

#         except KeyboardInterrupt:
#             print("\n[!] Shutting down proxy server...")
#             self.server_socket.close()
#             sys.exit(0)

#         except Exception as e:
#             print(f"[!] Error starting server: {e}")
#             sys.exit(1)

#     def handle_client(self, client_socket, client_address):
#         """Handle individual client requests"""
#         try:
#             # Receive request from client
#             request = client_socket.recv(self.buffer_size)
#             if not request:
#                 client_socket.close()
#                 return

#             # Parse the request to get the destination
#             request_line = request.decode("utf-8", errors="ignore").split("\n")[0]
#             print(f"[→] {request_line}")

#             # Extract URL from request
#             url = request_line.split(" ")[1]

#         except Exception as e:
#             print(f"[!] Error handling client: {e}")

#     def handle_http(self, client_socket, request, url):
#         """Handles HTTP requests"""
#         try:
#             # Parse the URL
#             parsed_url = urlparse(url if url.startswith("http") else f"http://{url}")
#             host = parsed_url.hostname
#             port = parsed_url.port or 80

#             # Create connection to destination server
#             self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             self.server_socket.connect((host, port))

#             # Forward client request to destination server
#             self.server_socket.sendall(request)

#             # Receive response from destination server and forward to client
#             while True:
#                 response = self.server_socket.recv(self.buffer_size)
#                 if len(response) > 0:
#                     client_socket.sendall(response)
#                 else:
#                     break
#             self.server_socket.close()

#         except Exception as e:
#             print(f"[!] HTTP Error: {e}")

#     def handle_https(self, client_socket, request_line):
#         """Handle HTTPS CONNECT requests (SSL tunnel)"""
#         try:
#             # Extract host and port from CONNECT request
#             url = request_line.split(" ")[1]

#             # Parse the URL
#             host, port = url.split(":")
#             port = int(port)
#             # Create connection to destination server
#             self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             self.server_socket.connect((host, port))

#             # Send success response to client
#             client_socket.sendall(b"HTTP/1.1 200 Connection established\r\n\r\n")

#             #  Set sockets to non-blocking mode for bidirectional forwarding
#             client_socket.setblocking(False)
#             self.server_socket.setblocking(False)

#             # Forward data between client and server
#             while True:
#                 try:
#                     #   Client to Server
#                     data = client_socket.recv(self.buffer_size)
#                     if data:
#                         self.server_socket.sendall(data)

#                 except:
#                     pass

#                 try:
#                     #   Server to Client
#                     data = self.server_socket.recv(self.buffer_size)
#                     if data:
#                         client_socket.sendall(data)

#                 except:
#                     pass

#         except Exception as e:
#             print(f"[!] HTTPS Error: {e}")


# def exit_program():
#     print("Exiting...")
#     sys.exit(0)


# if __name__ == "__main__":
#     # You can customize host and port here
#     proxy = Proxy(host="192.168.100.121", port=8888)
#     proxy.start()


# #!/usr/bin/env python3
# """
# Simple HTTP Proxy Server
# A basic implementation to learn proxy concepts
# """

# import socket
# import threading
# import sys
# from urllib.parse import urlparse


# class ProxyServer:
#     def __init__(self, host="0.0.0.0", port=8888):
#         self.host = host
#         self.port = port
#         self.buffer_size = 8192
#         self.running = True
#         self.server_socket = None

#     def start(self):
#         """Start the proxy server"""
#         try:
#             # Create a TCP socket
#             self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#             # Set timeout to allow periodic checks for shutdown
#             self.server_socket.settimeout(1.0)

#             # Bind to host and port
#             self.server_socket.bind((self.host, self.port))

#             # Listen for incoming connections (max 50 queued)
#             self.server_socket.listen(50)
#             print("=" * 50)
#             print(
#                 f"[*] Proxy server running on {'http://' if 'http' in self.host else 'https://'}{self.host}:{self.port}"
#             )
#             print(f"[*] Configure your browser to use this proxy")
#             print(f"[*] Press Ctrl+C to stop")
#             print("=" * 50)

#             while self.running:
#                 try:
#                     # Accept client connection
#                     client_socket, client_address = self.server_socket.accept()
#                     print(
#                         f"[+] Connection from {client_address[0]}:{client_address[1]}"
#                     )

#                     # Handle each client in a separate thread
#                     client_thread = threading.Thread(
#                         target=self.handle_client, args=(client_socket, client_address)
#                     )
#                     client_thread.daemon = True
#                     client_thread.start()
#                 except socket.timeout:
#                     # Timeout allows us to check if we should keep running
#                     continue
#                 except OSError:
#                     # Socket was closed
#                     break

#         except KeyboardInterrupt:
#             print("\n[!] Shutting down proxy server...")
#         except Exception as e:
#             print(f"[!] Error starting server: {e}")
#         finally:
#             self.shutdown()

#     def shutdown(self):
#         """Cleanly shutdown the server"""
#         self.running = False
#         if self.server_socket:
#             try:
#                 self.server_socket.close()
#                 print("[*] Server socket closed")
#             except:
#                 pass
#         print("[*] Shutdown complete")
#         sys.exit(0)

#     def handle_client(self, client_socket, client_address):
#         """Handle individual client requests"""
#         try:
#             # Receive request from client
#             request = client_socket.recv(self.buffer_size)
#             print(f"[→] request: {request}")

#             if not request:
#                 client_socket.close()
#                 return

#             # Parse the request to get the destination
#             request_line = request.decode("utf-8", errors="ignore").split("\n")[0]
#             print(f"[→] {request_line}")

#             # Extract URL from request
#             url = request_line.split(" ")[1]
#             print(f"[→] request_line: {request_line}")

#             # Determine if this is a CONNECT request (HTTPS) or regular HTTP
#             if request_line.startswith("CONNECT"):
#                 self.handle_https(client_socket, request_line)
#             else:
#                 self.handle_http(client_socket, request, url)

#         except Exception as e:
#             print(f"[!] Error handling client: {e}")
#         finally:
#             client_socket.close()

#     def handle_http(self, client_socket, request, url):
#         """Handle HTTP requests"""
#         try:
#             # Parse the URL
#             parsed_url = urlparse(url if url.startswith("http") else "http://" + url)
#             host = parsed_url.hostname
#             port = parsed_url.port or 80

#             # Create connection to destination server
#             server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             server_socket.connect((host, port))

#             # Forward client request to destination server
#             server_socket.sendall(request)

#             # Receive response from destination server and forward to client
#             while True:
#                 response = server_socket.recv(self.buffer_size)
#                 if len(response) > 0:
#                     client_socket.sendall(response)
#                 else:
#                     break

#             server_socket.close()

#         except Exception as e:
#             print(f"[!] HTTP Error: {e}")

#     def handle_https(self, client_socket, request_line):
#         """Handle HTTPS CONNECT requests (SSL tunnel)"""
#         try:
#             # Extract host and port from CONNECT request
#             url = request_line.split(" ")[1]
#             host, port = url.split(":")
#             port = int(port)

#             # Create connection to destination server
#             server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             server_socket.connect((host, port))

#             # Send success response to client
#             client_socket.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")

#             # Set sockets to non-blocking mode for bidirectional forwarding
#             client_socket.setblocking(False)
#             server_socket.setblocking(False)

#             # Forward data between client and server
#             while True:
#                 try:
#                     # Client to Server
#                     data = client_socket.recv(self.buffer_size)
#                     if data:
#                         server_socket.sendall(data)
#                 except:
#                     pass

#                 try:
#                     # Server to Client
#                     data = server_socket.recv(self.buffer_size)
#                     if data:
#                         client_socket.sendall(data)
#                 except:
#                     pass

#         except Exception as e:
#             print(f"[!] HTTPS Error: {e}")


# if __name__ == "__main__":
#     # You can customize host and port here
#     proxy = ProxyServer(host="192.168.100.121", port=8888)
#     proxy.start()

#!/usr/bin/env python3
"""
Simple HTTP Proxy Server
A basic implementation to learn proxy concepts
"""

import socket
import threading
import sys
from urllib.parse import urlparse

class ProxyServer:
    def __init__(self, host='0.0.0.0', port=8888):
        self.host = host
        self.port = port
        self.buffer_size = 8192
        self.running = True
        self.server_socket = None
        
    def start(self):
        """Start the proxy server"""
        try:
            # Create a TCP socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Set timeout to allow periodic checks for shutdown
            self.server_socket.settimeout(1.0)
            
            # Bind to host and port
            self.server_socket.bind((self.host, self.port))
            
            # Listen for incoming connections (max 50 queued)
            self.server_socket.listen(50)
            
            print(f"[*] Proxy server running on {self.host}:{self.port}")
            print(f"[*] Configure your browser to use this proxy")
            print(f"[*] Press Ctrl+C to stop\n")
            
            while self.running:
                try:
                    # Accept client connection
                    client_socket, client_address = self.server_socket.accept()
                    print(f"[+] Connection from {client_address[0]}:{client_address[1]}")
                    
                    # Handle each client in a separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except socket.timeout:
                    # Timeout allows us to check if we should keep running
                    continue
                except OSError:
                    # Socket was closed
                    break
                
        except KeyboardInterrupt:
            print("\n[!] Shutting down proxy server...")
        except Exception as e:
            print(f"[!] Error starting server: {e}")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Cleanly shutdown the server"""
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
                print("[*] Server socket closed")
            except:
                pass
        print("[*] Shutdown complete")
        sys.exit(0)
    
    def handle_client(self, client_socket, client_address):
        """Handle individual client requests"""
        try:
            # Receive request from client
            request = client_socket.recv(self.buffer_size)
            
            if not request:
                client_socket.close()
                return
            
            # Parse the request to get the destination
            request_line = request.decode('utf-8', errors='ignore').split('\n')[0]
            print(f"[→] {request_line}")
            
            # Extract URL from request
            url = request_line.split(' ')[1]
            
            # Determine if this is a CONNECT request (HTTPS) or regular HTTP
            if request_line.startswith('CONNECT'):
                self.handle_https(client_socket, request_line)
            else:
                self.handle_http(client_socket, request, url)
                
        except Exception as e:
            print(f"[!] Error handling client: {e}")
        finally:
            client_socket.close()
    
    def handle_http(self, client_socket, request, url):
        """Handle HTTP requests"""
        try:
            # Check if this is a direct request to the proxy itself
            if url == '/' or url.startswith(f'http://{self.host}') or url.startswith(f'http://localhost'):
                # Send a welcome page
                response = b"""HTTP/1.1 200 OK\r
Content-Type: text/html\r
Connection: close\r
\r
<!DOCTYPE html>
<html>
<head><title>Proxy Server</title></head>
<body>
<h1>HTTP Proxy Server is Running!</h1>
<p>This is a proxy server. Configure your browser to use this proxy.</p>
<p>Proxy Address: """ + f"{self.host}:{self.port}".encode() + b"""</p>
<p>This page appears because you accessed the proxy directly.</p>
</body>
</html>"""
                client_socket.sendall(response)
                return
            
            # Parse the URL
            parsed_url = urlparse(url if url.startswith('http') else 'http://' + url)
            host = parsed_url.hostname
            port = parsed_url.port or 80
            
            # Check if we got a valid hostname
            if not host:
                error_response = b"HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nInvalid URL"
                client_socket.sendall(error_response)
                return
            
            # Create connection to destination server
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.settimeout(10)
            server_socket.connect((host, port))
            
            # Forward client request to destination server
            server_socket.sendall(request)
            
            # Receive response from destination server and forward to client
            while True:
                response = server_socket.recv(self.buffer_size)
                if len(response) > 0:
                    client_socket.sendall(response)
                else:
                    break
            
            server_socket.close()
            
        except Exception as e:
            print(f"[!] HTTP Error: {e}")
    
    def handle_https(self, client_socket, request_line):
        """Handle HTTPS CONNECT requests (SSL tunnel)"""
        try:
            # Extract host and port from CONNECT request
            url = request_line.split(' ')[1]
            host, port = url.split(':')
            port = int(port)
            
            # Create connection to destination server
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((host, port))
            
            # Send success response to client
            client_socket.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            
            # Set sockets to non-blocking mode for bidirectional forwarding
            client_socket.setblocking(False)
            server_socket.setblocking(False)
            
            # Forward data between client and server
            while True:
                try:
                    # Client to Server
                    data = client_socket.recv(self.buffer_size)
                    if data:
                        server_socket.sendall(data)
                except:
                    pass
                
                try:
                    # Server to Client
                    data = server_socket.recv(self.buffer_size)
                    if data:
                        client_socket.sendall(data)
                except:
                    pass
            
        except Exception as e:
            print(f"[!] HTTPS Error: {e}")

if __name__ == "__main__":
    # You can customize host and port here
    proxy = ProxyServer(host='0.0.0.0', port=8888)
    proxy.start()