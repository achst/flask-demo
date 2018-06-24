from optparse import OptionParser


def init():
    parser = OptionParser()
    parser.add_option("--mode", default='dev', dest="mode", help="development environment", type=str)
    parser.add_option("--port", default=8080, dest="port", help="http listen port", type=int)
    options, args = parser.parse_args()
    return options, args
