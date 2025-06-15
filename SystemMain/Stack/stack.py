from SystemMain.BaseClass import basescene

class MyStack:
    def __init__(self) :
        self.stack : list[basescene] = []

    def push(self, item : basescene):
        self.stack.append(item)

    def pop(self):
        if len(self.stack) == 0:
            return None
        return self.stack.pop()
    
    def top(self):
        return self.stack[-1]
    
    def len(self):
        return len(self.stack)
    
    def all_remove(self):
        while len(self.stack) != 0:
            self.stack.pop()
