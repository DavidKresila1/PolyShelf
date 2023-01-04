from crypt import methods
from unittest import result
from flask import Blueprint, render_template, session, redirect, request, flash, send_from_directory, jsonify
from flask_login import login_required, current_user
from app import uploadFolder, app
import os
from werkzeug.utils import secure_filename
import json
from models import User
import shutil
from controllers import UploadFile, CreateDirectory, ChangeDirectory

main = Blueprint("main", __name__, template_folder="templates")


def currentDirectory():
    return app.config["UPLOAD_FOLDER"] + session["current_dir"]


def getSize(startPath):
    totalSize = 0
    for dirpath, dirnames, filenames in os.walk(startPath):
        for file in filenames:
            filepath = os.path.join(dirpath, file)
            totalSize += os.path.getSize(filepath)
    return totalSize


def setCurrenturDirectory(directoryName):
    if directoryName == ".":
        session["current_dir"] = "/" + str(current_user.id)
    elif directoryName == "..":
        rem = session["current_dir"].split("/")
        if len(rem) > 0:
            rem.pop()
        session["current_dir"] = ""
        for file in rem[1:]:
            session["current_dir"] += "/" + file
    elif directoryName != "":
        session["current_dir"] += "/" + directoryName

    if len(session["current_dir"]) <= 1:
        session["current_dir"] = "/" + str(current_user.id)


@main.route("/")
def index():
    return render_template("index.html")


@main.context_processor
def user_auth():
    def is_logged_in():
        return current_user.is_authenticated
    return dict(is_logged_in=is_logged_in)


@main.route("/drive")
@login_required
def drive():
    if current_user.is_authenticated:
        if not "current_dir" in session:
            session["current_dir"] = "/" + str(current_user.id)
        return render_template("drive.html",
                               u_form=UploadFile(),
                               d_form=CreateDirectory(),
                               dir=session['current_dir'])
    return redirect("/login")


@main.route("/upload", methods=["POST"])
def uploadFile():
    if "file" in request.files:
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(currentDirectory(), filename))
    else:
        flash("Chyba pri nahrávaný súboru")
    return redirect("drive")


@main.route("/makedir", methods=["POST"])
def createDirectory():
    form = CreateDirectory(request.form)
    if form.validate_on_submit():
        directoryName = form.directoryName.data
        try:
            if not directoryName == "public":
                os.makedirs(currentDirectory() + "/" + directoryName)
            else:
                flash("Meno je rezervované")
                raise OSError("reserverd name")
        except OSError:
            flash("Nepodarilo sa vytvoriť priečinok")
    else:
        flash("Chyba")
    return redirect("drive")


@main.route("/getFiles", methods=["GET"])
def getFiles():
    files = []
    fileSize = []
    folders = []
    folderSize = []
    if current_user.is_authenticated:
        for file in os.listdir(currentDirectory()):
            path = currentDirectory() + "/" + file
            if file != ".DS_Store":
                if os.path.isfile(path):
                    files.append(file)
                    fileSize.append(os.stat(path).st_size)
                if os.path.isdir(path):
                    folders.append(file)
                    folderSize.append(getSize(path))

        files = json.dumps(files)
        fileSize = json.dumps(fileSize)
        folders = json.dumps(folders)
        folderSize = json.dumps(folderSize)

        return jsonify(
            files=files,
            fileSize=fileSize,
            folders=folders,
            folderSize=folderSize
        )
    else:
        return redirect("/login")


@main.route("/changedir", methods=["POST"])
def changeDir():
    if current_user.is_authenticated:
        directoryName = request.json["change_dir"]
        if (directoryName == ".." or directoryName == "." or directoryName in os.listdir(currentDirectory())) and os.path.isdir(currentDirectory() + "/" + directoryName):
            setCurrentDirectory(directoryName)
            return jsonify(result="success",
                           directory=str(session["current_dir"]),
                           current=currentDirectory()
                           )
        else:
            return jsonify(result="failed")


@main.route("/getfile/<filename>", methods=["GET"])
def getFile(filename):
    if current_user.is_authenticated:
        absolutePath = currentDirectory() + "/" + filename
        if filename in os.listdir(currentDirectory()) and os.path.isfile(absolutePath):
            return send_from_directory(currentDirectory(), filename)
    else:
        return render_template("404.html")


@main.route("/delete", methods=["POST"])
def deleteFile():
    if current_user.is_authenticated:
        try:
            filename = request.json["del_file"]
            absolutePath = currentDirectory() + "/" + filename
            if filename in os.listdir(currentDirectory()):
                if os.path.isfile(absolutePath):
                    os.unlink(currentDirectory() + "/" + filename)
                elif os.path.isdir(absolutePath):
                    shutil.rmtree(absolutePath)
                else:
                    return jsonify(result="failed")
                return jsonify(result="success")
            return jsonify(result="failed")
        except:
            return jsonify(result="failed")
    return redirect("/login")
