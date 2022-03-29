import sys
import os
# from WebAutomation import log

hostname = ""


def main():
    thirdpartyinvoke(sys.argv[1])


def thirdpartyinvoke(hostname):
    try:

        os.system('nmap ' + '-sV ' + hostname)
        # print('nmap ' + '--script http-methods ' + hostname)
        #
        # os.system('nmap ' + '--script http-methods ' + hostname)
        os.system('SSLscan ' + hostname)

    except Exception as e:
        setattr(e, 'message', 'show this message')
        print(e.message)
        # log.record('debug', e.message)


main()
