* The script exportBlog.ts exports a blogger blog as json files.
  * To run it, ensure you are on the latest node version.
  * Ensure BLOG_ID of the blog to export and google API_KEY are available in a .env file in project root
  * Might have to use one of the blogger APIs to get the blog id using the blog url or something
  * Ensure MAX_PAGES, PAGE_SIZE, TOTAL_PAGES are set appropriately. Use the `getBlogDetails` to first get the total number of blogs
  * There is some code to export comments, but this is not supported fully and commented out.
  * Run the script using command:
    * `npx tsc && node build/index.js`
  * Posts are exported into a folder specified in `FOLDER_PREFIX` variable
* `main.py` is a python script that creates a word document out of the json files.
  * Use python `virtualenv` to run this. Run `source .venv/bin/activate` to activate virtualenv after setting up in VSCode or in any other way.
  * The script takes the input fiels path using `INPUT_FILES_PATH` variable. It doesn't create a single output file but can be used to create multiple volumes. To do this, run the script multiple times by setting the CURR_VOL variable.
  *
