#!/bin/bash

# Use curl to upload a file
curl -XPOST http://localhost:8000/uploadfile \
    -F "file_upload=@$1"
