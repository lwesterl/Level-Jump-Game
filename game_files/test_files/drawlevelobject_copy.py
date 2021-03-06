from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor


class DrawLevelObject(QGraphicsRectItem):
    #This class is used by gui to draw leveleditor object to a scene
    #It inherits QGraphicsRectItem to draw squares
    
    square_size = 20 #This tells square size for leveleditor objects
    distance_x = 0 #distance from scene left corner
    distance_y = 100 #distance from scene upper corner
    
    def __init__(self,owner):
        #owner is the levelobject this draw object represents

        x = owner.x * DrawLevelObject.square_size + DrawLevelObject.distance_x
        y = owner.y * DrawLevelObject.square_size + DrawLevelObject.distance_y
        super(DrawLevelObject, self).__init__(x, y, DrawLevelObject.square_size, DrawLevelObject.square_size)
        self.owner = owner #This is used to remove deleted object from scene
        self.set_color()


    def set_color(self):
        #This is called when object is initialized
        #It sets correct color to the object based on owner object type
        
        if self.owner.object_type == 'current':
            #creates a clear square
            color = Qcolor(255,255,255,50)
            #Notice that the 4th number is the alpha channel value

        elif self.owner.object_type == 'player':
            #creates a blue square
            color = Qcolor(0,0,255,255)

        elif self.owner.object_type == 'enemy':
            #creates a red squre
            color = Qcolor(255,0,0,255)

        elif self.owner.object_type == 'visible':
            #creates a brown square
            color = Qcolor(110,60,10,255)

        elif self.owner.object_type == 'finish':
            #creates a green square
            color = Qcolor(0,255,0,255)

        elif self.owner.object_type == 'invisible':
            #creates a black square
            color = Qcolor(0,0,0,255)

        self.setBrush(QBrush(color))
        

        
            
        

        
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
