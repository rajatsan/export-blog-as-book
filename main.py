from typing import List
from docx import Document
from htmldocx import HtmlToDocx
from os import listdir
import json
from datetime import datetime


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

    
INPUT_FILES_PATH_TEST = "/Users/sancraja/Desktop/expt/blog_export_node/test"
VOL1 = "2021_2023"
VOL2 = "2017_2020"
VOL3 = "2011_2016"
VOL4 = "2006_2010"

CURR_VOL = VOL4

INPUT_FILES_PATH = "/Users/sancraja/Desktop/expt/happinessofbeing/{}".format(CURR_VOL)
OUTPUT_FILE_NAME = "{}.docx".format(CURR_VOL)

def main():
    extractor = Extractor(input_files_path=INPUT_FILES_PATH_TEST)  # TODO: change this parameter 
    post_files = extractor.list_ordered_files()

    writer = Writer(post_files=post_files)
    writer.make_book()


main()
