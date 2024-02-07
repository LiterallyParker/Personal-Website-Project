
import random
import math
from colorama import Fore
from colorama import Back
import time
import os

commands_list = f'''\nCommands you can use:\n\n{Fore.BLUE}  Commands\n\n  {Fore.LIGHTBLACK_EX}(Your name){Fore.BLUE}{Fore.RED} / {Fore.BLUE}Inventory{Fore.RED} / {Fore.BLUE}Myself{Fore.RED} / {Fore.BLUE}Who Am I{Fore.RED} / {Fore.BLUE}Player\n\n  Inspect\n\n  Go {Fore.LIGHTBLACK_EX}(North, East, South, West){Fore.RED} / {Fore.BLUE}{Fore.LIGHTBLACK_EX}(n,e,s,w){Fore.BLUE}\n\n  Where am I{Fore.RED} / {Fore.BLUE}Where{Fore.RED} / {Fore.BLUE}Location\n\n  Pick Up{Fore.RED} / {Fore.BLUE}Get{Fore.RED} / {Fore.BLUE}Grab {Fore.LIGHTBLACK_EX}(Item){Fore.BLUE}\n\n  Eat {Fore.LIGHTBLACK_EX}(Item){Fore.BLUE}\n\n  Equip {Fore.LIGHTBLACK_EX}(Item){Fore.BLUE}\n\n  Attack{Fore.RED} / {Fore.BLUE}Hit{Fore.RED} / {Fore.BLUE}Stab{Fore.RED} / {Fore.BLUE}Kill {Fore.LIGHTBLACK_EX}(Sprite){Fore.RESET}\n'''

class Tile:
    def __init__(self,region,direction,color):
        self.id = 0 
        self.region = region
        self.direction = direction
        self.coords = [0,0]
        self.items = []
        self.sprites = []
        self.description = ""
        self.map_visual = "[ ]"
        self.n_false = False
        self.e_false = False
        self.s_false = False
        self.w_false = False
        self.color = color

    def remove_item(self,item):
        for i in self.items:
            if item == i:
                self.items.remove(i)
    def append_item(self,item):
        self.items.append(item)

    def __str__(self):
        string1 = "\n"
        if len(self.items) > 0:
            string1+="Items nearby:\n"
            for i in self.items:
                string1+=f"  {i}\n"
        string2 = "\n"
        if len(self.sprites) > 0:
            string2+=f"Sprites nearby:\n"
            for i in self.sprites:
                string2+=f"  {i}\n"
        return f'''{self.color}[{self.id}]{self.region}\n{self.description}{string1}{Fore.RESET}{self.color}{string2}\n{Fore.RESET}{60*"*"}\n'''
        
class Item:
    def __init__(self,name,color):
        self.color = color
        self.name = name
        self.type = ""
        self.ATT = 1
        self.price = 0
        self.cooked = False
        self.HP_gain = 0
        self.max_HP_gain = 0
        self.coat = False
    def __eq__(self, other):
        assert isinstance(other, Item)
        return self.name == other.name
    def calc_color(self):
        self.colored_name = self.color + self.name
    def __str__(self):
        self.calc_color()
        return self.colored_name

