import json
from Idealista import Idealista
import os


def get_city_location_id(city):

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
            json.dump(output, f_data, ensure_ascii=False)
    else:
        with open(get_json_name_from_params(params), "w", encoding="utf-8") as f_data:
            json.dump(output, f_data, ensure_ascii=False)


def read_idealista_secrets(keys_path):
    with open(os.path.join(keys_path, "api_key")) as f:
        key = f.readline()
    with open(os.path.join(keys_path, "secret")) as f:
        secret = f.readline()
    return key, secret


def get_available_cities(*excluded_cities):
    """
    excluded_cities: pass cities you want to exclude
    """
    return [c for c in json.load(open("cities.json", "r")) if c not in excluded_cities]


def main():
    n_pages_x_request = 100  # number of pages to query
    max_items_per_request = 50  # max current support is 50
    # num peticiones    = n_pages x n_cities
    idealista = Idealista(
        *read_idealista_secrets(f"{os.path.expanduser('~')}/.idealista_keys")
    )
    for c in get_available_cities("madrid"):
        print(f"City: {c}")
        for n_page in range(1, n_pages_x_request):
            """
            #TODO:
            #! desacoplar diccionario params de la ciudad para poder elegir elegir los
            #! parametros de búsqueda en funcion de la ciudad

            """

            data = []
            print(f"\tPage:{n_page}")
            params = {
                "operation": "sale",
                "locationId": get_city_location_id(c),
                "locationLevel": 6,
                "propertyType": "homes",
                "locale": "es",
                "maxItems": max_items_per_request,
                "maxPrice": 200000,
                "minPrice": 100000,
                "numPage": n_page,
            }

            data.append(idealista.make_request("POST", params, country="es"))
            register_data(params, data)


if __name__ == "__main__":
    main()
