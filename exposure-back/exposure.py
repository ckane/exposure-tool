#!/usr/bin/env python
from hashlib import file_digest
from flask import Flask, request, redirect
from policies.policy_checker import validate_policy
from datetime import datetime, timezone
import json
import os
import pathlib
import shutil
import tempfile

def validate_json(filename):
    # TODO: This function is mainly a placeholder to simulate validating the uploaded JSON is accurate
    #       and clean. This gets run before trying to do more work on the JSON right after upload.
    try:
        j = json.load(open(filename, 'rb'))
        if 'resources' not in j:
            return False
    except:
        return False
    return True

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024; # Limit uploads to 100MB (or whatever we want)
app.config['UPLOAD_FOLDER'] = '/data/reports'

# Fetch the data associated with a single report
@app.route("/report/<rpt>", methods=['GET'])
def get_report(rpt):
    try:
        report_data = {'resources': []}
        meta_file = "{reports}/{h}/metadata.json".format(reports=app.config['UPLOAD_FOLDER'], h=rpt)
        with open(meta_file, 'rb') as meta_fh:
            meta_data = json.load(meta_fh)
            report_data['title'] = meta_data.get('title', 'NO TITLE')
        rpt_folder = "{reports}/{h}/resources".format(reports=app.config['UPLOAD_FOLDER'], h=rpt)
        for path in pathlib.Path(rpt_folder).glob('*'):
            if not path.is_dir():
                with open(path, 'rb') as rsrcfile:
                    jsondata = json.load(rsrcfile)
                    report_data['resources'].append(jsondata)

        return {"error": False, "message": "", "report": report_data}
    except:
        pass  # Route exceptions to the "return error" case - should do better inspection though

    return {"error": True, "message": f"Couldn't fetch report {rpt}"}

# For enumerating the most recent ten reports in the tool
@app.route("/list", methods=['GET'])
def list_reports():
    reports = []
    count = 0
    for path in sorted(pathlib.Path(app.config['UPLOAD_FOLDER']).glob('*'), key=lambda p: os.stat(p).st_mtime, reverse=True):
        if path.is_dir():
            count += 1
            modtime = datetime.fromtimestamp(os.stat(path).st_mtime, tz=timezone.utc).isoformat()
            with open(f"{path}/metadata.json", 'rb') as meta_file:
                title = json.load(meta_file).get('title', 'NO TITLE')
                reports.append({"name": title, "digest": str(path.name), "date": modtime})
    return {"reports": reports}

# For uploading a new JSON assessment into the tool
@app.route("/uploadfile", methods=['POST'])
def uploadfile():
    if 'file_upload' not in request.files:
        return {"error": True, "message": "Field file_upload not provided in API input"}

    if 'title' not in request.form:
        return {"error": True, "message": "No title was provided"}

    uploaded_file = request.files['file_upload']
    title = request.form['title']

    if uploaded_file.filename == '':
        return {"error": True, "message": "File not selected"}

    if title == '':
        return {"error": True, "message": "Title was empty"}

    # Save file to a temp-named file temporarily (don't use uploader-supplied filename)
    with tempfile.NamedTemporaryFile(delete_on_close=False) as tmp:
        shutil.copyfileobj(request.files['file_upload'], tmp)
        tmp.close()

        # Before we try to do anything with it, make sure the JSON is good
        if not validate_json(tmp.name):
            return {"error": True, "message": "Bad JSON loaded"}

        # Hash the populated tempfile and move the data into a new location. Preserve the
        # original data from the submitter
        with open(tmp.name, 'rb') as digest_input:
            h = file_digest(digest_input, 'sha256').hexdigest()
            new_filename = '{reports}/{h}/upload.json'.format(reports=app.config['UPLOAD_FOLDER'], h=h)
            meta_filename = '{reports}/{h}/metadata.json'.format(reports=app.config['UPLOAD_FOLDER'], h=h)
            digest_input.close()
            pathlib.Path("{reports}/{h}/resources".format(reports=app.config['UPLOAD_FOLDER'], h=h)).mkdir(parents=True, exist_ok=True)
            shutil.move(tmp.name, new_filename)

            with open(new_filename, 'rb') as json_file, open(meta_filename, 'w') as meta_json:
                resource_data = json.load(json_file)
                meta_json.write(json.dumps({'title': title, 'digest': h}))
                meta_json.close()
                for rsrc in resource_data['resources']:
                    defects = validate_policy(rsrc)

                    # Add any discovered defects to the resource record
                    rsrc['defects'] = defects

                    # Then, write to report files
                    with open("{reports}/{h}/resources/{name}.json".format(reports=app.config['UPLOAD_FOLDER'], h=h, name=rsrc['name']), 'w') as resource_rpt:
                        json.dump(rsrc, resource_rpt)

            return {"message": "", "upload_id": h, "error": False}

    return {"error": True, "message": "Couldn't load file"}
