from typing import List
from docx import Document
from htmldocx import HtmlToDocx
from os import listdir
import json
from dateutil.parser import isoparse


class Extractor:
    def __init__(self, input_files_path: str) -> None:
        self.input_files_path = input_files_path 

    def list_ordered_files(self):
        files = listdir(self.input_files_path)
        files = sorted(files, reverse=True)
        files = [self.input_files_path + "/" + file for file in files]
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

        self.document.save(OUTPUT_FILE_NAME)
    
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
        self.parser.add_html_to_document("<h1>" + self.get_post_title_str(post_data) + "</h1>", self.document)
        self.parser.add_html_to_document("<br />", self.document)

    def get_post_title_str(self, post_data):
        publish_date = self.get_publish_datetime(post_data)
        return "[" + publish_date.strftime("%Y-%m-%d") + "] " + post_data["title"]

    def get_publish_datetime(self, post_data):
        raw_datetime = post_data["published"]
        return isoparse(raw_datetime)
    
    def write_body(self, post_data):
        self.parser.add_html_to_document(post_data["content"], self.document)

    
INPUT_FILES_PATH_TEST = "/Users/sancraja/Desktop/expt/blog_export_node/test"
VOL1 = "2021_2023"
VOL2 = "2017_2020"
VOL3 = "2011_2016"
VOL4 = "2006_2010"

CURR_VOL = VOL1

INPUT_FILES_PATH = "/Users/sancraja/Desktop/expt/happinessofbeing/{}".format(CURR_VOL)
OUTPUT_FILE_NAME = "doc_output/{}.docx".format(CURR_VOL)

def main():
    extractor = Extractor(input_files_path=INPUT_FILES_PATH)  # TODO: change this parameter 
    post_files = extractor.list_ordered_files()

    writer = Writer(post_files=post_files)
    writer.make_book()


main()
