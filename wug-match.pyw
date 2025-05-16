import os, sys, pygame, random, csv
from datetime import datetime

##########
# Appearances
##########

window_width = 1400
window_height = 900

white = '#ffffff'
green = '#e6f4f1'
brown = '#875300'
wug ='#a0c0e7'
space = '#013150'

##########
# Classes
##########
class Card:
    def __init__(self, text, pos, index):
        self.index = index
        self.open = False
        self.flipping = False
        self.selected = False
        self.original_y_pos = pos[1]
        self.elevation = -10
        self.dynamic_elecation = -10
        self.width = 100
        self.height = 150
        self.border_width = 4
        self.flip_start_time = None
        self.flip_duration = 300

        # card rectangle
        self.rect = self.cover_rect = pygame.Rect(pos,(self.width,self.height))
        self.small_rect = pygame.Rect((pos[0]+self.border_width, pos[1]+self.border_width),(self.width-(self.border_width*2),self.height-(self.border_width*2)))
        self.flipping_rect = pygame.Rect((pos[0]+(self.width/4), pos[1]),(self.width-(self.width/2),self.height))
        self.flipping_small_rect = pygame.Rect((pos[0]+self.border_width+(self.width/4), pos[1]+self.border_width),(self.width-(self.border_width*2)-(self.width/2),self.height-(self.border_width*2)))

        # card colors
        self.front_color = green
        self.back_color = space
        self.border_color = wug

        # card text
        self.text = text
        self.text_surf = card_font.render(text,True,space)
        self.text_rect = self.text_surf.get_rect(center = self.rect.center)

    def draw(self):
        # manipulate y position for lifting
        if self.selected:
            self.dynamic_elecation = self.elevation
        else:
            self.dynamic_elecation = 0
        self.rect.y = self.flipping_rect.y = self.original_y_pos + self.dynamic_elecation
        self.small_rect.y = self.flipping_small_rect.y= self.original_y_pos + self.border_width + self.dynamic_elecation
        self.text_rect.center = self.rect.center 
        
        # draw different states according to the state
        if self.open:
            pygame.draw.rect(screen,self.front_color, self.rect,border_radius = 12)
            screen.blit(self.text_surf, self.text_rect)
        # elif self.flipping:
        #     #pygame.draw.rect(screen,white, self.cover_rect,border_radius = 12)
        #     pygame.draw.rect(screen,self.border_color,self.flipping_rect,border_radius = 12)
        #     pygame.draw.rect(screen,self.back_color, self.flipping_small_rect,border_radius = 12)
        else:
            #pygame.draw.rect(screen,white, self.cover_rect,border_radius = 12)
            pygame.draw.rect(screen,self.border_color,self.rect,border_radius = 12)
            pygame.draw.rect(screen,self.back_color, self.small_rect,border_radius = 12)
        self.check_click()

    def check_click(self):
        if input_lock:
            return
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(screen,white, self.cover_rect,border_radius = 12)
                if not self.open and indices[self.index] not in selected and len(selected) < 2:
                    self.selected = True
                    selected.append(indices[self.index])
            elif pygame.mouse.get_pressed()[2]:
                pygame.draw.rect(screen,white, self.cover_rect,border_radius = 12)
                self.selected = False
                try:
                    selected.remove(indices[self.index])
                except ValueError:
                    pass
    
    # def flip(self):
    #     if self.selected and not self.flipping:
    #         self.flipping = True
    #         self.flip_start_time = pygame.time.get_ticks()
    
    # def update(self):
    #     if self.flipping:
    #         current_time = pygame.time.get_ticks()
    #         if current_time - self.flip_start_time >= self.flip_duration:
    #             self.flipping = False

# button code from:
# https://pythonprogramming.sssaltervista.org/buttons-in-pygame/?doing_wp_cron=1685564739.9689290523529052734375
class Button:
    def __init__(self,text,width,height,pos,elevation,onclickFunction=None):
        #Core attributes 
        self.pressed = False
        self.onclickFunction = onclickFunction
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = space

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = wug
        #text
        self.text = text
        self.text_surf = text_font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = green
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.onclickFunction()
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = space

########
# Functions
########

# wipe screen
def wipe():
    pygame.draw.rect(screen, white, pygame.Rect(0, 0, window_width, window_height))
    pygame.display.flip()

# onClickFunction for the quit button
def quit():
    global running
    running = False

# onClickFunction for the start button
def start():
    global started, start_time, recorded, selected, opened
    start_time = pygame.time.get_ticks()
    started = True
    recorded = False
    selected = []
    opened = set()
    #print("started =", started, "opened =", len(opened))
    #print(len(opened) >= 12)
    wipe()

# write high scores
def write_high_score():
    with open(save_file,'w') as highoutput:
        wr = csv.writer(highoutput, lineterminator='\n')
        for record in high_scores:
            wr.writerow([record,high_scores[record]])
