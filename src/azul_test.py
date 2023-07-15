import pytest
from azul import Azul, new_pile, new_board

@pytest.fixture()
def az2p_clean(): # 2 player Azul board, predefined
    az = Azul(2, auto_setup=False)

    az.load_game_state(
        player_count = 2,
        bag = new_pile(16, 16, 16, 16, 16),
        discard = new_pile(0, 0, 0, 0, 0),
        round = 1,
        turn = 0,
        displays = [
            new_pile(1, 1, 1, 1, 0),
            new_pile(1, 2, 1, 0, 0),
            new_pile(2, 0, 2, 0, 0),
            new_pile(0, 1, 0, 3, 0),
            new_pile(0, 0, 0, 0, 4),
            new_pile(0, 0, 0, 0, 0), # last display is the center
        ],
        boards = [new_board(), new_board()]
    )
    return az

def test_sanity():
    assert 2 + 2 == 4

def test_init_game():
    az = Azul(num_players = 2, auto_setup = True)
    assert sum(az.bag) == 80
    assert sum([sum(display) for display in az.displays]) == 20

def test_make_move_take_from_display_of_4(az2p_clean):
    az2p_clean.make_move(4, 4, 3)

    assert az2p_clean.displays[4] == new_pile(0, 0, 0, 0, 0)
    assert az2p_clean.boards[0]["rows"][3]["color"] == 4
    assert az2p_clean.boards[0]["rows"][3]["count"] == 4
    assert az2p_clean.turn == 1
    assert az2p_clean.displays[-1] == new_pile(0, 0, 0, 0, 0)

def test_make_move_take_from_display_of_3_and_1(az2p_clean):
    az2p_clean.make_move(display_i = 3, color_i = 3, row_i = 2)

    assert az2p_clean.displays[3] == new_pile(0, 1, 0, 0, 0)
    assert az2p_clean.boards[0]["rows"][2]["color"] == 3
    assert az2p_clean.boards[0]["rows"][2]["count"] == 3
    assert az2p_clean.turn == 1
    assert az2p_clean.displays[-1] == new_pile(0, 0, 0, 0, 0)

def test_make_move_take_from_display_of_1_each(az2p_clean):
    az2p_clean.make_move(display_i = 0, color_i = 2, row_i = 0)

    assert az2p_clean.displays[0] == new_pile(1, 1, 0, 1, 0)
    assert az2p_clean.boards[0]["rows"][0]["color"] == 2
    assert az2p_clean.boards[0]["rows"][0]["count"] == 1
    assert az2p_clean.turn == 1
    assert az2p_clean.displays[-1] == new_pile(0, 0, 0, 0, 0)

