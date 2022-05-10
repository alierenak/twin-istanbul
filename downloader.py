import os
import wget
import logging
import ssl

# IMM Data Portal causes SSL error when this line uncommented.
ssl._create_default_https_context = ssl._create_unverified_context
logging.basicConfig()
logging.root.setLevel(logging.NOTSET)

dataset_links = {
    "Hourly transportation data": {
        'hourly_transportation_202001.csv': "https://data.ibb.gov.tr/dataset/a6855ce7-4092-40a5-82b5-34cf3c7e36e3/resource/511c5034-0a1c-4c77-9831-157f30e62aee/download/hourly_transportation_202001.csv",
        'hourly_transportation_202002.csv': "https://data.ibb.gov.tr/dataset/a6855ce7-4092-40a5-82b5-34cf3c7e36e3/resource/de831d1d-85a3-478e-8167-72223ee7ffaa/download/hourly_transportation_202002.csv",
        "hourly_transportation_202003.csv": "https://data.ibb.gov.tr/dataset/a6855ce7-4092-40a5-82b5-34cf3c7e36e3/resource/fb49c73d-f0f5-439c-ad7b-64f3494a2d9f/download/hourly_transportation_202003.csv",
        "hourly_transportation_202004.csv": "https://data.ibb.gov.tr/dataset/a6855ce7-4092-40a5-82b5-34cf3c7e36e3/resource/75e25417-36df-4822-8a18-578f0f7a584a/download/hourly_transportation_202004.csv",
        "hourly_transportation_202005.csv": "https://data.ibb.gov.tr/dataset/a6855ce7-4092-40a5-82b5-34cf3c7e36e3/resource/3497a04f-5b78-44f3-8bdc-8c30ab19af88/download/hourly_transportation_202005.csv",
        "hourly_transportation_202006.csv": "https://data.ibb.gov.tr/dataset/a6855ce7-4092-40a5-82b5-34cf3c7e36e3/resource/4f1c434d-bd1f-4937-b88f-6e2df1a85dc5/download/hourly_transportation_202006.csv",
        "hourly_transportation_202007.csv": "https://data.ibb.gov.tr/dataset/a6855ce7-4092-40a5-82b5-34cf3c7e36e3/resource/0fdf0efb-2ae3-4ff5-a106-0c6c7392f6d4/download/hourly_transportation_202007.csv",
        "hourly_transportation_202008.csv": "https://data.ibb.gov.tr/dataset/a6855ce7-4092-40a5-82b5-34cf3c7e36e3/resource/a195a42f-727a-4f1e-ad55-471306788c99/download/hourly_transportation_202008.csv",
        "hourly_transportation_202009.csv": "https://data.ibb.gov.tr/dataset/a6855ce7-4092-40a5-82b5-34cf3c7e36e3/resource/5b3b12b7-575d-4b55-b497-62e3b544edb0/download/hourly_transportation_202009.csv",
        "hourly_transportation_202010.csv": "https://data.ibb.gov.tr/dataset/a6855ce7-4092-40a5-82b5-34cf3c7e36e3/resource/d5b65aa8-8cf0-4034-a827-17e170894b38/download/hourly_transportation_202010.csv",
        "hourly_transportation_202011.csv": "https://data.ibb.gov.tr/dataset/a6855ce7-4092-40a5-82b5-34cf3c7e36e3/resource/4691d5de-689e-4b0a-b5e7-5e54f893edfc/download/hourly_transportation_202011.csv",
        "hourly_transportation_202012.csv": "https://data.ibb.gov.tr/dataset/a6855ce7-4092-40a5-82b5-34cf3c7e36e3/resource/0d822ea9-bd44-4f09-a2aa-27f1b37e4538/download/hourly_transportation_202012.csv",
        'hourly_transportation_202101.csv': "https://data.ibb.gov.tr/dataset/a6855ce7-4092-40a5-82b5-34cf3c7e36e3/resource/004994f5-3a50-4721-8787-41d4940bdaee/download/hourly_transportation_202101.csv",
        'hourly_transportation_202102.csv': "https://data.ibb.gov.tr/dataset/a6855ce7-4092-40a5-82b5-34cf3c7e36e3/resource/a22578e4-3c72-454b-a9e4-d843b7e649e8/download/hourly_transportation_202102.csv",
        "hourly_transportation_202103.csv": "https://data.ibb.gov.tr/dataset/a6855ce7-4092-40a5-82b5-34cf3c7e36e3/resource/ef77dde9-9e0c-4417-a939-3ca4013ef919/download/hourly_transportation_202103.csv",
        "hourly_transportation_202104.csv": "https://data.ibb.gov.tr/dataset/a6855ce7-4092-40a5-82b5-34cf3c7e36e3/resource/7a86010b-2c38-4639-a13d-87155649b234/download/hourly_transportation_202104.csv",
        "hourly_transportation_202105.csv": "https://data.ibb.gov.tr/dataset/a6855ce7-4092-40a5-82b5-34cf3c7e36e3/resource/42b4a830-fee6-4765-9daf-3f3884f09b4b/download/hourly_transportation_202105.csv",
    },
    "Railway station-based data": {
        "railway_station_based_data.csv": "https://data.ibb.gov.tr/tr/dataset/ae3b2e4b-073a-48d0-8ef3-f28f19bcb19c/resource/604776d6-e99f-469c-bf25-25ccadc5e89b/download/rayl-sistemler-istasyon-bazl-yolcu-ve-yolculuk-saylar.csv"
    },
    "District and Social Economical Scores": {
        "district_and_building_counts.csv": "https://data.ibb.gov.tr/tr/dataset/be3582eb-09d7-42f8-84d3-b3817dc9ab0a/resource/cef193d5-0bd2-4e8d-8a69-275c50288875/download/2017-yl-mahalle-bazl-bina-saylar.csv",
        "ses_scores.xlsx": "https://data.ibb.gov.tr/tr/dataset/96e8a63a-649b-4b4b-86e1-5bd2481ac04c/resource/859f3f2d-d06e-4f1c-ba3d-5fcf89744048/download/2016-yl-mahallem-istanbul-ses-skorlar.xlsx",
    },
    "Traffic Index Data": {
        "daily_traffic_index.csv": "https://data.ibb.gov.tr/tr/dataset/b3fbb6ce-03a5-4777-8c6c-111c73775523/resource/ba47eacb-a4e1-441c-ae51-0e622d4a18e2/download/traffic_index.csv"
    },
    "GTFS Data": {
        "gtfs_calendar.csv": "https://data.ibb.gov.tr/tr/dataset/121a9892-7945-419a-9b89-49f6083926df/resource/c84ca913-29ac-4f15-87cd-076aef3dccd6/download/calendar.csv",
        "gtfs_routes.csv": "https://data.ibb.gov.tr/tr/dataset/121a9892-7945-419a-9b89-49f6083926df/resource/36b554c7-cae0-4b7e-978f-fc6a43664e88/download/routes.csv",
        "gtfs_shapes.csv": "https://data.ibb.gov.tr/tr/dataset/121a9892-7945-419a-9b89-49f6083926df/resource/83317085-aa56-41b0-9447-ea579567f2cb/download/shapes.csv",
        "gtfs_stop_times.csv": "https://data.ibb.gov.tr/tr/dataset/121a9892-7945-419a-9b89-49f6083926df/resource/ac646b83-3b6f-4ca2-afb4-9071ab44d9af/download/stop_times.csv",
        "gtfs_stops.csv": "https://data.ibb.gov.tr/tr/dataset/121a9892-7945-419a-9b89-49f6083926df/resource/d1f7c258-bbc1-406f-9ab2-7a7c1797c673/download/stops.csv",
        "gtfs_trips.csv": "https://data.ibb.gov.tr/tr/dataset/121a9892-7945-419a-9b89-49f6083926df/resource/dcee1700-e59f-4a5f-8009-f602045a4507/download/trips.csv"
    }

}

traffic_index_api_url = "https://api.ibb.gov.tr/tkmservices/api/TrafficData/v1/TrafficIndexHistory/"

def download_dataset():

    for dataset, info in dataset_links.items():
        logging.info(f"{dataset} is downloading...")
        for path, url in info.items():
            if not os.path.isfile(f'./data/{path}'):
                filename = wget.download(url, out=f"./data/{path}")
                logging.info(f"{filename} is downloaded.")
            else:
                logging.warning(f'{path} was already downloaded. Skipping...')
    logging.info("Download completed!\n")

    file_paths = {k:list(v.keys()) for k, v in dataset_links.items()}

    return f"./data/", file_paths

