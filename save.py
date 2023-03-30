import socket
import time
import sys

HOST = 'localhost'
PORT = 12000
sock = socket.socket(socket.AF_INET, # internet
                        socket.SOCK_STREAM) # TCP

def play(sock):

    def send_message(sock, message):
        sock.sendall(message.encode('UTF-8'))

    def show_message(message, sleeping = 0.05):
        for l in message:
            sys.stdout.write(l)
            sys.stdout.flush()
            if l == '.':
                sleeping = 0.1
            time.sleep(sleeping)
        print('\n')

    def get_monster_response(response):
        if response == "MONSTER_KILLED":
            show_message('Você derrotou o monstro! :D')
            show_message('E você ganhou {} pontos!'.format(response[2]))
        else:
            show_message('O monstro desviou e te atacou! :(')
            show_message('Você está com {} de vida'.format(response[1]))

    def get_monster_atack(msg, num):
        show_message(msg)
        answer = str(input())
        while not answer.isdigit() or int(answer) < 0 or int(answer) > int(num):
            show_message('Resposta inválida, bobinho! Digite um número de 0 a {}'.format(num))
            answer = str(input())
        send_message(sock, answer)

        get_monster_response(sock.recv(1024).decode('ASCII').split(';')[0])

    def get_nothing():
        show_message('Nada aconteceu... Voce resolveu continuar a aventura!')
        send_message(sock, 'WALK')

    def get_chest():
        show_message('Você encontrou um baú hihihi!\nPode ser que lá tenha algo bom... ou algo ruim...\nDeseja abrir o baú? (S/N)')
        answer = str(input())
        while answer != 'S' and answer != 's' and answer != 'N' and answer != 'n':
            show_message('Resposta inválida, bobinho! Digite S ou N')
            answer = str(input())
        send_message(sock, 'YES' if answer == 'S' or answer == 's' else 'NO')
        if answer == 'S' or answer == 's':
            show_message('Você abriu o baú e encontrou {} pontos!'.format(sock.recv(1024).decode('ASCII').split(';')[1]))
        else:
            sock.recv(1024).decode('ASCII')
            show_message('Você decidiu não abrir o baú :/')

    def game_over(message):
        show_message(f'Fim de jogo!, voce {"GANHOU" if message == "WIN" else "PERDEU"}')
        sock.close()

    def get_boss():
        show_message('Você se deparou com o chefe do jogo!!!\nVoce quer lutar contra ele?')
        show_message('Se voce escolher lutar e morrer, poderá perder bastante vida...')
        show_message('Se voce escolher fugir, perderá um pouco de vida...')
        show_message('Sim ou não? (S/N)', sleeping=0.01)
        answer = str(input())
        while answer != 'S' and answer != 's' and answer != 'N' and answer != 'n':
            show_message('Resposta inválida, bobinho! Digite S ou N')
            answer = str(input())
        if answer == 'S' or answer == 's':
            send_message(sock, 'FIGHT')
        else:
            send_message(sock, 'RUN')

        response = sock.recv(1024).decode('ASCII').split(';')[0]
        if response == 'BOSS_KILLED':
            show_message('Você derrotou o chefe! :D')
            show_message('E você ganhou {} pontos!'.format(response[1]))
        elif response == 'FILED_BOSS_FIGHT':
            show_message('O chefe desviou e te atacou! :(')
            show_message('Você está com {} de vida'.format(response[1]))
        else:
            show_message('Você fugiu do chefe e perdeu {} de vida!'.format(response[2]))

    # Connect to server
    sock.connect((HOST, PORT))

    # Start game
    send_message(sock, 'START')

    life = 0
    points = 0

    while True:
        # Receive message
        response = sock.recv(1024).decode('ASCII').split(';')

        try:
            life = int(response[2])
            points = int(response[3])
            show_message(' --- SUA VIDA: {}---\n--- SEUS PONTOS: {} ---'.format(life, points))
        except IndexError:
            life += 0
            points += 0    # send_message(sock, 'WALK')

        if response == 'GAME_OVER' or response == 'WIN':
            game_over()
            break

        # print(response) # verificar se response não está vazio

        elif response[0] == 'MONSTER_ATTACK':
            get_monster_atack('AH MEU DEUS, O MONSTRO TE ATACOU!!!\nRÁPIDO! Escolha um número de 0 a {} para contra-atacar!'.format(response[1]), response[1])

        elif response[0] == "TAKE_CHEST":
            get_chest()

        elif response[0] == "BOSS_EVENT":
            get_boss
            # sock.recv(1024)

        elif response[0] == "NOTHING_HAPPENED":
            get_nothing()

        else:
            show_message(response[0])

            send_message(sock, 'WALK')

if __name__ == '__main__':
    play(sock)
