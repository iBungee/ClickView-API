#!/usr/local/bin/python3


import json
import requests
import datetime
import re
import operator
import pprint
from flask import Flask, request
from flask_restplus import Resource, Api, fields, inputs, reqparse


app = Flask(__name__)
api = Api(app,
          default="ClickView Video",
          title="ClickView Video API",  # Documentation Title
          description="This is just a API for the purpose of a ClickView practical exam")  # Documentation Description

expectedVideoInformation = api.model(
    "video", {
    "name" : fields.String("Name of Video"),
    "duration" : fields.Integer("Video Length"),
    "description": fields.String("Descript of video"),
    "dateCreated": fields.DateTime(dt_format='rfc822'),
    "id" : fields.Integer("Date"),
    "thumbnail": fields.Url('todo_resource'),
	"folder": fields.String("Folder location"),
	"tags": fields.List(fields.String("Genres/Tags"))
    }
)

@api.route('/videos')
class Videos(Resource):
    @api.response(200, 'Successful')
    @api.doc(description="Gets all videos - This include all information associated with the video")
    def get(self):
        return db.getVideos();

    @api.response(201, 'New Video has been created')
    @api.response(200, 'Video already exists')
    @api.doc(description="Add a new video")
    @api.expect(expectedVideoInformation, validate=True)
    def post(self):
        payload = request.json
        id = payload['id']

        if db.idExistIn(id) == True:
            return {"message": "video has already been create"}, 201

        else:
            db.addVideo(payload)
            return {"message": "Created new video"}, 200

@api.route('/videos/<int:id>')
class VideosId(Resource):
    @api.response(404, 'Video was not found')
    @api.response(200, 'Successful')
    @api.doc(description="Delete a video by its ID")
    def delete(self, id):
        if (db.idExistIn(id) == False):
            api.abort(404, "video = {} doesn't exist".format(id))
        else:
            db.deleteId(id)
            return {"message": "Video = {} is removed".format(id)}, 200;

    @api.response(404, 'Video was not found')
    @api.response(200, 'Successful')
    @api.expect(expectedVideoInformation, validate=True)
    @api.doc(description="Replace video with everything you have inside payload box")
    def put(self, id):
        if (db.idExistIn(id) == False):
            api.abort(404, "video = {} doesn't exist".format(id))
        data = request.json
        db.updateVideoFile(id, data)
        return {"message": "Video = {} is updated".format(id)}, 200;

@api.route('/videos/folder/<string:folder>')
class VidoeosFolder(Resource):
    @api.response(404, 'videos was not found')
    @api.response(200, 'Successful')
    @api.doc(description="Get videos by folder. Folders must be input in format given in video.json e.g. 'Junior->English->Culture->USA'.")
    def get(self, folder):
        listOfVideos = db.byFolder(folder.replace(" ", ""))
        if len(listOfVideos) == 0:
            api.abort(404, "there are no videos inside {} ".format(folder))
        return listOfVideos

@api.route('/videos/tag/<string:tag>')
class VideosTag(Resource):
    @api.response(404, 'videos was not found')
    @api.response(200, 'Successful')
    @api.doc(description="Get a videos by its tag. Must be separated by comma and gets all videos that have any tags given E.g. 'USA, China'. Will fetch everything that has tag china and tag USA")
    def get(self, tag):
        listOfVideos = db.byTags(tag.replace(" ", ""));
        if len(listOfVideos) == 0:
            api.abort(404, "video with tag(s) {} doesn't exist".format(tag))
        return listOfVideos
"""
Supporter functions
"""
class dataBaseHandler():
    def __init__(self, startingFileName, storageSpace):
        self.__startingFileName = startingFileName
        self.__storageSpace = storageSpace
        self.__videoFile = self.__readVideoJson()

    def __readVideoJson(self):
        jsonFile = open(self.__startingFileName, "r") # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
        jsonFile.close() # Close the JSON file
        return data

    def __writeToDb(self):
        jsonFile = open(self.__storageSpace, "w+")
        jsonFile.write(json.dumps(self.getVideos()))
        jsonFile.close()

    def addVideo(self, data):
        self.__videoFile.append(data)
        self.__writeToDb()
        return;

    def getVideos(self):
        return self.__videoFile;

    def idExistIn(self,id):
        '''
        Check if this id exist
        '''
        #if not any(d['id'] == 'id' for d in videoFile):
        for video in self.getVideos():
            if(video['id'] == id):
                return True;
        return False;

    def deleteId(self,id):
        '''
        Delete video with id
        '''
        for i in range(len(self.getVideos())):
            if self.__videoFile[i]['id'] == id:
                del self.__videoFile[i]
                self.__writeToDb()
                return True;
        return False;

    def updateVideoFile(self,id, data):
        '''
        Updates our videos and changes accordingly
        '''
        for i in range(len(self.getVideos())):
            if self.__videoFile[i]['id'] == id:
                self.__videoFile[i] = data;
                self.__writeToDb()
                return True;
        return False;

    def byFolder(self, folders):
        '''
        This function searchs for videos with the folders that are input
        @return list of videos or empty list
        '''
        videosInsideFolder = list()

        for i in range(len(self.getVideos())):
            if self.__videoFile[i]['folder'] == folders:
                videosInsideFolder.append(self.__videoFile[i])
        return videosInsideFolder;

    def byTags(self, tags):
        '''
        This function searchs for videos with the tags that are input
        @pre: input variable must have no spaces
        @return list of videos or an empty list
        '''
        tagList = tags.split(",")
        videosWithTag = list()
        for i in range(len(self.getVideos())):
            for tag in self.__videoFile[i]['tags']:
                if tag in tagList:
                    videosWithTag.append(self.__videoFile[i])
                    break;
        return videosWithTag;

if __name__ == '__main__':
    db = dataBaseHandler("videos.json","newVideoFile.json")
    app.run(debug=True)
