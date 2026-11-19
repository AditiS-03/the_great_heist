class Player:

    def __init__(self, name, position, color):

        self.name = name
        self.position = position
        self.color = color

    def move_to(self, position):

        self.position = position