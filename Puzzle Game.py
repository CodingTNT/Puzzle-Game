import random
import simpleguitk as simplegui
import pygame  


pygame.mixer.init()


music_url = "chacha.mp3"  
pygame.mixer.music.load(music_url)


image_url = "https://c-ssl.duitang.com/uploads/blog/202307/15/y9S77V3Yiblw5W4.jpg" 
baymax = simplegui.load_image(image_url)  


image_width = 1600  
image_height = 1600  


canvas_width = 600 
canvas_height = 600 


tile_width = image_width / 3  
tile_height = image_height / 3 


all_coordinates = [
    [tile_width * 0.5, tile_height * 0.5],
    [tile_width * 1.5, tile_height * 0.5],
    [tile_width * 2.5, tile_height * 0.5],
    [tile_width * 0.5, tile_height * 1.5],
    [tile_width * 1.5, tile_height * 1.5],
    [tile_width * 2.5, tile_height * 1.5],
    [tile_width * 0.5, tile_height * 2.5],
    [tile_width * 1.5, tile_height * 2.5]
]


rows = 3
cols = 3
steps = 0  


board = [[None for _ in range(cols)] for _ in range(rows)]


class Square:
    def __init__(self, coordinate):
        self.center = coordinate 

    def draw(self, canvas, board_pos):
        if baymax is None:
            print("Baymax image is not loaded.")
        else:
            
            dest_center = [
                (board_pos[1] + 0.5) * (canvas_width / 3),
                (board_pos[0] + 0.5) * (canvas_width / 3)
            ]
            dest_size = [canvas_width / 3, canvas_width / 3]
            
            
            canvas.draw_image(
                baymax,
                self.center,
                [tile_width, tile_height],
                dest_center,
                dest_size
            )

def init_board():
    random.shuffle(all_coordinates)
    idx = 0
    for i in range(rows):
        for j in range(cols):
            if idx < len(all_coordinates):
                square_center = all_coordinates[idx]
                board[i][j] = Square(square_center)
                idx += 1
            else:
                board[i][j] = None  


def play_game():
    global steps
    steps = 0
    init_board()
    pygame.mixer.music.rewind() 
    pygame.mixer.music.play(-1)  


def draw(canvas):
    canvas.draw_text(f"Steps: {steps}", [10, canvas_height - 10], 24, "White")
    
    for i in range(rows):
        for j in range(cols):
            if board[i][j] is not None:
                board[i][j].draw(canvas, [i, j])


def mouseclick(pos):
    global steps
    r = int(pos[1] / (canvas_width / 3)) 
    c = int(pos[0] / (canvas_width / 3))  
    
    if r < 3 and c < 3 and board[r][c] is not None:
        current_square = board[r][c]
        if r - 1 >= 0 and board[r - 1][c] is None:
            board[r][c] = None
            board[r - 1][c] = current_square
            steps += 1
        elif c + 1 <= 2 and board[r][c + 1] is None: 
            board[r][c] = None
            board[r][c + 1] = current_square
            steps += 1
        elif r + 1 <= 2 and board[r + 1][c] is None: 
            board[r][c] = None
            board[r + 1][c] = current_square
            steps += 1
        elif c - 1 >= 0 and board[r][c - 1] is None: 
            board[r][c] = None
            board[r][c - 1] = current_square
            steps += 1


frame = simplegui.create_frame("Puzzle Game", canvas_width, canvas_height)
frame.set_canvas_background('Black')
frame.set_draw_handler(draw)
frame.add_button('Restart', play_game, 100)


frame.set_mouseclick_handler(mouseclick)


play_game()
frame.start()
