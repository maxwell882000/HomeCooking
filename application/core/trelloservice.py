from application import trello_client
from application.core.models import Order
from application.resources import strings
import settings


def add_order_to_trello_board(order: Order):
    trello_settings = settings.get_trello_settings()
    board_name = trello_settings[0]
    list_name = trello_settings[1]
    all_boards = trello_client.list_boards(board_filter='open')
    try:
        board = list(filter(lambda b: b.name == board_name, all_boards))[0]
    except IndexError:
        return
    all_lists = board.open_lists()
    try:
        orders_list = list(filter(lambda l: l.name == list_name, all_lists))[0]
    except IndexError:
        return
    card_name = 'Заказ #{}'.format(order.id)
    card_description = strings.from_order_trello_card(order)
    orders_list.add_card(name=card_name, desc=card_description)
