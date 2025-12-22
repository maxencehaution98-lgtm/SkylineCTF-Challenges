#!/bin/bash
docker build . -t docker.nexus.skyline.local:6000/file-quest-lvl-1 --platform linux/amd64
docker push docker.nexus.skyline.local:6000/file-quest-lvl-1 --platform linux/amd64

