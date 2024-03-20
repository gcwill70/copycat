import argparse
import glob
import logging
import os
import subprocess
import sys

VERSION = "1.10"

DEBUG=int(logging.DEBUG / 10)
INFO=int(logging.INFO / 10)
WARNING=int(logging.WARNING / 10)
ERROR=int(logging.ERROR / 10)
CRITICAL=int(logging.CRITICAL / 10)

FORMATS = {
    1: "%(asctime)s:%(levelname)s:%(message)s",
    2: "%(levelname)s:%(message)s",
    3: "%(message)s",
}

def process(patterns: list[str]):
    # find all matches
    logging.debug(f"finding files...")
    matches: list[str] = []
    for pattern in patterns:
        # ensure folder matches will return all files beneath it
        if (os.path.isdir(pattern)):
            pattern += "/**/*.*"
        elif (pattern.endswith("/**")):
            pattern += "/*.*"
        logging.debug(f"parsing: {pattern}")
        matches += glob.glob(pattern, recursive=True)
    # concatenate matches
    logging.debug(f"concatenating...")
    content = ""
    logging.info(f"lines\tfilepath")
    for match in matches:
        content += f"// {match}\n"
        try:
            num_lines = 0
            with open(match, "r", encoding="utf-8") as f:
                file_content = f.read() + "\n\n\n"
                content += file_content
                num_lines = file_content.count('\n')
            logging.info(f"{num_lines}\t{match}")
        except UnicodeDecodeError:
            logging.debug(f"skipping: {match}")
        except Exception as e:
            logging.debug(f"failed: {match}. {e}")
            pass
    return content

def copy_to_clipboard(content: str):
    try:
        process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        process.communicate(input=content.encode())
        process.stdin.close()
        process.wait()
        num_lines = content.count('\n')
        logging.info(f"copied {num_lines} lines to clipboard")
    except Exception:
        logging.error("clipboard copying is not available")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Concatenate and copy files to clipboard."
    )
    parser.add_argument(
        "patterns",
        nargs="*",
        default=["."],
        help="File names, file paths, or glob patterns matching the files to concatenate. Defaults to current directory.",
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'v{VERSION}',
        help='Show the version number and exit'
    )
    parser.add_argument(
        "--no-copy",
        action="store_true",
        help="Do not copy results to clipboard and print instead."
    )
    parser.add_argument(
        "--log",
        help="Log file to use. Defaults to stdout.",
    )
    parser.add_argument(
        "--log-level",
        type=int,
        choices=[DEBUG, INFO, WARNING, ERROR, CRITICAL],
        default=INFO,
        help=f'''Logging level. Defaults to {INFO}.
        DEBUG={DEBUG}
        INFO={INFO}
        WARNING={WARNING}
        ERROR={ERROR}
        CRITICAL={CRITICAL}'''
    )
    parser.add_argument(
        "--log-format",
        type=int,
        choices=[1, 2, 3],
        default=3,
        help=f'''Logging format. Defaults to 3.
        1='DATE TIME:LEVEL:MESSAGE'
        2='LEVEL:MESSAGE'
        3='MESSAGE'
        '''
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help=f"Sets `--log-level {DEBUG} --log-format {DEBUG}`"
    )

    args = parser.parse_args()

    if args.verbose:
        args.log_level = 1
        args.log_format = 1

    # logging
    logging.basicConfig(
        level=args.log_level * 10,
        format=FORMATS[args.log_format],
        handlers=[
            logging.StreamHandler(open(args.log, "w+") if args.log else sys.stdout)
        ],
    )
    logging.debug(f"{args}")

    content = process(args.patterns)

    if args.no_copy:
        print(content)
    else:
        copy_to_clipboard(content)

if __name__ == "__main__":
    main()