########
# Main game
########
def main():
    global screen, card_font, text_font
    global running, started, selected, opened, cards, indices
    global input_lock, start_time, high_scores, save_file
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()
    icon = pygame.image.load('assets/icon.ico')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Wug Match Up')
    screen.fill(white)
    card_font = pygame.font.Font(None,28)
    text_font = pygame.font.Font(None,50)

    # select text
    with open('assets/list.txt', 'r') as f:
        content = f.read().split(',')
        texts = random.sample(content, 6)
    words = texts + texts
    random.shuffle(words)
    #print(words)

    # load high scores
    home_dir = os.path.expanduser("~")
    save_folder = os.path.join(home_dir, "Documents/wug-match-up/data/")
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    save_file = save_folder+'high-scores.csv'
    with open(save_file,'a+') as highinput:
        highinput.seek(0)
        cr = csv.reader(highinput)
        content = [line for line in cr]
        high_scores = {}
        if len(content) > 0:
            for record in content:
                high_scores[int(record[0])] = record[1]

    # manage double esc quit
    esc_pressed = False
    last_esc_time = 0
    double_esc_time = 500  # milliseconds

    # game attributes
    started = False
    recorded = False
    indices = list(range(13))
    selected = []
    opened = set()
    match_check_pending = False
    match_check_time = 0
    match_delay = 1000
    input_lock = False
    start_button = Button('start', 120, 50, (640, 600), 3, start)
    quit_button = Button('quit', 120, 50, (1050, 700), 3, quit)

    # card shapes
    card_width = 100
    card_height = 150
    cols = 4
    rows = 3
    space_width = 1000
    space_height = 700
    x_gap = (space_width - cols * card_width) // (cols + 1)
    y_gap = (space_height - rows * card_height) // (rows + 1)

    # card locations
    locations = []
    index = 0
    for row in range(rows):
        for col in range(cols):
            x = x_gap + col * (card_width + x_gap)
            y = y_gap + row * (card_height + y_gap)
            locations.append([index, x, y])
            index += 1
    cards = [Card(words[i], (locations[i][1], locations[i][2]), locations[i][0]) for i in range(12)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # quit if esc key is pressed twice within double_esc_time (500ms)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    esc_pressed = True
                    current_time = pygame.time.get_ticks()
                    if esc_pressed and (current_time - last_esc_time) < double_esc_time:
                        pygame.quit()
                        sys.exit()
                    esc_pressed = True
                    last_esc_time = current_time
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    esc_pressed = False
        if not started:
            # instructions
            message1 = text_font.render('Wug Match Up', True, space)
            message2 = card_font.render("Find matching pairs of pseudowords!", True, space)
            screen.blit(message1, message1.get_rect(center = (700, 150)))
            screen.blit(message2, message2.get_rect(center = (700, 300)))
            # records
            # high scores
            high_message = text_font.render('high scores', True, space)
            screen.blit(high_message, high_message.get_rect(topleft = (600, 400)))
            scores = list(sorted(high_scores.items()))
            for i in range(3):
                try:
                    mes = card_font.render(scores[i][1]+'  '+str(scores[i][0]) + ' secs', True, space)
                    screen.blit(mes, mes.get_rect(topleft = (600, 450+i*30)))
                except IndexError:
                    mes = card_font.render('No record', True, space)
                    screen.blit(mes, mes.get_rect(topleft = (600, 450+i*30)))
            start_button.draw()
        elif len(opened) >= 12:
            quit_button.draw()
            for card in cards:
                card.open = True
                card.draw()
            # record current score
            if not recorded:
                now = datetime.now()
                now_string = now.strftime("%d/%m/%Y %H:%M")
                if len(high_scores) >= 6:
                    if elapsed_sec <= max(high_scores.keys()):
                        high_scores.pop(max(high_scores.keys()))
                        high_scores[elapsed_sec] = now_string
                else:
                    high_scores[elapsed_sec] = now_string
                write_high_score()
                recorded = True
            # show high scores
            high_message = text_font.render('high scores', True, space)
            screen.blit(high_message, high_message.get_rect(topleft = (1000, 180)))
            scores = list(sorted(high_scores.items()))
            for i in range(6):
                try:
                    if list(sorted(high_scores.items()))[i][1] == now_string:
                        mes = card_font.render(scores[i][1]+'  '+str(scores[i][0])+' secs'+'  New!', True, space)
                        screen.blit(mes, mes.get_rect(topleft = (1000, 220+i*30)))
                    else:
                        mes = card_font.render(scores[i][1]+'  '+str(scores[i][0])+' secs', True, space)
                        screen.blit(mes, mes.get_rect(topleft = (1000, 220+i*30)))
                except IndexError:
                    mes = card_font.render('No record', True, space)
                    screen.blit(mes, mes.get_rect(topleft = (1000, 220+i*30)))
        else:
            #print("game running")
            # show time
            elapsed_ms = pygame.time.get_ticks() - start_time
            elapsed_sec = elapsed_ms // 1000
            #print(elapsed_sec)
            mes = card_font.render('Time:', True, space)
            screen.blit(mes, mes.get_rect(center = (1200, 100)))
            pygame.draw.rect(screen,white, pygame.Rect((1175, 175),(50,50)))
            secs = text_font.render(str(elapsed_sec), True, space)
            screen.blit(secs, secs.get_rect(center = (1200, 200)))

            # draw cards
            for card in cards:
                #card.update()
                if card.index in opened:
                    card.open = True
                card.draw()
            
            # Check if 2 cards are selected
            if len(selected) == 2 and not match_check_pending:
                #print(selected)
                match_check_pending = True
                match_check_time = pygame.time.get_ticks()
                input_lock = True
                # Temporarily show both selected cards
                for i in selected:
                    cards[i].open = True

            # Handle match/mismatch after delay
            if match_check_pending:
                current_time = pygame.time.get_ticks()
                if current_time - match_check_time >= match_delay:
                    if words[selected[0]] == words[selected[1]]:
                        opened.update(selected)
                        #print(opened)
                    else:
                        for i in selected:
                            cards[i].open = False
                            cards[i].selected = False
                    selected.clear()
                    match_check_pending = False
                    wipe()
                    input_lock = False

        pygame.display.flip()
        clock.tick(60)
    
    # quit game
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()