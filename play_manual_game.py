import os
import sys
import time

import pygame

def play_manual_game(sock, host, port,):
     pygame.init()
     clock = pygame.time.Clock()
     fps = 60

     # Set the width and height of the screen [width, height]
     size = (800, 400)
     bottom_panel = 150
     screen = pygame.display.set_mode((size[0], size[1] + bottom_panel))
     pygame.display.set_caption("RPG")

     # Background Image
     background_image = pygame.image.load('.\img\Background/background.png').convert_alpha()
     background_image = pygame.transform.scale(background_image, (size[0], size[1]))

     panel_image = pygame.image.load('./img/Icons/panel.png').convert_alpha()
     panel_image = pygame.transform.scale(panel_image, (size[0], bottom_panel))

     def draw_bg():
     # screen.llit(background_image, [0, 0])
          screen.blit(background_image, (0, 0))

     def draw_panel():
     # screen.llit(background_image, [0, 0])
          screen.blit(panel_image, (0, size[1]))

     def get_input(events):
          for event in events:
               if event.type == pygame.QUIT:
                # Exit the game if the user closes the window
                    pygame.quit()
                    quit()
               elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Set the input box to active if the user clicks on it
                    if input_box.collidepoint(event.pos):
                         input_active = True
                    else:
                         input_active = False
               elif event.type == pygame.KEYDOWN:
                    # Add characters to the user input if the input box is active
                    if input_active:
                         if event.key == pygame.K_RETURN:
                              # Save the user input and clear the input box
                              print("User input:", user_input)
                              user_input = ""
                         elif event.key == pygame.K_BACKSPACE:
                              # Remove the last character from the user input
                              user_input = user_input[:-1]
                         else:
                              # Add the character to the user input
                              user_input += event.unicode
          return user_input

     def write_panel(msg, x, y):
          WHITE = (255, 255, 255)
          font = pygame.font.Font('freesansbold.ttf', 32)
          text = font.render(str(msg), True, WHITE)
          txt = text.get_rect()
          txt.center = (x, y)
          screen.blit(text, txt)

     class Fighter():
          def __init__(self, x, y, max_health, points, room):
               self.max_health = max_health
               self.health = max_health
               self.x = x
               self.y = y
               self.points = points
               self.room = room
               self.alive = True
               self.img_path = './img\Knight\Idle/0.png'
               img = pygame.image.load(self.img_path).convert_alpha()
               self.image = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
               self.rect = self.image.get_rect()
               self.rect.center = (self.x, self.y)

          def loose_health(self, hp):
               self.health -= hp

          def draw(self):
               screen.blit(self.image, (self.x, self.y))

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
               pass
               # show_message('Você derrotou o monstro! :D')
          else:
               # show_message('O monstro desviou e te atacou! :(')
               # show_message('Você está com {} de vida'.format(response[1]))
               life = response[1]
          return life

     def get_monster_atack(msg, num, life, choice):
          # show_message(msg)
          answer = str(choice)
          send_message(sock, answer)

          return get_monster_response(life)

     def get_nothing():
          pass
          # show_message('Nada aconteceu... Voce resolveu continuar a aventura!')

     def get_chest(points, choice):
          # show_message('Você encontrou um baú hihihi!\nPode ser que lá tenha algo bom... ou algo ruim...\nDeseja abrir o baú? (S/N)')
          answer = str(choice)
          send_message(sock, 'YES' if answer == 'S' or answer == 's' else 'NO')
          if answer == 'S' or answer == 's':
               pts = sock.recv(1024).decode('ASCII').split(';')[1]
               # show_message('Você abriu o baú e encontrou {} pontos!'.format(pts))
               points += int(pts)
          else:
               sock.recv(1024).decode('ASCII')
               # show_message('Você decidiu não abrir o baú :/')

          return points if points > 0 else 0

     def game_over(message):
          # show_message(f'Fim de jogo!, voce {"GANHOU" if message == "WIN" else "PERDEU"}')
          sock.close()

     def get_boss(life, choice):
          # show_message('Você se deparou com o chefe do jogo!!!\nVoce quer lutar contra ele?')
          # show_message('Se voce escolher lutar e morrer, poderá perder bastante vida...')
          # show_message('Se voce escolher fugir, perderá um pouco de vida...')
          # show_message('Desejas lutar? (S/N)', sleeping=0.01)
          answer = str(choice)
          if answer == 'S' or answer == 's':
               send_message(sock, 'FIGHT')
               print('Voce escolheu LUTAR!')
          else:
               send_message(sock, 'RUN')

          response = sock.recv(1024).decode('ASCII').split(';')
          if response[0] == 'BOSS_DEFEATED':
               pass
               # show_message('Você derrotou o chefe! :D')
               # show_message('E você ganhou {} pontos!'.format(response[2]))
          elif response[0] == 'FAILED_BOSS_FIGHT':
               # show_message('O chefe desviou e te atacou! :(')
               # show_message('Você está com {} de vida'.format(response[1]))
               life = response[1]
          else:
               # show_message('Você fugiu do chefe! Mas está com {} de vida!'.format(response[1]))
               life = response[1]
          return life
     # Connect to server
     sock.connect((host, port))

     # Start game
     # send_message(sock, 'START')

     life = 100
     points = 0
     room = 0
     knight = Fighter(70, 180, life, points, room)
     run = True
     while run:
          # GAME PART
          clock.tick(fps)
          draw_bg()

          # Draw background
          draw_panel()
          write_panel(knight.room, size[0] // 2, 50)
          knight.draw()
          knight.room += 1

          events = pygame.event.get()
          for event in events:
               events = pygame.event.get()
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
               # show_message(' --- SUA VIDA: {} ---\n--- SEUS PONTOS: {} ---'.format(life, points))

               if response[0] == 'GAME_OVER' or response == 'WIN':
                    game_over(response[0])
                    break

               # print(response) # verificar se response não está vazio

               elif response[0] == 'MONSTER_ATTACK':
                    # Fighter(700, 180, life, points, room).draw()
                    write_panel('AH MEU DEUS, O MONSTRO TE ATACOU!!!\nRÁPIDO! Escolha um número de 0 a {} para contra-atacar!'.format(response[1]), 50, 50)
                    input_box = pygame.Rect(50, 100, 300, 50)
                    user_input = ""
                    input_active = False
                    user_input = get_input(events)

                    life = get_monster_atack('AH MEU DEUS, O MONSTRO TE ATACOU!!!\nRÁPIDO! Escolha um número de 0 a {} para contra-atacar!'.format(response[1]), response[1], life, user_input)
                    send_message(sock, 'WALK')

               elif response[0] == "TAKE_CHEST":
                    points = get_chest(points)
                    send_message(sock, 'WALK')

               elif response[0] == "BOSS_EVENT":
                    life = get_boss(life)
                    send_message(sock, 'WALK')
                    # sock.recv(1024)

               elif response[0] == "NOTHING_HAPPENED":
                    get_nothing()
                    send_message(sock, 'WALK')

               if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    quit()
          pygame.display.update()
