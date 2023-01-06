#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil
import glob
import os

from typing import List

from dependency_injector.containers import DeclarativeContainer
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
import click



class ApplicationContainer(DeclarativeContainer):
    config = providers.Configuration(yaml_files=['./conf.yml'])

@inject
def _run_housekeep_on_dir(target_dir,conf: providers.Configuration=Provide[ApplicationContainer.config])-> None:
    for ext in conf['exts'].keys():
        outdir = f'{conf["outdir"]}/{conf["exts"][ext]}'
        os.makedirs(outdir, exist_ok=True)
        try:
          expand_path = os.path.expanduser(target_dir)
          target_list = glob.glob(f'{expand_path}/*.{ext}')
          for target in target_list:
            shutil.move(target, outdir)
        except FileNotFoundError:
          pass


def _init_container():
    container = ApplicationContainer()
    container.wire(modules=[__name__])

@inject
def run_housekeep(additional_target_dirs: List[str]=[], conf: providers.Configuration=Provide[ApplicationContainer.config])-> None:
    target_dirs= list(conf.get('target_dir')) + list(additional_target_dirs)
    for target_dir in target_dirs:
        _run_housekeep_on_dir(target_dir)

@click.command()
@click.option('-d', '--dir', 'additional_target_dirs', multiple=True)
def housekeep(additional_target_dirs):
    _init_container()
    run_housekeep(additional_target_dirs)



if __name__ == '__main__':
    housekeep()