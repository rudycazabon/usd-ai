import os
from io import StringIO

from dotenv import dotenv_values, load_dotenv

load_dotenv()

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}

def main():
    print(os.getenv("ENVVAR"))  # prints "foo"
    
if __name__ == "__main__":
    main()

