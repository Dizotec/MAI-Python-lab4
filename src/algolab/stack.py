from typing import Any 
class Stack():
    def __init__(self)->None:
        self.items = []
    def push(self,item: Any )->Any:
        self.items.append(item)
    def pop(self)-> Any:
        
        last_item = self.items.pop()
        return  last_item 
    def peek(self)->Any:
        last_item = self.items[-1]
        return  last_item 
    def __len__(self)->int:
        return len(self.items)
    def is_exist(self)->bool:
        return bool(self.items)