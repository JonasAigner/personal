"""
This is a project with an other programmer made with python3 and pygame.
We both have to code three Chracters with their own AI and they will battle each others.
The team who's kills the other team wins.

---- Autors: ----
Wizard: Hiheat
Priest: Hiheat



Github: Hiheat
"""

# --- import modules ----
import pygame
import sys
import os
import time
import random

# custim module
import timer
#import pybars


def write(background, text, x=50, y=150, color=(0,0,0),
          fontname="mono", fontsize=None, center=False):
        """write text on pygame surface. """
        if fontsize is None:
            fontsize = 24
        font = pygame.font.SysFont(fontname, fontsize, bold=True)
        fw, fh = font.size(text)
        surface = font.render(text, True, color)
        if center: # center text around x,y
            background.blit(surface, (x-fw//2, y-fh//2))
        else:      # topleft corner is x,y
            background.blit(surface, (x,y))



# ---- general functions ----
def set_icon(iconname):
    """icon has to be a 32*32 bitmap file"""
    icon=pygame.Surface((32,32))
    icon.set_colorkey((255,255,255))
    rawicon=pygame.image.load(os.path.join("data", iconname)) #must be 32x32, black is transparant
    for i in range(0,32):
        for j in range(0,32):
            icon.set_at((i,j), rawicon.get_at((i,j)))
    pygame.display.set_icon(icon)
    
def is_figureFree(pos):
    for group1 in Game.groups:
        for sprite in group1:
            if sprite.pos[0] == pos[0] and sprite.pos[1] == pos[1]:
                return sprite
    return True 
    
def get_distance(s1, s2):
    distancex = int(s1.pos[0] - s2.pos[0])
    distancex /= 75
    distancey = int(s1.pos[1] - s2.pos[1])
    distancey /= 70
    distancex = abs(distancex)
    distancey = abs(distancey)
    
    return [distancex, distancey]
    

def programmer_help():
    print("""------------------------ Programmer manual ------------------------
    
=== Figure ===
if team is an argument:
team has to be a list/tuble, with 0 as beginning

[set_image]....................sets the image and make it useable(set_colokey, convert_alpha, set rect) or make it a 1 by 1 surface
[animate]......................images: images for the animation(has to be a group)    change_time: how fast the animation will go(the smaller the faster)
[kill].........................kills the sprite
[move_act].....................adds the move to the pos
[move_to]......................moves to a coordinate
[collide]......................test if figure collides with a spezific team
[attack_cd]....................returns the direction for an attack against a spezific team
[attack].......................attacks with (ammo:like "spell_knife") a (team) with a (mode:like cd)
[dodge]........................W.I.P.

more Coming Soon\n\n""")
    
   
class Bar(pygame.sprite.Sprite):
    
    def __init__(self, start, color, width=5, height=20):
        self.value = start
        self.color = color
        self.width = width
        self.height = height
        self.create_image()
        
    def create_image(self):
        if self.value <= 0:
            self.image = pygame.Surface((1, self.height))
        else:
            self.image = pygame.Surface((self.value*self.width, self.height))
            self.image.fill(self.color)
        
    def remove(self, value):
        self.value -= value
        
    def set(self, value):
        self.value = value
        
    def add(self, value):
        self.value += value
        
    def divide(self, value):
        self.value /= value
        
    def multiply(self, value):
        self.value *= value
        
    def update(self):
        self.create_image()   
        
true = True

class Hud(pygame.sprite.Sprite):
    
    def __init__(self, picture, val=0, val2=0, val3=0):
        self.picture = picture
        self.image = None
        self.value1 = val
        self.value2 = val2
        self.value3 = val3
        self.bar1 = None
        self.bar2 = None
        self.bar3 = None
        #self.update()  
        self.create_image()
        
        
    def create_image(self):
        global true
        if true:
            self.image = None
            self.image0 = None
            self.bar1 = None
            self.image0 = self.picture
            bar1 = Bar(self.value1, (0, 200, 0), 1.05, 13)
            self.image0.blit(bar1.image, (72, 5))
            self.image = self.image0.copy()
            true = False
        else:
            self.image0 = self.picture
            bar1 = Bar(self.value1, (200, 0, 0), 1.05, 13)
            self.image0.blit(bar1.image, (72, 5))
            self.image = self.image0.copy()
        # ~ if self.value <= 0:
            # ~ self.image = pygame.Surface((1, self.height))
        # ~ else:
            # ~ self.image = pygame.Surface((self.value*self.width, self.height))
            # ~ self.image.fill(self.color)
            
            
    # ~ def update(self):
        # ~ self.create_image()
    
    
class Figure(pygame.sprite.Sprite):
    
    def __init__(self):
        self.team = None
        self.speed = [75, 70]
        self.hp = 100
        self.attacks = []
        self.image = None
        self.owner = None
        #self.groups = ()
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = [0, 0]
        self.move = [0, 0]
        self.stop_on_edge = False
        self.warp_on_edge = False
        self.kill_on_edge = False
        self.angle = None
        self.marked = None
        self.animdur = 0
        self.animevo = 0
        self.lifetime = 0
        self.richtungen = ["oben", "unten", "links", "rechts", "obenrechts", "obenlinks", "untenrechts", "untenlinks"]
        
    def set_image(self):
        if self.image != None:
            self.image.set_colorkey((255,255,255))
            self.image.convert_alpha()
            #self.image = pygame.transform.scale(self.bild, (200, 100))
            self.rect = self.image.get_rect()
            self.image0 = self.image.copy()
        else:
            self.image = pygame.Surface((1, 1))
            
    def animate(self, images, change_time):
        self.animdur += 1
        if self.animdur >= change_time:
            self.image = images[self.animevo]
            self.animevo += 1
            self.animdur == 0
        if self.animevo > 3:
            self.animevo = 0
            
    def kill(self):
        pygame.sprite.Sprite.kill(self)
        
    def move_act(self):
        self.pos[0] += self.move[0]
        self.pos[1] += self.move[1]
        
    def move_to(self):
        self.pos = self.move
        
    def collide(self, team):
        if len(team) > 2:
            for group1 in Game.groups:
                for sprite in group1:
                    if sprite.owner != self:
                        if sprite.team in team:
                            if self.pos[0]+55 == sprite.pos[0] and self.pos[1] == sprite.pos[1]:  #rechts
                                return sprite
                            elif self.pos[0]-75 == sprite.pos[0] and self.pos[1] == sprite.pos[1]:  #links
                                return sprite
                            elif self.pos[0] == sprite.pos[0] and self.pos[1] == sprite.pos[1]:  #unten
                                return sprite
                            elif self.pos[0] == sprite.pos[0] and self.pos[1] == sprite.pos[1]:  #oben
                                return sprite
                        
                        
        else:
            for group1 in Game.groups:
                for sprite in group1:
                    if sprite.team in team:
                        if sprite.owner != self:
                            if self.pos[0]+55 == sprite.pos[0] and self.pos[1] == sprite.pos[1]:  #rechts
                                return sprite
                            elif self.pos[0]-30 == sprite.pos[0] and self.pos[1] == sprite.pos[1]:  #links
                                return sprite
                            elif self.pos[0] == sprite.pos[0] and self.pos[1]+70 == sprite.pos[1]:  #unten
                                return sprite
                            elif self.pos[0] == sprite.pos[0] and self.pos[1]-70 == sprite.pos[1]:  #oben
                               return sprite
                            
        return False 
        

    def attack_cd(self, team, chance):
        if len(team) > 2:
            if random.random() < chance:
                for group1 in Game.groups:
                    for sprite in group1:
                        if sprite.team in team:
                            if self.pos[0] < sprite.pos[0] and self.pos[1] == sprite.pos[1]:  #rechts
                                return "rechts"
                            elif self.pos[0] > sprite.pos[0] and self.pos[1] == sprite.pos[1]:  #links
                                return "links"
                            elif self.pos[0] == sprite.pos[0] and self.pos[1] < sprite.pos[1]:  #oben
                                return "oben"
                            elif self.pos[0] == sprite.pos[0] and self.pos[1] > sprite.pos[1]:  #unten
                                return "unten"
                        
                        
        else:
            if random.random() < chance:
                for group1 in Game.groups:
                    for sprite in group1:
                        if sprite.team in team:
                            if self.pos[0] < sprite.pos[0] and self.pos[1] == sprite.pos[1]:  #rechts
                                return "rechts"
                            elif self.pos[0] > sprite.pos[0] and self.pos[1] == sprite.pos[1]:  #links
                                return "links"
                            elif self.pos[0] == sprite.pos[0] and self.pos[1] < sprite.pos[1]:  #oben
                                return "oben"
                            elif self.pos[0] == sprite.pos[0] and self.pos[1] > sprite.pos[1]:  #unten
                               return "unten"
                            
        return False 
         
         
    def get_random_enemy(self, team):
        enemys = []
        for sprite in Game.figuregroup:
            if sprite.team in team:
                enemys.append(sprite)
        try:
            x = random.choice(enemys)
            return x
        except IndexError:
            return False
                    

    def attack(self, mode, team, am, chance=0.3):
        if am == "no":
            return None
        elif am == "random_mage":
            am = random.choice(["spell_knife", "tornado"])
        elif am == "random_priest":
            am = random.choice(["cross", "cross", "cross", "big_cross"])
        if am == "big_cross":
            mode = "from_above"
        
        if mode == "cd":
            attackdir = self.attack_cd(team, chance)
            if attackdir != False:
                spellknife = None
                if attackdir == "rechts":
                    if self.angle != "rechts":
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.angle = "rechts"
                    
                    if am == "spell_knife":
                        spellknife = Spell_Knife(self, [self.pos[0]+75, self.pos[1]], "r")
                    elif am == "tornado":
                        tornado = Tornado(self, [self.pos[0]+75, self.pos[1]], "r")
                    elif am == "cross":
                        cross = Wood_Cross(self, [self.pos[0]+75, self.pos[1]], "r")
                    
                    
                elif attackdir == "links":
                    if self.angle != "links":
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.angle = "links"
                    if am == "spell_knife":
                        spellknife = Spell_Knife(self, [self.pos[0]-30, self.pos[1]], "l")
                    elif am == "tornado":
                        tornado = Tornado(self, [self.pos[0]-30, self.pos[1]], "l")
                    elif am == "cross":
                        cross = Wood_Cross(self, [self.pos[0]-30, self.pos[1]], "l")
                    
                elif attackdir == "oben":
                    if am == "spell_knife":
                        spellknife = Spell_Knife(self, [self.pos[0], self.pos[1]+75], "o")
                    elif am == "tornado":
                        tornado = Tornado(self, [self.pos[0], self.pos[1]+75], "o")
                    elif am == "cross":
                        cross = Wood_Cross(self, [self.pos[0], self.pos[1]+75], "o")
                    
                elif attackdir == "unten":
                    if am == "spell_knife":
                        spellknife = Spell_Knife(self, [self.pos[0], self.pos[1]-75], "u")
                    elif am == "tornado":
                        tornado = Tornado(self, [self.pos[0], self.pos[1]-75], "u")
                    elif am == "cross":
                        cross = Wood_Cross(self, [self.pos[0], self.pos[1]-75], "u")
                    
                if am == "spell_knife":
                    spellknife.act()
                    Game.sounds["spell1"].play()
                elif am == "tornado":
                    tornado.act()
                    Game.sounds["spell_wind"].play()
                elif am == "cross":
                    cross.act()
                    Game.sounds["attack1"].play()
                    
        elif mode == "from_above":
            enemy = self.get_random_enemy(team)
            if enemy != False:
                if random.random() < chance:
                    if am == "big_cross":
                        big_cross = Big_Cross(self, enemy.pos)
                            
        else:
            print("[ERROR]: Mode '{}' not found".format(mode))  
            
            
    def dodge(self):
        for attack in Game.groups[2]:
            distanz = get_distance(self, attack)
            if attack.owner != self:
                distanz = get_distance(self, attack)
                if distanz[0] <= 3:
                    self.move = [0, 70]
                    break
                elif distanz[1] < 3:
                    self.move = [75, 0]
                    break

            
    def get_random_direct(self):
        if random.random() < 0.3:
            direct = random.choice(self.richtungen)
            if direct == "oben":
                return [0, self.speed[1]]#(0, -70)
            elif direct == "unten":
                return [0, -self.speed[1]]#(0, 70)
            elif direct == "rechts":
                return [self.speed[0], 0]#(75, 0)
            elif direct == "links":
                return [-self.speed[0], 0]#(-75, 0)
            elif direct == "obenrechts":
                return [self.speed[0], self.speed[1]]
            elif direct == "obenlinks":
                return [-self.speed[0], self.speed[1]]
            elif direct == "untenrechts":
                return [self.speed[0], -self.speed[1]]
            elif direct == "untenlinks":
                return [-self.speed[0], -self.speed[1]]
        
        else:
            return [0, 0]    

            
    def direct_to_enemy(self, team):
        if len(team) > 2:
            for group1 in Game.groups:
                for sprite in group1:
                    if sprite.team in team:
                        if self.pos[0] < sprite.pos[0] and self.pos[1] == sprite.pos[1]:  #rechts
                            return [self.speed[0], 0]
                        elif self.pos[0] > sprite.pos[0] and self.pos[1] == sprite.pos[1]:  #links
                            return [-self.speed[0], 0]
                        elif self.pos[0] == sprite.pos[0] and self.pos[1] < sprite.pos[1]:  #oben
                            return [0, self.speed[1]]
                        elif self.pos[0] == sprite.pos[0] and self.pos[1] > sprite.pos[1]:  #unten
                            return [0, -self.speed[1]]
                        elif self.pos[0] < sprite.pos[0] and self.pos[1] < sprite.pos[1]:  #obenrechts  lll
                            return [self.speed[0], self.speed[1]]
                        elif self.pos[0] > sprite.pos[0] and self.pos[1] < sprite.pos[1]:  #obenlinks
                            return [-self.speed[0], self.speed[1]]
                        elif self.pos[0] < sprite.pos[0] and self.pos[1] > sprite.pos[1]:  #untenrechts
                            return -self.speed
                        elif self.pos[0] > sprite.pos[0] and self.pos[1] > sprite.pos[1]:  #untenlinks
                            return [-self.speed[0], -self.speed[1]]
                    
        
            
        else:    
            for group1 in Game.groups:
                for sprite in group1:
                    if sprite.team == team[1]:
                        if self.pos[0] < sprite.pos[0] and self.pos[1] == sprite.pos[1]:  #rechts
                            return [self.speed[0], 0]
                        elif self.pos[0] > sprite.pos[0] and self.pos[1] == sprite.pos[1]:  #links
                            return [-self.speed[0], 0]
                        elif self.pos[0] == sprite.pos[0] and self.pos[1] < sprite.pos[1]:  #oben
                            return [0, self.speed[1]]
                        elif self.pos[0] == sprite.pos[0] and self.pos[1] > sprite.pos[1]:  #unten
                            return [0, -self.speed[1]]
                        elif self.pos[0] < sprite.pos[0] and self.pos[1] < sprite.pos[1]:  #obenrechts
                            return [self.speed[0], self.speed[1]]
                        elif self.pos[0] > sprite.pos[0] and self.pos[1] < sprite.pos[1]:  #obenlinks
                            return [-self.speed[0], self.speed[1]]
                        elif self.pos[0] < sprite.pos[0] and self.pos[1] > sprite.pos[1]:  #untenrechts
                            return [self.speed[0], -self.speed[1]]
                        elif self.pos[0] > sprite.pos[0] and self.pos[1] > sprite.pos[1]:  #untenlinks
                            return [-self.speed[0], -self.speed[1]]
                
        return False
        
    def move_to_attack_cd(self, team, distance=4):    # cd means cardinal direction
         if len(team) > 2:
            for group1 in Game.groups:
                for sprite in group1:
                    if sprite.team in team:
                        if self.pos[0] < sprite.pos[0] and self.pos[1] < sprite.pos[1]:  #obenrechts   distanz ausrechnen
                            return [0, self.speed[1]]
                        elif self.pos[0] > sprite.pos[0] and self.pos[1] < sprite.pos[1]:  #obenlinks
                            return [0, self.speed[1]]
                        elif self.pos[0] < sprite.pos[0] and self.pos[1] > sprite.pos[1]:  #untenrechts
                            return [0, -self.speed[1]]
                        elif self.pos[0] > sprite.pos[0] and self.pos[1] > sprite.pos[1]:  #untenlinks
                            return [0, -self.speed[1]]
                        
                        
                        
         else:
             for group1 in Game.groups:
                 for sprite in group1:
                    if sprite.team in team:
                        if self.pos[0] < sprite.pos[0] and self.pos[1] < sprite.pos[1]:  #obenrechts   distanz ausrechnen
                            return [0, self.speed[1]]
                        elif self.pos[0] > sprite.pos[0] and self.pos[1] < sprite.pos[1]:  #obenlinks
                            return [0, self.speed[1]]
                        elif self.pos[0] < sprite.pos[0] and self.pos[1] > sprite.pos[1]:  #untenrechts
                            return [0, -self.speed[1]]
                        elif self.pos[0] > sprite.pos[0] and self.pos[1] > sprite.pos[1]:  #untenlinks
                            return [0, -self.speed[1]]
                        
         return False
         
    

       
            
    def wall_action(self):
        # ------- left edge ----
        if self.pos[0] < 0:
            if self.stop_on_edge:
                #self.move = [0, 0]
                self.pos[0] = 0
            elif self.warp_on_edge:
                self.pos[0] = Game.width 
            elif self.kill_on_edge:
                self.kill()
        # -------- upper edge -----
        if self.pos[1]  < 0:
            if self.stop_on_edge:
                #self.move = [0, 0]
                 self.pos[1] = 0
            elif self.warp_on_edge:
                self.pos[1] = -Game.height
            elif self.kill_on_edge:
                self.kill()
        # -------- right edge -----                
        if self.pos[0]  > Game.width:
            if self.stop_on_edge:
                #self.move = [0, 0]
                 self.pos[0] = Game.width
            elif self.warp_on_edge:
                self.pos[0] = 0
            elif self.kill_on_edge:
                self.kill()
        # --------- lower edge ------------
        if self.pos[1]   > Game.height:
            if self.stop_on_edge:
                #self.move = [0, 0]
                 self.pos[1] = Game.height
            elif self.warp_on_edge:
                self.pos[1] = 0
            elif self.kill_on_edge:
                self.kill()
                
                

                    
    def move_or_melee(self, mode, ammo, team=(0, 2), chance=0.07):
        self.move = [0, 0]
        if random.random() < chance:
            if mode == "near":
                self.move = self.direct_to_enemy(team)
            elif mode == "random":
                print("[ERROR]: Mode 'random' is available for move_func only")
                sys.exit()
                #self.move = self.get_random_direct()
            elif mode == "attack_cd":
                self.move = self.move_to_attack_cd(team)
                self.attack("cd", team, ammo)
            else:
                print("[ERROR]: Mode '{}' not found".format(mode))
                sys.exit()
            if self.move != False:
                pos1 = [self.pos[0]+self.move[0], self.pos[1]+self.move[1]]
                if is_figureFree(pos1) == True:
                  #  self.dodge()
                    self.move_act()
                    self.wall_action()
                else:
                    if random.random() < chance+0.5:
                        target = is_figureFree(pos1)
                        Melee_Attack(target)
                        Game.sounds["attack2"].play()
                    
    def move_func(self, mode, team=(0, 2), chance=0.07):
        self.move = [0, 0]
        if random.random() < chance:
            if mode == "near":
                self.move = self.direct_to_enemy(team)
            elif mode == "random":
                self.move = self.get_random_direct()
            else:
                print("[ERROR]: Mode '{}' is not available".format(mode))
                sys.exit()
            if self.move != False:
                pos1 = [self.pos[0]+self.move[0], self.pos[1]+self.move[1]]
                if is_figureFree(pos1) == True:
                    self.move_act()
                    self.wall_action()
        
                    
    def alive(self):
        if self.hp <= 0:
            self.kill()
                        
    
    def update(self):
        self.alive()
        target = self.collide([0, 3])
        if target != False:
            self.hp -= target.damage
            target.kill() 
        
    def overwrite_values(self):
        pass
        

class Attack(Figure):
    
    def __init__(self):
        Figure.__init__(self)
        self.damage = 100
        self.owner = None
        
    def act(self):
        pass
        
        
class Melee_Attack(Attack):
    
    def __init__(self, target, dm=random.randint(1, 10)):
        Attack.__init__(self)
        self.set_image()
        self.target = target
        self.damage = dm
        self.act()
        
    def act(self):
        self.target.hp -= self.damage
        print("Target HP: {}".format(self.target.hp))


class cd_Attack(Attack):
    
    def __init__(self):
        Attack.__init__(self)
        self.team = 3
        self.speed = [5, 10] 
        self.kill_on_edge = True
        self.bolmove = False
        
        
        
        
    def act(self):
        if self.direction == "r":
            self.move = [self.speed[0], 0]
        elif self.direction == "l":
            self.move = [-self.speed[0], 0]
            self.image = pygame.transform.flip(self.image0, True, True)
        elif self.direction == "o":
            self.move = [0, self.speed[1]]
            self.image = pygame.transform.rotate(self.image0, 270)
        elif self.direction == "u":
            self.move = [0, -self.speed[1]]
            self.image = pygame.transform.rotate(self.image0, 90)
        self.bolmove = True
        
    def update(self):
        if self.bolmove:
            self.wall_action()
            self.move_act()

        
class Spell_Knife(Attack):
    
    def __init__(self, owner, pos, direct, dm=random.randint(20, 30)):
        Attack.__init__(self)
        self.overwrite_values(owner, pos, direct, dm)
        self.set_image()
        self.act()
        
    def set_image(self):
        if self.image != None:
            self.image.convert_alpha()
            #self.image = pygame.transform.scale(self.bild, (200, 100))
            self.rect = self.image.get_rect()
            self.image0 = self.image.copy()
        else:
            self.image = pygame.Surface((1, 1))
        
        
    def overwrite_values(self, owner, pos, direct, dm):
        self.owner = owner
        self.team = 3
        self.pos = pos
        self.direction = direct
        self.damage = dm
        self.image = Game.images["spell_knife"]
        self.speed = [5, 10] 
        self.kill_on_edge = True
        self.bolmove = False 
        
    def act(self):
        if self.direction == "r":
            self.move = [self.speed[0], 0]
        elif self.direction == "l":
            self.move = [-self.speed[0], 0]
            self.image = pygame.transform.flip(self.image0, True, True)
        elif self.direction == "o":
            self.move = [0, self.speed[1]]
            self.image = pygame.transform.rotate(self.image0, 270)
        elif self.direction == "u":
            self.move = [0, -self.speed[1]]
            self.image = pygame.transform.rotate(Game.images["spell_knife"], 90)
        self.bolmove = True
        
    def update(self):
        if self.bolmove:
            self.wall_action()
            self.move_act()
            
            

class Tornado(Attack):   
    
    def __init__(self, owner, pos, direct, dm=random.randint(30, 40)):
        Attack.__init__(self)
        self.overwrite_values(owner, pos, direct, dm)
        self.set_image()
        self.act()
        
    def set_image(self):
        if self.image != None:
            self.image.convert_alpha()
            #self.image = pygame.transform.scale(self.bild, (200, 100))
            self.rect = self.image.get_rect()
            self.image0 = self.image.copy()
        else:
            self.image = pygame.Surface((1, 1))
        
        
    def overwrite_values(self, owner, pos, direct, dm):
        self.owner = owner
        self.team = 3
        self.pos = pos
        self.direction = direct
        self.damage = dm
        self.image = Game.anims_tornado[0]
        self.speed = [5, 10] 
        self.kill_on_edge = True
        self.bolmove = False 
        
    def act(self):
        if self.direction == "r":
            self.move = [self.speed[0], 0]
        elif self.direction == "l":
            self.move = [-self.speed[0], 0]
        elif self.direction == "o":
            self.move = [0, self.speed[1]]
        elif self.direction == "u":
            self.move = [0, -self.speed[1]]
        self.bolmove = True
        
    def update(self):
        self.animate(Game.anims_tornado, 5)
        if self.bolmove:
            self.wall_action()
            self.move_act()   
            
class Big_Cross(Attack):   
    
    def __init__(self, owner, pos, dm=random.randint(20, 40)):
        Attack.__init__(self)
        self.overwrite_values(owner, pos, dm)
        self.set_image()
        self.act()
        print(self.endpos)
        
        
        
    def overwrite_values(self, owner, pos, dm):
        self.owner = owner
        self.team = 3
        self.endpos = pos
        self.pos = [self.endpos[0], 0]
        self.damage = dm
        self.image = Game.images["big_cross"]
        self.speed = [5, 10] 
        self.kill_on_edge = True
        self.bolmove = False 
        self.sound = True
        
    def kill(self):
        self.lifetime += 1
        if self.sound:
            Game.sounds["big_cross_landing"].play()
            self.sound = False
        if self.lifetime >= 70:
            pygame.sprite.Sprite.kill(self)
        
    def act(self):
        if self.pos[1] == self.endpos[1]:
            self.kill()
            self.bolmove = False
        else:
            self.move = [0, self.speed[1]]
            self.bolmove = True
        
    def update(self):
        self.act()
        if self.bolmove:
            self.wall_action()
            self.move_act()   
            
            
class Wood_Cross(cd_Attack):
    
    def __init__(self, owner, pos, direct, dm=random.randint(20, 30)):
        cd_Attack.__init__(self)
        self.overwrite_values(owner, pos, direct, dm)
        self.set_image()
        self.act()
        
    def overwrite_values(self, owner, pos, direct, dm):
        self.owner = owner
        self.pos = pos
        self.direction = direct
        self.damage = dm
        self.image = Game.images["cross"]
        
    def act(self):
        if self.direction == "r":
            self.move = [self.speed[0], 0]
            self.image = pygame.transform.rotate(self.image0, 270)
        elif self.direction == "l":
            self.move = [-self.speed[0], 0]
            self.image = pygame.transform.rotate(self.image0, 90)
        elif self.direction == "o":
            self.move = [0, self.speed[1]]
        elif self.direction == "u":
            self.move = [0, -self.speed[1]]
            self.image = pygame.transform.rotate(self.image0, 180)
        self.bolmove = True
          
        
        


class Dummy(Figure):
    
    def __init__(self, pos=(0, 0), team=2, hp=100):
        Figure.__init__(self)
        self.overwrite_values(pos, team, hp)
        self.set_image()
        
    def overwrite_values(self, pos, team, hp):
        self.angle = "rechts"
        self.team = team
        self.hp = hp
        self.pos = pos
        self.image = Game.images["dummy"]
        
    def update(self):
        self.alive()
        target = self.collide([0, 3])
        if target != False:
            self.hp -= target.damage
            print("[Dummy]: HP at {})".format(self.hp))
            target.kill()
       
        
class Wizard1(Figure):
    
    def __init__(self):
        Figure.__init__(self)
        self.overwrite_values()
        self.set_image()
        self.image = pygame.transform.flip(self.image, True, False)
        self.controled = False
        
    def overwrite_values(self):
        self.angle = "rechts"
        self.pos = [675, 630]
        self.team = 1
        self.image = Game.images["wizard1"]
        self.stop_on_edge = True
        
    def alive(self):
        if self.hp <= 0:
            for group1 in Game.groups:
                for sprite in group1:
                    if sprite.team == self.team:
                        sprite.hp += 40
            self.kill()
            
        
    def update(self):
        self.alive()
        if self.controled != True:
            self.move_or_melee("attack_cd", "random_mage")
        target = self.collide([0, 3])
        if target != False:
            self.hp -= target.damage
            print("hit 1: {} hp left".format(self.hp))
            target.kill()
            
            
class Priest(Figure):
    
    def __init__(self):
        Figure.__init__(self)
        self.overwrite_values()
        self.set_image()
        self.controled = False
        
    def overwrite_values(self):
        self.angle = "rechts"
        self.pos = [150, 420]
        self.hp = 75
        self.team = 2
        self.image = Game.images["priest"]
        self.stop_on_edge = True
    
    def alive(self):
        if self.hp <= 0:
            grave = Grave(self, self.pos)
            self.kill()
        
    def update(self):
        self.alive()
        if self.controled != True:
            self.move_or_melee("attack_cd", "random_priest", (0, 1))
        target = self.collide([0, 3])
        if target != False:
            self.hp -= target.damage
            print("hit priest: {} hp left".format(self.hp))
            target.kill()

class Grave(Figure):
    
    def __init__(self, owner, pos):
        Figure.__init__(self)
        self.overwrite_values(pos, owner)
        self.set_image()
        
    def overwrite_values(self, pos, owner):
        self.pos = pos
        self.owner = owner
        self.team = self.owner.team
        self.image = Game.images["grave"]
        
    def update(self):
        self.alive()
        target = self.collide([0, 3])
        if target != False:
            self.hp -= target.damage
            print("hit grave: {} hp left".format(self.hp))
            target.kill()
        if self.lifetime >= 130:
            skeleton = Skeleton(self, self.pos)
            self.kill()
            
class Skeleton(Figure):
    
    def __init__(self, owner, pos):
        Figure.__init__(self)
        self.overwrite_values(owner, pos)
        self.set_image()
        
    def overwrite_values(self, owner, pos):
        self.pos = pos
        self.owner = owner
        self.team = self.owner.team
        self.targetteam = [0, 1, 2]
        self.targetteam.remove(self.team)
        self.image = Game.images["skeleton"]
        
    def update(self):
        self.alive()
        self.move_or_melee("near", "no", self.targetteam)
        self.wall_action()
        target = self.collide([0, 3])
        if target != False:
            self.hp -= target.damage
            print("hit priest: {} hp left".format(self.hp))
            target.kill()
        
                
        
class Wizard2(Figure):
    
    def __init__(self):
        Figure.__init__(self)
        self.overwrite_values()
        self.set_image()
        self.image = pygame.transform.flip(self.image, True, False)
        
    def overwrite_values(self):
        self.angle = "rechts"
        self.pos = [675, 0]
        self.team = 2
        self.image = Game.images["wizard1"]
        self.stop_on_edge = True
        
    def alive(self):
        if self.hp <= 0:
            for group1 in Game.groups:
                for sprite in group1:
                    if sprite.team == self.team:
                        sprite.hp += 40
            self.kill()
            
        
    def update(self):
        self.alive()
        self.move_or_melee("attack_cd", "spell_knife", (0, 1))
        target = self.collide([0, 3])
        if target != False:
            self.hp -= target.damage
            print("hit 2: {} hp left".format(self.hp))
            target.kill()
                
        
                  


class Game():
    width = 0
    height = 0
    images = {}
    sounds = {}
    teamcount = [1, 2, 3]
    #glfiguregroup = pygame.sprite.Group()
    
    def __init__(self, w=1200, h=700, fps=30):
        Game.width = w
        Game.height = h
        Game.fps = fps
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        set_icon("battleicon.bmp")
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        pygame.display.set_caption("KI-Battle")
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        
        self.load_bg("bg1.png")
        self.load_data()
        self.prepare_sprites()
        
    #maß pro feld: 75 70
        
    def load_data(self):
        # ---- images ----
        Game.images["wizard1"] = pygame.image.load(os.path.join("data", "wizard1.png")) 
        Game.images["dummy"] = pygame.image.load(os.path.join("data", "dummy.png"))
        Game.images["spell_knife"] = pygame.image.load(os.path.join("data", "spell_knife.png"))
        Game.images["priest"] = pygame.image.load(os.path.join("data", "priest.png"))
        Game.images["cross"] = pygame.image.load(os.path.join("data", "kreuz.png"))
        Game.images["big_cross"] = pygame.image.load(os.path.join("data", "grosses_kreuz.png"))
        Game.images["grave"] = pygame.image.load(os.path.join("data", "grab.png"))
        Game.images["skeleton"] = pygame.image.load(os.path.join("data", "skeleton.png"))
        Game.images["hud_wizard"] = pygame.image.load(os.path.join("data", "hud-base_wizard.png"))
        Game.images["hud_wizard"] = pygame.transform.scale(Game.images["hud_wizard"], (200, 64))
        
        # ---- animations ----
        Game.anims_tornado = [pygame.image.load(os.path.join("data", "tornado1.png")), pygame.image.load(os.path.join("data", "tornado2.png")),
                              pygame.image.load(os.path.join("data", "tornado3.png")), pygame.image.load(os.path.join("data", "tornado4.png"))]
        
        # ---- sounds ----
        Game.sounds["spell1"] = pygame.mixer.Sound(os.path.join("data", "spell1.wav"))
        Game.sounds["spell_wind"] = pygame.mixer.Sound(os.path.join("data", "spell_wind.wav"))
        Game.sounds["attack1"] = pygame.mixer.Sound(os.path.join("data", "attack1.wav"))
        Game.sounds["attack2"] = pygame.mixer.Sound(os.path.join("data", "attack2.wav"))
        Game.sounds["attack3"] = pygame.mixer.Sound(os.path.join("data", "attack3.wav"))
        Game.sounds["big_cross_landing"] = pygame.mixer.Sound(os.path.join("data", "big_cross_landing.wav"))
        
    def load_bg(self, bgim=None):
        try:
            if bgim != None:
                bgim1 = pygame.image.load(os.path.join("data", bgim))
                bgim1.set_colorkey((0, 0, 0))
                bgim1.convert_alpha()
                self.background.blit(bgim1, (0, 0))
            else:
                self.background.fill((255,255,255)) # hintergrund ist weiß
        except pygame.error:
            print("[ERROR]: image '{}' not found in data".format(bgim))
            self.background.fill((255,255,255)) # hintergrund ist weiß
            
    def prepare_sprites(self):
        # gruppe wo alles drin ist um gezeichnet zu werden
        self.allgroup = pygame.sprite.LayeredUpdates()
        # spezifische gruppen zum Testen
        self.figuregroup = pygame.sprite.Group()
        self.dummygroup = pygame.sprite.Group()
        self.attackgroup = pygame.sprite.Group()
        # ordnet klassen ihren gruppen zu
        Figure.groups = self.allgroup, self.figuregroup
        Attack.groups = self.allgroup, self.attackgroup
        Dummy.groups = self.allgroup, self.dummygroup
        #Wizard1.groups = self.allgroup, self.figuregroup
        #Dummy.groups =
        
        Game.groups = [self.figuregroup, self.dummygroup, self.attackgroup]
        Game.figuregroup = self.figuregroup
        
            
        
    def run(self):
        running = True
        player1_control = False
        player1_figure = 3
        player2_control = False
        player2_figure = 4
        self.wizard1 = Wizard1()   # 0
        self.priest = Priest()     # 1
        #self.wizard2 = Wizard2()
        while running:
            milliseconds = self.clock.tick(self.fps)
            self.screen.blit(self.background, (0, 0))
            
            if player1_figure == player2_figure:
                player2_figure += 1
                
            if player1_figure > 1:
                player1_figure = 0
                
            if player2_figure > 1:
                player2_figure = 0
            
            if player1_figure == 0:
                player1_figure = self.wizard1
            elif player1_figure == 1:
                player1_figure = self.priest
                
            if player2_figure == 0:
                player2_figure = self.wizard1
            elif player2_figure == 1:
                player2_figure = self.priest
            
            # ---- events ----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_p:
                        print("plus")
                        if player1_control == False:
                            player1_control = True
                        else:
                            player2_control = True
                    if player1_control:
                        player1_figure.controled = True

                        if event.key == pygame.K_LEFT:
                            player1_figure.pos[0] -= 75
                            if player1_figure.angle != "links":
                                player1_figure.image = pygame.transform.flip(player1_figure.image, True, False)
                                player1_figure.angle = "links"
                        if event.key == pygame.K_RIGHT:
                            player1_figure.pos[0] += 75
                            if player1_figure.angle != "rechts":
                                player1_figure.image = pygame.transform.flip(player1_figure.image, True, False)
                                player1_figure.angle = "rechts"
                        if event.key == pygame.K_UP:
                            player1_figure.pos[1] -= 70
                        if event.key == pygame.K_DOWN:
                            player1_figure.pos[1] += 70
                        
                        if player1_figure == self.wizard1:
                            player1_figure = 0
                        elif player1_figure == self.priest:
                            player1_figure = 1
                         
                        if event.key == pygame.K_RETURN:
                            player1_figure += 1

                        
                        
                    else:
                        player1_figure.controled = False
                        
                    
                    if player2_control:
                        player2_figure.controled = True
                        
                        
                        
                        if event.key == pygame.K_RETURN:
                            player2_figure += 1
                            
                    else:
                        player2_figure.controled = False
                        
            
            if player1_figure == self.wizard1:
                player1_figure = 0
            elif player1_figure == self.priest:
                player1_figure = 1 
                
            
            if player2_figure == self.wizard1:
                player2_figure = 0
            elif player2_figure == self.priest:
                player2_figure = 1   
                  
                        
            
            # ---- move figures ----
            for group1 in Game.groups:
                for sprite in group1:
                    sprite.update()
                
            # ---- collision detections ----

            
            # player - attacks
            
            
            # ---- deletes everything on screen ----
            self.screen.blit(self.background, (0, 0))
            
            
            write(self.screen, "hallo", x=50, y=100)
            
            # ---- hp bars ----
            # ~ self.bar1 = Bar(self.wizard1.hp, (0, 200, 0), 2)
            # ~ self.screen.blit(self.bar1.image, (10, 10))
            
            # ~ self.bar2 = Bar(self.priest.hp, (0, 200, 0), 2)
            # ~ self.screen.blit(self.bar2.image, (10, 40))
           # self.hud1.update()
            self.hud1 = Hud(Game.images["hud_wizard"], self.wizard1.hp)
            self.screen.blit(self.hud1.image, (10, 10))
            
            # ---- erzeugt alles in der allgroup, +1 lifetime ----
            for sprite in self.allgroup:
                self.screen.blit(sprite.image, sprite.pos)
                sprite.lifetime += 1
                
                
            
            # ---- update display ----
            pygame.display.flip()
            




game = Game()
game.run()
