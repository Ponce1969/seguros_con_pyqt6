import sys
from .main_app import AplicacionSeguros

def main():
    app = AplicacionSeguros(sys.argv)
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
