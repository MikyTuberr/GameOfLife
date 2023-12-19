import pygame
from pygame.locals import *
import sys
from Worlds.SquareWorld import SquareWorld
from EnumsAndConsts.StatusType import StatusType
from EnumsAndConsts.Parameters import *
from EnumsAndConsts.ExtraStatusType import ExtraStatusType
from GUI.Point import Point

from Organisms.Animals.Fox import Fox
from Organisms.Animals.Wolf import Wolf
from Organisms.Animals.CyberSheep import Cybersheep
from Organisms.Animals.Sheep import Sheep
from Organisms.Animals.Turtle import Turtle
from Organisms.Animals.Antelope import Antelope

from Organisms.Plants.Grass import Grass
from Organisms.Plants.Guarana import Guarana
from Organisms.Plants.Belladonna import Belladonna
from Organisms.Plants.Dandelion import Dandelion
from Organisms.Plants.SosnowskysHogweed import SosnowskysHogweed

# BACKGROUND COLOR (WHITE)
BACKGROUND_COLOR = (0, 0, 0)
# MENU'S RECTANGLES COLOR (BLACK)
RECTANGLE_COLOR = (0, 0, 0)
# BORDER COLOR
BORDER_COLOR = (255, 255, 255)
# SQUARE FIELDS SIZE
SQUARE_SIZE = 40


