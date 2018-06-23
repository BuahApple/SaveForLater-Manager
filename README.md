# SaveForLater-Manager
chrome native messanging extension with their host program which allow their user to back up all  webpage on their current browser window to their local computer instantly.

First of all, you must install the native app in default directory directory, DO NOT! change the directory because registry data to connect the native app and extension. after that extract the folder of downloaded extension.

Then open you chrome extension, then select *Developer Mode* then click *Load Unpacked* then load the extracted downloaded extension folder directory.

In case if uploaded raw extension list isn't same as the one below, change the allowed_origin of native app host manifest in main program directory called "com.buahapple.sfl.downloader.json", open it with text editor, and change the allowed_origin of extension.

And therefore there will be certain webpage that cannot be saved due of blocked User Agent or unrecognized html address, that because some website just doesn't like people trying to save their pages or scrapp it which obviously out of my ability to fix it.

"allowed_origins": [
    "chrome-extension://*your new generated ID from uploaded raw extension*/"
  ]

NOTE:
    Currently i was unabled to upload my extension to Google Chrome Extension Market, due financial issues and afterall
    there still many feature need to be added to extension such as: Save As PDF, MHTML, CSS Fetcher, GUI adjustment, more User         Agent, And advanced vanilla browser SaveAsHTML feature, and therefore I am very sorry for lacks of professionalism, this     is     my first applicableprogram and extension, Hope you enjoy my program! and please contact me for any suggestion for this             program or if you find any bug on this program.
