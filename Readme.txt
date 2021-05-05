Scratch NintendoRemote Extension by 6oranges

This extension is for use with the Scratch offline editor. It has been written in Python and runs on any operating system. The extension is set to run on port 9018 by default. To change then you will have to edit the s2e file and the py file.

The extension has no window and will only end once the Stop Extension block is pressed.

You will need to tell Scratch about the extension so shift + click the File menu in the Scratch offline editor and select "Import Experimental Extension". Find the Speak.s2e file.
You should now have new blocks in the more blocks category. You should also have a green dot to show that the NintendoRemote Extension has been connected. If it's red ensure the extension is running and ports are correct.

You can test the extension without scratch by using a browser. The url for port 9018 would be

http://localhost:9018/poll

You should see all of the values of the NintendoRemote

The new blocks the extension provides are;
	Stop Extension - stops running extension

and reporter blocks:
	
    Arrow Pressed  [up,down,left,right]
    Button Pressed [A,B,select,start]

Happy Scratching.

Thanks to David Mellis for Arduino Extension:
    Based on HTTPExtensionExample by John Maloney.
    Inspired by Tom Lauwers Finch/Hummingbird server and Conner Hudson's Snap extensions.
Thanks to Procd for text-speech extension