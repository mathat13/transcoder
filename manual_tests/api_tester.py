import json

from infrastructure import (
    RadarrAPIAdapter,
    JellyfinAPIAdapter,
    HTTPClient
)

def get_value_from_json(json_file, key, sub_key):
   try:
       with open(json_file) as f:
           data = json.load(f)
           return data[key][sub_key]
   except Exception as e:
       print("Error: ", e)

def radarr_api_calls(host, api_key):
    host = get_value_from_json("secrets.json", "radarr", "host")
    api_key = get_value_from_json("secrets.json", "radarr", "api_key")
    client = HTTPClient()
    adapter = RadarrAPIAdapter(
        client,
        host=host,
        api_key=api_key
    )

    movie_id = 105

    print("Radarr: Rescanning movie...")
    ok = adapter.rescan_movie(movie_id)

    print("OK:", ok)

    print("Radarr: Fetching movie files...")
    files = adapter.get_moviefile(movie_id)

    print("OK:", ok)

def jellyfin_api_calls(host, api_key):
    client = HTTPClient()
    adapter = JellyfinAPIAdapter(
        client,
        host=host,
        api_key=api_key
    )

    print("Jellyfin: Attempting library refresh...")
    ok = adapter.refresh_library()

    print("OK:", ok)

def main():
    radarr_host = get_value_from_json("secrets.json", "radarr", "host")
    radarr_api_key = get_value_from_json("secrets.json", "radarr", "api_key")
    radarr_api_calls(radarr_host, radarr_api_key)

    jellyfin_host = get_value_from_json("secrets.json", "jellyfin", "host")
    jellyfin_api_key = get_value_from_json("secrets.json", "jellyfin", "api_key")
    jellyfin_api_calls(jellyfin_host, jellyfin_api_key)

if __name__ == "__main__":
    main()