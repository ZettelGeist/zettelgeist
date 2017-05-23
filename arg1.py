import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
parser.add_argument('--foo', action='store_const', const=True, default=False)
args = parser.parse_args(['35','--foo'])
print(args.echo, args.foo)
args = parser.parse_args(['35'])
#args = parser.parse_args()
print(args.echo, args.foo)