class Map:
    def __init__(self):
        self.tiles = []
        self.regions = ["Spawn\n","Forrest\n","Plains\n","Village\n","Farmland\n","Frozen Wasteland\n","Jungle\n","Caves\n","Deep Forrest\n"]
        self.directions = ["South West","West","North West","South","Center","North","South East","East","North East"]
        
    def fill_tiles(self):
        x = 0
        for region in self.regions:
            for direction in self.directions:
                self.tiles.append(Tile(region,direction,""))
        for i in range(len(self.tiles)):
            self.tiles[i].id = x
            x+=1
            if self.tiles[i].id in [5]:
                self.tiles[i].description+="You hear the birds. They chirp a tune of wonder and hope.\n\n"
            if self.tiles[i].id in [2]:
                self.tiles[i].description+="The leaves under your feet crunch with delight.\n\n"
            if self.tiles[i].id in [1]:
                self.tiles[i].description+="A smell of roses is in the air.\n\n"
            if self.tiles[i].id in [0]:
                self.tiles[i].description+="The sun shines through a clearing, the rays pass across\nyour arms.\n\n"
            if self.tiles[i].id in [3]:
                self.tiles[i].description+="A cool breeze hits you from the south, refreshing your soul.\n\n"
            if self.tiles[i].id in [6]:
                self.tiles[i].description+="You feel enlightened, and prepared for anything.\n\n"
            if self.tiles[i].id in [7]:
                self.tiles[i].description+="You hear the faint sound of civilization, and it gives you\npurpose.\n\n"
            if self.tiles[i].id in [8]:
                self.tiles[i].description+="...\n\n"
            if self.tiles[i].id in [0,1,2]:
                self.tiles[i].description+="The path west became too rocky.\n"
                self.tiles[i].w_false = True
            if self.tiles[i].id in [0,3,6]:
                self.tiles[i].description+="Going south will certainly freeze your bones.\n"
                self.tiles[i].s_false = True
            if self.tiles[i].id in [2,5,8]:
                self.tiles[i].description+="A forrest is just north of here.\n"
            if self.tiles[i].id in [6,7,8]:
                self.tiles[i].description+="The village is to your east.\n"
            if self.tiles[i].id in [18,21,24]:
                self.tiles[i].description+="The village is to your south.\n"
            if self.tiles[i].id in [18,19,20]:
                self.tiles[i].description+="A forrest is just east of here.\n"
            if self.tiles[i].id in [9,10,11]:
                self.tiles[i].description+="Something about going west feels dangerous...\n"
            if self.tiles[i].id in [15,16,17]:
                self.tiles[i].description+="An open field can be seen in the east.\n"
            if self.tiles[i].id in [27,30,33]:
                self.tiles[i].description+="The village's food grows south of here.\n"
            if self.tiles[i].id in [29,32,35]:
                self.tiles[i].description+="An open field can be seen in the north.\n"
            if self.tiles[i].id in [36,37,38]:
                self.tiles[i].description+="Going west will certainly freeze your bones.\n"
                self.tiles[i].w_false = True
            if self.tiles[i].id in [38,41,44]:
                self.tiles[i].description+="The village is to your north.\n"
            if self.tiles[i].id in [45,46,47]:
                self.tiles[i].description+="A thick and fruitful forrest is west of here.\n"
            if self.tiles[i].id in [51,52,53]:
                self.tiles[i].description+="The village's farmland can be seen in the east.\n"
            if self.tiles[i].id in [56,62]:
                self.tiles[i].description+="The path north becomes too rocky.\n"
                self.n_false = True
            if self.tiles[i].id in [59]:
                self.tiles[i].description+="There is a cave entrance north. A blast of putrid smelling\nair hits your nostrils.\n"
            if self.tiles[i].id in [60,61,62]:
                self.tiles[i].description+="Going east will certainly freeze your bones\n"
                self.e_false = True
            if self.tiles[i].id in [68]:
                self.tiles[i].description+="A cave exit leads north.\n"
            if self.tiles[i].id in [66]:
                self.tiles[i].description+="A cave exit leads south.\n"
            if self.tiles[i].id in [72,78]:
                self.tiles[i].description+="The path south becomes too rocky.\n"
                self.s_false = True
            if self.tiles[i].id in [75]:
                self.tiles[i].description+="There is a cave entrance south. A blast of putrid smelling\nair hits your nostrils.\n"
            if self.tiles[i].id in [78,79,80]:
                self.tiles[i].description+="The forrest gets more sparse going east.\n"
            if self.tiles[i].id in [11,14,17,20,23,26,74,77,80]:
                self.tiles[i].description+="The vast ocean can be seen for miles north of here.\n"
                self.tiles[i].n_false = True
            if self.tiles[i].id in [36,39,42,45,48,51,54,57,60]:
                self.tiles[i].description+="The ocean crashes against the shore on your south.\n"
                self.tiles[i].s_false = True
            if self.tiles[i].id in [24,25,26,33,35,42,43,44]:
                self.tiles[i].description+="Calm ocean waters paint the landscape to your east.\n"
                self.tiles[i].e_false = True
            if self.tiles[i].id in [34]:
                self.tiles[i].description+=f"Go west to exit.\nUse potions to gain Max HP or Increase your Attack.\nThe {Fore.YELLOW}Alchemist{Fore.BLACK} Awaits you..."
                self.tiles[i].e_false = True
                self.tiles[i].n_false = True
                self.tiles[i].s_false = True
            if self.tiles[i].id in [35]:
                self.tiles[i].s_false = True
            if self.tiles[i].id in [33]:
                self.tiles[i].n_false = True
            if self.tiles[i].id in [54,55,56,72,73,74]:
                self.tiles[i].description+="A mountain blocks your path west.\n"
                self.tiles[i].w_false = True
            if self.tiles[i].id in [65,64,63]:
                self.tiles[i].w_false = True
            if self.tiles[i].id in [4]:
                self.tiles[i].description+="Your adventure begins. A cool breeze washes over you.\nSunlight creeps up from the horizon. A new day begins.\n"
                self.tiles[i].description+="\nType 'Commands' at any point to view a list of commands you\ncan use. Feel free to figure them out on your own though!\n"
            if self.tiles[i].region == "Forrest\n":
                self.tiles[i].coords[1]+=3
                self.tiles[i].color=Fore.LIGHTGREEN_EX
            if self.tiles[i].region == "Plains\n":
                self.tiles[i].coords[0]+=3
                self.tiles[i].coords[1]+=3
                self.tiles[i].color=Fore.YELLOW
            if self.tiles[i].region == "Village\n":
                self.tiles[i].coords[0]+=3
                self.tiles[i].color=Fore.LIGHTBLACK_EX
            if self.tiles[i].region == "Farmland\n":
                self.tiles[i].coords[0]+=3
                self.tiles[i].coords[1]-=3
                self.tiles[i].color=Fore.LIGHTYELLOW_EX
            if self.tiles[i].region == "Frozen Wasteland\n":
                self.tiles[i].coords[1]-=3
                self.tiles[i].color=Fore.LIGHTBLUE_EX
            if self.tiles[i].region == "Jungle\n":
                self.tiles[i].coords[0]-=3
                self.tiles[i].coords[1]-=3
                self.tiles[i].color=Fore.GREEN
            if self.tiles[i].region == "Caves\n":
                self.tiles[i].coords[0]-=3
                self.tiles[i].color=Fore.BLACK
            if self.tiles[i].region == "Deep Forrest\n":
                self.tiles[i].coords[0]-=3
                self.tiles[i].coords[1]+=3
                self.tiles[i].color=Fore.CYAN
            if self.tiles[i].direction == "North":
                self.tiles[i].coords[1]+=1
            if self.tiles[i].direction == "East":
                self.tiles[i].coords[0]+=1
            if self.tiles[i].direction == "South":
                self.tiles[i].coords[1]-=1
            if self.tiles[i].direction == "West":
                self.tiles[i].coords[0]-=1
            if self.tiles[i].direction == "North West":
                self.tiles[i].coords[0]-=1
                self.tiles[i].coords[1]+=1
            if self.tiles[i].direction == "South West":
                self.tiles[i].coords[0]-=1
                self.tiles[i].coords[1]-=1
            if self.tiles[i].direction == "North East":
                self.tiles[i].coords[0]+=1
                self.tiles[i].coords[1]+=1
            if self.tiles[i].direction == "South East":
                self.tiles[i].coords[0]+=1
                self.tiles[i].coords[1]-=1
            
    def __str__(self):
        string = "\n"
        for i in [74,77,80]:
            string+=Fore.CYAN + f"{self.tiles[i].map_visual}"
        for i in [11,14,17]:
            string+=Fore.LIGHTGREEN_EX + f"{self.tiles[i].map_visual}"
        for i in [20,23,26]:
            string+=Fore.YELLOW + f"{self.tiles[i].map_visual}"
        string+="\n"
        for i in [73,76,79]:
            string+=Fore.CYAN + f"{self.tiles[i].map_visual}"
        for i in [10,13,16]:
            string+=Fore.LIGHTGREEN_EX + f"{self.tiles[i].map_visual}"
        for i in [19,22,25]:
            string+=Fore.YELLOW + f"{self.tiles[i].map_visual}"
        string+="\n"
        for i in [72,75,78]:
            string+=Fore.CYAN + f"{self.tiles[i].map_visual}"
        for i in [9,12,15]:
            string+=Fore.LIGHTGREEN_EX + f"{self.tiles[i].map_visual}"
        for i in [18,21,24]:
            string+=Fore.YELLOW + f"{self.tiles[i].map_visual}"
        string+="\n"
        for i in [65,68,71]:
            string+=Fore.BLACK + f"{self.tiles[i].map_visual}"
        for i in [2,5,8]:
            string+=Fore.RESET + f"{self.tiles[i].map_visual}"
        for i in [29,32,35]:
            string+=Fore.LIGHTBLACK_EX + f"{self.tiles[i].map_visual}"
        string+="\n"
        for i in [64,67,70]:
            string+=Fore.BLACK + f"{self.tiles[i].map_visual}"
        for i in [1,4,7]:
            string+=Fore.RESET + f"{self.tiles[i].map_visual}"
        for i in [28,31,34]:
            string+=Fore.LIGHTBLACK_EX + f"{self.tiles[i].map_visual}"
        string+="\n"
        for i in [63,66,69]:
            string+=Fore.BLACK + f"{self.tiles[i].map_visual}"
        for i in [0,3,6]:
            string+=Fore.RESET + f"{self.tiles[i].map_visual}"
        for i in [27,30,33]:
            string+=Fore.LIGHTBLACK_EX + f"{self.tiles[i].map_visual}"
        string+="\n"
        for i in [56,59,62]:
            string+=Fore.GREEN + f"{self.tiles[i].map_visual}"
        for i in [47,50,53]:
            string+=Fore.LIGHTBLUE_EX + f"{self.tiles[i].map_visual}"
        for i in [42,45,48]:
            string+=Fore.LIGHTYELLOW_EX + f"{self.tiles[i].map_visual}"
        string+="\n"
        for i in [55,58,61]:
            string+=Fore.GREEN + f"{self.tiles[i].map_visual}"
        for i in [46,49,52]:
            string+=Fore.LIGHTBLUE_EX + f"{self.tiles[i].map_visual}"
        for i in [41,44,47]:
            string+=Fore.LIGHTYELLOW_EX + f"{self.tiles[i].map_visual}"
        string+="\n"
        for i in [54,57,60]:
            string+=Fore.GREEN + f"{self.tiles[i].map_visual}"
        for i in [45,48,51]:
            string+=Fore.LIGHTBLUE_EX + f"{self.tiles[i].map_visual}"
        for i in [40,43,46]:
            string+=Fore.LIGHTYELLOW_EX + f"{self.tiles[i].map_visual}" + Fore.RESET
        string+=Back.RESET
        return string

