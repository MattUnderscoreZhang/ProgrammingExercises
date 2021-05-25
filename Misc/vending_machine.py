class VendingItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class VendingMachine:
    def __init__(self):
        self.inventory = self.make_inventory()

    def make_inventory(self):
        cheetos = VendingItem("cheetos", 1.00)
        flaming_hot_cheetos = VendingItem("flaming_hot_cheetos", 1.00)
        oreos = VendingItem("oreos", 2.00)
        m_and_ms = VendingItem("m_and_ms", 1.50)
        kit_kats = VendingItem("kit_kats", 1.00)
        doritos = VendingItem("doritos", 1.00)
        slim_jims = VendingItem("slim_jims", 2.00)

        inventory = [
            [(cheetos, 3), (flaming_hot_cheetos, 8)],
            [(oreos, 4), (m_and_ms, 4)],
            [(kit_kats, 0), (doritos, 5)],
            [(slim_jims, 2), None],
        ]

        return inventory

    def vend(self, selection):
        if (type(selection) is not tuple) or (len(selection) != 2):
            print("Incorrect selection")
        elif (item_details := self.inventory[selection[0]][selection[1]]) is not None:
            item, number_left = item_details
            if number_left <= 0:
                print("Out of", item.name)
            else:
                print("Vending", item.name, "for", item.price, "dollars")
                self.inventory[selection[0]][selection[1]] = (item, number_left - 1)
        return


if __name__ == '__main__':
    vending_machine = VendingMachine()
    vending_machine.vend(3)  # incorrect choice
    vending_machine.vend((0, 0))  # cheetos
    vending_machine.vend((3, 1))  # None
    vending_machine.vend((2, 0))  # kit_kats (empty)
    vending_machine.vend((3, 0))  # slim_jims
    vending_machine.vend((3, 0))
    vending_machine.vend((3, 0))
    vending_machine.vend((3, 0))
