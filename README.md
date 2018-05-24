# SaveForLater-Manager
chrome native messanging extension with their host program which allow the the user to back up all  webpage on their current browser window to their local computer instantly.

to install the program
first open the registerin.reg with text-editor
then set the path to:
	@="C:\\...Path to this file folder...\\com.kamal.sfl.downloader.json"

and open the com.kamal.sfl.downloader.json 
then set the "path" section into:
	C:\\...Path to this file and the application located...\\sfl-downloader.exe

and dont forget to add the the extension id (if theres no one) "in allowed-origins" with
the extension id.


and in the saveforlater2 folder, extract somewhere and add it into chrome through
the extension page on browser with Developer mode enabled, then upload the raw-extension with
the extracted saveforlater2 folder and before you do it pls check the

saveforlater2 manifest.json id and make sure it match with the commented id in manifest.json

extension id : //allowed_origins extension id: chrome-extension://kejkdiaeeekhienockhiokpbocdfpfof/
