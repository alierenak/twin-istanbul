import pandas as pd
import uuid
import os

def create_twin_istanbul(data_frames, service_client):

    # MODEL
    id = uuid.uuid4()
    istanbul = {
            "@id": id,
            "@type": "Interface",
            "@context": "dtmi:dtdl:context;2",
            "displayName": "twin istanbul",
            "contents": [
                {
                    "@type": ["Telemetry", "Traffic Index"],
                    "name": "traffic index",
                    "unit": "index",
                    "schema": "integer"
                },
            ]
        }

    station_ids = {}
    cities = []
    for city in data_frames['district_data'].ilce_adi.unique():
        city_id  = uuid.uuid4()
        city_dt = {
            "@id": city_id,
            "@type": "Interface",
            "@context": "dtmi:dtdl:context;2",
            "displayName": f"{city}",
            "contents": [
                {
                    "@type": ["Telemetry", "Traffic Index"],
                    "name": "traffic index",
                    "unit": "index",
                    "schema": "integer"
                },
                {
                    "@type": "Relationship",
                    "@id": city_id,
                    "name": "is_city_of_istanbul",
                    "displayName": f"Istanbul has {city}",
                    "target": f"dtmi:com:adt:dtsample:{city};1",
                    "properties": [
                    ]
                }
            ]
        }
        for i, district in data_frames['district_data'][data_frames['district_data'].ilce_adi == city].iterrows():
            district_dt = {
              "@type": "Property",
              "name": f"{district.mahalle_adi}",
              "schema": {
                "@type": "Object",
                "fields": [
                    {
                    "1980_oncesi": f"{district['1980_oncesi']}",
                    "schema": "string"
                    },
                    {
                    "1980-2000_arasi": f"{district['1980-2000_arasi']}",
                    "schema": "string"
                    },
                    {
                    "2000_sonrasi": f"{district['2000_sonrasi']}",
                    "schema": "string"
                    },
                    {
                    "1-4 kat_arasi": f"{district['1-4 kat_arasi']}",
                    "schema": "string"
                    },
                    {
                    "5-9 kat_arasi": f"{district['5-9 kat_arasi']}",
                    "schema": "integer"
                    },
                    {
                    "9-19 kat_arasi": f"{district['9-19 kat_arasi']}",
                    "schema": "integer"
                    },
                    {
                    "ses_level": f"{district.ses_level}",
                    "schema": "string"
                    },
                    {
                    "ses_scores": f"{district.ses_scores}",
                    "schema": "integer"
                    },
                    {
                        "@type": ["Telemetry", "Dense Index"],
                        "name": "station dense index",
                        "unit": "dense",
                        "schema": "integer"
                    },
                ]
              }
            }
            city_dt['contents'].append(district_dt)

            for i, row in data_frames['railway_stations'][data_frames['railway_stations'].TOWN == city].iterrows():
                station_id = uuid.uuid4()
                station_ids[row.STATION_NAME] = station_id
                station_dt = {
                  "@id": station_id,
                  "@type": "Property",
                  "name": f"{row.STATION_NAME}",
                  "schema": {
                    "@type": "Object",
                    "fields": [
                        {
                            "line": f"{row.LINE}",
                            "schema": "string"
                        },
                        {
                            "code": f"{row.STATION_NUMBER}",
                            "schema": "integer"
                        },
                        {
                            "latitude": f"{row.LATITUDE}",
                            "schema": "float"
                        },
                        {
                            "longitude": f"{row.LONITUDE}",
                            "schema": "float"
                        },

                    ]
                  }
                }
                city_dt['contents'].append(station_dt)

            cities.append(city)

    models = service_client.create_models(istanbul, cities)
    print(models, "created!")

    ## TELEMETRIES
    for i, row in data_frames['daily_traffic_index'].iterrows():
        service_client.publish_component_telemetry(
            id,
            "traffic index",
            {
                'date': row.TRAFFIC_INDEX_DATE,
                'traffic_index': row.AVARAGE_TRAFIC_INDEX
             }
        )

    curr = 0
    while True:
        time_stamps = os.listdir('data/traffic_index/')
        time_stamps = [int(i.split('.')[0]) for i in time_stamps]

        last = max(time_stamps)
        if last != curr:
            df = pd.read_csv(f"daata/traffic_index/{last}.csv")
            for i, row in df.iterrows():
                id = station_ids[row.STATION_NAME]
                service_client.publish_component_telemetry(
                    id,
                    "traffic index",
                    {
                        'timestamp': last,
                        'traffic_index': row.traffic_index
                    }
                )
