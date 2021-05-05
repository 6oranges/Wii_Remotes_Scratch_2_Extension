#!/usr/bin/env python
import sys
import socket
import cwiid
import time
LISTENQ = 5
PLUS    = 4096
UP      = 2048
DOWN    = 1024
RIGHT   = 512
LEFT    = 256
HOME    = 128
##VOID  = 64
##VOID  = 32

MINUS   = 16
ABUTTON = 8
BBUTTON = 4
BUTTON1 = 2
BUTTON2 = 1
class Wiimote():
  def __init__(self):
    self.remote = cwiid.Wiimote()
    self.remote.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_IR
  def inbuttons(self,button): # checks to see if button is in buttons
    return self.remote.state['buttons'] & button
  def get_position(self,sx,sy): # calculates position of remote onscreen
    y = self.remote.state['ir_src'][0]
    if y != None:
      x = y['pos']
      return ((x[0]/-1000.0+1)*sx,(x[1]/800.0)*sy)
    else:
      return None
  def get_light(self,lightnum):
    if (self.remote.state["led"] & (1 << lightnum)) > 0:
      return True
    else:
      return False
  def set_light(self,lightnum,value):
    if value == True:
      self.remote.led = (self.remote.state["led"] | (1 << lightnum))
    else:
      self.remote.led = (self.remote.state["led"] & (~(1 << lightnum)))
def CreateServerSocket(port):
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveraddr = ('', port)
    serversock.bind(serveraddr)
    serversock.listen(LISTENQ)
    return serversock
def main():
    emptywiiset={"A":False,"B":False,"1":False,"2":False,"left":False,"right":False,"up":False,"down":False,"home":False,"+":False,"-":False}
    wiimotes = []
    try:
        wiimotes.append((Wiimote(),emptywiiset))
        print "Connected to Wiimote"
    except:
        pass
    serversock = CreateServerSocket(9075)
    serversock.setblocking(0)
    done = False
    update = []
    info = ""
    wiibuttons={"A":8,"B":4,"1":2,"2":1,"home":128,"+":4096,"-":16}
    wiiarrows={"left":256,"right":512,"up":2048,"down":1024}
    while not done:
        update = []
        for remote in range(len(wiimotes)):
            pos = wiimotes[remote][0].get_position(480,360)
            if pos != None:
                update.append("xir/"+str(remote+1)+":"+str(pos[0]))
                update.append("yir/"+str(remote+1)+":"+str(pos[1]))
            update.append("acc/"+str(remote+1)+"/x:"+str(wiimotes[remote][0].remote.state["acc"][0]))
            update.append("acc/"+str(remote+1)+"/y:"+str(wiimotes[remote][0].remote.state["acc"][1]))
            update.append("acc/"+str(remote+1)+"/z:"+str(wiimotes[remote][0].remote.state["acc"][2]))
            for key in wiiarrows:
                if wiimotes[remote][0].inbuttons(wiiarrows[key]):
                    if wiimotes[remote][1][key] == False:
                        wiimotes[remote][1][key] = True
                        update.append("getArrow/"+str(remote+1)+"/"+key+":true")
                else:
                    if wiimotes[remote][1][key] == True:
                        wiimotes[remote][1][key] = False
                        update.append("getArrow/"+str(remote+1)+"/"+key+":false")
            for key in wiibuttons:
                if wiimotes[remote][0].inbuttons(wiibuttons[key]):
                    if wiimotes[remote][1][key] == False:
                        wiimotes[remote][1][key] = True
                        update.append("getButton/"+str(remote+1)+"/"+key+":true")
                else:
                    if wiimotes[remote][1][key] == True:
                        wiimotes[remote][1][key] = False
                        update.append("getButton/"+str(remote+1)+"/"+key+":false")
        try:
            info = sock.recv(512)
        except:
            info = ""
        if len(info)>0:
            x=info.split(",")
            for command in x:
                inputs=command.split("/")
                if inputs[0] == "rumble" and int(inputs[2]) <= len(wiimotes):
                    if inputs[1] == "on":
                        wiimotes[int(inputs[2])-1][0].remote.rumble = 1
                        update.append("rumbling/"+inputs[2]+":true")
                    elif inputs[1] == "off":
                        wiimotes[int(inputs[2])-1][0].remote.rumble = 0
                        update.append("rumbling/"+inputs[2]+":false")
                elif inputs[0] == "light" and int(inputs[3]) <= len(wiimotes):
                    if inputs[2] == "on":
                        wiimotes[int(inputs[3])-1][0].set_light(int(inputs[1])-1,True)
                        update.append("lighton/"+inputs[3]+"/"+inputs[1]+":true")
                    if inputs[2] == "off":
                        wiimotes[int(inputs[3])-1][0].set_light(int(inputs[1])-1,False)
                        update.append("lighton/"+inputs[3]+"/"+inputs[1]+":false")
                elif inputs[0] == "con":
                    try:
                        wiimotes.append((Wiimote(),emptywiiset))
                        print "Wiimote connected"
                    except:
                        pass
                    update.append("wiimotes:"+str(len(wiimotes)))
                elif inputs[0] == "kill":
                    done = True
        try:
            sock.send(",".join(update)+",")
        except:
            pass
        try:
            (sock, clientaddr) = serversock.accept()
            sock.setblocking(0)
            print 'connection from %s, port %d' % clientaddr
        except:
            pass
        time.sleep(0.0166)
    sock.shutdown(1)
    sock.close()
time.sleep(0.0166)
main()

