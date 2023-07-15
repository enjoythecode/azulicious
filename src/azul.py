import random
import bisect

def new_row():
    return {
        "color": None,
        "count": 0
    }

def new_pile(w, b, y, r, k):
    return [w, b, y, r, k]

def new_board():
    return {
        "grid": [[0 for _ in range(5)] for _ in range(5)],
        "rows": [new_row() for _ in range(5)],
        "floor": new_pile(0, 0, 0, 0, 0)
        }


TILE_COLORS = ["white", "blue", "yellow", "red", "black"]
NUM_TILES_PER_DISPLAY = 4

def choose_random_from_pile(p):
    if sum(p) == 0:
        return None
    running_sum = [p[0]]
    for val in p[1:]:
        running_sum.append(running_sum[-1] + val)
    choice = random.randint(0, running_sum[-1])
    index = bisect.bisect(running_sum, choice)
    if index > len(TILE_COLORS):
        index -= 1
    return index

class Azul():
    def __init__(self, num_players, auto_setup = True):
        self.player_count = num_players

        if auto_setup:
            self.bag = new_pile(20, 20, 20, 20, 20)
            self.discard = new_pile(0,0,0,0,0)
            num_displays = {
                2: 5,
                3: 7,
                4: 9
            }[num_players]
            assert num_displays is not None

            self.round = 1
            self.turn = 0 # index of player with the turn
            self.displays = [new_pile(0,0,0,0,0) for _ in range(num_displays + 1)]
            self.boards = [new_board(), new_board()]
            self.first_player_token_location = -1 
            self.replenish_displays()

    def load_game_state(self, player_count, bag, discard, round, turn, displays, boards, first_player_token_location):
        self.player_count = player_count
        self.bag = bag
        self.discard = discard
        self.round = round
        self.turn = turn
        self.displays = displays
        self.boards = boards
        self.first_player_token_location = first_player_token_location

    def replenish_displays(self):
        for display_i in range(len(self.displays) - 1): # last "display" is the center, don't put tiles to it from the bag
            for i in range(NUM_TILES_PER_DISPLAY):
                assert sum(self.bag) > 0, "implement re-shuffling the discard into the bag"
                self.take_random_from_bag_to_display(display_i)

    def take_random_from_bag_to_display(self, display_i):
        color = choose_random_from_pile(self.bag)
        self.bag[color] -= 1
        self.displays[display_i][color] += 1
        
    def make_move(self, display_i, color_i, row_i):

        assert display_i < len(self.displays)

        tile_count = self.displays[display_i][color_i]
        target_row = self.boards[self.turn]["rows"][row_i]
        
        assert tile_count > 0
        assert target_row["color"] in [color_i, None]
        
        row_empty_spaces = (row_i + 1) - target_row["count"]

        if row_empty_spaces >= tile_count:
            count_to_row = tile_count
            count_to_floor = 0
        else:
            count_to_row = row_empty_spaces
            count_to_floor = tile_count - row_empty_spaces

        # put the rest of the display on to the floor
        for display_color_i in range(len(TILE_COLORS)):
            if color_i != display_color_i:
                self.displays[-1][display_color_i] += self.displays[display_i][display_color_i]
                self.displays[display_i][display_color_i] = 0

        # move the taken color to the player board on the selected row
        self.displays[display_i][color_i] = 0
        self.boards[self.turn]["rows"][row_i]["color"] = color_i
        self.boards[self.turn]["rows"][row_i]["count"] += count_to_row
        self.boards[self.turn]["floor"][color_i] += count_to_floor


    
        # taking from center, and the first player token is also there!
        if display_i == len(self.displays) - 1 and self.first_player_token_location == -1:
            self.first_player_token_location = self.turn # that player now owns this first player token (in their floor line...)
        self.turn = (self.turn + 1) % self.player_count

        assert sum([sum(display) for display in self.displays]) > 0, "implement triggering scoring when board is empty"
