# REDCap-Uploader

To open the GUI to upload to REDCap

$ . run_app.py

or

$ python interview_uploader.py

Please note: for the python script to work, 

a) the required packages are xlrd, pandas, PyQt5, PyCap
You can install it by 
$ pip install xlrd pandas PyQt5 PyCap 

b) The required files are REDCAP_API_KEY.txt and masi.jpg


To build application for Mac OS
$ python setup.py bdist_mac --iconfile="upload.ics"

Interview Uploader GUI 
![](/images/Uploader%20GUI.png)
