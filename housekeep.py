#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import yaml
import shutil
import glob
import os
import pathlib


def hk_argparse(conf):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', '-d', nargs="*", type=str, help='Target dir name')
    if parser.parse_args().dir:
        conf['target_dir'].extend(parser.parse_args().dir)

def load_config():
    with open('./conf.yml') as f:
        conf = yaml.safe_load(f)
    return conf

def housekeep(dirname, conf):
    for ext in conf['exts'].keys():
        outdir = f'{conf["outdir"]}/{conf["exts"][ext]}'
        os.makedirs(outdir, exist_ok=True)
        #if ext == 'tar.gz':
        #    import pdb; pdb.set_trace()
        try:
          expand_path = os.path.expanduser(dirname)
          target_list = glob.glob(f'{expand_path}/*.{ext}')
          for target in target_list:
            shutil.move(target, outdir)
        except FileNotFoundError:
          pass

def main():
    conf = load_config()
    hk_argparse(conf)
    for dirname in conf['target_dir']:
        housekeep(dirname, conf)

if __name__ == '__main__':
    main()

