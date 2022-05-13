import os
import json
import asyncio

from azure.identity import DefaultAzureCredential
from azure.digitaltwins.core import DigitalTwinsClient

from downloader import download_dataset
from preprocessor import preprocess_all
from dt_manager import create_twin_istanbul
from traffic_manager import traffic_flow_tiles


if __name__ == "__main__":

    # DefaultAzureCredential supports different authentication mechanisms and determines the appropriate credential type based of the environment it is executing in.
    # It attempts to use multiple credential types in an order until it finds a working credential.
    env = json.loads(open("variables.env").read())
    for k, v in env.items():
        os.environ[k] = v

    # - AZURE_URL: The URL to the ADT in Azure
    url = os.getenv("AZURE_URL")

    credential = DefaultAzureCredential()
    service_client = DigitalTwinsClient("https://twin-istanbul.api.weu.digitaltwins.azure.net", credential)

    # download data if needed!
    path, file_paths = download_dataset()

    # load data to pandas dataframe, preprocess if needed
    data_frames = preprocess_all(path, file_paths)

    # create digital twin instance in Azure
    create_twin_istanbul(data_frames, service_client)

    #  will continue to extract traffic tiles per 5 minutes
    asyncio.run(traffic_flow_tiles(data_frames))

