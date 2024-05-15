# Notifies a list of observers (dependents) of any state change or update

# Lets say that we have some buttons on a GUI ...
# If one of the buttons is active, all other buttons must be disabled
from __future__ import annotations
from typing import Protocol

class Observer(Protocol):
    # The observer protocol in this case is just that it must implement update.
    def update(self) -> None:
        ...
    
class ButtonSubject:
    _observers: list[Observer] = []
       
    @classmethod    
    def attach(cls, btn: Observer):
        cls._observers.append(btn)
    
    @classmethod 
    def detach(cls, btn: Observer):
        cls._observers.remove(btn)

    @classmethod 
    def notify(cls, modifier: Observer):
        for observer in cls._observers:
            if observer is modifier:
                continue
            else:
                observer.update()

            print(observer.name, observer.disabled)

class Button(Observer, ButtonSubject):
    def __init__(self, name: str):
        self.name = name
        self.disabled = False
    
    def click(self) -> None:
        self.disabled = not self.disabled
        self.notify(self)
        print(self.name, self.disabled)            

    def update(self) -> None:
        self.disabled = False

if __name__ == "__main__":
    subject = ButtonSubject()
    button1 = Button("button1")
    button2 = Button("button2")
    button3 = Button("button3")
    subject.attach(button1)
    subject.attach(button2)
    subject.attach(button3)
    button1.click()
    print("-----------------------------")
    button2.click()
    
