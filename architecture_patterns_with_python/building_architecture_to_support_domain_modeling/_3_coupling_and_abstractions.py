# When we cannot change B without impacting/changing A, then A and B are coupled
# To decouple, we add a an abstraction layer between compnents B and A

# Suppose we have a function sync() that works between two source and destination folders:
# 1. walk the source folder and build a dict of the file names and hashes
# 2. walk the desintation folder and build a dict for the file anme and hshes
# 3. if there is a file that is not in source, delete it
# 4. if there is a file in source that has a different path in destination, move it
# 5. if the file exists in source but not destination, then copy it to destination

# Imagine all of this is in one sync function, our busines logic (steps 3-4) is tightly ...
# coupled with our abstraction of the folder structure (dicts with hashed files as the key and path as the value) ...
# and with the IO operation utilities.

# If the details of one of these changes, we need to change more of sync() than we would probably like to.
# The solution to fix thight coupling is by creating abstractions.

# To do this, we want to seperate the business logic and find simplifying abstractions for everything else.
# Seperate what we want to do, from how we will do it.

# Also, testing one single sync function is more difficult. We have to setup the filesystem then check the specifc ...
# outcome in that file system to test. Really, we would only like to test the business logic in isolation and not ...
# have to do that setup.

def test_when_a_file_exists_in_the_source_but_not_the_destination():
    # This absraction already exists, but we would like to pass it in
    src_hashes = {"hash1": "fn1"}
    dest_hashes = {}
    # Abstract the actual action/operation of copying, or moving a file.
    expected_actions = [{"COPY", "/src/fn1", "/dst/fn1"}]

def test_when_a_file_has_been_renamed_in_the_source():
    src_hashes = {"hash1": "fn1"}
    dest_hashes = {"hash1": "fn2"}
    expected_actions = [{"MOVE", "/src/fn2", "/dst/fn1"}]

# Now we can test the busines logic seperately, which takes a file representation and outputs a command object
# This is really what we want to test.

import hashlib
import os
import shutil
from pathlib import Path

def sync(source, dest):
    source_hashes = read_paths_and_hashes(source)
    dest_hashes = read_paths_and_hashes(dest)

    actions = determine_actions(source_hashes, dest_hashes, source, dest)
    
    for action, *paths in actions:
        if action == "COPY":
            shutil.copyfile(*paths)
        if action == "MOVE":
            shutil.move(*paths)
        if action == "DELETE":
            os.remove(paths[0])
            
BLOCKSIZE = 65536


def hash_file(path):
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf = file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
    return hasher.hexdigest()


def read_paths_and_hashes(root):
    hashes = {}
    for folder, _, files in os.walk(root):
        for fn in files:
            hashes[hash_file(Path(folder) / fn)] = fn
    return hashes


def determine_actions(source_hashes, dest_hashes, source_folder, dest_folder):
    for sha, filename in source_hashes.items():
        if sha not in dest_hashes:
            sourcepath = Path(source_folder) / filename
            destpath = Path(dest_folder) / filename
            yield "COPY", sourcepath, destpath

        elif dest_hashes[sha] != filename:
            olddestpath = Path(dest_folder) / dest_hashes[sha]
            newdestpath = Path(dest_folder) / filename
            yield "MOVE", olddestpath, newdestpath

    for sha, filename in dest_hashes.items():
        if sha not in source_hashes:
            yield "DELETE", dest_folder / filename
            
# There is still a bit of an issue with testing sync, It is fine for unit testing, because we have decoupled the components. 
# but if we do an integration test for sync, we need to mock the IO functions for example.

# Use DI so that we can choose what filesystem to pass sync.
# For example, we create a Filesystem class that implements the copy, delete, and move interface
# This gets injected into sync, (we can simply pass it in as an arg)
# To mock we can create FakeFilesystem which implements the interface while also capturing the args passed in ...
# This is actually a spy, since we care about the args passed to it in our test assertion and it does not return output.
# A mock would be a fake that actually returns some output and could be used in the rest of the code.

# DI is typically preferable to patching because:
# 1. patching does nothing to improve the design, e.g. we could have just monkeypatched the original implementation to test ...
#    and we would have been left with something that is tightly coupled and difficult to modify
# 2. patching creates a more complicated test setup.






