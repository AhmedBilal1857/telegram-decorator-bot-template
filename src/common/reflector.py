import os
import inspect
import importlib

import glob
import secrets
import string
import sys

def get_all_handlers(working_dir: str = os.getcwd(), 
                      file_patterns: list[str] = ["handlers"],
                      files_to_skip: list[str] = ["__init__.py", "__main__.py"]) -> list[str]:
    # TODO: Need to change it to regex based only in future
    handler_files = []
    for file in glob.iglob(os.getcwd() + "/**/*.py", recursive=True):
        if any(f in file for f in files_to_skip):
            continue
        if any(f in file for f in file_patterns):
            handler_files.append(file)
    return handler_files
#----------------------------------------------------------------------------
def file_path_to_module(file_path: str, working_dir: str = os.getcwd()):
    # TODO: Neeed to improve the shit code... with string builder maybe?
    file_path = file_path.removeprefix(working_dir + "/")
    file_path = file_path.replace("/", ".")
    file_path = file_path.removesuffix(".py")

    return file_path
#----------------------------------------------------------------------------
def is_module_function(mod, func):
    ' checks that func is a function defined in module mod '
    return inspect.iscoroutine(func) or inspect.isfunction(func)
#----------------------------------------------------------------------------
def get_function_names(mod):
    ' list of function names defined in module mod '
    return [func.__name__ for func in mod.__dict__.values() 
            if is_module_function(mod, func)]
#----------------------------------------------------------------------------
def get_functions(mod):
    ' list of functions defined in module mod '
    functions = []

    for function in mod.__dict__.values():
        if is_module_function(mod, function) is False:
            continue
        functions.append(function)
    return functions
    return [func for func in mod.__dict__.values() 
            if is_module_function(mod, func)]
#----------------------------------------------------------------------------
def gensym(length=32, prefix="gensym_"):
    """
    Generates a fairly unique symbol, used to make a module name,
    used as a helper function for load_module

    :return: generated symbol
    """
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
    symbol = "".join([secrets.choice(alphabet) for i in range(length)])

    return prefix + symbol
#----------------------------------------------------------------------------
def load_module(source, module_name=None):
    """
    Reads file source and loads it as a module

    :param source: file to load
    :param module_name: name of module to register in sys.modules
    :return: loaded module
    """

    if module_name is None:
        module_name = gensym()

    spec = importlib.util.spec_from_file_location(module_name, source)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module
#----------------------------------------------------------------------------