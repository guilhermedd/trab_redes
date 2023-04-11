import os
import sys
import time

def play_manual(sock, host, port,):

    def clear_terminal():
        syst = 'cls' if os.name == 'nt' else 'clear'
        os.system(syst)

    def send_message(sock, message):
        sock.sendall(message.encode('UTF-8'))

    def show_message(message, sleeping = 0.5):
        for l in message:
            sys.stdout.write(l)
            sys.stdout.flush()
            if l == '.':
                sleeping = 0.1
            else:
                sleeping = 0.05
            time.sleep(sleeping)
        print('\n')

    def get_monster_response(life):
        response = sock.recv(1024).decode('ASCII').split(';')
        if response[0] == "MONSTER_KILLED":
            show_message('Você derrotou o monstro! :D')
        else:
            show_message('O monstro desviou e te atacou! :(')
            show_message('Você está com {} de vida'.format(response[1]))
            life = int(response[1])
        return life, int(response[2])

    def get_monster_atack(msg, num, life):
        show_message(msg)
        answer = str(input())
        while not answer.isdigit() or int(answer) < 0 or int(answer) > int(num):
            show_message('Resposta inválida, bobinho! Digite um número de 0 a {}'.format(num))
            answer = str(input())
        send_message(sock, answer)

        return get_monster_response(life)

    def get_nothing():
        show_message('Nada aconteceu... Voce resolveu continuar a aventura!')

    def get_chest(points):
        show_message('Você encontrou um baú hihihi!\nPode ser que lá tenha algo bom... ou algo ruim...\nDeseja abrir o baú? (S/N)')
        answer = str(input())
        while answer != 'S' and answer != 's' and answer != 'N' and answer != 'n':
            show_message('Resposta inválida, bobinho! Digite S ou N')
            answer = str(input())
        send_message(sock, 'YES' if answer == 'S' or answer == 's' else 'NO')
        if answer == 'S' or answer == 's':
            pts = sock.recv(1024).decode('ASCII').split(';')[1]
            show_message('Você abriu o baú e encontrou {} pontos!'.format(pts))
            points += int(pts)
        else:
            sock.recv(1024).decode('ASCII')
            show_message('Você decidiu não abrir o baú :/')

        return points if points > 0 else 0

    def game_over(message):
        show_message(f'Fim de jogo!, voce {"GANHOU" if message == "WIN" else "PERDEU"}')
        sock.close()

    def get_boss(life):
        show_message('Você se deparou com o chefe do jogo!!!\nVoce quer lutar contra ele?')
        show_message('Se voce escolher lutar e morrer, poderá perder bastante vida...')
        show_message('Se voce escolher fugir, perderá um pouco de vida...')
        show_message('Desejas lutar? (S/N)', sleeping=0.01)
        answer = str(input())
        while answer != 'S' and answer != 's' and answer != 'N' and answer != 'n':
            show_message('Resposta inválida, bobinho! Digite S ou N')
            answer = str(input())
        if answer == 'S' or answer == 's':
            send_message(sock, 'FIGHT')
            print('Voce escolheu LUTAR!')
        else:
            send_message(sock, 'RUN')

        response = sock.recv(1024).decode('ASCII').split(';')
        if response[0] == 'BOSS_DEFEATED':
            show_message('Você derrotou o chefe! :D')
            show_message('E você ganhou {} pontos!'.format(response[2]))
        elif response[0] == 'FAILED_BOSS_FIGHT':
            show_message('O chefe desviou e te atacou! :(')
            show_message('Você está com {} de vida'.format(response[1]))
            life = response[1]
        else:
            show_message('Você fugiu do chefe! Mas está com {} de vida!'.format(response[1]))
        life = int(response[1])
        return life, int(response[2])
    # Connect to server
    sock.connect((host, port))

    # Start game
    send_message(sock, 'START')

    life = 100
    points = 0
    room = 0

    while True:
        clear_terminal()
        room += 1
        print(f"Room: {room}")
        # Receive message
        response = sock.recv(1024).decode('ASCII').split(';')

        try:
            if response[0] != 'NOTHING_HAPPENED' and response[0] != 'TAKE_CHEST' :
                life = int(response[2]) if response[0] == 'MONSTER_ATTACK' else int(response[1])
                points = int(response[3])
        except IndexError:
            pass
        show_message(' --- SUA VIDA: {} ---\n--- SEUS PONTOS: {} ---'.format(life, points))

        if response[0] == 'GAME_OVER' or response == 'WIN':
            game_over(response[0])
            break

        # print(response) # verificar se response não está vazio

        elif response[0] == 'MONSTER_ATTACK':
            life, points = get_monster_atack('AH MEU DEUS, O MONSTRO TE ATACOU!!!\nRÁPIDO! Escolha um número de 0 a {} para contra-atacar!'.format(response[1]), response[1], life)
            send_message(sock, 'WALK')

        elif response[0] == "TAKE_CHEST":
            points = get_chest(points)
            send_message(sock, 'WALK')

        elif response[0] == "BOSS_EVENT":
            life, points = get_boss(life)
            send_message(sock, 'WALK')
            # sock.recv(1024)

        elif response[0] == "NOTHING_HAPPENED":
            get_nothing()
            send_message(sock, 'WALK')

        if room >= 20:
            game_over('WIN')
            break

        elif  int(life) <= 0:
            game_over('LOSE')
            break

        print('Para seguir para a próxima sala, aperte ENTER')
        if input():
            send_message(sock, 'WALK')
