"""
08/05/2018 ver 0.1
15:13 PM

09/08/2018 ver 0.2 (New Update)
10:13 AM

By: Suryo Slamet Kamal Kalamillah
Gmail: kamal.kalamillah@gmail.com
Github: https://github.com/BuahApple

彡 = Update Mark

SaveForLater v.0.1 -> v.0.2
Experimental version, still need many adjustment for final
version of this program, however the primary function is finally
done and now ready for use, but not final.
theres still alot of things that need to be added to this program
for example the path directory function to enable user set the directory
to where the file that he downloaded locate. Currently here the list
of things need to be update:

    1.GUI Adjustment and improvement 彡, 彡 - update ver 0.1 extend period
    2.Directory Selector Widget 彡 - update ver 0.1 extend period
    3.MHTML Support, CSS capturer support(for those who what dowmload
      the whole website)
    4.Installer Support 彡 - update ver 0.1 extend period
    5.Auto Registry installer(the current one have to add it manualy)
    6.More Custom User-Agent
    7.Support for Mac, Linux user
    8.Support for another Mozilla-base browser (Mozilla, Safari, etc)
    9.Perfomance adjustment
    10.Graphic adjustment 彡, 彡 - update ver 0.1 extend period
    11.Exception for unrecognized url protocol 彡 - update ver 0.1 extend period
    
"""


import struct, sys, threading, queue
import requests, os, bs4, json, demjson, ast, urllib
import lxml.html
from urllib.request import Request, urlopen

from PyQt5 import QtWidgets
from sfl_ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QDialog, QInputDialog, QLineEdit, QFileDialog, QWidget, QMessageBox, QPushButton

"""
AT LEAST!!! FINALLY I CAN IMPORT AN GENERATED PY FROM UI FILE!!
FINALLY NOW I CAN ADD MY CODE TO MAKE THE PROGRAM WITH BETTER UI WORK

PRAISE ALLAH!
"""



def send_message(message):
    sys.stdout.write(struct.pack('I', len(message)))

    sys.stdout.write(message)
    sys.stdout.flush()

def read_thread_func(queue):
    message_number = 0
    while 1:
        text_length_bytes = sys.stdin.buffer.read(4)

        if len(text_length_bytes) == 0:
            if queue:
                queue.put(None)
            sys.exit(0)

        text_length = struct.unpack('@i', text_length_bytes)[0]
        text = sys.stdin.buffer.read(text_length).decode('utf-8')

        queue.put(text)
        


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, queue):
        super(MainWindow, self).__init__()

        self.queue = queue

        self.curhtmlpath = ""
        self.setupUi(self)
        self.processMessage()

        self.pushButton_2.clicked.connect(self.onDonlot)
        self.pushButton.clicked.connect(self.select_directory_dialog)
        self.pushButton_3.clicked.connect(self.processMessage)
        self.setWindowTitle("SFL DOWNLOADER v0.2")
        

    def select_directory_dialog(self):
        self.dirpath = QFileDialog.getExistingDirectory(self, "Select Directory")
            
        dbslash = dict.fromkeys(map(ord, '/'), "\\")

        self.realdirpath = self.dirpath.translate(dbslash)

        self.curhtmlpath = self.realdirpath

        self.lineEdit.setText(self.realdirpath)



    def processMessage(self):
        while not self.queue.empty():
            message = self.queue.get_nowait()
            if message == None:
                self.quit()
                return
            self.textEdit.setText(message)

    def onDonlot(self):
        """insert, delete, or place certain character to text.box
            (1.0, tkinter.END) = (begin, end)"""
        url = self.textEdit.toPlainText()
        url = ast.literal_eval(url)
        os.makedirs("Downloaded Bulk Stuff", exist_ok=True)
        """
        self.text.delete(1.0, tkinter.END)
        self.text.insert(1.0, url)
        ca = url[0]
        ba = url[1]
        self.text.insert(1.0, ca)
        self.text.insert(1.0, ba)
        """
        for i in url:
            """
            Take the url from stdin in form of binary file
            with custom User-Agent to avoid 403:Forbidden Error
            (because default urllib.request.urlopen() access their
            website without specifiy user-agent or maybe they
            just blocked by website).
            for some website, don't know why some website probaly
            block the urllib python agent, ( maybe they doesn't like
            people scrapping their website... )
            """
            takeurl = Request(i, headers={'User-Agent': 'Mozilla/5.0'})
            try: 
                redurl = urlopen(takeurl)

            except urllib.error.HTTPError:
                continue
            except urllib.error.URLError:
                continue
                
            readurl= redurl.read()

            try:
                    
                page = requests.get(i)
                    
            except requests.exceptions.InvalidSchema:
                continue
                    
            sfilename = bs4.BeautifulSoup(page.content, 'html.parser')

            #the dict var contain an list of impossible character on file renaming
            #may change the page title to avoid ErrorInput
            impchar = dict.fromkeys(map(ord, '/\\:*|\"\'<>?'), None)

            #take the title from page content created by bs4
            raw_filename = sfilename.title.string

            #translate the raw unscanned string to scanned string without
            #impossible character
            filename = raw_filename.translate(impchar)

            path = self.curhtmlpath

            if path == "":
                path = os.getcwd()

            filenamewithdir = os.path.join(path, filename+".html")
                
            #a = ["/", "\"", "\'", "<", ">", "\\", ":", "*", "|"]

            """download the html page, currently i have no idea how to set
            a directory folder for file, since in python 3.x the backslash
            i often used in python 2.x, declared as a string variable same
            as filename var, so it cause an ErrorInput for create impossible
            character"""
            dlw = open(filenamewithdir, "wb")
            dlw.write(readurl)
            dlw.close

                                    
        self.end = QMessageBox.question(self, "Download Complete", "Download Succes!", QMessageBox.Ok)

    def log(self, message):
        self.textEdit.setText(message)

    """
    def awe(self):
        self.textEdit.setText(self.aw)

        without 'self' prefix infront of aw, the variable will refer to local variable of function
        or child scope not the parent one(the parent which they inherited from __init__ func using
        'self' prefix, it was the main reason why we should use class, self and __init__ func)
    """


def main():
    kueue = queue.Queue()
    
    app = QtWidgets.QApplication(sys.argv)
    sfl_win = MainWindow(kueue)

    thread = threading.Thread(target=read_thread_func, args=(kueue,))
    thread.daemon = True
    thread.start()
    
    sfl_win.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

