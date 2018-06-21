import os
from pathlib import Path

def adjustPathString(currentPath: str, innerPath: str) -> str:
    return currentPath + '\\' + innerPath

def recursive_list(name: Path) -> [Path]:
    '''Puts every item in a given path into a list, recursively repeating this in subdirectories until
    it finally has one list of path objects to return.'''
    final = []
    first = []
    second = []
    items = os.listdir(name)
    items.sort()
    for item in items:
        r = name / item
        if r.is_dir() == False:
            first.append(r)
        elif r.is_dir() == True:
            t = recursive_list(r)
            for x in t:
                second.append(x)
    for x in first:
        final.append(x)
    for x in second:
        final.append(x)
    return final

def validPath(fileStr: str) -> bool:
    return os.path.exists(fileStr)
