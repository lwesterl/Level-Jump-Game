import sys, os
from PyQt5.QtWidgets import QMainWindow, QMenuBar
from PyQt5.QtWidgets import QPushButton, QGraphicsScene,  QGraphicsView, QGraphicsTextItem, QLineEdit
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QStackedLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QEvent, QSize, QRect
from PyQt5.QtGui import QPixmap, QColor
from gamefield import GameField
from position import Position
from drawdynamic import DrawDynamic
from drawstatic import DrawStatic
from drawvisible import DrawVisible
from drawground import DrawGround
from drawfinish import DrawFinish
from config import Config


class Gui(QMainWindow):

    #class variables
    #Distance_right_limit = 50
    Distance_right_limit = Config.distance_right_limit
    Level_number = Config.level_number

    #signal for emitting key presses
    key_pressed = pyqtSignal(QEvent)
    
    #if thegame ends these signals are raised
    lose_screen_signal = pyqtSignal()
    win_screen_signal = pyqtSignal()
    
    reset_signal = pyqtSignal()


    
    def __init__(self):
        super(Gui, self).__init__()  #calls the upper class init

        self.update_class_variables()

        #variables used to capture key press
        self.space = 0
        self.right_arrow = 0
        self.left_arrow = 0
        self.enter = 0
        
        self.count = 0 #mostly for testing use
        self.color = 0
        
        self.game = False #tells if game is running
        self.scene = None #graphicsscene added later
        self.gamefield = None #gamefield object, added later
        self.gamefield_start = None #gamefield object, added later, it's copy of start gamefield
        self.gamefield_level = '' #tells which level is currently used as gamefield

        self.key_pressed.connect(self.determine_key)
        
        #Main window size:
        #starting screen can be dynamically adjusted
        #for dynamic window size changes
        self.win_width = 0
        self.win_width_prev = 0
        self.win_height = 0
        self.win_changed = False
        self.restart = False # is game is restarted the scene has to be adjusted
        self.screen = 0 #these are used to determine which object the player should see
        self.screen_prev = 0
        
        self.setWindowTitle('Tasohyppely')#can be changed later
        
        #set layout to draw multiple objects
        self.layout = QHBoxLayout()
        
        
        '''#read pic (it min size can be set later)
        pixmap = QPixmap('start_screen_test.png')#this pic will be changed later
        
        widget = QLabel()
        widget.setPixmap(pixmap)
        
        widget.setScaledContents(True)#makes dynamic scaling possible
        
        #set pic to back side of the screen
    
        self.setCentralWidget(widget)
        self.centralWidget().setLayout(self.layout)

        
        

        #set pushbutton which starts the game:
        
        #first create button object and connect to start game method
        self.start_button = QPushButton('Start Game')
        self.start_button.setStyleSheet('QPushButton {background-color: transparent;}')#can be changed later
        self.start_button.clicked.connect(self.start_game)
        self.start_button.setFixedSize(100,100) #this can be changed later
        #add the start button to layout
        self.layout.addWidget(self.start_button)
        self.start_button.move(100,50)#this can be changed later

        '''


    
        #connect all the end game signals
        self.__connect_signals__()


        #create a continue button for win and lose screens
        self.continue_button = QPushButton('Continue')
        self.continue_button.setFixedSize(0,0)
        self.continue_button.clicked.connect(self.reset_gui)
        self.continue_button.setEnabled(False)

        #add continue button to the layout
        self.layout.addWidget(self.continue_button)
        #self.start_button.move(100,50)#this can be changed later
        

        


        #handles to scene items, set when items are added to scene
        self.enemy_items = []
        self.static_items = []
        self.player_item = None
      

        #when game is started gui updates screen by calling drawgame
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        #set timer value to 20 ms, can be changed later
        self.timer.start(20)



        #for the different screens
        self.first_win_screen = True
        self.first_lose_screen = True
        self.selecting_level = False
        self.end_text = QGraphicsTextItem('GAME OVER,')
        self.continue_text = QGraphicsTextItem('Continue by pressing the button')
        self.win_text = QGraphicsTextItem('YOU WON!')
        self.lose_text = QGraphicsTextItem('YOU LOST')
        
        #Menu testing
        #self.menu = QMenuBar()
        #self.menu.addMenu('Menu')
        
        self.vertical_layout = QVBoxLayout()
        
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.layout)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.cancel_game)
        self.cancel_button.setFixedSize(0,0)
        self.cancel_button.setEnabled(False)
        self.cancel_button.setStyleSheet('QPushButton {background-color: transparent;}')#can be changed later
        #self.switch_button.move(0,0)
        #self.vertical_layout.addWidget(self.switch_button)
        self.layout.addWidget(self.cancel_button)
        
        

        self.switch_button = QPushButton('Game')
        self.switch_button.clicked.connect(self.game_)
        self.switch_button.setFixedSize(100,50)
        
        #self.vertical_layout.addWidget(self.switch_button)
        self.layout.addWidget(self.switch_button)
        

        self.switch3 = QPushButton('Select level')
        self.switch3.clicked.connect(self.select_level)
        self.switch3.setFixedSize(100,50)
        
    
        self.layout.addWidget(self.switch3)

        self.switch4 = QPushButton('Level Editor')
        self.switch4.clicked.connect(self.level_editor)
        self.switch4.setFixedSize(100,50)
        self.layout.addWidget(self.switch4)

        self.switch2 = QPushButton('Help')
        self.switch2.clicked.connect(self.switch2_)
        self.switch2.setFixedSize(100,50)
        
     
        self.layout.addWidget(self.switch2)


        #first create button object and connect to start game method
        self.start_button = QPushButton('Start Game')
        self.start_button.setStyleSheet('QPushButton {background-color: transparent;}')#can be changed later
        self.start_button.clicked.connect(self.start_game)
        self.start_button.setFixedSize(0,0)
        self.start_button.setEnabled(False)
        #add the start button to layout
        self.layout.addWidget(self.start_button)
        #self.start_button.move(100,50)#this can be changed later

        self.select_level()
        self.level_text = 'my_level1'
        self.enter += 1
        #self.cancel_level_select()
        #self.set_level()
        
        #self.start_game()
        #self.reset_gui()
        #self.start_game()
        

    def switch2_(self):
        print('moi')

        
    def select_level(self):
        #set switches to the correct state
        self.set_switches_off()
        self.cancel_button.clicked.connect(self.cancel_level_select)

        #initialize enter-key value and set correct state to selecting_level
        self.enter = 0
        self.selecting_level = True
        self.level_text = ''
        

        #initialize a scene where to put levels
        self.level_scene = QGraphicsScene()
        
        #view for scene
        self.level_scene_view = QGraphicsView(self.level_scene, self)
        
        self.level_scene_view.adjustSize()
        self.level_scene_view.show()
        self.layout.addWidget(self.level_scene_view)
        
        

        level = QGraphicsTextItem('Level')

        path = os.getcwd() #get the current working dir
        os.chdir(path) #change dir to the current working dir
        os.chdir('game_levels')
        
        position = 50
        levels = []
        data = os.listdir()
        for item in data:
            if os.path.isfile(item):
                levels.append(item)
                #add also item to level_scene to show user what levels there are to choose from
                level = QGraphicsTextItem(item)
                self.level_scene.addItem(level)
                level.setPos(0,position)
                position +=20


        self.qline_edit = QLineEdit()
        self.layout.addWidget(self.qline_edit)
        
        self.qline_edit.textEdited[str].connect(self.qline_edited)        
                
                
        
        

        os.chdir(path) #remember to change back to the working dir where all classes etc are

    def qline_edited(self,text):
        #This is just a helper method which assigns qline edited text
        self.level_text = text
        

    def set_level(self):
        #This method sets the level to self.gamefield that user has chosen if possible
        #It is called via keypress event when enter is pressed and user is selecting level (self.selecting_level == True)

        try :
            path = os.getcwd() #get the current working dir
            os.chdir(path) #change dir to the current working dir
            os.chdir('game_levels')

            #open the file if possible
            
            file = open(self.level_text, 'r')

        

            #parse a gamefield and a copy from the file
            gamefield = GameField()
            game_copy = GameField()
            return_value = gamefield.parse_gamefield(file)
            file.seek(0)#This is very important otherwise program will die
            game_copy.parse_gamefield(file)

            
            file.close()
            
            if return_value:
                #if return value is False, the level is broken
                self.set_gamefield(gamefield,game_copy)
                self.gamefield_level = self.level_text #this is used by reset_gui method
                print('Level successfully changed')

            else:
                print('Level is not ok, using the previous level')


            
            

            
            
            
        except FileNotFoundError:
            print('Level with name {} not found'. format(self.level_text))

        finally:
            os.chdir(path)#This changes back to working directory where classes etc are defined
            
        
        
    def cancel_level_select(self):
        self.selecting_level = False
        #self.layout.removeWidget(self.qline_edit)
        #self.qline_edit = None
        self.qline_edit.setFixedSize(0,0)
        
        #make the level_scene not visible
        self.level_scene.setSceneRect(0,0,0,0)
        self.level_scene_view.setFixedSize(0,0)
        #delete all the items in the scene
        self.level_scene.clear()
        self.cancel_button.clicked.connect(self.cancel_game)

    def cancel_game(self):
        #This method returns the mainmenu view
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.layout)
        
        self.cancel_button.setFixedSize(0,0)
        self.cancel_button.setEnabled(False)

        self.start_button.setFixedSize(0,0)
        self.start_button.setEnabled(False)

        self.switch_button.setFixedSize(100,50)
        self.switch_button.setEnabled(True)
        self.switch2.setFixedSize(100,50)
        self.switch2.setEnabled(True)
        self.switch3.setFixedSize(100,50)
        self.switch3.setEnabled(True)
        self.switch4.setEnabled(True)
        self.switch4.setFixedSize(100,50)


    def set_switches_off(self):
        #This is a helper method called to set starting screen switches off
        #sets also cancel_button on

        self.switch_button.setFixedSize(0,0)
        self.switch_button.setEnabled(False)
        self.switch2.setFixedSize(0,0)
        self.switch2.setEnabled(False)
        self.switch3.setFixedSize(0,0)
        self.switch3.setEnabled(False)
        self.switch4.setFixedSize(0,0)
        self.switch4.setEnabled(False)

        self.cancel_button.setFixedSize(70,50)
        self.cancel_button.setEnabled(True)
        

    def game_(self):

        #Set the starting screen switches off
        self.set_switches_off()
        
        

        self.start_button.setFixedSize(70,50)
        self.start_button.setEnabled(True)
       
        
        #read pic (it min size can be set later)
        pixmap = QPixmap('start_screen_test.png')#this pic will be changed later
        
        widget = QLabel()
        widget.setPixmap(pixmap)
        
        widget.setScaledContents(True)#makes dynamic scaling possible
        
        #set pic to back side of the screen
        #print('hei')
        #i= 0
        #print('tama on count{}'.format(self.layout.count()))
       
    
        self.setCentralWidget(widget)
    
        self.centralWidget().setLayout(self.layout)
       

        
        

        '''#set pushbutton which starts the game:
        
        #first create button object and connect to start game method
        self.start_button = QPushButton('Start Game')
        self.start_button.setStyleSheet('QPushButton {background-color: transparent;}')#can be changed later
        self.start_button.clicked.connect(self.start_game)
        self.start_button.setFixedSize(100,100) #this can be changed later
        #add the start button to layout
        self.layout.addWidget(self.start_button)
        self.start_button.move(100,50)#this can be changed later
        '''

    def level_editor(self):
        print('level editor')
        
    def __connect_signals__(self):
        #This method is called from init to init all the signals called
        #after the game has ended
        #This method is called only once
        self.reset_signal.connect(self.reset_gui)
        self.lose_screen_signal.connect(self.lose_screen)
        self.win_screen_signal.connect(self.win_screen)
        
        

        
    def update_class_variables(self):
        #This method is called from init to update all the gui class variables to match Config
        Gui.Distance_right_limit = Config.distance_right_limit
        Gui.Level_number = Config.level_number

       
        

    def keyPressEvent(self, event):
        self.key_pressed.emit(event) # connects to determine_key -method

    def determine_key(self, event):


        if event.key() == Qt.Key_Return:
            self.enter += 1
            if self.selecting_level:
                self.set_level()
                
            
            
        if event.key() == Qt.Key_Space: # this is called whenever the space is pressed
            self.space += 1
            if self.game:
                GameField.Space += 1
                print(GameField.Space)
            #print (self.space)  

        if event.key() == Qt.Key_A or event.key() == Qt.Key_Left:
            self.left_arrow += 1
            if self.game:
                GameField.Left_arrow += 1
                print(GameField.Left_arrow)
            #print(self.left_arrow)

        if event.key() == Qt.Key_D or event.key() == Qt.Key_Right:
            self.right_arrow += 1
            if self.game:
                GameField.Right_arrow += 1
                print(GameField.Right_arrow)
            #print(self.right_arrow)

        if event.key() == Qt.Key_Q:
            self.left_arrow += 1 #if Q is pressed, the player wants jump left
            self.space += 1
            
            if self.game:
                GameField.Left_arrow += 1
                GameField.Space += 1

        if event.key() == Qt.Key_E: #if E is pressed, the player wants jump right
            self.right_arrow += 1
            self.space += 1
            
            if self.game:
                GameField.Right_arrow += 1
                GameField.Space += 1

        

        elif event.key() == Qt.Key_Escape: 
            print ("Exit button activated")
            self.close()

    def resizeEvent(self,event):
        #used to adjust scene object positions
        #This redefines Qt5 resizeEvent
       
        self.win_width = event.size().width()
        self.win_height = event.size().height()
        self.win_changed = True
        

    def start_game(self):
        #change to the game window
        
        self.cancel_button.setEnabled(False)
        self.cancel_button.setFixedSize(0,0)
        self.start_button.setEnabled(False)
        self.start_button.setFixedSize(0,0)

        #set new central widget for drawing the game
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.layout)
        
        
        #init drawing scene for drawing game and add drawobjects to scene
        self.init_drawing_scene()
        self.add_DrawGame_objects()
        self.get_scene_items_number()#for testing only
        
        self.game = True
        GameField.Game_running = True

    def update_game(self):
        
    
        if self.game: #for testing only
            if self.count ==0:
                self.setStyleSheet("""background: rgb(20,5,40);""")
                self.count += 1
            
            
          
            if self.win_changed or self.restart:

                #user has changed window size or game has been restarted when rect has to be readjusted
            
                self.scene.setSceneRect(0,0,self.win_width,self.win_height)
                self.correct_scene_item_positions()
                self.win_changed = False
                self.restart = False
            
            self.gamefield.update_objects_positions()
            self.player_item.move_item() #see drawdynamic
            
            #also enemies has to be moved
           
            for i in range(len(self.enemy_items)):
                
                #print(self.enemy_items[i].owner_object)
                self.enemy_items[i].move_item() #see drawdynamic
                

            #now check where player is in the screen and adjust position based on that information
            self.adjust_moving_items_coordinates()
            
            #check if also static items have to be moved
            
            if self.screen != self.screen_prev:
                #static items have to be moved
                self.adjust_static_objects_positions()
                
                self.screen_prev = self.screen

            if not GameField.Game_running:
               
                #this must be reimplemented later
                #there should be separate screens for winning and losing the game
                if GameField.Fail:
                    
                    self.lose_screen_signal.emit()
                    
                else:
                    self.win_screen_signal.emit()
                
                #self.reset_signal.emit()
                


    def reset_gui(self):

        #this method is called when game has ended and is
        #switched back to starting screen
        #this is test version of this method


        #Init win and lose screen values for a new game 
        self.first_win_screen = True
        self.first_lose_screen = True
        self.restart = True # This adjusts scene rect when user restarts the game
        
        #initialize gamefield's key press capturing class variables
        GameField.Right_arrow = 0
        GameField.Left_arrow = 0
        GameField.Space = 0

        #create same widget as in init, make scene and view not drawn
        self.scene.setSceneRect(0,0,0,0)
        self.scene_view.setFixedSize(0,0)
        
        #delete all the items in the scene
        self.scene.clear()
        #These need to be redefined because the old items were destroyed above
        self.end_text = QGraphicsTextItem('GAME OVER,')
        self.continue_text = QGraphicsTextItem('Continue by pressing the button')
        self.win_text = QGraphicsTextItem('YOU WON!')
        self.lose_text = QGraphicsTextItem('YOU LOST')

        #initialize gamefield
        path = os.getcwd() #get the current working dir
        os.chdir(path) #change dir to the current working dir
        os.chdir('game_levels')

        #open the file, it should always success because this file has been already opened and checked
        
            
        file = open(self.gamefield_level, 'r')
        
        

        

        #parse a gamefield and a copy from the file

        gamefield = GameField()
        
        return_value = gamefield.parse_gamefield(file)
        file.close()
        self.gamefield = gamefield

        os.chdir(path) #change dir to the current working dir

        #initialize all lists of scene items
        self.enemy_items = []
        self.static_items = []
        
        
        #set the correct screen style 
        GameField.Fail = False
        
        pixmap = QPixmap('start_screen_test.png')#this pic will be changed later
        

        widget = QLabel()
        widget.setPixmap(pixmap)
        widget.setScaledContents(True)
        self.setCentralWidget(widget)
        self.centralWidget().setLayout(self.layout)
        
        #enable start and cancel buttons and disable continue button
        self.start_button.setEnabled(True)
        self.start_button.setFixedSize(70,50)
        self.cancel_button.setEnabled(True)
        self.cancel_button.setFixedSize(70,50)
        
        self.continue_button.setFixedSize(0,0)
        self.continue_button.setEnabled(False)

      
        
        #this is for changing the background color, prior was used for testing (that's why name is not good)
        self.count = 0
        

    def lose_screen(self):
        #This method is called if a player has lost the game
        #It creates a screen that informs the player that the game has been lost
        #After the player continues from this screen reset_gui method will be called
        if self.first_lose_screen:
            #stop the game
            self.game = False
            GameField.Game_running = False
            
            #Enable continue button
            self.continue_button.setStyleSheet('QPushButton {color : red;}')
            self.continue_button.setFixedSize(100,100)
            self.continue_button.setEnabled(True)
           

            #Set correct texts in the scene
            self.end_text.setDefaultTextColor(QColor(250,0,0))
            self.lose_text.setDefaultTextColor(QColor(250,0,0))
            self.continue_text.setDefaultTextColor(QColor(90,20,20))
                                                            
            self.scene.addItem(self.end_text)
            self.scene.addItem(self.lose_text)
            self.scene.addItem(self.continue_text)

            self.first_win_screen = False
            
        self.end_text.setPos(self.win_width *0.5 -100 ,30)
        self.lose_text.setPos(self.win_width * 0.5 -100, 50)
        self.continue_text.setPos(self.win_width * 0.5 -150, 100)
        

    def win_screen(self):
        #This method is called if a player has win the game
        #It creates a screen that informs the player that the game has been won
        #After the player continues from this screen reset_gui method will be called
        if self.first_win_screen:

            #stop the game
            self.game = False
            GameField.Game_running = False

            #Enable continue button
            self.continue_button.setStyleSheet('QPushButton {color : green;}')
            self.continue_button.setFixedSize(100,100)
            self.continue_button.setEnabled(True)
            

            #Set correct texts in the scene
            self.end_text.setDefaultTextColor(QColor(0,180,0))
            self.win_text.setDefaultTextColor(QColor(0,180,0))
            self.continue_text.setDefaultTextColor(QColor(20,90,20))
                                                            
            self.scene.addItem(self.end_text)
            self.scene.addItem(self.win_text)
            self.scene.addItem(self.continue_text)

            self.first_win_screen = False
            
        self.end_text.setPos(self.win_width *0.5 -100 ,30)
        self.win_text.setPos(self.win_width * 0.5 -100, 50)
        self.continue_text.setPos(self.win_width * 0.5 -150, 100)

    def init_drawing_scene(self):
        #initializes the scene where objects are placed
        self.scene = QGraphicsScene()
        
        #view for scene
        self.scene_view = QGraphicsView(self.scene, self)
        
        self.scene_view.adjustSize()
        self.scene_view.show()
        self.layout.addWidget(self.scene_view)
        self.scene_view.show()


    def set_gamefield(self,gamefield,copy_of_gamefield):
        #helper method which sets handle to gamefield object
        self.gamefield = gamefield
        self.gamefield_start = copy_of_gamefield

        
    def add_DrawGame_objects(self):
        #this method requires that a gamefield has been set
        #this method requires that a drawing scene has been set
        
        #it adds correct drawgame type objects for whole gamefield content
        #this method is called only once per started game, otherwise it creates duplicates

        #create drawitem for player and add it to scene
        #first create pixmap from player model picture and scale it
        pixmap = QPixmap('player_model_clear_3.png')
        pixmap = pixmap.scaled(Position.player_width,Position.player_heigth)
        
        player_item = DrawDynamic(self.gamefield.player,pixmap)
        self.scene.addItem(player_item)

        #add pointer to the item so that it's pos can be changed
        self.player_item = player_item
        self.player_item.move_item()
        
        #create drawitem for all enemies and add them to scene
        for i in range(len(self.gamefield.enemies)):
            
            #create pixmap and scale it corectly
            pixmap = QPixmap('enemy_model_clear1.png')
            pixmap = pixmap.scaled(Position.enemy_width,Position.enemy_heigth)
            
            enemy_item = DrawDynamic(self.gamefield.enemies[i],pixmap)
            self.scene.addItem(enemy_item)
            #move item to correct location
            enemy_item.move_item()
            #add enemy items to list so they can be moved
            self.enemy_items.append(enemy_item)

        #create drawitem for all ground objects
        for i in range(0,len(self.gamefield.ground_objects)):
            ground_item = DrawGround(self.gamefield.ground_objects[i])
            self.scene.addItem(ground_item)
            #add to the list of static objects
            self.static_items.append(ground_item)

        #create drawitem for all finidsh and visible objects

        for i in range(0,len(self.gamefield.static_objects)):
            if self.gamefield.static_objects[i].type == 'visible_object':
                visible_item = DrawVisible(self.gamefield.static_objects[i])
                self.scene.addItem(visible_item)
                self.static_items.append(visible_item)

            elif self.gamefield.static_objects[i].type == 'finish_object':
                finish_item = DrawFinish(self.gamefield.static_objects[i])
                self.scene.addItem(finish_item)
                self.static_items.append(finish_item)

    def correct_scene_item_positions(self):
        #This method is called after user has changed window size
        #it sets new y_min coordinates for ground items in scene
        #so that window remains looking the same style as before adjusting the size

        delta_y = self.win_height - GameField.MainWindow_Heigth
        
        if delta_y > 0:

            #correct ground objects y-coordinates:
            for i in range(0,len(self.static_items)):

                if self.static_items[i].type == 'ground_object':
                    x = self.static_items[i].x #left corner
                    y = self.static_items[i].y #upper corner
                    width = self.static_items[i].width
                    height = self.static_items[i].height + delta_y
                    self.static_items[i].new_height = height # used by adjust_static_objects_positions

                    #set new height
                    self.static_items[i].setRect(x,y,width,height)

    def adjust_moving_items_coordinates(self):
        #This method is called after player and enemy objects are moved
        #It adjust x_min coordinates to match player position

        #value = self.player_item.owner_object.position.x_max // (self.win_width -Gui.Distance_right_limit)
        #value = sel

        if self.player_item.owner_object.position.x_max >= ((self.win_width -Gui.Distance_right_limit) + \
            self.screen * (self.win_width - Gui.Distance_right_limit - Position.Distance_x)):
            
            self.screen += 1 #player is on the right edge outside of the current screen 
            self.win_width_prev = self.win_width #this is done cause user can ajust screen anytime
            #and we don't want dynamic objects to move when the aren't near the edges
            
        elif (self.screen != 0) and self.player_item.owner_object.position.x_max < ((self.win_width -Gui.Distance_right_limit) + \
           (self.screen -1) * (self.win_width - Gui.Distance_right_limit - Position.Distance_x)):
            
            self.screen -= 1 #player is on the left edge of the current screen
            self.win_width_prev = self.win_width
        
        

        if self.screen > 0:
        
            delta_x = self.screen *(self.win_width_prev - Position.Distance_x -Gui.Distance_right_limit)#Distance_x tells where the most left object should be located in the screen

            # adjust player item location
            y = self.player_item.owner_object.position.y_max #upper corner
            x = self.player_item.owner_object.position.x_min #left corner
            self.player_item.setPos(x - delta_x, y)

            # adjust enemy positions
            for i in range(len(self.enemy_items)):
                
                y = self.enemy_items[i].owner_object.position.y_max
                x = self.enemy_items[i].owner_object.position.x_min
                self.enemy_items[i].setPos(x - delta_x, y)
            
                

                
        
        #if value = 0, player is still in screen and nothing has to be done
                   
        #notice that self.screen is also used to adjust  static object locations
                
        
    def adjust_static_objects_positions(self):
        #this method is called when self.screen != self.screen_prev
        # it adjusts static_object position to correctly fit object to the screen

        delta_x = self.screen *(self.win_width - Position.Distance_x -Gui.Distance_right_limit)
        
        for i in range (len(self.static_items)):
            
            y = self.static_items[i].y #upper corner, it's not changed
            x = self.static_items[i].x - delta_x #left corner
            
            width = self.static_items[i].width
            height = self.static_items[i].height
            
            if self.static_items[i].type == 'ground_object':
                
                if self.static_items[i].new_height != 0:
                    #if correct_scene_item_positions method has been called ground's draw height doesn't match owner_object height
                    height = self.static_items[i].new_height
                    
            
            self.static_items[i].setRect(x,y,width,height)

        
    
            
    def get_scene_items_number(self):
        #this is for testing use only
        print('there is {} items in scene'.format(len(self.scene.items())))
            
        
    def set_gamefield_to_start(self):
        #this is called from reset gui
        #it sets self.gamefield objects positions match self.gamefield_start
        pass #implemented later
        
        
        
       
        
        

