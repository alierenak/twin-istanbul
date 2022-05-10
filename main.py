from downloader import download_dataset
from preprocessor import preprocess_all




if __name__ == "__main__":

    path, file_paths = download_dataset()
    preprocess_all(path, file_paths)
