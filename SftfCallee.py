import sys
import getopt
from SftfClientBase import SftfClientBase


class SftfCallee(SftfClientBase):
    pass


# -----------------------------------------------------

if __name__ == '__main__':
    callee = SftfCallee()
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "h:p:t:s",
                                   ["host=", "port=", "timeout=", "cert=", "ssl"])
    except getopt.GetoptError as err:
        print(err)
        print(SftfCallee.usage())
        sys.exit(2)

    if len(opts) == 0 and len(args) == 0:
        print(SftfCallee.usage())
        sys.exit(1)

    for o, a in opts:
        if o in ("-h", "--host"):
            callee.host = a
        elif o in ("-p", "--port"):
            callee.port = int(a)
        elif o in ("-t", "--timeout"):
            callee.timeout = float(a)
        elif o == "--cert":
            callee.cert_file = a
        elif o in ("-s", "--ssl"):
            callee.use_ssl = True
        else:
            print("unknown option %s" % o)
            print(SftfCallee.usage())
            sys.exit(2)

    # start manager
    callee.run()