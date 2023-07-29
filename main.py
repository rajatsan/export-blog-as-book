from typing import List
from docx import Document
from htmldocx import HtmlToDocx
from os import listdir
import json
from datetime import datetime, date


class Extractor:
    def __init__(self, exports_path: str) -> None:
        self.exports_path = exports_path 

    def list_ordered_files(self):
        files = listdir(self.exports_path)
        files = sorted(files, reverse=True)
        files = [self.exports_path + "/" + file for file in files]
        return files


class Writer:
    def __init__(self, post_files: List[str]) -> None:
        self.document = Document()
        self.parser = HtmlToDocx()
        self.post_files = post_files

    def make_book(self):
        print("Making book...")

        for post_file in self.post_files:
            print("Writing post", post_file)
            self.write_post_from_file(post_file)

        self.document.save(EXPORT_FILE_NAME)
    
    def get_post_data(self, location):
        with open(location, "r") as f:
          content = f.read()
        return json.loads(content)

    def write_post_from_file(self, post_file):
        post_data = self.get_post_data(post_file)
        self.write_header(post_data)
        self.write_body(post_data)
        self.document.add_page_break()

    def write_header(self, post_data):
        title = post_data["title"]
        self.parser.add_html_to_document("<h1>" + title + "</h1>", self.document)
        self.parser.add_html_to_document("<h4>" + self.get_publish_date(post_data=post_data) + "</h4>", self.document)
        self.parser.add_html_to_document("<br />", self.document)


    def get_publish_date(self, post_data):
        raw_datetime = post_data["published"]
        d = datetime.fromisoformat(raw_datetime)
        parsed = d.strftime("%A, %d %B %Y")
        return parsed
    
    def write_body(self, post_data):
        self.parser.add_html_to_document(post_data["content"], self.document)

    
EXPORTS_PATH_TEST = "/Users/sancraja/Desktop/expt/happinessofbeing_test"
VOL1 = "2021_2023"
VOL2 = "2017_2020"
VOL3 = "2011_2016"
VOL4 = "2006_2010"

CURR_VOL = VOL4

EXPORTS_PATH = "/Users/sancraja/Desktop/expt/happinessofbeing/{}".format(CURR_VOL)
EXPORT_FILE_NAME = "{}.docx".format(CURR_VOL)

def main():
    extractor = Extractor(exports_path=EXPORTS_PATH)
    post_files = extractor.list_ordered_files()

    writer = Writer(post_files=post_files)
    writer.make_book()


main()
