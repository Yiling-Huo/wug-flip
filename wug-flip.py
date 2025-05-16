import os, sys, pygame, random

##########
# Appearances
##########

window_width = 1400
window_height = 900

white = '#ffffff'
quartz ='#aaa1c8'
space = '#192a51'

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
        self.front_color = white
        self.back_color = space

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
        elif self.flipping:
            #pygame.draw.rect(screen,white, self.cover_rect,border_radius = 12)
            pygame.draw.rect(screen,quartz,self.flipping_rect,border_radius = 12)
            pygame.draw.rect(screen,self.back_color, self.flipping_small_rect,border_radius = 12)
        else:
            #pygame.draw.rect(screen,white, self.cover_rect,border_radius = 12)
            pygame.draw.rect(screen,quartz,self.rect,border_radius = 12)
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
    
    def flip(self):
        if self.selected and not self.flipping:
            self.flipping = True
            self.flip_start_time = pygame.time.get_ticks()
    
    def update(self):
        if self.flipping:
            current_time = pygame.time.get_ticks()
            if current_time - self.flip_start_time >= self.flip_duration:
                self.flipping = False

########
# Functions
########

# wipe screen
def wipe():
    pygame.draw.rect(screen, white, pygame.Rect(0, 0, window_width, window_height))
    pygame.display.flip()

########
# Main game
########
def main():
    global screen, card_font
    global cards, selected, indices, input_lock
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()
    #icon = pygame.image.load('assets/icon.png')
    #pygame.display.set_icon(icon)
    pygame.display.set_caption('Wug Flip')
    screen.fill(white)
    card_font = pygame.font.Font(None,28)
    text_font = pygame.font.Font(None,50)

    # select text
    with open('list.txt', 'r') as f:
        content = f.read().split(',')
        texts = random.sample(content, 6)
    words = texts + texts
    random.shuffle(words)
    print(words)

    # manage double esc quit
    esc_pressed = False
    last_esc_time = 0
    double_esc_time = 500  # milliseconds

    # game attributes
    indices = list(range(13))
    selected = []
    opened = set()
    # cards
    card_width = 100
    card_height = 150
    cols = 4
    rows = 3
    space_width = 1000
    space_height = 700
    x_gap = (space_width - cols * card_width) // (cols + 1)
    y_gap = (space_height - rows * card_height) // (rows + 1)

    locations = []
    index = 0
    for row in range(rows):
        for col in range(cols):
            x = x_gap + col * (card_width + x_gap)
            y = y_gap + row * (card_height + y_gap)
            locations.append([index, x, y])
            index += 1
    cards = [Card(words[i], (locations[i][1], locations[i][2]), locations[i][0]) for i in range(12)]

    match_check_pending = False
    match_check_time = 0
    match_delay = 1000
    input_lock = False

    while True:
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

        for card in cards:
            card.update()
            if card.index in opened:
                card.open = True
            card.draw()
        
        # Check if 2 cards are selected
        if len(selected) == 2 and not match_check_pending:
            print(selected)
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
                    print(opened)
                else:
                    for i in selected:
                        cards[i].open = False
                        cards[i].selected = False
                selected.clear()
                match_check_pending = False
                input_lock = False

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()