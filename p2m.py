import turtle
import math
import random
import keyboard


#Radar class: each radar is defined by its x-axis position in the the front bumper of the vehicle, 
#its field of view, an error_rate, maximum range, and an objectsDetected List which saves all objects 
#detected by the radar ( with a certain error rate )
class Radar:
    def __init__(self, pos, color, radar_range, fieldOfView, error_rate):
        self.pos = pos
        self.color = color
        self.radar_range = radar_range*3.5
        self.fieldOfView = fieldOfView
        self.error_rate = error_rate
        self.objectsDetected = []

        #Used for radar visualization        
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.pensize(2)
        self.turtle.ht()
    
    #Used to make another copy of this radar
    def copy(self):
        newRadar = Radar(self.pos, self.color, self.radar_range, self.fieldOfView, self.error_rate)
        newRadar.objectsDetected = self.objectsDetected.copy()
        return newRadar

    #drawing the radar and its detections ( taking into consideration the error rate )
    def drawRadarData(self):
        drawRadar(self,False)
        correctRadarlines(self)
        for obj in self.objectsDetected:
            sceneObj = SceneObject(obj.x, obj.y, obj.radius)
            sceneObj.draw(self.turtle, self.color)

    #Used for debugging
    def __str__(self):
        string = "radar positioned : "+str(self.pos) + "\n"
        for object in self.objectsDetected:
            string += "("+str(object.distance)+","+str(object.angle)+")"+"\n"
        return string

#RadarObject class: each RadarObject is saved using its distance, angle of arrival, and a radius 
#( replacing the Surface équivalente radar )
#we also saved the x and y-axis cords ( considering the error rate, just to visualize it )
class RadarObject:
    def __init__(self, distance, angle, radius, x, y):
        self.distance = distance
        self.angle = angle
        self.radius = radius
        self.x = x
        self.y = y

    #making sure that this object is the same as another object passed as an argument
    #two objects can be considered the same ( taking into consideration the error rate ) 
    #if both angles of arrival, distances, and radius values are too close to each other.
    def compare(self, obj):
        if(obj==None):
            return False
        if(abs(self.angle-obj.angle) < 5):
            if(abs(self.distance-obj.distance) < self.radius):
                if(self.radius - obj.radius < 0.5):
                    return True
        return False

    #Used to make another copy of this radarObject
    def copy(self):
        return RadarObject(self.distance, self.angle, self.radius, self.x, self.y)

#SceneObject is defined by its x and y-axis cords and a radius
#this class is used to just generate a scenario on which we implement our fusion model
class SceneObject:
    def __init__(self, x, y, radius):
        self.x = x + x0
        self.y = y + y0
        self.radius = radius
    
    #allows the object to be detected by a certain radar considering the error_rate,
    #and whether the radar is able to directly see the object or not ( behind another object )
    def radarDetection(self, radar, isNewObj):
        randomN = math.floor(random.random()*2)
        if(randomN == 0):
            signX = -1
        else:
            signX = 1
        randomN = math.floor(random.random()*2)
        if(randomN == 0):
            signY = -1
        else:
            signY = 1
        x = self.x + self.x * radar.error_rate * signX
        y = self.y + self.y * radar.error_rate * signY

        distance = math.sqrt((radar.pos-x)*(radar.pos-x)+(y0-y)*(y0-y))
        if(distance <= radar.radar_range):
            angle = math.degrees(math.asin((abs(y-y0))/distance))
            if(angle >= (180-radar.fieldOfView)/2):
                if(not isBehindAnotherObject(angle, self.radius, radar.objectsDetected)):
                    if(x < radar.pos):
                        angle = 180-angle
                    if(isNewObj):
                        radar.objectsDetected.append(RadarObject(
                            distance, angle, self.radius, x-x0, y-y0))
                    else:
                        radar.turtle.up()
                        radar.turtle.setpos(x, y)
                        radar.turtle.down()
                        radar.turtle.dot(self.radius, radar.color)

    #used for debugging
    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"

    #visualizing data
    def draw(self, turtle, color):
        turtle.up()
        turtle.setpos(self.x, self.y)
        turtle.down()
        turtle.dot(self.radius, color)


