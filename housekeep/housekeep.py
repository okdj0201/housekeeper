#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import yaml
import shutil
import glob
import datetime
import os
import pathlib


def hk_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', '-d', nargs="*", type=str, help='Target dir name')
    parser.add_argument('--conf', '-c', type=str, help='Configuration file name')
    return parser.parse_args()

def expand_target_dir(conf, dirs):
    if dirs:
        conf['target_dir'].extend(parser.parse_args().dir)

def load_config(conf):
    if conf:
        conf_path = conf
    else:
        conf_path = os.path.expanduser('~/.housekeep_conf.yml')
    with open(conf_path) as f:
        conf = yaml.safe_load(f)
    return conf

def housekeep(dirname, conf):
    for ext in conf['exts'].keys():
        outdir = os.path.expanduser(f'{conf["outdir"]}/{conf["exts"][ext]}')
        os.makedirs(outdir, exist_ok=True)
        try:
          expand_path = os.path.expanduser(dirname)
          target_list = glob.glob(f'{expand_path}/*.{ext}')
          for target in target_list:
            try:
              shutil.move(target, outdir)
            except:
              fname=f'{target.rsplit("/")[-1]}_{str(datetime.date.today())}'
              newout = os.path.join(outdir,fname)
              shutil.move(target, newout)
        except FileNotFoundError:
          pass

def main():
    args = hk_argparse()
    conf = load_config(args.conf)
    expand_target_dir(conf, args.dir)
    for dirname in conf['target_dir']:
        housekeep(dirname, conf)

if __name__ == '__main__':
    main()

