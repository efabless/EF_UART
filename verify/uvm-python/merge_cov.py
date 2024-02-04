
from caravel_cocotb.scripts.merge_coverage import merge_fun_cov
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Call a function with a path.')
    parser.add_argument('path', type=str, help='The path to use for the function.')
    args = parser.parse_args()
    merge_fun_cov(args.path)
