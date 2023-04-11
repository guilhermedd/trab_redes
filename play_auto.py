from AI import QLearn
import time
import sys
import os

def play_auto(sock, host, port,):

    qlearn = QLearn()
    state = 0

    def clear_terminal():
        syst = 'cls' if os.name == 'nt' else 'clear'
        os.system(syst)

    def send_message(sock, message):
        sock.sendall(message.encode('UTF-8'))

    def show_message(message, sleeping = 0.1):
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
        efficacy = 0
        if response[0] == "MONSTER_KILLED":
            show_message('Você derrotou o monstro! :D')
        else:
            show_message('O monstro desviou e te atacou! :(')
            show_message('Você está com {} de vida'.format(response[1]))
            life = response[1]
            efficacy = -1
        return life, efficacy, int(response[2])

    def get_monster_atack(msg, num, life, choice):
        show_message(msg)
        answer = str(choice)
        print(f'Eu escolho... {answer}')
        send_message(sock, answer)

        return get_monster_response(life)

    def get_nothing():
        show_message('Nada aconteceu... Voce resolveu continuar a aventura!')

    def get_chest(choice, points):
        show_message('Você encontrou um baú hihihi!\nPode ser que lá tenha algo bom... ou algo ruim...\nDeseja abrir o baú? (S/N)')
        print('Eu escolho: ' + str(choice))
        answer = str(choice)
        send_message(sock, answer)
        if answer == 'YES':
            pontos = sock.recv(1024).decode('ASCII').split(';')[1]
            show_message('Você abriu o baú e encontrou {} pontos!'.format(pontos))
            points += int(pontos)
            return -1 if int(pontos) < 0 else 1, int(points) if int(points) > 0 else 0
        else:
            sock.recv(1024).decode('ASCII')
            show_message('Você decidiu não abrir o baú :/')
            return 0, int(points)

    def game_over(message):
        show_message(f'Fim de jogo!, voce {"GANHOU" if message == "WIN" else "PERDEU"}')
        sock.close()

    def get_boss(choice, life):
        show_message('Você se deparou com o chefe do jogo!!!\nVoce quer lutar contra ele?')
        show_message('Se voce escolher lutar e morrer, poderá perder bastante vida...')
        show_message('Se voce escolher fugir, perderá um pouco de vida...')
        show_message('Desejas lutar? (S/N)', sleeping=0.01)
        answer = str(choice)
        print(f'Eu escolho...{answer}')
        send_message(sock, answer)

        response = sock.recv(1024).decode('ASCII').split(';')
        life = response[1]
        if response[0] == 'BOSS_DEFEATED':
            show_message('Você derrotou o chefe! :D')
            show_message('E você ganhou {} pontos!'.format(response[2]))
            return  1, life
        elif response[0] == 'FAILED_BOSS_FIGHT':
            show_message('O chefe desviou e te atacou! :(')
            show_message('Você está com {} de vida'.format(response[1]))
            return -1, life
        show_message('Você fugiu do chefe! Mas está com {} de vida!'.format(response[1]))
        return 0, life, int(response[2])

    # Connect to server
    sock.connect((host, port))

    # Start game
    send_message(sock, 'START')

    life = 100
    points = 0
    room = 0
    next_state = 0

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
            life += 0
            points += 0    # send_message(sock, 'WALK')
        show_message(' --- SUA VIDA: {} ---\n--- SEUS PONTOS: {} ---'.format(life, points))

        if response[0] == 'GAME_OVER' or response == 'WIN':
            game_over(response[0])
            break

        # print(response) # verificar se response não está vazio

        elif response[0] == 'MONSTER_ATTACK':
            state = 0
            choice = qlearn.choose_action(event='MONSTER_ATTACK', num=response[1], state=state)
            life, reward, points = get_monster_atack('AH MEU DEUS, O MONSTRO TE ATACOU!!!\nRÁPIDO! Escolha um número de 0 a {} para contra-atacar!'.format(response[1]), response[1], life, choice)
            send_message(sock, 'WALK')

        elif response[0] == "TAKE_CHEST":
            state = 1
            choice = qlearn.choose_action(event='TAKE_CHEST', state=state, num = 0)
            reward, points = get_chest(choice, points)
            send_message(sock, 'WALK')

        elif response[0] == "BOSS_EVENT":
            state = 2
            choice = qlearn.choose_action(event='BOSS_EVENT', state=state, num = 0)
            reward, life, points = get_boss(choice, life)
            send_message(sock, 'WALK')
            # sock.recv(1024)

        elif response[0] == "NOTHING_HAPPENED":
            get_nothing()
            send_message(sock, 'WALK')

        # send_message(sock, 'WALK')
        if response[0] != "NOTHING_HAPPENED":
            qlearn.learn(response[0], choice, reward, state)

        if room >= 20:
            game_over('WIN')
            break
        elif  int(life) <= 0:
            game_over('LOSE')
            break

        time.sleep(1.5)
