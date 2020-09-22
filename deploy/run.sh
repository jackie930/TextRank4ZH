#!/bin/bash
echo "inference mode"
cd /opt/ml/code/
python -m flask run --host=0.0.0.0 --port=8080