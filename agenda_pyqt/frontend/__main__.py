import sys
from .main_app import SegurosApp

def main():
    app = SegurosApp(sys.argv)
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