#drawing radar to the scene ( visualizing data )
def drawRadar(radar,fusionOn):
    if fusionOn:
        if(radar==radars[mainRadarIndex]):
            finalRadar.turtle.color("deep pink")
        else :
            finalRadar.turtle.color("#2EFF2E")
        angle = (180-radar.fieldOfView)/2
        finalRadar.turtle.up()
        finalRadar.turtle.setpos(x0+radar.pos, y0)
        finalRadar.turtle.setheading(angle)
        finalRadar.turtle.down()
        finalRadar.turtle.forward(radar.radar_range)
        finalRadar.turtle.setheading(90+angle) 
        finalRadar.turtle.circle(radar.radar_range, radar.fieldOfView)
        finalRadar.turtle.setheading(-angle)
        finalRadar.turtle.forward(radar.radar_range) 
    else:
        angle = (180-radar.fieldOfView)/2
        radar.turtle.up()
        radar.turtle.setpos(x0+radar.pos, y0)
        radar.turtle.setheading(angle)
        radar.turtle.down()
        radar.turtle.forward(radar.radar_range)
        radar.turtle.setheading(90+angle) 
        radar.turtle.circle(radar.radar_range, radar.fieldOfView)
        radar.turtle.setheading(-angle)
        radar.turtle.forward(radar.radar_range) 


#redrawing Lines ( priority levels )
def correctRadarlines(radar):
    angle = (180-radar.fieldOfView)/2
    radar.turtle.pencolor(radar.color)
    radar.turtle.up()
    radar.turtle.setpos(x0+radar.pos, y0)
    radar.turtle.setheading(angle)
    radar.turtle.down()
    radar.turtle.forward(radar.radar_range)
    radar.turtle.setheading(90+angle)
    radar.turtle.circle(radar.radar_range, radar.fieldOfView)
    radar.turtle.setheading(-angle)
    radar.turtle.forward(radar.radar_range)


#collision detection ( making sure that no two objects can collide while making a new scene )
def collisionDetected(obj1, objectList):
    if(len(objectList) == 0):
        return False
    for obj2 in objectList:
        distance = math.sqrt(math.pow((obj1.x-obj2.x), 2) +
                             math.pow((obj1.y-obj2.y), 2))
        if(distance < obj1.radius + obj2.radius +50): 
            return True
    return False


#returns true if the radar cannot detect the object directly
def isBehindAnotherObject(angle, radius, objectsDetected) -> bool:
    for obj2 in objectsDetected:
        if(abs(angle-obj2.angle) < 5):
            if(radius-obj2.radius < 5):
                return True
    return False


#Used for debugging ( draws a wave each 2° )
def drawWaves(radar):
    for angle in range(math.floor((180-radar.fieldOfView)/2), math.floor((180-radar.fieldOfView)/2+radar.fieldOfView), 2):
        radar.turtle.pensize(1)
        radar.turtle.up()
        radar.turtle.setpos(radar.pos, y0)
        radar.turtle.down()
        radar.turtle.setheading(angle)
        radar.turtle.forward(radar.radar_range)


#fusing data by shifting it from one radar to another ( AOA and range traduction )
#and comparing if two objects are the same
def fuse2Radars(radar1, radar2) -> Radar:
    objectsDetected = []
    radar1_objects = radar1.objectsDetected.copy()
    radar2_objects = radar2.objectsDetected.copy()
    for i in range(len(radar1_objects)):  
        #shifting data from radar1 to radar2
        radar1_objects[i].distance = math.sqrt(math.pow(radar2.pos-radar1_objects[i].x,2)+math.pow(radar1_objects[i].y,2))
        y_distance = abs(radar1_objects[i].y) 
        radar1_objects[i].angle = math.degrees(math.asin(y_distance/radar1_objects[i].distance)) 
        if(radar1_objects[i].x<radar2.pos):
            radar1_objects[i].angle = 180-radar1_objects[i].angle
        #comparing it with all the objects already detected in radar2
        for j in range(len(radar2_objects)): 
            if(radar1_objects[i]==None or radar2_objects[j]==None):
                continue
            if(radar1_objects[i].compare(radar2_objects[j])):
                newObj = RadarObject((radar1_objects[i].distance+radar2_objects[j].distance)/2, (radar1_objects[i].angle +
                                     radar2_objects[j].angle)/2, radar1_objects[i].radius, (radar1_objects[i].x+radar2_objects[j].x)/2, (radar1_objects[i].y+radar2_objects[j].y)/2)
                objectsDetected.append(newObj)
                radar2_objects[j]=None
                radar1_objects[i]=None 
    #fusing the data into a new List to return
    for obj in radar2_objects:
        if obj!=None:
            objectsDetected.append(obj)
    for obj in radar1_objects:
        if obj!=None:
            objectsDetected.append(obj)
    radar = radar2
    radar.objectsDetected = objectsDetected
    return radar 


