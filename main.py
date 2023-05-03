from file_operation import *
from replica_operation import *

import argparse
import time

def get_arguments():
    CLI=argparse.ArgumentParser()
    CLI.add_argument(
      "--src",  # name on the CLI - drop the `--` for positional/required parameters
      nargs=1,  # 0 or more values expected => creates a list
      type=str,
      default="",
      help="Source Folder Path", # default if nothing is provided
    )
    CLI.add_argument(
      "--repl",
      nargs=1,
      type=str,  # any type/callable can be used here
      default="",
      help="Replica folder path",
    )
    CLI.add_argument(
      "--p",
      nargs=1,
      type=float,  # any type/callable can be used here
      default=-1.0,
      help="Loop period (in seconds)",
    )
    CLI.add_argument(
      "--log",
      nargs=1,
      type=str,  # any type/callable can be used here
      default="",
      help="Log file path",
    )

    args = CLI.parse_args()
    return (args.src[0], args.repl[0], args.p[0], args.log[0])
    
def main():
    src_path, repl_path, period, log_path = get_arguments()
    clear_replica(repl_path)
    log_file_stream = open(log_path, "w")
    start_time = time.time()
    update_replica(src_path, repl_path, log_file_stream)
    log_file_stream.close()

    while True:
        log_file_stream = open(log_path, "a")
        if(time.time() - start_time) >= period:
            update_replica(src_path, repl_path, log_file_stream)
            start_time = time.time()
        log_file_stream.close()

if __name__ == "__main__":
    main()