import json

from uuid import uuid4

from domain import (
    ExternalMediaIDs,
    OperationContext,
)

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

def radarr_rescan_movie(host, api_key, context):
    host = host
    api_key = api_key
    client = HTTPClient()
    adapter = RadarrAPIAdapter(
        client,
        host=host,
        api_key=api_key
    )

    media_ids = ExternalMediaIDs.create(105)

    print("Radarr: Rescanning movie...")
    adapter.rescan_movie(media_ids, context)

    print("OK")

def radarr_get_moviefile(host, api_key, context):
    host = host
    api_key = api_key
    client = HTTPClient()
    adapter = RadarrAPIAdapter(
        client,
        host=host,
        api_key=api_key
    )

    media_ids = ExternalMediaIDs.create(105)

    print("Radarr: Fetching movie files...")
    file = adapter.get_moviefile(media_ids, context)

    print("Path:", file.path)

def jellyfin_refresh_library(host, api_key, context):
    client = HTTPClient()
    adapter = JellyfinAPIAdapter(
        client,
        host=host,
        api_key=api_key
    )

    print("Jellyfin: Attempting library refresh...")
    ok = adapter.refresh_library(context)

    print("OK")

def main():
    context = OperationContext.create()
    radarr_host = get_value_from_json("secrets.json", "radarr", "host")
    radarr_api_key = get_value_from_json("secrets.json", "radarr", "api_key")
    jellyfin_host = get_value_from_json("secrets.json", "jellyfin", "host")
    jellyfin_api_key = get_value_from_json("secrets.json", "jellyfin", "api_key")

    # radarr_get_moviefile(radarr_host, radarr_api_key, context)
    # radarr_rescan_movie(radarr_host, radarr_api_key, context)
    jellyfin_refresh_library(jellyfin_host, jellyfin_api_key, context)

if __name__ == "__main__":
    main()