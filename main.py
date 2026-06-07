from theater_lib.controller import *


def menu():
    print("\n0 - zakończ program")
    print("1 - wyświetl teatry")
    print("2 - dodaj teatr")
    print("3 - usuń teatr")
    print("4 - aktualizuj teatr")
    print("5 - wyświetl klientów")
    print("6 - dodaj klienta")
    print("7 - usuń klienta")
    print("8 - wyświetl pracowników")
    print("9 - dodaj pracownika")
    print("10 - usuń pracownika")


def main():
    while True:

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

        elif choice == "5":
            show_clients()

        elif choice == "6":
            add_client()

        elif choice == "7":
            delete_client()

        elif choice == "8":
            show_employees()

        elif choice == "9":
            add_employee()

        elif choice == "10":
            delete_employee()

        else:
            print("Nieprawidłowa opcja")


if __name__ == "__main__":
    main()