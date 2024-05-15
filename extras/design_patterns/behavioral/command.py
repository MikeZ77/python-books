# The controller encapsulates all information needed to perform an action / job.
# The controller passes the command to the object that knows how to perform it.
# Each command object is reponsible for performing and keeping track of its result if needed ...
#   For example, the client performs an action.
#   The controller passes that command to the responsible object.
#   The client then asks to undo the action ...
#   The undo command is passed to the responsible object.
from __future__ import annotations
from typing import Literal, TypeAlias, TypeVar
# from pathlib import Path

CommandName: TypeAlias = Literal["open", "add", "undo", "delete", "save"]
C = TypeVar('C') # C for command type

   
class FileController:
    """ Allows you to work with single files"""
    commands: C = {}
    
    @classmethod
    def register_command(cls, name: CommandName, command: C):
        cls.commands[name] = command()

    @classmethod
    def execute(cls, name: CommandName):
        cls.commands[name]
        
    @staticmethod
    def register(command: CommandName):
        def inner(cls: C):
            FileController.register_command(command, cls)
            return cls
        return inner

@FileController.register("add")
class AddText:
    def __init__(self):
        self.text: list[str] = []
        
    def execute(self, text):
        self.text.append(text)
        
    def undo(self):
        self.text.pop()

@FileController.register("save")
class SaveFile:
    def execute(self): ...

@FileController.register("delete")
class DeleteFile:
    def execute(self): ...

@FileController.register("open")
class OpenFile:
    def execute(self): ...
        
# if __name__ == "__main__":
#     # For simplicity, lets suppose we have some "master" file ...
#     # which is a single file we need to open or close at different points ...
#     # of our programs execution.
#     doc = FileController()

# Most examples we pass the Command class directly to the controller to register it. 
# Therefore if we had different params to pass for the Command constructor, we could ...
# Register a new command with different params.


# What if we tried adding a context, which could be updated before running a command ...
# If its behavior needed to change, like work on a new file?

from dataclasses import dataclass
from typing import Protocol

@dataclass
class Context:
    file: str

class Command(Protocol):
    def execute(self):
        raise NotImplementedError
    
class FileController:
    """ Allows you to work with single files"""
    commands: dict[CommandName, Command] = {}
    context: Context
    
    @classmethod
    def register_command(cls, name: Command, command: C):
        cls.commands[name] = command()

    @classmethod
    def execute(cls, name: CommandName):
        cls.commands[name].execute()
        
    @staticmethod
    def register(command: Command):
        def inner(cls: C):
            FileController.register_command(command, cls)
            return cls
        return inner    


@FileController.register("open")
class OpenFile:
    def execute(self):
        print(f"Openning file to {FileController.context.file}")


if __name__ == "__main__":
    FileController.context = Context(file="path_to_file.csv")
    doc = FileController()
    doc.execute("open")
    
    #TODO: A better idea may be do decouple the command with the controller with regards ...
    # to context i.e. accessing the context like this. FileController.context.file.
    # Maybe have context be a descriptor s.t. everytime it is updated, it re-registers ...
    # all the commands passing the context as an instance variable.