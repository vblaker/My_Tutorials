import argparse

# Set debug parameter from the command prompt
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--last_name", help="Last Name")
parser.add_argument("-v", "--version", help="Display version of the update utility and exit")
args = parser.parse_args()

if args.last_name:
    print(f"The passed argument was {args.last_name}")

if args.version:
    print(f"The version argument was {args.version}")