class Sprite:
    def __init__(self,name,color):
        self.color = color
        self.name = name
        self.agro = False
        self.ATT = 2
        self.HP = 1
        self.alive = True
        self.items = []
        self.weapon = []
        self.coins = 0
        self.shop = False

    def __eq__(self, other):
        assert isinstance(other, Sprite)
        return self.name == other.name
    
    def agro_type(self):
        if self.agro:
            return "Agressive"
        else:
            return "Passive"
    
    def calc_color(self):
        self.colored_name = self.color + self.name

    def remove_item(self,item):
        for i in self.items:
            if item == i:
                self.items.remove(i)
    def append_item(self,item):
        self.items.append(item)
    def append_weapon(self,item):
        self.weapon.append(item)

    def calc_ATT(self):
        if len(self.weapon) > 0:
            self.ATT = self.weapon[0].ATT
        else:
            self.ATT = 2
    def equip(self,item):
        self.weapon.append(item)
        self.calc_ATT()

    def check_shop(self):
        string = ""
        if self.shop:
            string+=f"\n\n{Fore.LIGHTGREEN_EX}    Items for sale:\n"
            if len(self.items) > 0:
                for i in self.items:
                    string+=f"\n      {i}{Fore.RESET} - {i.price}"
            else:
                string = ""
        return string
            

    def __str__(self):
        self.calc_color()
        return self.colored_name + self.check_shop()

