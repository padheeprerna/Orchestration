import sys
import os
import traceback
# from WebAutomation import log

hostname = ""
orchPath = str(os.path.dirname(os.path.realpath(sys.argv[0])))

def main():
    thirdpartyinvoke(sys.argv[1])


def thirdpartyinvoke(hostname):
    try:
        #os.chdir('C:\\Program Files (x86)\\Nmap')
        os.system('nmap ' + '-sV ' + hostname)
        #os.system('nmap ' + hostname)

        #os.chdir(orchPath + "\\..\\SSLScan")
        #os.chdir('//home//ubuntu//Tools//Working_SSL//sslscan-1.11.11-rbsec')
        #os.system('SSLscan ' + hostname)
        #os.system('./sslscan ' + hostname)
        os.system('python -m sslyze ' + hostname)
        print('SSLScan ' + hostname)

    except Exception as e:
        traceback.print_exc()
        print(str(e))
        # log.record('debug', e.message)


main()
