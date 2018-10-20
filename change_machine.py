# Written with Python 3.7

#!/usr/bin/env python

from math import floor

class ChangeMachine:
    def __init__(self):
        self.denominations = [100, 50, 20, 10, 5, 1, 0.25, 0.10, 0.05, 0.01]

    def _validate_input(self, input_value):
        """Restricts values to floats and integers."""
        input_is_float = type(input_value) == float
        input_is_int = type(input_value) == int
        if input_is_float or input_is_int:
            return input_value >= 0
        else:
            return False

    def add_denomination(self, denomination):
        """Lets user add less-common denominations like $2 bills and 50-cent coins."""
        if self._validate_input(denomination) == True:
            denomination_set = set(self.denominations)
            denomination_set.add(denomination)
            new_denomination_list = list(denomination_set)
            new_denomination_list = reversed(sorted(new_denomination_list))
            self.denominations = list(new_denomination_list)

    def remove_denomination(self, denomination):
        if denomination in self.denominations:
            self.denominations.remove(denomination)

    def change_breakdown(self, cash):
        result_dictionary = dict()
        for denomination in self.denominations:
            denomination_count = floor(cash / denomination)
            if denomination_count > 0:
                result_dictionary[denomination] = denomination_count
                cash = cash - denomination * denomination_count
                cash = round(cash, 2)
        return result_dictionary

    def transaction(self, cost=1, cash=1):
        if self._validate_input(cost) and self._validate_input(cash):
            if cash < cost:
                print("Not enough money to cover transaction.")
            else:
                change = cash - cost
                change = round(change, 2)
                breakdown = self.change_breakdown(change)
                print("Change is ${0}. The breakdown is:".format(change))
                for denomination, count in breakdown.items():
                    print("${0}: {1}".format(denomination, count))
        else:
            print("Invalid transaction inputs.")

if __name__ == '__main__':

    input_cost_string = input("Purchase cost: ")
    input_cash_string = input("Cash given: ")

    input_cost = float(input_cost_string)
    input_cash = float(input_cash_string)

    change_machine = ChangeMachine()

    print("Paying for ${0:0.2f} with ${1:0.2f}".format(input_cost, input_cash))
    change_machine.transaction(input_cost, input_cash)
