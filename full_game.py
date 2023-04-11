import socket
from AI import QLearn
from play_manual import play_manual
from play_auto import play_auto

HOST = 'localhost'
PORT = 12000
sock = socket.socket(socket.AF_INET, # internet
                        socket.SOCK_STREAM) # TCP

if __name__ == '__main__':
    print('voce quer jogar (1) ou quer que a IA jogue sozinha (2)?')
    result = input()
    while result != '1' and result != '2':
        print('voce quer jogar (1) ou quer que a IA jogue sozinha (2)?')
        result = input()
    if result == '1':
        play_manual(sock, HOST, PORT)
    else:
        play_auto(sock, HOST, PORT)
