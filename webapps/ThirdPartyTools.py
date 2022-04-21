import sys
import os
# from WebAutomation import log

hostname = ""
orchPath = str(os.path.dirname(os.path.realpath(sys.argv[0])))

def main():
    thirdpartyinvoke(sys.argv[1])


def thirdpartyinvoke(hostname):
    try:
        os.chdir('C:\\Program Files (x86)\\Nmap')
        os.system('nmap ' + '-sV ' + hostname)

        os.chdir(orchPath + "\\..\\SSLScan")
        os.system('SSLscan ' + hostname)
        print('SSLScan ' + hostname)

    except Exception as e:
        print(str(e))
        # log.record('debug', e.message)


main()
