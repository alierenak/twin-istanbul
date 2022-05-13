import os
import math
import aiohttp
import aiofiles
from PIL import Image
import time

from geopy import distance
import pandas as pd

import seaborn as sns
import numpy as np
import json

import logging
logging.basicConfig()
logging.root.setLevel(logging.NOTSET)

env = json.loads(open("variables.env").read())
for k, v in env.items():
    os.environ[k] = v

async def get_tiles(format_="png", increase_zoom=4):

    substriction_key = os.getenv("SUBSCRIPTION_KEY")
    style = "absolute"

    zoom = 10 + increase_zoom

    # left-upper bound
    x1 = 593 * 2**increase_zoom
    y1 = 382 * 2**increase_zoom

    # right-bottom bound
    x2 = ((593+2) * 2**increase_zoom) + increase_zoom
    y2 = ((382+2) * 2**increase_zoom) + increase_zoom

    files = {}
    async with aiohttp.ClientSession(trust_env=True) as session:
        # for i, tile in enumerate(tiles):
        curr_x = x1
        while curr_x < x2:
            curr_y = y1
            while curr_y < y2:
                async with session.get(
                        f"https://atlas.microsoft.com/traffic/flow/tile/{format_}?subscription-key={substriction_key}&api-version=1.0&style={style}&zoom={zoom}&x={curr_x}&y={curr_y}",
                        ssl=False) as resp:
                    if resp.status == 200:
                        f = await aiofiles.open(f'utils/map{curr_x}-{curr_y}.{format_}', mode='wb')
                        await f.write(await resp.read())
                        await f.close()
                        files[f"{curr_x-x1},{curr_y-y1}"] = f'utils/map{curr_x}-{curr_y}.{format_}'
                    else:
                        logging.warning(resp)
                curr_y+=1
            curr_x+=1

    return files, (x1, y1), (x2, y2)

def preprocess_png_tiles(tiles, x1, x2):
    size = x2-x1
    new_tile = Image.new("RGB", (size*256, size*256), "white")
    for tile, path in tiles.items():
        img = Image.open(path)
        x, y = tile.split(',')
        new_tile.paste(img, (int(x)*256, int(y)*256))
        os.remove(path)

    new_tile.save("utils/concat.png")
    return "utils/concat.png"

def get_coordinates_of_pixel(pixelX, pixelY, tileSize):
    # https://docs.microsoft.com/en-us/azure/azure-maps/zoom-levels-and-tile-grid?tabs=csharp
    tmp = math.e ** ((0.5 - pixelY / (tileSize * math.pow(2, 14))) * 4 * math.pi)
    sinLatitude = (tmp - 1) / (tmp + 1)
    latitude = math.asin(sinLatitude) * 180 / math.pi
    longitude = 360 * pixelX / (math.pow(2, 14) * tileSize) - 180
    return longitude, latitude

def get_dense_coordinates(path, coordinate1, coordinate2):

    img = Image.open(path).load()
    tileSize = 256 * (coordinate2[0]-coordinate1[0])

    x = 0
    vector_tile = np.zeros((tileSize, tileSize))
    while x < tileSize:
        y=0
        while y < tileSize:
            curr_heat = img[x, y][0] - img[x, y][1]
            if x != 0:
                pix = img[x-1, y]
                if pix[0] - pix[1] < curr_heat:
                    curr_heat += 50

            if x != tileSize-1:
                pix = img[x + 1, y]
                if pix[0] - pix[1] < curr_heat:
                    curr_heat += 50

            if y != 0:
                pix = img[x, y-1]
                if pix[0] - pix[1] < curr_heat:
                    curr_heat += 50

            if y != tileSize-1:
                pix = img[x - 1, y]
                if pix[0] - pix[1] < curr_heat:
                    curr_heat += 50

            vector_tile[y][x] = curr_heat
            y+=1
        x+=1

    # sns.heatmap(vector_tile).get_figure().savefig("utils/heatmap.png")
    pixelStartX = 256 * coordinate1[0]
    pixelStartY = 256 * coordinate1[1]

    indices = np.nonzero(vector_tile > 350)
    coordinates = []
    for i in range(len(indices[1])):
        x = indices[1][i]
        y = indices[0][i]
        long, lat = get_coordinates_of_pixel(pixelStartX+x, pixelStartY+y, tileSize)
        coordinates.append((long, lat))

    return coordinates

async def traffic_flow_tiles(data_frames):

    while True:

        tiles, coordinate1, coordinate2 = await get_tiles(format_="png")

        # Create concatanated png 
        time_stamp = time.time()
        concat_path = preprocess_png_tiles(tiles, coordinate1[0], coordinate2[0])

        # extract density date
        coordinates = get_dense_coordinates(concat_path, (593 * 2**4, 382 * 2**4), (((593+2) * 2**4) + 4, ((382+2) * 2**4) + 4))

        railway_stations = data_frames['railway_stations']
        unique_station_names = railway_stations['STATION_NAME'].drop_duplicates()
        stations = railway_stations.iloc[unique_station_names.index.to_list()]
        traffic_index = np.zeros(len(stations))
        for i in coordinates:
            for j, row in stations.iterrows():
                s_x = row['LONGITUDE']
                s_y = row['LATITUDE']
                if pd.notna(s_x) and pd.notna(s_y):
                    dist = distance.geodesic((i[1], i[0], ), (s_y, s_x)).km
                    if dist < 3:
                        traffic_index[j] += 1

        stations['traffic_index'] = traffic_index
        stations.to_csv(f'utils/traffic_index/{time_stamp}.csv')

        # wait 5m to get next traffic index
        current_time = time.time()
        run_time = current_time-time_stamp
        if run_time > 0:
            time.sleep(500-(run_time))
