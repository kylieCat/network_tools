import socket
from HTTPExceptions import HTTP400Error, HTTP404Error, HTTP405Error

def request_parser(raw_request):
    import pdb; pdb.set_trace()
    raw_request = raw_request.split('\r\n')
    keys = ('method', 'URI', 'protocol')
    request = dict(zip(keys, raw_request[0].split()))
    for element in raw_request[1:]:
        if element.lower().startswith('host:'):
            request['host'] = element.split()[1]
            break
    return request if len(request) == 4 else 
    
    if len(request) != 3:
        raise IndexError
    method, URI, protocol, host_key, host = request[:5]
    if method != "GET":
        raise AttributeError
    if URI[0] != "/":
        raise SyntaxError
    if protocol.strip() != "HTTP/1.1":
        raise NameError
    if host_key not in ("Host:"):
        raise ValueError
    return URI


def http_server():
    SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    SERVER_SOCKET.bind(('127.0.0.1', 50000))
    print('Waiting for message...')
    while True:
        final_output = ''
        done = False
        buffsize = 32
        SERVER_SOCKET.listen(1)
        conn, addr = SERVER_SOCKET.accept()
        while not done:
            msg_part = conn.recv(buffsize)
            final_output += msg_part
            if len(msg_part) < buffsize:
                done = True
        try:
            URI = request_parser(final_output)
            response = "200 OK: Your URI is {}".format(URI)
        except IndexError:
            response = "400 Bad Request"
        except AttributeError:
            response = "405 Method Not Allowed"
        except SyntaxError:
            response = "404 Not Found"
        except NameError:
            response = "400 Bad Request"
        except ValueError:
            response = "404 Not Found"
        conn.sendall(response)
        conn.close()
       # if final_output:
        #    break
    SERVER_SOCKET.close()
    return final_output


if __name__ == '__main__':
    http_server()