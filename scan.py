#Importing modules
from socket import *
from threading import *
import optparse
import os

#Operating system is checked because color codes only work on linux, not windows.
if os.name == "posix":
  class colors:
    G = '\033[92m'
    R = '\033[91m'
    ENDC = '\033[0m'
    C = '\033[96m'
else:
  class colors:
    G = ''
    R = ''
    ENDC = ''
    C = ''

#If the user does not specify a port, scanning will be done with default ports.
class defaultPorts:
  dp = ['20','21','22','23','25','53','67','68','80','161','162','123','443','7104','7102','7105']

def hostScan(targetHost,targetPorts):
  #The host and port information to be scanned is transferred here.
  #try is used to error when hostname is not found
  try:
    #The ip of the specified host is passed to the variable.
    targetIp = gethostbyname(targetHost)
    try:
      #Sometimes gethostbyaddr is written in "try" because it can throw an error.
      targetName = gethostbyaddr(targetIp)
      #The query made here was made to make the lines in the output look more beautiful.
      if (len(targetName[0]) > len(targetIp)):
        stickLen = len(targetName[0])
      else: 
        stickLen = len(targetIp)
    except:
      stickLen = len(targetIp)
    #It is transferred to the variable so that it is not crowded because there is coloring in the rows. (so that the whole output looks good)
    #colors.G is Green
    infoG = colors.G + " [INFO] " + colors.ENDC
    #colors.R is Red
    infoR = colors.R + " [INFO] " + colors.ENDC
    #Line (for beautiful appearance)
    print(colors.R + " " + "-"*18, "-"*stickLen + colors.ENDC, sep="")
    #Information about the host
    print(infoG + "Ip address: " + str(targetIp))
    #"try" is used because other addresses may sometimes output blank or throw an error.
    try:
      print(infoG + "Host name: " + str(targetName[0]))
      #Checking if targetName[1] is not empty.
      if (str(targetName[1]) != "[]"):
        print(infoG + "Host IP address: " + str(targetName[1]))
    except:
      #If it gives an error:
      print(infoR + "Other addresses not found")
    #If the length of the specified ports is more than 10, closed ports will not be shown in the output, only open ports will be shown.
    if len(targetPorts) > 10:
      #If the ports are "default ports" is shown in the output in a special way.
      if targetPorts == defaultPorts.dp:
        print(infoG + "Ports: Default ports => 20 21 22 23 25 53 67 68 80 161 162 123 443 7104 7102 7105")
      else:
        #If the ports are not "default ports", only the first and last port numbers of the specified ports are displayed.
        print(infoG + "Ports: All ports " + str(targetPorts[0]) + " to " + str(targetPorts[-1:][0]))
      print(colors.G + " [INFO] Note: Since the length of the output will exceed 10 lines, closed ports will not be shown in the output, only open ports will be shown." + colors.ENDC)
      #Created a variable named "clean Console" for later use and added "True" (this indicates ports greater than 10).
      cleanConsole = True
    else:
      #If ports are less than 10, ports and closed ports are shown directly in the output.
      print(infoG + "Port(s): " + str(targetPorts))
      cleanConsole = False
    #Line (for beautiful appearance)
    print(colors.R + " " + "-"*18, "-"*stickLen + colors.ENDC, sep="")
    #to indicate that the scan has started.
    print(infoG + "Port(s) Scanning...")
  except:
    print(colors.R + "\n [INFO] " + colors.ENDC + "Hostname not found: " + str(targetHost))
    exit(0)

  #processes are executed with "thread", it takes longer if scanned one by one,
  #because scanning takes place on average 100 ports and therefore takes longer, the logic of using threads:
  #not scanning ports one by one, is to create as many threads as the size of the ports and transfer the ports in the list to the threads one by one.
  for targetPort in targetPorts:
    #Threads are created by sending the targetHost, targetPort, and cleanConsole variables to the portScan function.
    thre = Thread(target=portScan, args=(targetHost, int(targetPort), cleanConsole))
    thre.start()

def portScan(targetHost,targetPort,cleanConsole):
  #if cleanConsole is True i.e. the length of the ports is greater than 10
  if cleanConsole == True:
    #With socket, a request is sent to host:port, if the request fails, that is, if the port is closed, the "except" part of the "try" works.
    try: 
      #if it does not give an error, the "try" part continues to work, indicating in the output that the port is open.
      sock = socket(AF_INET,SOCK_STREAM)
      sock.connect((targetHost,targetPort))
      print(colors.G + " [OK] " + str(targetPort) + " Port open" + colors.ENDC)
    except:
      print(end = "")
    finally:
      sock.close()
  else:
    #The above code the difference is that the output shows the closed port here.
    try:
      sock = socket(AF_INET,SOCK_STREAM)
      sock.connect((targetHost,targetPort))
      print(colors.G + " [OK] " + str(targetPort) + " Port open" + colors.ENDC)
    except:
      print(colors.R + " [X] " + str(targetPort) + " Port close" + colors.ENDC)
    finally:
      sock.close()

