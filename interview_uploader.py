#!/usr/bin/env python

import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
import redcap

# print(sys.getrecursionlimit())   # recursionlimit before
# # 1000
# sys.setrecursionlimit(10000)
# print(sys.getrecursionlimit())

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interview Uploader")
        self.setGeometry(240, 240, 350, 350)
        # masi logo in the background
        # oImage = QtGui.QImage("/Users/kanakap/Downloads/masi_old1.png")
        # sImage = oImage.scaled(QtCore.QSize(360, 360))
        # palette = QtGui.QPalette()
        # palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(sImage))
        # self.setPalette(palette)
        self.UI()

    def UI(self):
        #masi lab logo
        self.masi_label = QLabel(self)
        self.masi_label.setGeometry(QtCore.QRect(250, 250, 70, 70))
        #pixmap = QtGui.QPixmap('/Users/kanakap/Downloads/masi.jpg')
        pixmap = QtGui.QPixmap('/Applications/InterviewUploader-0.1.app/Contents/Resources/masi.jpg')
        self.masi_label.setPixmap(pixmap.scaled(75, 75, QtCore.Qt.KeepAspectRatio))

        # set labels for the text boxes
        self.label_1 = QLabel("Participant ID", self)
        #self.label_1.setStyleSheet("font-size: 400%")
        self.label_1.setFont(QtGui.QFont('Laksaman', 15))
        self.label_1.move(50, 30)

        self.label_2 = QLabel("Visit", self)
        self.label_2.setFont(QtGui.QFont('Laksaman', 15))
        self.label_2.move(50, 80)


        self.label_3 = QLabel("Interview File", self)
        self.label_3.setFont(QtGui.QFont('Laksaman', 15))
        self.label_3.move(50, 125)

        # text boxes for participant and visit
        self.nameTextbox = QLineEdit(self)
        self.nameTextbox.setFont(QtGui.QFont('Laksaman', 15))
        self.nameTextbox.move(160, 30)

        # self.passTextbox = QLineEdit(self)
        # self.passTextbox.move(150, 70)
        self.dropdown = QComboBox(self)
        self.dropdown.addItem("Visit 1")
        self.dropdown.addItem("Visit 2")
        self.dropdown.addItem("Visit 3")
        self.dropdown.addItem("Visit 4")
        self.dropdown.addItem("Extra Visit 1")
        self.dropdown.addItem("Extra Visit 2")
        self.dropdown.addItem("Extra Visit 3")
        self.dropdown.addItem("Extra Visit 4")
        self.dropdown.addItem("Extra Visit 5")
        self.dropdown.setFont(QtGui.QFont('Laksaman', 15))
        self.dropdown.move(150, 75)

        # push button to browse file
        # self.pushButton = QPushButton("Browse File", self)
        # self.pushButton.move(150, 100)
        self.excel_path = ''
        # self.pushButton.clicked.connect(self.pushButton_handler)

        # self.select_image_label = QLabel(self)
        # self.select_image_label.setObjectName("bubble_para")
        # self.select_image_label.setText("Choose Image")
        # self.select_image_label.move(30, 50)

        # for textfeild after push button
        # self.image_path = QLineEdit(self)
        # self.image_path.setObjectName("path_text")
        # self.image_path.move(150, 105)

        self.image_path = QLabel(self)
        self.image_path.setObjectName("path_text")
        self.image_path.move(250, 120)

        self.browse_button = QPushButton(self)

        self.browse_button.setText("Browse")
        self.browse_button.setObjectName("browse_button")
        self.browse_button.clicked.connect(self.pushButton_handler)
        #self.browse_button.move(240, 125)
        self.browse_button.setFont(QtGui.QFont('Helvetica', 15))
        self.browse_button.move(150, 120)


        # push button to upload to redcap
        self.button = QPushButton("Upload to REDCap", self)
        self.button.setFont(QtGui.QFont('Helvetica', 15))
        self.button.move(90, 180)
        #self.openedwin = []
        self.button.clicked.connect(self.save)

        self.show()

    def onChanged(self):
        print((self.comboBox.currentText(), self.comboBox.currentIndex()))

    def pushButton_handler(self):
        print("Button pressed")
        self.excel_path = self.open_dialog_box()
        print(self.excel_path)

    def open_dialog_box(self):
        # filename = QFileDialog.getOpenFileName(self)
        # path = filename[0]
        # print(path)
        # raw_excel = pd.read_excel(path, sheet_name=None)
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        #fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
        #                                          "Excel Files (*.xlsx)", options=options)
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Excel Files (*.xlsx)", options=options)


        if fileName:
            print("filename is", fileName)
            self.image_path.setWordWrap(True)
            self.image_path.setText(fileName)
            self.image_path.adjustSize()
        return fileName


    def save(self):
        visit_dict = {"Visit 1": "visit_1_arm_1", "Visit 2": "visit_2_arm_1", "Visit 3": "vist_3_arm_1",
                 "Visit 4": "visit_4_arm_1", "Extra Visit 1": "extra_visit_1_arm_1",
                 "Extra Visit 2": "extra_visit_2_arm_1", "Extra Visit 3": "extra_visit_3_arm_1",
                 "Extra Visit 4": "extra_visit_4_arm_1", "Extra Visit 5": "extra_visit_5_arm_1"}
        participant_id = self.nameTextbox.text()
        visit = visit_dict[self.dropdown.currentText()]
        print(participant_id, visit)
        print(self.excel_path)
        interview_file = self.excel_path

        # Message
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setText("Error")
        # Check if the file was selected
        try:
            fobj = open(interview_file, 'rb')
        except FileNotFoundError:
            print('File was not selected')
            self.msg.setInformativeText('File not selected')
            self.msg.setWindowTitle("Error")
            self.msg.exec_()
        else:
            # Asset the excel file
            excel_data_df = pd.read_excel(interview_file)

            # Throw errors an error each for wrong column headers
            if excel_data_df.columns[0] != 'SubjectID':
                self.msg.setInformativeText('Column 1 header should be SubjectID')
                self.msg.setWindowTitle("Error")
                self.msg.exec_()
            elif excel_data_df.columns[1] != 'InterviewDate':
                self.msg.setInformativeText('Column 2 header should be InterviewDate')
                self.msg.setWindowTitle("Error")
                self.msg.exec_()
            elif excel_data_df.columns[2] != 'InterviewerName':
                self.msg.setInformativeText('Column 3 header should be InterviewerName')
                self.msg.setWindowTitle("Error")
                self.msg.exec_()
            elif excel_data_df.columns[3] != 'StudyName':
                self.msg.setInformativeText('Column 4 header should be StudyName')
                self.msg.setWindowTitle("Error")
                self.msg.exec_()
            elif excel_data_df.columns[4] != 'IsComplete':
                self.msg.setInformativeText('Column 5 header should be IsComplete')
                self.msg.setWindowTitle("Error")
                self.msg.exec_()

            # If the subject ID row is not present
            elif not (excel_data_df['SubjectID'] == participant_id).any():
                print('SubjectID not present')
                self.msg.setInformativeText('The SubjectID given does not exists in Excel')
                self.msg.setWindowTitle("Error")
                self.msg.exec_()

            # If subject ID row present
            elif (excel_data_df['SubjectID'] == participant_id).any():
                # get scoring values
                p_values = excel_data_df[excel_data_df['SubjectID'] == participant_id].filter(regex='^P[0-9]').values
                # ndarray -> list
                print(p_values)
                print(p_values.size)
                # check if the scoring columns are present
                if p_values.size == 0:
                    print('here')
                    self.msg.setInformativeText('There are no scoring columns')
                    self.msg.setWindowTitle("Error")
                    self.msg.exec_()

                # check if atleast one scoring values is present
                elif p_values.size != 0:
                    if (1 or 2 or 3 or float(1) or float(2) or float(3)) not in p_values:
                        self.msg.setInformativeText('There are no preferred values (1 or 2 or 3) in scoring columns')
                        self.msg.setWindowTitle("Error")
                        self.msg.exec_()
                    else:
                        print('The Excel file is in good format')
                        # Importing to REDCap
                        #current_working_dir = os.getcwd()
                        #redcap_key_dir = os.path.join(current_working_dir,"build/InterviewUploader-0.1.app/Contents/MacOS/REDCAP_API_KEY.txt")

                        redcap_key_file = open('/Applications/InterviewUploader-0.1.app/Contents/Resources/REDCAP_API_KEY.txt', "r")
                        redcap_key_file.seek(0, 0)
                        redcap_key = redcap_key_file.read().replace('\n', '')
                        proj = redcap.Project('https://redcap.vanderbilt.edu/api/', redcap_key)
                        print('Connected to REDCap')
                        print(str(visit))

                        # Check if the upload file/record exists on REDCap
                        try:
                            print('Check if the file exsits in REDCap')
                            proj.export_file(record=str(participant_id), field='upload', event=str(visit))
                            print('File exists on REDCap')
                            # self.msg_warn = QMessageBox()
                            # self.msg_warn.setIcon(QMessageBox.Critical)
                            # self.msg_warn.setText("Warning")
                            self.msg.setInformativeText('Excel file already exists for this visit. Try a new SubjectID')
                            self.msg.setWindowTitle("Warning")
                            self.msg.exec_()

                        #except requests.HTTPError:
                        except redcap.RedcapError:
                            print('Excel not in redcap')
                            # import record first
                            to_import = [{'subject_id': str(participant_id), 'redcap_event_name': str(visit),
                                          'einterview_record_complete': '1'}]
                            response = proj.import_records(to_import)
                            print('REDCap import record response', response)
                            # Upload file to REDCap
                            proj.import_file(record=str(participant_id), field='upload', event=str(visit),
                                             fname=interview_file,
                                             fobj=fobj)

                            # after file is uploaded change the status to complete
                            to_import = [{'subject_id': str(participant_id), 'redcap_event_name': str(visit),
                                          'einterview_record_complete': '2'}]
                            response = proj.import_records(to_import)
                            print('REDCap uploaded file response', response)






def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
