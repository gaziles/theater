def menu():
    print("0 - zakończ program")
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
        choice = input("Wybierz opcję: ")

        if choice == "0":
            print("Koniec programu")
            break

        elif choice == "1":
            print("Wybrano wyświetlanie teatrów")

        elif choice == "2":
            print("Wybrano dodawanie teatru")

        elif choice == "3":
            print("Wybrano usuwanie teatru")

        elif choice == "4":
            print("Wybrano aktualizację teatru")

        elif choice == "5":
            print("Wybrano wyświetlanie klientów")

        elif choice == "6":
            print("Wybrano wyświetlanie pracowników")

        elif choice == "7":
            print("Wybrano wyświetlanie spektakli")

        else:
            print("Nieprawidłowa opcja")


if __name__ == "__main__":
    main()