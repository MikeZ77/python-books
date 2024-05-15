# Defines the program skeleton of an algorithm in an operation ...
# deferring some steps to the subclass (meaning that the subclass overrides some steps)

# Suppose we have a project that is a pdf doc ...
# We can optionally insert images, or data

class Template:
    def __init__(self, content: str, image_paths: list[str], csv_paths: list[str]):
        self.content = content
        self.image_paths = image_paths
        self.csv_paths = csv_paths
    
    def add_content(self, text: str): ...

    def add_images(self, *image_path: str): ...
    
    def add_data(self, *csv_path: str): ...

    def compile_project(self, text, images, csvs): ...
    
    def __call__(self):
        images = self.add_images(*self.image_paths)
        data = self.add_data(*self.image_paths)
        return self.compile_project(self.content, images, data)
    
class MyProject(Template):
    def __init__(self, content: str, image_paths: list[str], csv_paths: list[str]):
        super().__init__(content, image_paths, csv_paths)
            
    def add_data(self, *csv_path: str):
        print("images get added on each page instead of the default")
        

# What is the difference between template and the facade?

# In the facade pattern, we are encapsulating a complex system with different parts ...
# through a universal interface. It has no flexibility though. For simplicity we just 
# call a method method and we don't care about all the steps.

# With the template pattern, we override steps with our own implementation (update the template).

# What is the difference between the template pattern and the strategy pattern?

# The strategy pattern chooses the implementation at runtime based on some data. 
# The template pattern implementation is decided at compile time.


if __name__ == "__main__":
    my_project = MyProject("blah blah blah", "home/my_image.jpg", "home/my_data.csv")
    my_project()