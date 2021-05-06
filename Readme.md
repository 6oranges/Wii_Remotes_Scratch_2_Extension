# Scratch Wii Remote Extension

This extension is for use with the Scratch offline editor. It has been written in Python 2.
![extension visable in scratch](wii%20remotes.png?raw=true "Title")

It is a bit of a nightmare to use this as it was written in 2016 in python 2. Even worse the wii remote library I am using only works on linux so the setup is more complicated.
First find yourself a raspberry pie or similar. Install python2 and cwiid. Run `Wii Server.py` on the raspberry pie. On your main machine edit Wii Remote.py so that it connects
to the correct address instead of 192.168.1.230 which is certanly not the ip address of your raspberry pie. Run Wii Remote.py. Now scratch should be able to connect to the
extension and you should be able to use wii remotes within scratch.

The extension has no window but can be killed with the Stop Extension block.

You will need to tell Scratch about the extension so shift + click the File menu in the Scratch offline editor and select "Import Experimental Extension". Find the Wii Remote.s2e file.
You should now have new blocks in the more blocks category. You should also have a green dot to show that the Wii Remote Extension has been connected. If it's red ensure the setup is correct.

You can test the extension without scratch by using a browser. The url for port 9013 would be

http://localhost:9013/poll

You should see all of the values of the Wii Remotes

Happy Scratching.

Thanks to David Mellis for Arduino Extension:
    Based on HTTPExtensionExample by John Maloney.
    Inspired by Tom Lauwers Finch/Hummingbird server and Conner Hudson's Snap extensions.
Thanks to Procd for text-speech extension
