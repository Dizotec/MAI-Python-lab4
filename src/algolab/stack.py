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
def demo_stack() -> None:
    # пример 
    stack = Stack()
    print(f"Пустой стек: len={len(stack)}, bool={bool(stack)}")

    for value in (10, 20, 30):
        stack.push(value)
        print(f"push({value})")

    print(f"peek() → {stack.peek()}")
    print(f"Размер после peek(): {len(stack)}")

    while stack:
        print(f"pop() → {stack.pop()}")

    print(f"После извлечения: len={len(stack)}, bool={bool(stack)}")

    try:
        stack.pop()
    except IndexError:
        print("pop() на пустом стеке → IndexError")