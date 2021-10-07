from Colour import *
class Game:
    def __init__(self,N = 4): 
        self.N = N
        self.grid = np.zeros((N,N),int) #Create an array of 4,4 shape having all ele as 0
        self.width = 600
        self.height = 600
        pygame.init() #Inititalize the window for pygame
        pygame.display.set_caption("PyGame 2048") 
        self.screen = pygame.display.set_mode((self.width, self.height))
    def InsertRandom(self,k = 1): #Insert one random number in the grid
        empty_pos = list(zip(*np.where(self.grid == 0))) #creates a list of (row,col) for empty spaces
        for pos in random.choices(empty_pos, k = k): 
            #Randomly chooses 2 or 4 having probability 0.9 and 0.1 respectively
            random_num = random.choices([2,4], weights = [0.9,0.1])[0]  
            self.grid[pos] = random_num 
    #self instance is not required over here and also is never called so we can declare it as a static method
    @staticmethod
    def add(modify):
        mod_final = []
        flag = False #Makes skipping of element easier
        for i in range(len(modify)):
            if flag:
                flag = False
                continue
            if i != len(modify) - 1 and modify[i] == modify[i+1]:  #If suppose 'i' is the last element then 'i+1' will go out of bounds
                new_num = modify[i] *2 
                flag = True
            else:
                new_num = modify[i]
            mod_final.append(new_num)
        return np.array(mod_final)
    def update(self,user_input):#Updates the grid whenever user input is given
        for i in range(self.N):
            #When user input says shift left(a) or right(d)
            if user_input in "ad":
                gridpart = self.grid[i,:] #Isolate that part of grid
                if user_input == "a":
                    non_zero_gridpart = self.add(gridpart[gridpart != 0]) #Look for the non zero elements ,i.e., the ones we have to work on
                else:
                    non_zero_gridpart = self.add(gridpart[gridpart != 0][::-1]) #For shifting right just reverse the array
                gridpart_new = np.zeros_like(gridpart) #Create a new 0 array similar to 'gridpart'
                gridpart_new[0:len(non_zero_gridpart)] = non_zero_gridpart 
                if user_input == "a":
                    self.grid[i,:] = gridpart_new
                else: 
                    self.grid[i,:] = gridpart_new[::-1]
            #When user inuput says shift up(w) or down(s)
            if user_input in "ws":
                gridpart = self.grid[:,i]
                if user_input == "w":
                    non_zero_gridpart = self.add(gridpart[gridpart != 0])
                else:
                    non_zero_gridpart = self.add(gridpart[gridpart != 0][::-1])
                gridpart_new = np.zeros_like(gridpart)
                gridpart_new[0:len(non_zero_gridpart)] = non_zero_gridpart
                if user_input == "w":
                    self.grid[:,i] = gridpart_new
                else: 
                    self.grid[:,i] = gridpart_new[::-1]
    def GameOver(self): #Checkes whether game is over or not 
        if list(zip(*np.where(self.grid == 0))) == []: #If empty spaces == 0 then game is over
            return True
        else:
            return False       
    def display(self): #Display the game grid using PyGame
        self.screen.fill(const['back'])
        for i in range(self.N):
            for j in range(self.N):
                ele = self.grid[i][j]

                X = j*self.width//self.N # Find the x co-ordinate of the element in grid
                Y = i * self.height//self.N #Find the y co-ordinate of the element in the grid
                W = self.width //self. N  #Determine the width of the element box
                H = self.height//self.N #Determine the height of the element box
                
                pygame.draw.rect(self.screen,const[ele],pygame.Rect(X,Y,W,H))
                if ele == 0:
                    continue
                #Display the number in its box
                font = pygame.font.SysFont("Arial",50)
                text_surface = font.render(str(ele), True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(X + W / 2,Y + H / 2))
                self.screen.blit(text_surface, text_rect)
    @staticmethod
    def K_input(): #Get input from the pygame window
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_w:
                        return 'w'
                    elif event.key == K_d:
                        return 'd'
                    elif event.key == K_a:
                        return 'a'
                    elif event.key == K_s:
                        return 's'
                    elif event.key == K_ESCAPE:
                        return 'q'
    def play(self):
        self.InsertRandom(k=2) #Start with inserting 2's at 2 different position
        while True:
            self.display()
            pygame.display.flip() #Keeps refreshing the screen
            user_input = self.K_input()
            if user_input == 'q':
                break
            self.update(user_input)
            self.InsertRandom()
            if self.GameOver():
                font = pygame.font.SysFont("Arial",100)                
                text = "GAME OVER!"
                game_over_text = font.render(text,True,(0,0,0))
                self.screen.fill(const['back'])
                self.screen.blit(game_over_text,((self.width - game_over_text.get_width())/2,(self.height - game_over_text.get_height())/2))
                pygame.display.flip()
                time.sleep(5)
                break
game = Game() #Default value of grid is 4x4 
game.play()