import os
from glob import glob
import argparse
from hyp3lib.cutGeotiffs import cutFiles

parser = argparse.ArgumentParser(
    prog=os.path.basename(__file__),
    description=__doc__,
    )

parser.add_argument(
"--start-dir",
help="Geotiff files to clip; output will be have _clip appended to the file name"
)

parser.add_argument(
    "--pattern", nargs='+',
    help="search partten"
)

args = parser.parse_args()



files = []
start_dir = args.start_dir
pattern   = args.pattern

for dir,_,_ in os.walk(start_dir):
    for item in pattern:
        files.extend(glob(os.path.join(dir, item)))

cutFiles(files)

print('completed...')

