"""
08/05/2018
15:13 PM

By: Suryo Slamet Kamal Kalamillah
Gmail: kamal.kalamillah@gmail.com
Github: https://github.com/BuahApple

SaveForLater v.0.1
Experimental version, still need many adjustment for final
version of this program, however the primary function is finally
done and now ready for use, but not final.
theres still alot of things that need to be added to this program
for example the path directory function to enable user set the directory
to where the file that he downloaded locate. Currently here the list
of things need to be update:

    1.GUI Adjustment and improvement
    2.Directory Selector Widget
    3.MHTML Support, CSS capturer support(for those who what dowmload
      the whole website)
    4.Installer Support
    5.Auto Registry installer(the current one have to add it manualy)
    6.More Custom User-Agent
    7.Support for Mac, Linux user
    8.Support for another Mozilla-base browser (Mozilla, Safari, etc)
    9.Perfomance adjustment
    10.Graphic adjustment
    11.Exception for unrecognized url protocol
    
"""

import struct, sys, threading, queue
import requests, os, bs4, json, demjson, ast, urllib
import lxml.html
from urllib.request import Request, urlopen

try:
    import tkinter
    import tkinter.messagebox
    from tkinter import filedialog

except ImportError:
    tkinter = None

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

if tkinter:
    class NativeMessagingWindow(tkinter.Frame):
        def __init__(self, queue):
            self.queue = queue

            tkinter.Frame.__init__(self)
            self.pack()

            self.curhtmlpath = ""

            self.text = tkinter.Text(self)
            self.text.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
            self.text.config(state = tkinter.NORMAL, height=10, width=50)

            self.dirtext = tkinter.Text(self)
            self.dirtext.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
            self.dirtext.config(state = tkinter.NORMAL, height=1, width=50 )

            self.dirButton = tkinter.Button(self, text="Set Directory", command=self.select_directory_dialog)
            self.dirButton.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
            
            self.downloadButton = tkinter.Button(self, text="Download", command=self.onDonlot)
            self.downloadButton.grid(row=1, column=2, padx=10, pady=10)

            self.labelku = tkinter.Label(self, text="By: Suryo Slamet Kamal Kalamillah\nGmail: kamal.kalamillah@gmail.com\nGitHub: https://github.com/BuahApple")
            self.labelku.grid(row=0, column=2, padx=10, pady=10)

            self.after(100, self.processMessage)

        def select_directory_dialog(self):
            self.dirpath = tkinter.filedialog.askdirectory()
            
            dbslash = dict.fromkeys(map(ord, '/'), "\\")

            self.realdirpath = self.dirpath.translate(dbslash)

            self.curhtmlpath = self.realdirpath

            self.dirtext.insert(1.0, self.realdirpath)



        def processMessage(self):
            while not self.queue.empty():
                message = self.queue.get_nowait()
                if message == None:
                    self.quit()
                    return
                self.log(message)

            self.after(100, self.processMessage)

        def onDonlot(self):
            """insert, delete, or place certain character to text.box
               (1.0, tkinter.END) = (begin, end)"""
            url = self.text.get(1.0, tkinter.END)
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

                                    
            tkinter.messagebox.showinfo("Info", "Download Success!")
            sys.exit(1)

        def log(self, message):
            self.text.config(state=tkinter.NORMAL)
            self.text.insert(1.0, message)
            self.text.config(state=tkinter.DISABLED)

def Main():
    if not tkinter:
        send_message("Sorry but tkinter module wasn\'t found. Please install tkinter module.")
        read_thread_func(None)
        sys.exit(0)

    kueue = queue.Queue()

    main_window = NativeMessagingWindow(kueue)
    main_window.master.title("SFL Downloader")
    main_window.master.iconbitmap(r'C:\Users\Kamal\Documents\extension\SaveForLater Manager\favicon.ico')

    thread = threading.Thread(target=read_thread_func, args=(kueue,))
    thread.daemon = True
    thread.start()

    main_window.mainloop()

    sys.exit(0)

if __name__ == '__main__':
    Main()


#>>> dada = "haha.haha.a"
#>>> dada[dada.rfind(".") + 1:]
#'a'
#>>> 
