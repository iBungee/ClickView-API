# ClickView-API
HOW TO RUN FILE
Please install all python requirements in requirements.txt file (run command "pip3 install -r requirements.txt")
Run python3 api.py (run command "python3 api.py")


Notes you should know:


Create a new video (POST)
- Follow the example given you
- Does not require all variables

Retrieve all videos (GET)
- Gets you all videos

Update an existing video (PUT)
- Will replace with everything inside the payload

Delete an existing video (DELETE)
-Nothing speical about this one

fetch videos by folder (GET - /folder/{folder})
- Folders must be input in format given in video.json e.g. "Junior->English->Culture->USA".

fetch videos by Tag (GET - /tag/{tag})
- Must be separated by comma  
- Gets all videos that have any tags given E.g. 'USA, China'. Will fetch everything that has tag china and tag USA
