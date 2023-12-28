from game import location
import game.config as config
from game.display import announce


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

    def enter(self):
        announce ("You have made it to a secret Island that has many dangers on it!\n" +
                  "The ship you arrived on is stationed on the south side of the Island.\n" +
                  "Gather as much material as you can to survive your time on Kyle's Island!!")
    def process_verb (self, verb, cmd_list, nouns):
         if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
         elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["southSide"]
         elif (verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations[f"{verb}Side"]


class NorthSide (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "northSide"

    def enter(self):
        announce("You get to the north side of the island, this is the only part of the Island that is safe.")

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
    def enter(self):
        announce("You have not entered the west side of the Island where there is no shelter for you")

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
    def enter(self):
        announce("You walk through the side of the island you are on and come across a bridge that connects all the sides on the island together")

        def process_verb (self, verb, cmd_list, nouns):
            if (verb == "exit" or verb == "leave"):
                config.the_player.next_loc = self.main_location.locations["northSide"]
                config.the_player.go = True
    