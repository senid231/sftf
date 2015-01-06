import sys
import getopt
from SftfClientBase import SftfClientBase


class SftfCaller(SftfClientBase):
    pass


# -----------------------------------------------------

if __name__ == '__main__':
    caller = SftfCaller()
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "h:p:t:s",
                                   ["host=", "port=", "timeout=", "cert=", "ssl"])
    except getopt.GetoptError as err:
        print(err)
        print(SftfCaller.usage())
        sys.exit(2)

    if len(opts) == 0 and len(args) == 0:
        print(SftfCaller.usage())
        sys.exit(1)

    for o, a in opts:
        if o in ("-h", "--host"):
            caller.host = a
        elif o in ("-p", "--port"):
            caller.port = int(a)
        elif o in ("-t", "--timeout"):
            caller.timeout = float(a)
        elif o == "--cert":
            caller.cert_file = a
        elif o in ("-s", "--ssl"):
            caller.use_ssl = True
        else:
            print("unknown option %s" % o)
            print(SftfCaller.usage())
            sys.exit(2)

    # start manager
    caller.run()