#The function and class here have been moved to a separate place to avoid crowding the main function
def banner():
  banner = ("""{}  _____           _      _____                                 
 |  __ \         | |    / ____|                                
 | |__) |__  _ __| |_  | (___   ___ __ _ _ __  _ __   ___ _ __
 |  ___/ _ \| '__| __|  \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|{}
 | |  | (_) | |  | |_   ____) | (_| (_| | | | | | | |  __/ |{}
 |_|   \___/|_|   \__| |_____/ \___\__,_|_| |_|_| |_|\___|_|{}""".format(colors.C, colors.G, colors.R, colors.ENDC))
  print(banner)

class parserOp:
  text = (colors.G + " " + "-"*59 + colors.C + 
  """\n Command usage: python3 scan.py [option] arg,arg
 Opitons:
   -H <host address, ex: 192.168.1.30 or example.com>
   -p <port, ex: 80 or 80,144,265>
   -r <port range, ex: 80,1024>\n
 Command examples:
   -H and -p usage ex: python3 scan.py -H 192.168.1.30 -p 80
   -H and -r usage ex: python3 scan.py -H google.com -r 20,90\n""" + colors.G + " " + "-"*59 + colors.ENDC)

def main():
  banner()
  #Parser is used to specify options while running the file
  parser = optparse.OptionParser(parserOp.text)
  parser.add_option("-H", dest="targetHost", type="string", help="The web address or IP address to be scanned.")
  parser.add_option("-p", dest="targetPort", type="string", help="The port address(es) of the entered address to be scanned.")
  parser.add_option("-r", dest="targetPortRange", type="string", help="The port address range of the entered address to be scanned.")
  (options,args) = parser.parse_args()
  #Specified options are passed to variable
  targetHost = options.targetHost
  targetPortMain = str(options.targetPort).split(",")
  targetPortRange = str(options.targetPortRange).split(",")

  #Options are shown if file is run without specifying -H
  if targetHost == None:
    print(parser.usage)
    exit(0)
  else:
    #If the address specified in the -H option is a website link and contains "https://", "https://" is deleted
    if "https://" in targetHost:
      targetHost = targetHost[8:]
    if "http://" in targetHost:
      targetHost = targetHost[7:]
    if "/" in targetHost:
      targetHost = targetHost[:-1]
    #Since -r and -p cannot be used at the same time, options are shown if used
    if targetPortMain != ['None'] and targetPortRange != ['None']:
      print(parser.usage)
      exit(0)
    else:
      #If -p is not empty, the value specified in the -p option is used in scanning.
      if targetPortMain != ['None']:
        targetPorts = targetPortMain
      else:
        #If -r is empty, the user only specified the -H option, so default ports will be used for scanning.
        if targetPortRange == ['None']:
          targetPorts = defaultPorts.dp
        #If -r has a value, it must have at least 2 values, -r checks to see if it has 2 values. if not, options are shown
        elif targetPortRange[1] == ['None']:
          print(parser.usage)
          exit(0)
        else:
          #if it has 2 values ​​a list named portRange is created
          portRange = []
          #if 1st value is greater than 2nd value
          if targetPortRange[0]>targetPortRange[1]:
            #The logic of the loop that is intended to be done here is: 
            #The specified small value is added to the list by continuously increasing +1 until the second larger value, so that all numbers in the 2 specified ranges are added to the list.
            tpr1 = int(targetPortRange[0])+1
            tpr2 = int(targetPortRange[1])
            while tpr1 != tpr2:
              portRange.append(tpr2)
              tpr2=tpr2+1
          #if 2nd value is greater than 1st value
          elif targetPortRange[0]<targetPortRange[1]:
            #The logic of the loop done here is almost the same as above, the difference is that the values ​​are orders of magnitude
            tpr1 = int(targetPortRange[0])
            tpr2 = int(targetPortRange[1])+1
            while tpr1 != tpr2:
              portRange.append(tpr1)
              tpr1=tpr1+1
          #After the loop(s) is finished, the generated list is passed to the variable for use in scanning.
          targetPorts = portRange
  #After all the queries and loops are finished, the variables are passed to the scan.
  hostScan(targetHost,targetPorts)

if __name__ == "__main__":
  main()
