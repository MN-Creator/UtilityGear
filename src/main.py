from app import App
import os
import sys


def main():
    title = "UtilityGear"
    app = App(title)
    app.mainloop()
    if app.restart:
        python_path = sys.executable
        os.execl(python_path, python_path, *sys.argv)


if __name__ == "__main__":
    main()