class Player():
    def __init__(self,color):
        self.name = input(f"Name?\n{Fore.YELLOW}")
        self.title_name = color + str.title(self.name)
        self.coords = [0,0]
        self.region = "Spawn"
        self.items = []
        self.HP = 1000
        self.ATT = 1
        self.max_HP = 20
        self.alive = True
        self.weapon = []
        self.coins = 1000
        self.coat = False

    def remove_item(self,item):
        for i in self.items:
            if item == i:
                self.items.remove(i)
    def append_item(self,item):
        self.items.append(item)
        self.weapon.append(item)

    def calc_ATT(self):
        if len(self.weapon) > 0:
            self.ATT = self.weapon[0].ATT
        else:
            self.ATT = 1
    def equip(self,item):
        self.weapon.append(item)
        self.items.remove(item)
        self.calc_ATT()
    def unequip(self):
        x = self.weapon.pop()
        self.items.append(x)
        self.calc_ATT()

    def equipped_string(self):
        string = ""
        if len(self.weapon) > 0:
            string = f"\nEquipped Weapon:\n  {self.weapon[0]}{Fore.RESET}\n"
        return string
    def items_string(self):
        string = ""
        if len(self.items) > 0:
            string+="\nInventory:\n"
            for i in self.items:
                string+=f"  {i}{Fore.RESET}\n"
        return string
    def __str__(self):
        return f'''\n{self.title_name}{Fore.RESET}\nHP: {self.HP}\nATT: {self.ATT}\nCoins: {self.coins}\n{self.items_string()}{self.equipped_string()}\n{60*"*"}'''

class Game:
    def __init__(self): 
        self.player = Player(Fore.YELLOW)
        self.map = Map()
        self.map.fill_tiles()
        self.item_names = ["Weak Potion","Buff Potion","Steel Potion","Apple","Beef","Lettuce","Tomato","Bread","Potato","Stick","Metal Rod","Rusty Sword","Iron Sword","Steel Sword","Goblin's Sword","Knight's Sword","Hero's Sword","Hammer","Shovel","Crowbar","Snow Coat"]
        self.item_library = []
        self.sprite_names = ["Dummy","Goblin","Whisp","Imp","Traveling Merchant","Farmer","Alchemist"]
        self.sprite_library = []
        for i in self.item_names:
            self.item_library.append(self.create_item(i))
        for i in self.sprite_names:
            self.sprite_library.append(self.create_sprite(i))
        self.player_input = ""
        self.output = "\n"
        self.game_over = False

