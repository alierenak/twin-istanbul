import pandas as pd

def preprocess_hourly_transportation(path, file_paths):
    data_frames = {}
    for i in file_paths:
        file_path = f"{path}{i}"
        df = pd.read_csv(file_path)
        df.sort_values(by='DATE_TIME', inplace=True)
        data_frames[i] = df

    return data_frames

def preprocess_railway_stations(path):
    df = pd.read_csv(path)
    return df

# encoding problem
def fix_district_data(district_data_path):

    # Downloaded file has a problem about encoding the turkish characters
    content = open(district_data_path, encoding="ISO-8859-1").readlines()
    out = open(district_data_path[:-4]+"_corrected.csv", "w")
    correct_names = open("utils/mahalleler.txt").readlines()

    out.write(";".join(content[0].split(";")))
    for i, line in enumerate(content[1:]):
        line = line.split(";")
        tmp = correct_names[i].split()
        if len(tmp) != 2:
            tmp[1] = " ".join(tmp[1:])

        line[0] = tmp[0]
        line[1] = tmp[1]
        out.write(f"{';'.join(line)}")

def preprocess_district_and_data(district_data_path, ses_scores_path):

    # ses scores
    ses_scores = pd.read_excel(ses_scores_path)
    ses_scores.columns = ['ilce_adi', 'mahalle_adi', 'ses_level',  'ses_scores']

    # district data
    districts = pd.read_csv(district_data_path, delimiter=";")

    # merge ses scores to district data
    df = pd.merge(districts, ses_scores, on=['ilce_adi', 'mahalle_adi'])

    return df

def preprocess_daily_traffic_index(path):
    df = pd.read_csv(path)
    return df

def preprocess_gtfs_data(path):
    pass

def preprocess_all(path, file_paths):
    hourly_transportation_by_months = preprocess_hourly_transportation(path, file_paths["Hourly transportation data"])
    railway_stations = preprocess_railway_stations(f"{path}{file_paths['Railway station-based data'][0]}")

    # data about districts and buildings
    fix_district_data(f"{path}{file_paths['District and Social Economical Scores'][0]}")
    district_data = preprocess_district_and_data(f"{path}{file_paths['District and Social Economical Scores'][0][:-4]}_corrected.csv", f"{path}{file_paths['District and Social Economical Scores'][1]}")

    # daily traffic index in istanbul but not spesific to districts or anything
    daily_traffic_index = preprocess_daily_traffic_index(f"{path}{file_paths['Traffic Index Data'][0]}")

    # gtfs data
    # preprocess_gtfs_data(f"{path}{file_paths['GTFS Data']}")

    return {
        'hourly transportation': hourly_transportation_by_months,
        'railway_stations': railway_stations,
        'district_data': district_data,
        'daily_traffic_index': daily_traffic_index
    }