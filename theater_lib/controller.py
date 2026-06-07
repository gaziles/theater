from theater_lib.model import theaters


def show_theaters():
    for theater in theaters:
        print()
        print(f"Nazwa: {theater['name']}")
        print(f"Miasto: {theater['location']}")
        print("-" * 30)


def add_theater():
    name = input("Podaj nazwę teatru: ")
    location = input("Podaj miasto: ")

    theater = {
        "name": name,
        "location": location,
        "performances": [],
        "clients": [],
        "employees": []
    }

    theaters.append(theater)

    print("Teatr został dodany.")


def delete_theater():
    name = input("Podaj nazwę teatru do usunięcia: ")

    for theater in theaters:
        if theater["name"] == name:
            theaters.remove(theater)
            print("Teatr został usunięty.")
            return

    print("Nie znaleziono teatru.")


def update_theater():
    name = input("Podaj nazwę teatru do aktualizacji: ")

    for theater in theaters:
        if theater["name"] == name:

            theater["name"] = input("Nowa nazwa: ")
            theater["location"] = input("Nowe miasto: ")

            print("Teatr został zaktualizowany.")
            return

    print("Nie znaleziono teatru.")