# misc commands
    def create_sprite(self,name):
        sprite = Sprite("null","")
        for i in self.sprite_names:
            if name == i:
                sprite = Sprite(name,"")
                if sprite.name == "Dummy":
                    sprite.HP = 100000
                    sprite.color+=Fore.BLACK
                    sprite.calc_color()
                if sprite.name == "Goblin":
                    sprite.agro = True
                    sprite.HP = 50
                    sprite.coins = random.randrange(100,150)
                    sprite.color+=Fore.GREEN
                    sprite.equip(self.create_item("Goblin's Sword"))
                    if random.randrange(100) > 90:
                        sprite.items.append("Buff Potion")
                if sprite.name == "Whisp":
                    sprite.agro = True
                    sprite.HP = 5
                    sprite.coins = random.randrange(5,10)
                    sprite.color+=Fore.LIGHTMAGENTA_EX
                if sprite.name == "Imp":
                    sprite.agro = True
                    sprite.HP = 10
                    sprite.coins = random.randrange(10,20)
                    sprite.color+=Fore.CYAN
                    sprite.equip(self.create_item("Rusty Sword"))
                if sprite.name == "Traveling Merchant":
                    sprite.HP = 10
                    sprite.color+=Fore.BLUE
                    sprite.shop = True
                    sprite.items.append(self.create_item("Beef"))
                    sprite.items.append(self.create_item("Bread"))
                    sprite.items.append(self.create_item("Hammer"))
                    if self.player.coat == False:
                        sprite.items.append(self.create_item("Snow Coat"))
                    else:
                        sprite.items.append(self.create_item("Iron Sword"))
                if sprite.name == "Farmer":
                    sprite.HP = 10
                    sprite.color+=Fore.RED
                    sprite.shop = True
                    sprite.items.append(self.create_item("Tomato"))
                    sprite.items.append(self.create_item("Lettuce"))
                    sprite.items.append(self.create_item("Potato"))
                if sprite.name == "Alchemist":
                    sprite.HP = 100
                    sprite.color+=Fore.YELLOW
                    sprite.shop = True
                    sprite.items.append(self.create_item("Weak Potion"))
                    sprite.items.append(self.create_item("Buff Potion"))
                    sprite.items.append(self.create_item("Steel Potion"))
        return sprite
    def create_item(self,name):
        item = Item("null",Fore.RESET)
        for i in self.item_names:
            if name == i:
                item = Item(name,Fore.RESET)
                if item.name == "Weak Potion":
                    item.color = Fore.CYAN
                    item.type = "potion"
                    item.price = 25
                    item.max_HP_gain = 10
                if item.name == "Buff Potion":
                    item.color = Fore.CYAN
                    item.type = "potion"
                    item.price = 150
                    item.max_HP_gain = 20
                if item.name == "Steel Potion":
                    item.color = Fore.CYAN
                    item.type = "potion"
                    item.price = 250
                    item.max_HP_gain = 50
                if item.name == "Snow Coat":
                    item.color = Fore.LIGHTBLUE_EX
                    item.type = "coat"
                    item.price = 25
                    item.coat = True
                if item.name == "Apple":
                    item.color = Fore.RED
                    item.type = "food"
                    item.HP_gain = 3
                    item.price = 2
                if item.name == "Beef":
                    item.color = Fore.RED
                    item.type = "food"
                    item.HP_gain = 5
                    item.price = 5
                if item.name == "Lettuce":
                    item.color = Fore.RED
                    item.type = "food"
                    item.HP_gain = 5
                    item.price = 7
                if item.name == "Tomato":
                    item.color = Fore.RED
                    item.type = "food"
                    item.HP_gain = 10
                    item.price = 10
                if item.name == "Bread":
                    item.color = Fore.RED
                    item.type = "food"
                    item.HP_gain = 20
                    item.price = 15
                if item.name == "Potato":
                    item.color = Fore.RED
                    item.type = "food"
                    item.HP_gain = 15
                    item.price = 10
                if item.name == "Stick":
                    item.color = Fore.MAGENTA
                    item.type = "weapon"
                    item.ATT = 2
                    item.price = 2
                if item.name == "Metal Rod":
                    item.color = Fore.MAGENTA
                    item.type = "weapon"
                    item.ATT = 4
                    item.price = 5
                if item.name == "Rusty Sword":
                    item.color = Fore.MAGENTA
                    item.type = "weapon"
                    item.ATT = 6
                    item.price = 15
                if item.name == "Iron Sword":
                    item.color = Fore.MAGENTA
                    item.type = "weapon"
                    item.ATT = 10
                    item.price = 35
                if item.name == "Steel Sword":
                    item.color = Fore.MAGENTA
                    item.type = "weapon"
                    item.ATT = 20
                    item.price = 50
                if item.name == "Goblin's Sword":
                    item.color = Fore.MAGENTA
                    item.type = "weapon"
                    item.ATT = 26
                    item.price = 70
                if item.name == "Knight's Sword":
                    item.color = Fore.MAGENTA
                    item.type = "weapon"
                    item.ATT = 36
                    item.price = 100
                if item.name == "Hero's Sword":
                    item.color = Fore.MAGENTA
                    item.type = "weapon"
                    item.ATT = 50
                    item.price = 175
                if item.name == "Hammer":
                    item.color = Fore.MAGENTA
                    item.type = "weapon"
                    item.ATT = 10
                    item.price = 10
                if item.name == "Shovel":
                    item.color = Fore.MAGENTA
                    item.type = "weapon"
                    item.ATT = 10
                    item.price = 10
                if item.name == "Crowbar":
                    item.color = Fore.MAGENTA
                    item.type = "weapon"
                    item.ATT = 10
                    item.price = 10
        return item
    def player_tile(self):
        for i in range(len(self.map.tiles)):
            if self.player.coords == self.map.tiles[i].coords:
                x = self.map.tiles[i]
                self.map.tiles[i].map_visual = "[X]"
                return x
    def player_has(self,name):
        player_has = []
        for i in self.player.items:
            for j in self.item_names:
                if i.name == j:
                    player_has.append(j)
        if name in player_has:
            return True
        else:
            return False
    def input_item(self):
        x = self.create_item("null")
        for item in self.item_library:
            if str.lower(item.name) in self.player_input:
                x = item
        return x
    def input_sprite(self):
        x = self.create_sprite("null")
        for sprite in self.sprite_library:
            if str.lower(sprite.name) in self.player_input:
                x = sprite
        return x
    def spawn_whisp(self):
        if random.randrange(20) > 17 and self.player_tile().id in range(0,9):
            self.player_tile().sprites.append(self.create_sprite("Whisp"))
    def spawn_imp(self):
        if random.randrange(20) > 17 and self.player_tile().id in range(9,18):
            self.player_tile().sprites.append(self.create_sprite("Imp"))
    def spawn_goblin(self):
        if random.randrange(20) > 17 and self.player_tile().id in range(63,72):
            self.player_tile().sprites.append(self.create_sprite("Goblin"))
    def spawn_traveling_merchant(self):
        if random.randrange(10) > 7 and self.player_tile().id in range(27,36):
            self.player_tile().sprites.append(self.create_sprite("Traveling Merchant"))
    def spawn_farmer(self):
        if random.randrange(10) > 7 and self.player_tile().id in range(36,45):
            self.player_tile().sprites.append(self.create_sprite("Farmer"))

    def despawn_traveling_merchant(self):
        if len(self.player_tile().sprites) > 0:
            if self.player_tile().sprites[0].name == "Traveling Merchant":
                self.player_tile().sprites.pop()
    def despawn_farmer(self):
        if len(self.player_tile().sprites) > 0:
            if self.player_tile().sprites[0].name == "Farmer":
                self.player_tile().sprites.pop()

