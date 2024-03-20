from mip import Model, xsum, minimize, BINARY


m = Model("Simple energy system")

class AddVariables():
    def __init__(self):
        x = m.add_var(self)
        
    def addContinuous(self):
        m.add_var(self)


class AddConstraints():
    def __init__(self):
    