#only for testing

if __name__=="__main__":

    
    app = QApplication(sys.argv)
    app.setApplicationName('Gui')

    #only for testing purposes
    config = Config() #create config object, this must be done before creating gui or gamefield objects
    if config.config_return_value:
        #If is true when return value is 1 or 2

        if config.config_return_value == 2:
            print('NOTICE: There is something wrong in the config file')
            print('The game is partially using standard set values')
            
        #file = open('erikoisempi_kentta.txt','r')
        #file = open('vihollis_testi_kentta.txt','r')
        file = open('game_testi.txt','r')
        #file = open('leijuva_testi_kentta.txt','r')
        #file = open ('erilainen_kentta.txt','r')
        #file = open('melko_tyhja_kentta.txt','r')
    
        gamefield = GameField()
        gamefield.parse_gamefield(file)
        file.close()
        
    
        #file = open('erikoisempi_kentta.txt','r')
        #file = open('vihollis_testi_kentta.txt','r')
        #file = open('game_testi.txt','r')
        #file = open('leijuva_testi_kentta.txt','r')
        #file = open ('erilainen_kentta.txt','r')
        file = open('melko_tyhja_kentta.txt','r')
    
        gamefield_copy = GameField()
        gamefield_copy.parse_gamefield(file)
        file.close()
    
    

        main = Gui()
    
        #print(Gui.Level_number)
        #print(Config.level_number)
   
          
        main.set_gamefield(gamefield,gamefield_copy)
        main.gamefield_level = 'game_testi.txt'
    
   
    
        main.show()

        sys.exit(app.exec_())


    else:
        #when config is 0

        print('A fatal error happened during reading the config file')
        print("Check that 'config.txt' file exists in a folder named 'game_config', one level below the current working directory")
        print("Check also that 'config.txt' contains 'level_number' ")
    
