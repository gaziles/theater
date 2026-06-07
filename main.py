from theater_lib.controller import *


def menu():
    print("\n0 - zakończ program")
    print("1 - wyświetl teatry")
    print("2 - dodaj teatr")
    print("3 - usuń teatr")
    print("4 - aktualizuj teatr")
    print("5 - wyświetl klientów")
    print("6 - wyświetl pracowników")
    print("7 - wyświetl spektakle")


def main():
    while True:

        menu()

        menu()
        choice = input("Wybierz opcję: ")

        if choice == "0":
            print("Koniec programu")
            break

        elif choice == "1":
            show_theaters()

        elif choice == "2":
            add_theater()

        elif choice == "3":
            delete_theater()

        elif choice == "4":
            update_theater()

        else:
            print("Nieprawidłowa opcja")


if __name__ == "__main__":
    main()