import urllib.request
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests, validators, uuid, pathlib, os


def image_handler(specific_element, requested_url):

    image_paths = []

    images = [img["src"] for img in specific_element]
    for i in specific_element:
        image_path = i.attrs["src"]
        valid_imgpath = validators.url(image_path)

        if valid_imgpath == True:
            full_path = image_path

        else:
            full_path = urljoin(requested_url, image_path)
            image_paths.append(full_path)

    return image_paths


def main(requested_url="https://ondiek-elijah.me/"):
    try:
        source = requests.get(requested_url).text
        # parser library?
        soup = BeautifulSoup(source, "html.parser")

        specific_element = soup.find_all("img")

        counter = len(specific_element)

        image_paths = image_handler(specific_element, requested_url)

        # return {
        #     "url": requested_url,
        #     "counter": counter,
        #     "image_paths": image_paths,
        #     "results": specific_element,
        # }

        downloader(specific_element, requested_url)

    except BaseException as error:
        raise "An exception occurred: {}".format(error)


def downloader(specific_element, requested_url):
    try:
        for img in image_handler(specific_element, requested_url):
            image_url = img

            filename = str(uuid.uuid4())
            file_ext = pathlib.Path(image_url).suffix

            picture_filename = filename + file_ext

            downloads_path = str(pathlib.Path.home() / "Desktop")

            picture_path = os.path.join(downloads_path, picture_filename)

            urllib.request.urlretrieve(image_url, picture_path)

    except BaseException as error:
        raise "An exception occurred: {}".format(error)

    return downloader


main()
