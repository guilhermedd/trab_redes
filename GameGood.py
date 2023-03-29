import socket
import time
import sys

HOST = 'localhost'
PORT = 12000
sock = socket.socket(socket.AF_INET, # internet
                        socket.SOCK_STREAM) # TCP

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

def play(sock):
    # Connect to server
    sock.connect((HOST, PORT))

    # Start game
    send_message(sock, 'START')

    #Enter the game
    # response = sock.recv(1024).decode('ASCII')
    # print(response)
    # Receive message
    life = 0
    points = 0
    while True:
        response = sock.recv(1024).decode('ASCII')
        try:
            life = int(response.split(';')[2])
            points = int(response.split(';')[3])
            show_message(' --- SUA VIDA: {}---\n--- SEUS PONTOS: {} ---'.format(life, points))
        except IndexError:
            life += 0
            points += 0    # send_message(sock, 'WALK')

        if response == 'GAME_OVER' or response == 'WIN':
            show_message('Fim de jogo!')
            sock.close()
            break

        # print(response) # verificar se response não está vazio

        elif response.startswith("MONSTER_ATTACK;"):
            show_message('AH MEU DEUS, O MONSTRO TE ATACOU!!!\nRÁPIDO! Escolha um número de 0 a {} para contra-atacar!'.format(response.split(';')[1]))
            answer = str(input())
            while not answer.isdigit() or int(answer) < 0 or int(answer) > int(response.split(';')[1]):
                show_message('Resposta inválida, bobinho! Digite um número de 0 a {}'.format(response.split(';')[1]))
                answer = str(input())
            send_message(sock, answer)
            # print(sock.recv(1024).decode('ASCII'))

        elif response.startswith("TAKE_CHEST"):
            show_message('Você encontrou um baú hihihi!\nPode ser que lá tenha algo bom... ou algo ruim...\nDeseja abrir o baú? (S/N)')
            answer = str(input())
            while answer != 'S' and answer != 's' and answer != 'N' and answer != 'n':
                show_message('Resposta inválida, bobinho! Digite S ou N')
                answer = str(input())
            if answer == 'S' or answer == 's':
                send_message(sock, 'YES')
            elif answer == 'N' or answer == 'n':
                send_message(sock, 'NO')
            # sock.recv(1024)

        elif response.startswith("BOSS_EVENT"):
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
            # sock.recv(1024)

        elif response.startswith("NOTHING_HAPPENED"):
            send_message(sock, 'WALK')

        else:
            if response.startswith("CHEST_VALUE"):
                show_message('Você abriu o baú e encontrou {} pontos!'.format(response.split(';')[1]))
            elif response.startswith("FAILED_BOSS_FIGHT"):
                show_message(f'Você perdeu sua luta contra o chefe e perdeu {response.split(";")[1]} de vida... :(')
            elif response.startswith("ESCAPED"):
                show_message('Você conseguiu fugir do chefe!\n...Mas perdeu um pouco de vida :/')
                show_message('Você está com {} de vida'.format(response.split(';')[1]))
            elif response.startswith("BOSS_DEFEATED"):
                show_message('Você derrotou o chefe! :D')
                show_message('E ficou com {} pontos :D'.format(response.split(';')[2]))
                show_message('Mas... perdeu {} pontos de vida :D'.format(response.split(';')[1]))
            elif response.startswith("MONSTER_KILLED"):
                show_message('Você derrotou o monstro! :D')
                show_message('E você ganhou {} pontos!'.format(response.split(';')[2]))
            elif response.startswith("MONSTER_ESCAPED"):
                show_message('Você não conseguiu derrotar o monstro... :(')
            elif response.startswith("MONSTER_ATTACKED"):
                show_message('O monstro desviou e te atacou! :(')
                show_message('Você está com {} de vida'.format(response.split(';')[1]))
            elif response.startswith("FAILED_BOSS_FIGHT"):
                show_message('Você perdeu sua luta contra o chefe... :(')
            elif response.startswith("SKIPPING_CHEST"):
                show_message('Você decidiu não abrir o baú :/')
            elif response.startswith("GAME_OVER") or response.startswith("WIN"):
                show_message('Fim de jogo!')
                sock.close()
                break
            else:
                show_message(response)

            send_message(sock, 'WALK')

if __name__ == '__main__':
    play(sock)
    sock.close()