#generating the main scene 
def generateScene(objects, nbrOfObjects):
    # mainSceneTurtle.fillcolor("#d3f8d3")
    # mainSceneTurtle.pencolor("#d3f8d3")
    mainSceneTurtle.hideturtle()
    mainSceneTurtle.up()
    mainSceneTurtle.setpos(x0-distance_between_radars,y0)
    mainSceneTurtle.down()
    mainSceneTurtle.setheading(0)
    mainSceneTurtle.forward(distance_between_radars*2)
    mainSceneTurtle.setheading(270)
    mainSceneTurtle.forward(distance_between_radars*3)
    mainSceneTurtle.setheading(180)
    mainSceneTurtle.forward(distance_between_radars*2)
    mainSceneTurtle.setheading(90)
    mainSceneTurtle.forward(distance_between_radars*3)
    mainSceneTurtle.speed(0)
    mainSceneTurtle.pensize(2)
    for i in range(nbrOfObjects):
        collided = True
        newObj = None
        while (collided):
            randomN = math.floor(random.random()*2)
            if(randomN == 0):
                signX = -1
            else:
                signX = 1
            newObj = SceneObject(math.floor(random.random()*radar_range*1.2)*signX,
                                 100 + math.floor(random.random()
                                                  * radar_range*0.85),
                                 15+math.floor(random.random()*15))
            collided = collisionDetected(newObj, objects) 
        newObj.draw(mainSceneTurtle, "black")
        objects.append(newObj)
    newObj = SceneObject(0,150,15)
    objects.append(newObj)
    objects = sorted(objects, key=lambda obj: obj.y, reverse=False)
    for newObj in objects:
        for radar in radars:
            newObj.radarDetection(radar, True)
    return objects

#Shifting data ( AOA and range ) from one radar to another
def shiftData(object,radar) -> RadarObject:
    distance = math.sqrt(math.pow(radar.pos-object.x,2)+math.pow(object.y,2))
    y_distance = abs(object.y) 
    angle = math.degrees(math.asin(y_distance/distance)) 
    if(object.x<radar.pos):
        angle = 180-object.angle
    return RadarObject(distance,angle,object.radius, object.x, object.y)


#removing old scene and redrawing the current radar as the currentId changes
def redrawScene() -> None:
    for i in range(len(radars)):
        if(i!=currentId):
            radars[i].turtle.clear() 
    radars[currentId].drawRadarData()

#toggeling between drawing and hiding fusion results
def drawFusionResult(fusionResultOnScreen):
    if(not fusionResultOnScreen):
        showAllRadarsBorders()
        #drawing the new detected objects after fusion 
        for obj in finalRadar.objectsDetected: 
            finalRadar.turtle.up()
            finalRadar.turtle.setpos(obj.x,obj.y+y0)
            finalRadar.turtle.down()
            finalRadar.turtle.dot(obj.radius,"#2EFF2E")
            finalRadar.turtle.color('deep pink')
            style = ('Courier', 8, 'italic')
            finalRadar.turtle.write("aoa:"+"{:.2f}".format(obj.angle)+"\n"+"range:"+"{:.2f}".format(obj.distance), font=style)
        return True
    else:  
        finalRadar.turtle.clear()
        return False
    
def showAllRadarsBorders():
    for radar in radars:
        drawRadar(radar,True)
