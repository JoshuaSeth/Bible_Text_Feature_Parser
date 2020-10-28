import importlib
import inspect
import os
from plugins.plugin import Plugin

def LoadPlugins():
    plugins = []
    for file in os.listdir("/Users/sethvanderbijl/Coding Projects/Bible_features/app/plugins"):
        name = os.path.splitext(os.path.basename(file))[0]
        # add package prefix to name, if required
        module = importlib.import_module("plugins."+name)
        for member in dir(module):
            # do something with the member named member
            handler_class = getattr(module, member)
            if inspect.isclass(handler_class):
                if issubclass(handler_class, Plugin) and not member == "Plugin":
                    print("Loading plugin:",member, handler_class)
                    plugins.append(handler_class)

    return plugins