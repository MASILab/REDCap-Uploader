pip install virtualenv
virtualenv -p python3 uploader_env
source uploader_env/bin/activate
pip install xlrd PyQt5 PyCap pandas
python interview_uploader.py
