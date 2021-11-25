# Port Scanner
Scan ports of website or ip address

## Installation / Git Clone

* Clone the repo:
 ```sh
git clone https://github.com/encoderpie/portScanner.git
 ```
 
## Usage

* To see the command options:
 ```sh
python3 scan.py
 ```
 
* Options:
  -H <host address, ex: 192.168.1.30 or example.com>
  -p <port, ex: 80 or 80,144,265>
  -r <port range, ex: 80,1024>

### Example Usages:
The web address or IP address to be scanned. (Scans specified address only with default ports)
└─── ```sh
python3 scan.py -H example.com
 ```

The port address(es) of the entered address to be scanned. (Scans only ports specified with comma in the -p option)
```sh
python3 scan.py -H 192.168.1.34 -p 80,144
 ```

The port address range of the entered address to be scanned. (Scans all ports between the 2 values specified in the -r option)
```sh
python3 scan.py -H 127.0.0.1 -r 80,144
 ```
 
## Contact
Bug reports and feedback for:
Discord: encoderpie#3312
