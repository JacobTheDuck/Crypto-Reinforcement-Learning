""" This file will take the data inside the data.csv, instantiate the first state, and use
the Q_table file to make actions, step through to the terminal state, and return a dictionary that can
be used to estimate the returns and update the Q_table.
"""

import csv

class State:
    actions = ['Buy', 'Sell', 'Hold']

    def __init__(self, data_dict):
        self.sma = data_dict.get('20SMA')
        self.bollingeru = data_dict.get('BollingerU')
        self.bollingerl = data_dict.get('BollingerL')
        self.rsi = data_dict.get('RSI')
        self.ma20 = data_dict.get('MA20')
        self.ma5 = data_dict.get('MA5')

    def get_self(self):
        return(self.sma, self.bollingeru, self.bollingerl, self.rsi, self.ma20, self.ma5)


def get_data():
    with open("data.csv", "r") as file:
        reader = csv.DictReader(file)
        data = list(reader)

        # Instantiate empty values to zero.
        for day in data:
            for lable, value in day.items():
                if not value:
                    day[lable] = 0

        return(data)


def print_data(data_list_dicts):
    print(data_list_dicts)

def generate_episode(data_list_dicts):

    # Initialilize start and end state.
    # Find first day where all values are instantiated.
    def find_start_day():
        for _list in data_list_dicts:
            start_state = State(_list)
            full = all(start_state.get_self())
            if full:
                return start_state
    start_state = find_start_day()
    print(start_state.get_self())





if __name__ == "__main__":
    # Get the data into a list of dicts.
    data = get_data()

    # Generate episode using data.
    generate_episode(data)