class GUI:
    def __init__(self):
        self.symbol = None
        self.world = None
        # INITIALIZATION OF PYGAME
        pygame.init()
        # WINDOW SETTINGS
        self.window_width = 600
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("GameOfLife")
        # FONT
        self.font = pygame.font.Font(None, 36)
        self.organism_buttons = []

    def getWorld(self):
        return self.world

    # MENU
    def mainMenu(self):

        while True:
            # FILL BACKGROUND
            self.window.fill(BACKGROUND_COLOR)

            # RENDER MENU'S OPTIONS
            new_game_text = self.font.render("New Game", True, (0, 0, 0))
            quit_text = self.font.render("Quit", True, (0, 0, 0))

            # POSITIONS OF MENU'S OPTIONS
            new_game_rect = pygame.Rect(self.window_width // 2 - 75, self.window_height // 2 - 70, 150, 40)
            quit_rect = pygame.Rect(self.window_width // 2 - 75, self.window_height // 2 - 10, 150, 40)

            # DISPLAY RECTANGLES
            pygame.draw.rect(self.window, (255, 255, 255), new_game_rect)
            pygame.draw.rect(self.window, (255, 255, 255), quit_rect)

            # TEXT POSITIONS
            new_game_text_rect = new_game_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 50))
            quit_text_rect = quit_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 10))

            # DISPLAY MENU'S OPTIONS
            self.window.blit(new_game_text, new_game_text_rect)
            self.window.blit(quit_text, quit_text_rect)

            # DISPLAY UPDATE
            pygame.display.update()

            # HANDLE EVENTS
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if new_game_rect.collidepoint(mouse_pos):
                        self.inputSize()
                    elif quit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

    # INSERT MAP SIZE
    def inputSize(self):
        size_input = ""
        font = pygame.font.Font(None, 36)
        while True:
            # FILL BACKGROUND
            self.window.fill(BACKGROUND_COLOR)

            # RENDER INFO
            text = font.render("Insert map size (max 2 numbers):", True, (255, 255, 255))
            input_text = font.render("Size: " + size_input, True, (255, 255, 255))

            # POSITION OF INFO
            text_rect = text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 50))
            input_text_rect = input_text.get_rect(center=(self.window_width // 2, self.window_height // 2))

            # DISPLAY TEXT
            self.window.blit(text, text_rect)
            self.window.blit(input_text, input_text_rect)

            # UPDATE DISPLAY
            pygame.display.update()

            # EVENT HANDLER
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.mainMenu()
                    elif event.key == K_RETURN:
                        if len(size_input) == 2 and size_input.isdigit() and int(size_input) > 0:
                            print("MAP SIZE:", size_input)
                            self.generateSquareBoard(int(size_input))
                            return
                        else:
                            print("INSERT CORRECT MAP SIZE!")
                    elif event.key == K_BACKSPACE:
                        size_input = size_input[:-1]
                    elif event.unicode.isdigit() and len(size_input) < 2:
                        size_input += event.unicode

    # GENERATE BOARD
    def generateSquareBoard(self, size):
        # SPECIFY WINDOW DIMENSIONS
        self.world = SquareWorld(size, size)
        window_width = size * SQUARE_SIZE
        window_height = size * SQUARE_SIZE

        # SETTINGS OF GAME WINDOW
        window = pygame.display.set_mode((window_width + 200, window_height))
        pygame.display.set_caption("GameOfLife")

        symbol_to_icon = {
            'A': 'Icons/antelope.png',  # ANTELOPE ICON PATH
            'B': 'Icons/belladonna.png',  # BELLADONNA ICON PATH
            'C': 'Icons/csheep.png',  # CYBER SHEEP ICON PATH
            'W': 'Icons/wolf.png',  # WOLF ICON PATH
            'T': 'Icons/turtle.png',  # TURTLE ICON PATH
            'S': 'Icons/sheep.png',  # SHEEP ICON PATH
            'H': 'Icons/human.png',  # HUMAN ICON PATH
            'F': 'Icons/fox.png',  # FOX ICON PATH
            'D': 'Icons/dandelion.png',  # DANDELION ICON PATH
            'G': 'Icons/grass.png',  # GRASS ICON PATH
            'U': 'Icons/guarana.png',  # GUARANA ICON PATH
            'P': 'Icons/sosnowsky.png'  # SOSNOWSKYS HOGWEED ICON PATH
        }

        # Initialize organism buttons
        self.organism_buttons = []
        for symbol, icon_path in symbol_to_icon.items():
            image = pygame.image.load(icon_path)
            image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
            button_rect = pygame.Rect(window_width + 10, (list(symbol_to_icon.keys()).index(symbol) + 1) * SQUARE_SIZE,
                                      SQUARE_SIZE, SQUARE_SIZE)
            self.organism_buttons.append((symbol, image, button_rect))

        selected_organism = None  # Currently selected organism symbol

        while True:
            # FILL BACKGROUND
            window.fill(BACKGROUND_COLOR)

            for row in range(size):
                for col in range(size):
                    square_rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    pygame.draw.rect(window, RECTANGLE_COLOR, square_rect)
                    pygame.draw.rect(window, BORDER_COLOR, square_rect, 1)
                    position = Point(col, row)

                    if self.world.findOrganism(position):
                        organism = self.world.findOrganism(position)
                        # LOAD IMAGE
                        image = pygame.image.load(symbol_to_icon[organism.symbol])
                        # SCALING ICON TO SQUARE SIZE
                        image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
                        # DISPLAY ICON IN CORRECT PLACE
                        window.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

            # Draw organism buttons
            for symbol, image, button_rect in self.organism_buttons:
                pygame.draw.rect(window, RECTANGLE_COLOR, button_rect)
                pygame.draw.rect(window, BORDER_COLOR, button_rect, 1)
                window.blit(image, (button_rect.x, button_rect.y))

            # UPDATE DISPLAY
            pygame.display.update()

            # EVENT HANDLER
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if 0 <= mouse_pos[0] < window_width and 0 <= mouse_pos[1] < window_height:
                        clicked_row = mouse_pos[1] // SQUARE_SIZE
                        clicked_col = mouse_pos[0] // SQUARE_SIZE
                        print("CLICKED ON:", clicked_row, clicked_col)
                        newOrganism = None
                        if self.world.findOrganism(Point(clicked_col, clicked_row)) is None:
                            if self.symbol == 'A':
                                newOrganism = Antelope(ANTELOPE_POWER, StatusType.DEFAULT,
                                                       Point(clicked_col, clicked_row),
                                                       self.world, ExtraStatusType.DEFAULT)
                            elif self.symbol == 'B':
                                newOrganism = Belladonna(BELLADONNA_POWER, BELLADONNA,
                                                         StatusType.DEFAULT, Point(clicked_col, clicked_row),
                                                         self.world,
                                                         BELLADONNA_SPREAD_PROBABILITY,
                                                         ExtraStatusType.DEFAULT)
                            elif self.symbol == 'C':
                                newOrganism = Cybersheep(CYBER_SHEEP_POWER, StatusType.DEFAULT,
                                                         Point(clicked_col, clicked_row),
                                                         self.world, ExtraStatusType.DEFAULT)
                            elif self.symbol == 'W':
                                newOrganism = Wolf(WOLF_POWER, StatusType.DEFAULT, Point(clicked_col, clicked_row),
                                                   self.world, ExtraStatusType.DEFAULT)
                            elif self.symbol == 'T':
                                newOrganism = Turtle(TURTLE_POWER, StatusType.DEFAULT, Point(clicked_col, clicked_row),
                                                     self.world, ExtraStatusType.DEFAULT)
                            elif self.symbol == 'S':
                                newOrganism = Sheep(SHEEP_POWER, StatusType.DEFAULT, Point(clicked_col, clicked_row),
                                                    self.world, ExtraStatusType.DEFAULT)
                            elif self.symbol == 'F':
                                newOrganism = Fox(FOX_POWER, StatusType.DEFAULT, Point(clicked_col, clicked_row),
                                                  self.world, ExtraStatusType.DEFAULT)
                            elif self.symbol == 'D':
                                newOrganism = Dandelion(DANDELION_POWER, DANDELION,
                                                        StatusType.DEFAULT, Point(clicked_col, clicked_row),
                                                        self.world,
                                                        DANDELION_SPREAD_PROBABILITY,
                                                        ExtraStatusType.DEFAULT)
                            elif self.symbol == 'G':
                                newOrganism = Grass(GRASS_POWER, GRASS,
                                                    StatusType.DEFAULT, Point(clicked_col, clicked_row),
                                                    self.world,
                                                    GRASS_SPREAD_PROBABILITY,
                                                    ExtraStatusType.DEFAULT)
                            elif self.symbol == 'U':
                                newOrganism = Guarana(GUARANA_POWER, GUARANA,
                                                      StatusType.DEFAULT, Point(clicked_col, clicked_row),
                                                      self.world,
                                                      GUARANA_SPREAD_PROBABILITY,
                                                      ExtraStatusType.DEFAULT)
                            elif self.symbol == 'P':
                                newOrganism = SosnowskysHogweed(SOSNOWSKYS_HOGWEED_POWER, SOSNOWSKYS_HOGWEED,
                                                                StatusType.DEFAULT, Point(clicked_col, clicked_row),
                                                                self.world,
                                                                SOSNOWSKYS_HOGWEED_SPREAD_PROBABILITY,
                                                                ExtraStatusType.DEFAULT)
                                self.world.addSosnowskyHogweed(newOrganism)
                            self.world.addOrganism(newOrganism)
                            print("NEW ORGANISM ADDED" + str(newOrganism.printLog()))
                        else:
                            print("FIELD IS ALREADY OCCUPIED")
                    elif window_width + 20 <= mouse_pos[0] < window_width + 80 and 0 <= mouse_pos[1] <= window_height:
                        clicked_row = mouse_pos[1] // SQUARE_SIZE
                        clicked_col = mouse_pos[0] // SQUARE_SIZE
                        print("CLICKED ON:", clicked_row, clicked_col)
                        print(self.symbol)
                        if clicked_row == 1:
                            self.symbol = 'A'
                        elif clicked_row == 2:
                            self.symbol = 'B'
                        elif clicked_row == 3:
                            self.symbol = 'C'
                        elif clicked_row == 4:
                            self.symbol = 'W'
                        elif clicked_row == 5:
                            self.symbol = 'T'
                        elif clicked_row == 6:
                            self.symbol = 'S'
                        elif clicked_row == 8:
                            self.symbol = 'F'
                        elif clicked_row == 9:
                            self.symbol = 'D'
                        elif clicked_row == 10:
                            self.symbol = 'G'
                        elif clicked_row == 11:
                            self.symbol = 'U'
                        elif clicked_row == 12:
                            self.symbol = 'P'
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.world.makeTour()
                        break
                    elif event.key == pygame.K_s:
                        self.world.saveTheGame("./save.txt")
                        print("GAME SAVED PROPERLY")
                    elif event.key == pygame.K_l:
                        self.world.loadTheGame("./save.txt")
                        print("GAME LOADED PROPERLY")