# player input commands
    def equip(self):
        if "equip" in self.player_input:
            if self.input_item().name != "null":
                if self.input_item() in self.player.items:
                    if self.input_item().type == "coat":
                        self.player.items.remove(self.input_item())
                        self.player.coat = True
                        self.output+=f"You are now wearing the {self.input_item()}{Fore.RESET}.\n"
                        for i in [0,3,6]:
                            self.map.tiles[i].description = "A Frozen Wasteland lie south of this road.\n"
                            self.map.tiles[i].s_false = False
                        for i in [36,37,38]:
                            self.map.tiles[i].description = "A Frozen Wasteland lie west of this road.\n"
                            self.map.tiles[i].w_false = False
                        for i in [60,61,62]:
                            self.map.tiles[i].description = "A Frosen Wastland lie east of this road.\n"
                            self.map.tiles[i].e_false = False
                    else:
                        if len(self.player.weapon) == 0:
                            self.player.equip(self.input_item())
                            self.output+=f"{self.player}\nYou equipped {self.input_item()}{Fore.RESET}.\n"
                        else:
                            self.player.unequip()
                            self.equip()
                else:
                    self.output+="You don't have that.\n"
            else:
                self.output+="Item does not exist.\n"
    def print_map(self):
        if "map" in self.player_input:
            self.output+=f"{self.map}\n"
    def inspect(self):
        if "inspect" in self.player_input:
            string = ""
            if len(self.player_tile().items) > 0:
                string+=f"Items nearby:\n\n"
                for i in self.player_tile().items:
                    string+=f"{i}{Fore.RESET} - {str.title(i.type)}"
                    if i.type == "weapon":
                        string+=f"\n  Attack: {i.ATT}\n  Value: {i.price} Coins\n"
                    if i.type == "food":
                        string+=f"\n  Health gain: {i.HP_gain}\n  Value: {i.price} Coins\n"
            if len(self.player_tile().sprites) > 0:
                string+=f"\nSprites nearby:\n\n{self.player_tile().sprites[0]}{Fore.RESET} - {self.player_tile().sprites[0].agro_type()}\n  Health: {self.player_tile().sprites[0].HP}\n  Attack: {self.player_tile().sprites[0].ATT}\n"
                
            self.output+=string
    def player_location(self):
        if "where" in self.player_input or "location" in self.player_input:
            self.output+=f"\n{self.player_tile()}{self.map}\n"
    def about_player(self):
        if str.lower(self.player.name) in self.player_input or "about me" in self.player_input or "player" in self.player_input or "inventory" in self.player_input or "myself" in self.player_input or "who am i" in self.player_input:
            self.output+=f"{self.player}"
    def move(self):
        options = ["go n","go e","go s","go w","go north","go east","go south","go west","n","e","s","w","north","east","south","west"]
        if self.player_input in options:
            if options[0] in self.player_input or options[4] in self.player_input or options[8] in self.player_input or options[12] in self.player_input:
                if self.player_tile().n_false == False:
                    self.player_tile().map_visual = "[ ]"
                    self.player.coords[1]+=1
                    self.output+="\nYou went north.\n"
                    if len(self.player_tile().sprites) < 1:
                        self.spawn_whisp()
                        self.spawn_imp()
                        self.spawn_goblin()
                        self.spawn_traveling_merchant()
                        self.spawn_farmer()
                    else:
                        self.despawn_traveling_merchant()
                        self.despawn_farmer()
                    self.output+=str(f"\n{self.player_tile()}")
                else:
                    self.reset_output
                    self.output+="Can't go that way.\n"
            if options[1] in self.player_input or options[5] in self.player_input or options[9] in self.player_input or options[13] in self.player_input:
                if self.player_tile().e_false == False:
                    self.player_tile().map_visual = "[ ]"
                    self.player.coords[0]+=1
                    self.output+="\nYou went east.\n"
                    if len(self.player_tile().sprites) < 1:
                        self.spawn_whisp()
                        self.spawn_imp()
                        self.spawn_goblin()
                        self.spawn_traveling_merchant()
                        self.spawn_farmer()
                    else:
                        self.despawn_traveling_merchant()
                        self.despawn_farmer()
                    self.output+=str(f"\n{self.player_tile()}")
                else:
                    self.reset_output
                    self.output+="Can't go that way.\n"
            if options[2] in self.player_input or options[6] in self.player_input or options[10] in self.player_input or options[14] in self.player_input:
                if not self.player_tile().s_false:
                    self.player_tile().map_visual = "[ ]"
                    self.player.coords[1]-=1
                    self.output+="\nYou went south.\n"
                    if len(self.player_tile().sprites) < 1:
                        self.spawn_whisp()
                        self.spawn_imp()
                        self.spawn_goblin()
                        self.spawn_traveling_merchant()
                        self.spawn_farmer()
                    else:
                        self.despawn_traveling_merchant()
                        self.despawn_farmer()
                    self.output+=str(f"\n{self.player_tile()}")
                else:
                    self.reset_output
                    self.output+="Can't go that way.\n"
            if options[3] in self.player_input or options[7] in self.player_input or options[11] in self.player_input or options[15] in self.player_input:
                if self.player_tile().w_false == False:
                    self.player_tile().map_visual = "[ ]"
                    self.player.coords[0]-=1
                    self.output+="\nYou went west.\n"
                    if len(self.player_tile().sprites) < 1:
                        self.spawn_whisp()
                        self.spawn_imp()
                        self.spawn_goblin()
                        self.spawn_traveling_merchant()
                        self.spawn_farmer()
                    else:
                        self.despawn_traveling_merchant()
                        self.despawn_farmer()
                    self.output+=str(f"\n{self.player_tile()}")
                else:
                    self.reset_output
                    self.output+="Can't go that way.\n"
    def pick_up(self):
        if "pick up" in self.player_input or "get" in self.player_input or "grab" in self.player_input:
            if self.input_item().name != "null":
                for i in self.player_tile().items:
                    if self.input_item() == i:
                        self.player.items.append(i)
                        self.player_tile().items.remove(i)
                        self.output+=f"{self.player}\nYou picked up {i}{Fore.RESET}.\n"
                    else:
                        self.output+="Item isn't here.\n"
            else:
                self.output+="Item does not exist.\n"
    def list_commands(self):
        if "commands" in self.player_input:
            self.output+=commands_list
    def eat(self):
        if "eat" in self.player_input:
            if self.input_item().name != "null":
                if self.input_item() in self.player.items:
                    if self.input_item().type == "food":
                        if self.player.HP < self.player.max_HP - self.input_item().HP_gain:
                            self.player.items.remove(self.input_item())
                            self.player.HP += self.input_item().HP_gain
                            self.output+=f"\nYou ate the {self.input_item()}.\nIt gave you {self.input_item().HP_gain} HP.\n"
                        elif self.player.HP < self.player.max_HP:
                            self.player.items.remove(self.input_item())
                            self.player.HP = self.player.max_HP
                            self.output+=f"\nYou ate the {self.input_item()}.\nYou are now at max HP: {self.player.max_HP}\n"
                        else:
                            self.output+="\nYou are at max HP. Save it for later!\n"
                    else:
                        self.output+="\nThat would hurt.\n"
                else:
                    self.output+="\nYou don't have that.\n"
            else:
                self.output+="\nItem doesn't exist.\n"
    def drink(self):
        if "drink" in self.player_input:
            if self.input_item().name != "null":
                if self.input_item() in self.player.items:
                    if self.input_item().type == "potion":
                        self.player.items.remove(self.input_item())
                        self.player.max_HP+=self.input_item().max_HP_gain
                        self.output+=f"\nYou gained {self.input_item().max_HP_gain} max health!\n"
                        self.player.HP = self.player.max_HP
                        self.output+=f"You are now at max health.\n{self.player}"
                    else:
                        self.output+="\nDrink a solid? Really?\n"
                else:
                    self.output+="\nYou don't have that.\n"
            else:
                self.output+="\nItem doesn't exist.\n"
    def attack(self):
        if "attack" in self.player_input or "hit" in self.player_input or "stab" in self.player_input or "kill" in self.player_input:
            if self.input_sprite().name != "null":
                if self.input_sprite() in self.player_tile().sprites:
                    self.player_tile().sprites[0].HP -= self.player.ATT
                    if self.player_tile().sprites[0].HP > 0:
                        if len(self.player.weapon) > 0:
                            if "Sword" in self.player.weapon[0].name:
                                self.output+=f"\nYou used The {self.player.weapon[0]}{Fore.RESET} to slash the {self.player_tile().sprites[0]}{Fore.RESET} for {self.player.ATT} damage!\n{self.player_tile().sprites[0]}'s{Fore.RESET} HP: {self.player_tile().sprites[0].HP}\n"
                        else:
                            self.output+=f"\nYou hit the {self.player_tile().sprites[0]}{Fore.RESET} for {self.player.ATT} damage!\n{self.player_tile().sprites[0]}'s{Fore.RESET} HP: {self.player_tile().sprites[0].HP}\n"
                        if self.player_tile().sprites[0].agro:
                            x = self.player_tile().sprites[0].ATT
                            if x > 10:
                                x = random.randrange(x - 10, x)
                            self.player.HP-=x
                            if self.player.HP <= 0:
                                self.output+=f"\nThe {self.player_tile().sprites[0]}{Fore.RESET} hit you back for {x} damage!\n"
                                self.player.alive = False
                            else:
                                self.output+=f"\nThe {self.player_tile().sprites[0]}{Fore.RESET} hit you back for {x} damage!\nYour HP: {self.player.HP}\n"
                            
                    else:
                        self.output+=f"\nYou killed the {self.player_tile().sprites[0]}{Fore.RESET}.\n"
                        if self.player_tile().sprites[0].coins > 0:
                            x = self.player_tile().sprites[0].coins
                            self.player.coins+=x
                            self.output+=f"You gained {x} coins!\n"
                        if len(self.player_tile().sprites[0].items) > 0:
                            x = self.player_tile().sprites[0].items.pop()
                            self.player_tile().items.append(x)
                            self.output+=f"The {self.player_tile().sprites[0]}{Fore.RESET} dropped the {x}{Fore.RESET}.\n"
                        if len(self.player_tile().sprites[0].weapon) > 0:
                            if random.randrange(0,10) > 7:
                                x = self.player_tile().sprites[0].weapon.pop()
                                self.player_tile().items.append(x)
                                self.output+=f"The {self.player_tile().sprites[0]}{Fore.RESET} dropped the {x}{Fore.RESET}.\n"
                        self.player_tile().sprites.pop()
                else:
                    self.output+="\nTarget isn't here.\n"
            else:
                self.output+="\nInvalid target.\n  ATTACK (TARGET)\n"
    def buy(self):
        if "buy" in self.player_input or "purchase" in self.player_input:
            if len(self.player_tile().sprites) > 0 and self.player_tile().sprites[0].shop:
                if self.input_item() in self.player_tile().sprites[0].items and self.input_item().name != "null":
                    if self.input_item().price <= self.player.coins:
                        self.player_tile().sprites[0].items.remove(self.input_item())
                        self.player.items.append(self.input_item())
                        self.player.coins-=self.input_item().price
                        self.output+=f"\nYou bought the {self.input_item()}{Fore.RESET}!\nYou have {str(self.player.coins)} coins.\n\n{self.player_tile().sprites[0]}{Fore.RESET}\n"
                    else:
                        self.output+=f"\nNot Enough Coins!\nYou have {str(self.player.coins)} coins.\n\n{self.player_tile().sprites[0]}{Fore.RESET}\n"
                else:
                    self.output+=f"\nThe {self.player_tile().sprites[0].color}{self.player_tile().sprites[0].name}{Fore.RESET} doesn't have that.\n\n{self.player_tile().sprites[0]}{Fore.RESET}\n"
            else:
                self.output+="\nFind a Seller...\n"
    def sell(self):
        if "sell" in self.player_input:
            if len(self.player_tile().sprites) > 0 and self.player_tile().sprites[0].shop:
                if self.input_item() in self.player.items and self.input_item().name != "null":
                    self.player.items.remove(self.input_item())
                    self.player.coins+=self.input_item().price
                    self.output+=f"\nYou sold the {self.input_item()}{Fore.RESET}.\nCoins: {self.player.coins}\n\n{self.player_tile().sprites[0]}{Fore.RESET}\n"
                else:
                    self.output+=f"\nYou don't have that.\n\n{self.player_tile().sprites[0]}{Fore.RESET}\n"
            else:
                self.output+=f"\nFind a Buyer...\n"

