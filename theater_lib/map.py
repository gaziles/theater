import folium
import requests
from bs4 import BeautifulSoup

from theater_lib.model import theaters


def get_coordinates(location):

    location = location.replace(" ", "_")

    url = f"https://pl.wikipedia.org/wiki/{location}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    latitude = float(
        soup.select(".latitude")[1].text.replace(",", ".")
    )

    longitude = float(
        soup.select(".longitude")[1].text.replace(",", ".")
    )

    return [latitude, longitude]


def generate_theater_map():

    mapa = folium.Map(
        location=[52, 19],
        zoom_start=6
    )

    for theater in theaters:

        try:

            coordinates = get_coordinates(
                theater["location"]
            )

            folium.Marker(
                location=coordinates,
                popup=theater["name"],
                tooltip=theater["name"]
            ).add_to(mapa)

        except Exception:

            print(
                f"Nie udało się pobrać współrzędnych dla miasta: {theater['location']}"
            )

    mapa.save("mapa_teatrow.html")

    print("Mapa teatrów została wygenerowana.")


def generate_clients_map():

    mapa = folium.Map(
        location=[52, 19],
        zoom_start=6
    )

    for theater in theaters:

        for client in theater["clients"]:

            try:

                coordinates = get_coordinates(
                    client["location"]
                )

                folium.Marker(
                    location=coordinates,
                    popup=client["name"],
                    tooltip=client["name"]
                ).add_to(mapa)

            except Exception:

                print(
                    f"Nie udało się pobrać współrzędnych dla klienta: {client['name']}"
                )

    mapa.save("mapa_klientow.html")

    print("Mapa klientów została wygenerowana.")


def generate_employees_map():

    mapa = folium.Map(
        location=[52, 19],
        zoom_start=6
    )

    for theater in theaters:

        for employee in theater["employees"]:

            try:

                coordinates = get_coordinates(
                    employee["location"]
                )

                folium.Marker(
                    location=coordinates,
                    popup=employee["name"],
                    tooltip=employee["name"]
                ).add_to(mapa)

            except Exception:

                print(
                    f"Nie udało się pobrać współrzędnych dla pracownika: {employee['name']}"
                )

    mapa.save("mapa_pracownikow.html")

    print("Mapa pracowników została wygenerowana.")