from game import location
import game.config as config
from game.display import announce
from game import event
import game.combat as combat
import random
import game.items as items


class KyleIsland(location.Location):

    def __init__(self, x, y, world):
        super().__init__(x, y ,world)
        self.name = "Kyles Island"
        self.symbol = 'I'
        self.visitable = True
        self.starting_location = LandWithShip(self)
        self.locations = {}

        self.locations["southSide"] = self.starting_location
        self.locations["northSide"] = NorthSide(self)
        self.locations["eastSide"] = EastSide(self)
        self.locations["westSide"] = WestSide(self)

        self.locations["bridge"] = Bridge(self)
       


    def enter (self, ship):
        announce("You've finally struck land after a long journey overseas.")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class LandWithShip (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "southSide"
        self.verbs['north'] = self 
        self.verbs['south'] = self 
        self.verbs['west'] = self 
        self.verbs['east'] = self
        self.event_chance = 100
        self.events.append(Winter())
        self.events.append(GunPowder())
        

    def enter(self):
        announce ("You have made it to a secret Island that has many dangers on it!\n" +
                  "The ship you arrived on is stationed on the south side of the Island.\n" +
                  "Gather as much material as you can to survive your time on Kyle's Island!!")
        #self.main_location.firewood += 1
    def process_verb (self, verb, cmd_list, nouns):
         if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
         elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["bridge"]
         elif (verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations[f"{verb}Side"]


class NorthSide (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "northSide"
        self.event_chance = 100
        self.events.append(Heat())
        self.events.append(DryWood())

    def enter(self):
        announce("You get to the north side of the island and are exposed to extreme heat and there is no water to drink on this side !")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["bridge"]
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["eastSide"]
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["westSide"]
        

class EastSide (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "eastSide"
        self.event_chance = 50
        self.events.append(ManEatingWolves())

    def enter(self):
        announce("You have now entered the east side of the Island BEWARE OF DANGER")
        
    def process_verb (self, verb, cmd_list, nouns):
            if (verb == "west"):
                config.the_player.next_loc = self.main_location.locations["bridge"]
            if (verb == "south"):
                config.the_player.next_loc = self.main_location.locations["southSide"]
            if (verb == "north"):
                config.the_player.next_loc = self.main_location.locations["northSide"]

class WestSide (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "westSide"
        self.event_chance = 100
        self.events.append(Storm())
    def enter(self):
        announce("You have now entered the west side of the Island where there is no shelter for you")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["bridge"]
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["southSide"]
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["northSide"]

class Bridge (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "bridge"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 100
        self.events.append(BossBattle())
    def enter(self):
        announce("You walk through the side of the island you are on and come across a bridge that connects all the sides on the island together")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east" or verb == "west" or verb == "north" or verb == "south"):
            config.the_player.next_loc = self.main_location.locations[f"{verb}Side"]

class Wolf(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(50,70), (20,30)]
        #75 to 90 hp, bite attack, 160 to 200 speed (100 is "normal")
        super().__init__(name, random.randrange(75,90), attacks, 130 + random.randrange(-20,21))

class ManEatingWolves (event.Event):
    '''
    A combat encounter with a pack of hungry wolves.
    When the event is drawn, creates a combat encounter with 4 to 8 wolves, kicks control over to the combat code to resolve the fight.
    The wolves are "edible", which is modeled by increasing the ship's food by 3 per monkey appearing and adding an apropriate message to the result.
    '''

    def __init__ (self):
        self.name = " wolf attack"

    def process (self, world):
        result = {}
        result["message"] = "the wolves are defeated!... They look pretty tasty and they can also provide shelter materials!"
        monsters = []
        n_appearing = random.randrange(4,8)
        n = 1
        while n <= n_appearing:
            monsters.append(Wolf("Man-eating Wolf "+str(n)))
            n += 1
        announce ("The crew is attacked by a pack of man-eating wolves!")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        
        config.the_player.ship.food += n_appearing*3
        config.the_player.ship.shelter += n_appearing 

        return result   
class Winter(event.Event):
    def __init__ (self):
        self.name = "a random member of the ship gets hypothermia"

    def process (self, world):
        ''' A random crew member gets hypothermia and takes damage... Unless the pirates have firewood !
        '''
        p = random.choice(config.the_player.get_pirates())
        result = {}
        if config.the_player.ship.firewood >= 5:
            config.the_player.ship.firewood -= 5
            result["message"] = " you use up 5 blocks of firewood to start a fire and avoid sickness "
            result["newevents"] = [ self ]
        else:
            damage = 15
            deathcause = "froze to death"
            died = p.inflict_damage (damage, deathcause)
            if(died is not None):
                result["message"] = p.get_name() + " got very sick from hypothermia and is now dead" 
                result["newevents"] = [ self ]
            else:
                result["message"] = p.get_name() + "took 15 damage from the freezing temperatures !"
                result["newevents"] = [ self ]
        return result

class Storm(event.Event):
    def __init__(self):
        self.name = "A storm comes after you arrive on the island"
    def process(self, world):
        '''A raondom crew member takes damage from the storm... unless the pirates have shelter !'''
        announce(" The pirates get caught in a rain storm !")
        config.the_player.ship.water += 5
        announce("5 water has been added to your inventory!")
        p = random.choice(config.the_player.get_pirates())
        result = {}
        if config.the_player.ship.shelter >=5:
            config.the_player.ship.shelter -= 5
            result["message"] = " 5 large branches are used to set up shelter" 
            result["newevents"] = [ self ]
        else:
            p.set_sickness (True)
            result["message"] = p.get_name() + " gets deathly ill from the rain storm !"
            result["newevents"] = [ self ]
        return result
    
class Heat(event.Event):
    def __init__(self):
        self.name = "Extreme heat fills this side of the island"

    def process (self, world):
        ''' A crew memeber gets heat exaustion and starts to take damage... counter by drinking water'''
        p = random.choice(config.the_player.get_pirates())
        result = {}
        if config.the_player.ship.water >=3:
            config.the_player.ship.water -= 3
            result["message"] = "you drink 3 water supplies in order to avoid heat exhaustion."
            result["newevents"] = [ self ]
        else:
            damage = 10
            deathcause = "extreme heat exhaustion"
            died = p.inflict_damage (damage, deathcause)
            if(died is not None):
                result["message"] = p.get_name() + " suffered from extreme heat and has now died from it"
                result["newevents"] = [ self ]
            else:
                result["message"] = p.get_name() + " has taken 10 damage from the high rising temperatures"
                result["newevents"] = [ self ]
        return result
class DryWood(event.Event):
    '''Fire wood materials can be collected here to make fires and keep warm and avoid taking damages !!'''
    def __init__ (self):
        self.name = "Dry wood supplies"

    def process (self, world):
        result = {}
        config.the_player.ship.firewood += 3
        result["message"] = "3 firewood materials were added to invenotry"
        result["newevents"] = [ self ]
        return result
class Boss(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["punch"] = ["punches", random.randrange(65,80), (35,45)]
        super().__init__(name,random.randrange(300, 450), attacks, 120)
class BossBattle (event.Event):
    '''you encounter the boss and have to fight him.
    '''
    def __init__ (self):
        self.name = "boss attack"

    def process (self, world):
        result = {}
        result["message"] = "You have defeated the boss ! "
        monsters = []
        monsters.append(Boss("Gorilla Warrior"))
        announce ("the pirates come across a angry gorilla on the bridge and are attacked !")
        combat.Combat(monsters).combat()
        result["newevents"] = []
        config.the_player.inventory.append(WaterChest())
        config.the_player.ship.water += 100
        return result
    
class WaterChest(items.Item):
    def __init__(self):
        super().__init__("water-chest",450)

class GunPowder(event.Event):
    def __init__ (self):
        self.name = "You come across gun powder!!!"

    def process (self, world):
        ''''''
        #CREWMATE.powder = 32
        for p in config.the_player.get_pirates():
            p.powder = 32
        result = {}
        result["message"] = "you get 32 packages of gun powder!!"
        result["newevents"] = [ self ]
        return result


