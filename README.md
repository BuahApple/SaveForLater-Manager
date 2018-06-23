# SaveForLater-Manager
chrome native messanging extension with their host program which allow their user to back up all  webpage on their current browser window to their local computer instantly.

First of all, you must install the native app in default directory directory, DO NOT! change the directory because registry data to connect the native app and extension. 

Then open you chrome extension, then select *Developer Mode* then click 

In case if uploaded raw extension list isn't same as the one below, change the allowed_origin of native app host manifest in main program directory called "com.buahapple.sfl.downloader.json", open it with text editor, and change the allowed_origin of extension.

"allowed_origins": [
    "chrome-extension://*your new generated ID from uploaded raw extension*/"
  ]