####################################################################################
##------------------------------------- Main -------------------------------------##
####################################################################################
#common radar configuration
global y0, x0, radars, objects, mainSceneTurtle, currentId, fusionResultOnScreen
y0 = -200
x0 = 0

#Contains all the SceneObjects
objects = []

#Contains all the Radars currently in use
radars = []

#Making sure to always display the mainScene data ( car and objects )
mainSceneTurtle = turtle.Turtle()

#default radar configuration
radar_range = 450
distance_between_radars = 35
fieldOfView = 130
error_rate = 0.02

#making sure to detect the keyboard.onPress only once
leftIsPressed = False
rightIsPressed = False
fIsPressed = False

#toggeling between showing and hiding fusion result
fusionResultOnScreen = False

#circulating between the radars currently used
currentId = 0

screen = turtle.Screen()
screen.setup(width = 1.0, height = 1.0)

#creating a costumized radar
radars.append(Radar(0, "red", 180, 90, error_rate))

#creating more radars with the common radar configuration
#Radar(x-axis_Position, color, maximum_range, field_of_view, error_rate)
radars.append(Radar(35, "blue", 100, 130, error_rate))
radars.append(Radar(-35, "yellow", 100, 130, error_rate)) 
#Sorting the radars from left to right
radars = sorted(radars, key=lambda radar: radar.pos, reverse=False)

#Deciding which radar is the main radar ( to compare with and without fusion algo )
mainRadarIndex = 1

#Drawing instructions of how to use the simulation
mainSceneTurtle.up()
mainSceneTurtle.setpos(50,y0-50)
mainSceneTurtle.down()
mainSceneTurtle.color('deep pink')
style = ('Courier', 15, 'italic')
mainSceneTurtle.write("Press 'Left' and 'Right' arrows \nto switch between radars", font=style)

mainSceneTurtle.up()
mainSceneTurtle.setpos(50,y0-100)
mainSceneTurtle.down()
style = ('Courier', 15, 'italic')
mainSceneTurtle.write("Press 'f' to toggle On/Off the fusion result", font=style)

mainSceneTurtle.color('black')

#generating scene ( objects )
#radars should be created before this line of code ( each object added to the scene 
#will run a method that allows each radar to either detect it or not, any radar added after the 
#scene generation will not function )
objects = generateScene(objects,40)

#Making a copy of the main radar
middleRadar = radars[mainRadarIndex].copy()
finalRadar = None

#Fusing data into a new final radar
if(len(radars)!=0):
    finalRadar = radars[0].copy()
    for currentRadar in radars:
        radar = currentRadar.copy() 
        # drawWaves(currentRadar)
        # radar.turtle.clear()
        finalRadar = fuse2Radars(finalRadar,radar) 

#Shifting data to the mainRadar back :
for i in range(len(finalRadar.objectsDetected)):
    finalRadar.objectsDetected[i] = shiftData(finalRadar.objectsDetected[i],middleRadar).copy()

'''   
    turtle.hideturtle()
    ts = turtle.getscreen()
    ts.getcanvas().postscript(file=str(i)+"_dataFusion2.eps")
 
    """  ts = turtle.getscreen()
    ts.getcanvas().postscript(file=str(i)+"_dataFusion1.eps")
    ts.clear() """  
 '''


while True:
    #pressing left and right arrow circulates between radars
    if not keyboard.is_pressed('left arrow'):
        leftIsPressed = False
    if not leftIsPressed:
        if keyboard.is_pressed('left arrow'): 
            currentId = (currentId-1)%len(radars) 
            redrawScene()
            leftIsPressed = True

    if not keyboard.is_pressed('right arrow'):
            rightIsPressed = False
    if not rightIsPressed:
        if keyboard.is_pressed('right arrow'):
            currentId = (currentId+1)%3
            redrawScene() 
            rightIsPressed = True
    
    #pressing f toggles between showing fusion result and hiding it
    if not keyboard.is_pressed('f'):
            fIsPressed = False
    if not fIsPressed:
        if keyboard.is_pressed('f'): 
            fusionResultOnScreen = drawFusionResult(fusionResultOnScreen) 
            fIsPressed = True
