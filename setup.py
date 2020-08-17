# to build the app run this file with this command -> $ python setup.py bdist_mac --iconfile="upload.icns"
# On Mac OS, move the created app in the build folder to the applications folder for it to work
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["requests"],  "excludes": ["tkinter"], "include_files": ["upload.icns","masi.jpg", "REDCAP_API_KEY.txt"]}

bdist_mac_options = {"include_resources": [("REDCAP_API_KEY.txt", "REDCAP_API_KEY.txt"),
                                           ("masi.jpg", "masi.jpg")],
                     "iconfile": ["upload.icns"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="InterviewUploader",
      version="0.1",
      description="UPLOADER!",
      options={"bdist_mac": bdist_mac_options,
               "build_exe": build_exe_options},
      executables=[Executable("interview_uploader.py")])