# reset for the next command
    def reset_input(self):
        self.player_input = str.lower(input(f"What do you want to do?\n{60*"*"}\n"))
    def reset_output(self):
        self.output=f"\n{Fore.RED}{60*"#"}{Fore.RESET}\n"
    def reset(self):
        self.reset_input()
        self.reset_output()
    def check_game_over(self):
        if self.player.alive == False:
            self.game_over = True
            self.output+=f"{Fore.RED}{60*("X")}\n\nYou have died.\n\n{60*"X"}{Fore.RESET}"
    def check_allow_movement(self):
        if len(self.player_tile().sprites) < 1:
            self.move()
        elif not self.player_tile().sprites[0].agro:
            self.move()
        elif self.player_tile().sprites[0].agro:
            self.output += f"{Fore.RED}\nCannot move when hostiles are near!\n\n{Fore.RESET}{self.player_tile()}"

    def play(self):
        self.map.tiles[4].items.append(self.create_item("Apple"))
        self.map.tiles[4].items.append(self.create_item("Knight's Sword"))
        self.map.tiles[6].items.append(self.create_item("Apple"))
        self.map.tiles[0].items.append(self.create_item("Apple"))
        self.map.tiles[4].sprites.append(self.create_sprite("Dummy"))
        self.map.tiles[34].region = f"{Fore.MAGENTA}Potions Shop{Fore.BLACK}\n"
        self.map.tiles[34].sprites.append(self.create_sprite("Alchemist"))
        print(f"\n{Fore.RESET}Your name is {self.player.title_name}{Fore.RESET}.\nYou are an adventurer in seek of Eternal Glory.\n")
        print(self.player)
        print(self.player_tile())
        self.reset()
        while self.game_over == False:
            if type(self.player_input) == str:

                self.player_tile()          # initiates X on the map

                self.pick_up()              #
                self.buy()
                self.sell()
                self.inspect()
                self.print_map()            # command options the player can use
                self.about_player()         #
                self.player_location()      #
                self.list_commands()        #
                self.equip()                #
                self.eat()                  #
                self.drink()
                self.attack()
                self.check_allow_movement() #

                self.check_game_over()
                os.system("cls")
                print(self.output)          # prints output after each command
                if self.game_over == False:
                    self.reset()            # resets output and input
os.system('cls')
Gork = Game()
Gork.play()