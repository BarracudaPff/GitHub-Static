import argparse
import os
import tarfile
from shutil import copyfile

import boto3
import progressbar

arg_parser = argparse.ArgumentParser(description="Model downloader")
arg_parser.add_argument("--aws_id", type=str, help="AWS access id key", metavar="<awsId>", required=True)
arg_parser.add_argument("--aws_secret", type=str, help="AWS access secret key", metavar="<awsSecret>", required=True)
arg_parser.add_argument("--aws_bucket", type=str, help="AWS bucket", metavar="<awsBucket>", required=True)
arg_parser.add_argument("--aws_filename", type=str, help="AWS file", metavar="<awsBucket>", required=True)


def __download_file(filename: str, dest_file: str, AWS_ID: str, AWS_SECRET: str, bucket: str):
    print(f"Connecting to S3")
    s3 = boto3.client("s3", aws_access_key_id=AWS_ID, aws_secret_access_key=AWS_SECRET)
    print(f"S3 connected")

    size = float(s3.head_object(Bucket=bucket, Key=filename)["ContentLength"])
    up_progress = progressbar.progressbar.ProgressBar(maxval=size)
    up_progress.start()

    def upload_progress(chunk):
        up_progress.update(up_progress.currval + chunk)
        print(up_progress._format_line())

    print(f"Downloading '{filename}'")
    os.makedirs(os.path.dirname(f"raw/{filename}"), exist_ok=True)
    s3.download_file(bucket, filename, f"raw/{filename}", Callback=upload_progress)
    up_progress.finish()
    print(f"File {filename} downloaded from s3://{bucket}/{filename}")

    __use_raw_file(f"raw/{filename}", dest_file)


def __use_raw_file(filename: str, dest_file: str):
    if filename.endswith(".tar.gz") or filename.endswith(".tar"):
        __unpack_archive(filename, dest_file)
        print(f"Unpacked {filename} to {dest_file}")
    else:
        copyfile(filename, dest_file)
        print(f"File {dest_file} copied from {filename}")


def __unpack_archive(archive_path: str, dest_path: str):
    if archive_path.endswith(".tar.gz"):
        tar = tarfile.open(archive_path, "r:gz")
    elif archive_path.endswith(".tar"):
        tar = tarfile.open(archive_path, "r:")
    else:
        raise ValueError(f"File {archive_path} is not of a known archive type.")

    tar.extractall(dest_path)
    tar.close()


if __name__ == '__main__':
    args = arg_parser.parse_args()
    __download_file(args.aws_filename", f"models/{args.aws_filename}", args.aws_id, args.aws_secret, args.aws_bucket)
