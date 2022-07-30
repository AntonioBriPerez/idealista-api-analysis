import json
from Idealista import Idealista
import os


def get_city(city):

    with open("cities.json", "r", encoding="utf-8") as f_cities:
        return json.load(f_cities)[city]["locationId"]


def get_json_name_from_params(params):
    if not os.path.isdir("./dataset/"):
        os.makedirs("./dataset/")
    return os.path.join(
        "./dataset/",
        str(
            json.dumps(params)
            .replace('"', "")
            .replace(":", "=")
            .replace("{", "")
            .replace(" ", "")
            .replace(",", " ")
            .replace("}", "")
        )
        + ".json",
    )


def register_data(params, output):
    if not os.path.isfile(get_json_name_from_params(params)):
        with open(get_json_name_from_params(params), "x", encoding="utf-8") as f_data:
            json.dump(output, f_data)
    else:
        with open(get_json_name_from_params(params), "w", encoding="utf-8") as f_data:
            json.dump(output, f_data)


def read_idealista_secrets(keys_path):
    with open(os.path.join(keys_path, "api_key")) as f:
        key = f.readline()
    with open(os.path.join(keys_path, "secret")) as f:
        secret = f.readline()
    return key, secret


def get_available_cities():
    return [c for c in json.load(open("cities.json", "r"))]


def main():
    for c in get_available_cities():
        for n in range(1, 3):
            """
            #TODO:
            #! desacoplar diccionario params de la ciudad para poder elegir elegir los
            #! parametros de búsqueda en funcion de la ciudad

            """

            data = []
            print(f"Page:{n}")
            params = {
                "operation": "sale",
                "locationId": c,
                "locationLevel": 6,
                "propertyType": "homes",
                "locale": "es",
                "maxItems": 1,
                "maxPrice": 200000,
                "minPrice": 100000,
                "numPage": n,
            }

            idealista = Idealista(
                *read_idealista_secrets(f"{os.path.expanduser('~')}/.idealista_keys")
            )
            data.append(idealista.make_request("POST", params, country="es"))

            register_data(params, data)


if __name__ == "__main__":
    main()
