from socket import *
from threading import *
import optparse

class colors:
  G = '\033[92m'
  R = '\033[91m'
  ENDC = '\033[0m'

class defaultPorts:
  dp = ['20','21','22','23','25','53','67','68','80','161','162','123','443','7104','7102','7105']

def hostScan(targetHost,targetPorts):
  try:
    targetIp = gethostbyname(targetHost)
    targetName = gethostbyaddr(targetIp)
    if (len(targetName[0]) > len(targetIp)):
      stickLen = len(targetName[0])
    else: 
      stickLen = len(targetIp)
    infoG = colors.G + " [INFO] " + colors.ENDC
    infoR = colors.R + " [INFO] " + colors.ENDC
    print(colors.R + " " + "-"*18, "-"*stickLen + colors.ENDC, sep="")
    print(infoG + "Ip address: " + str(targetIp))
    try:
      print(infoG + "Host name: " + str(targetName[0]))
      if (str(targetName[1]) != "[]"):
        print(infoG + "Host IP address: " + str(targetName[1]))
    except:
      print(infoR + "Other addresses not found")
    if len(targetPorts) > 10:
      if targetPorts == defaultPorts.dp:
        print(infoG + "Ports: Default ports => 20 21 22 23 25 53 67 68 80 161 162 123 443 7104 7102 7105")
      else:
        print(infoG + "Ports: All ports " + str(targetPorts[0]) + " to " + str(targetPorts[-1:][0]))
      print(colors.G + " [INFO] Note: Since the length of the output will exceed 10 lines, closed ports will not be shown in the output, only open ports will be shown." + colors.ENDC)
      cleanConsole = True
    else:
      print(infoG + "Port(s): " + str(targetPorts))
      cleanConsole = False
    print(colors.R + " " + "-"*18, "-"*stickLen + colors.ENDC, sep="")
    print(infoG + "Port(s) Scanning...")
  except:
    print(infoR + "Hostname not found: " + str(targetHost))
    exit(0)

  for targetPort in targetPorts:
    thre = Thread(target=portScan, args=(targetHost, int(targetPort), cleanConsole))
    thre.start()

def portScan(targetHost,targetPort,cleanConsole):
  if cleanConsole == True:
    try:  
      sock = socket(AF_INET,SOCK_STREAM)
      sock.connect((targetHost,targetPort))
      print(colors.G + " [OK] " + str(targetPort) + " Port open" + colors.ENDC)
    except:
      print(end = "")
    finally:
      sock.close()
  else:
    try:  
      sock = socket(AF_INET,SOCK_STREAM)
      sock.connect((targetHost,targetPort))
      print(colors.G + " [OK] " + str(targetPort) + " Port open" + colors.ENDC)
    except:
      print(colors.R + " [X] " + str(targetPort) + " Port close" + colors.ENDC)
    finally:
      sock.close()

def main():
  parser = optparse.OptionParser("Command usage: python3 scan.py [option] arg [option] arg\nOpitons:\n  -H <host address, ex: 192.168.1.30 or example.com>\n  -p <port, ex: 80 or 80,144,265>\n  -r <port range, ex: 80,1024>\n\nCommand examples:\n  -H and -p usage ex: python3 scan.py -H 192.168.1.30 -p 80\n  -H and -r usage ex: python3 scan.py -H google.com -r 20,90")
  parser.add_option("-H", dest="targetHost", type="string", help="The web address or IP address to be scanned.")
  parser.add_option("-p", dest="targetPort", type="string", help="The port address(es) of the entered address to be scanned.")
  parser.add_option("-r", dest="targetPortRange", type="string", help="The port address range of the entered address to be scanned.")
  (options,args) = parser.parse_args()
  targetHost = options.targetHost
  targetPortMain = str(options.targetPort).split(",")
  targetPortRange = str(options.targetPortRange).split(",")
  try:
    if targetHost == None:
      exit(0)
    else:
      if targetPortMain == ['None'] and targetPortRange == ['None']:
        targetPorts = defaultPorts.dp
      elif targetPortMain == ['None']:
        if targetPortRange[0] == ['None'] and targetPortRange[1] == ['None']:
          print(parser.usage)
          exit(0)
        else:
          portRange = []
          if targetPortRange[0]>targetPortRange[1]:
            tpr1 = int(targetPortRange[0])+1
            tpr2 = int(targetPortRange[1])
            while tpr1 != tpr2:
              portRange.append(tpr2)
              tpr2=tpr2+1
          elif targetPortRange[0]<targetPortRange[1]:
            tpr1 = int(targetPortRange[0])
            tpr2 = int(targetPortRange[1])+1
            while tpr1 != tpr2:
              portRange.append(tpr1)
              tpr1=tpr1+1
          targetPorts = portRange
      else:
        targetPorts = targetPortMain
  except:
    print(parser.usage)
    exit(0)

  hostScan(targetHost,targetPorts)

if __name__ == "__main__":
  main()