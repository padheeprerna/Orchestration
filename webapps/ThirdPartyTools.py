import sys
import os
# from WebAutomation import log

hostname = ""


def main():
    thirdpartyinvoke(sys.argv[1])


def thirdpartyinvoke(hostname):
    try:
        os.chdir('C:\\Program Files (x86)\\Nmap')
        os.system('nmap ' + '-sV ' + hostname)

        os.chdir('C:\\Users\\Public\\Desktop\\code\\SSLScan')
        os.system('SSLscan ' + hostname)

        print ('SSLScan ' + hostname)

    except Exception as e:
        print(str(e))
        # log.record('debug', e.message)


main()
