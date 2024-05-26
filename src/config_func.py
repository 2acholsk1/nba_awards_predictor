import yaml
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def load_config(filename):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

def print_in_box(message):
    width = len(message) + 4
    top_bottom = '+' + '-' * width + '+'
    middle = f'|  {message}  |'

    print(Fore.GREEN + top_bottom)
    print(Fore.GREEN + middle)
    print(Fore.GREEN + top_bottom)