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


def show_clients():
    for theater in theaters:
        print()
        print(f"Teatr: {theater['name']}")

        for client in theater["clients"]:
            print(client["name"])


def add_client():
    theater_name = input("Podaj nazwę teatru: ")
    client_name = input("Podaj imię klienta: ")

    for theater in theaters:
        if theater["name"] == theater_name:

            theater["clients"].append(
                {
                    "name": client_name,
                    "performances": []
                }
            )

            print("Klient został dodany.")
            return

    print("Nie znaleziono teatru.")


def delete_client():
    theater_name = input("Podaj nazwę teatru: ")
    client_name = input("Podaj imię klienta: ")

    for theater in theaters:

        if theater["name"] == theater_name:

            for client in theater["clients"]:

                if client["name"] == client_name:

                    theater["clients"].remove(client)

                    print("Klient został usunięty.")
                    return

            print("Nie znaleziono klienta.")
            return

    print("Nie znaleziono teatru.")


def show_employees():
    for theater in theaters:
        print()
        print(f"Teatr: {theater['name']}")

        for employee in theater["employees"]:
            print(employee)


def add_employee():
    theater_name = input("Podaj nazwę teatru: ")
    employee_name = input("Podaj imię pracownika: ")

    for theater in theaters:
        if theater["name"] == theater_name:
            theater["employees"].append(employee_name)

            print("Pracownik został dodany.")
            return

    print("Nie znaleziono teatru.")


def delete_employee():
    theater_name = input("Podaj nazwę teatru: ")
    employee_name = input("Podaj imię pracownika: ")

    for theater in theaters:

        if theater["name"] == theater_name:

            if employee_name in theater["employees"]:

                theater["employees"].remove(employee_name)

                print("Pracownik został usunięty.")
                return

            print("Nie znaleziono pracownika.")
            return

    print("Nie znaleziono teatru.")


def show_client_performances():

    client_name = input("Podaj imię klienta: ")

    for theater in theaters:

        for client in theater["clients"]:

            if client["name"] == client_name:

                print("\nObejrzane spektakle:")

                for performance in client["performances"]:
                    print(performance)

                return

    print("Nie znaleziono klienta.")


def add_performance_to_client():

    client_name = input("Podaj imię klienta: ")
    performance = input("Podaj nazwę spektaklu: ")

    for theater in theaters:

        for client in theater["clients"]:

            if client["name"] == client_name:

                client["performances"].append(
                    performance
                )

                print("Dodano spektakl klientowi.")
                return

    print("Nie znaleziono klienta.")