# -*- coding: utf-8 -*-
import os
import sys
import argparse
from shutil import rmtree
from multiprocessing import cpu_count
from importlib import import_module


def run_examples(example, pipelines, data_path, plugin=None, rm_base_dir=True):
    from nipype import config
    from nipype.interfaces.base import CommandLine

    if plugin is None:
        plugin = 'MultiProc'

    print('running example: %s with plugin: %s' % (example, plugin))
    config.enable_debug_mode()
    config.enable_provenance()
    CommandLine.set_default_terminal_output("stream")

    plugin_args = {}
    if plugin == 'MultiProc':
        plugin_args['n_procs'] = int(
            os.getenv('NIPYPE_NUMBER_OF_CPUS', cpu_count()))

    module = import_module('.' + example, 'niflow.nipype1.examples')
    for pipeline in pipelines:
        wf = getattr(module, pipeline)
        wf.base_dir = os.path.join(os.getcwd(), 'output', example, plugin)

        results_dir = os.path.join(wf.base_dir, wf.name)
        if rm_base_dir and os.path.exists(results_dir):
            rmtree(results_dir)

        # Handle a logging directory
        log_dir = os.path.join(os.getcwd(), 'logs', example)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        wf.config = {
            'execution': {
                'hash_method': 'timestamp',
                'stop_on_first_rerun': 'true',
                'write_provenance': 'true',
                'poll_sleep_duration': 2
            },
            'logging': {
                'log_directory': log_dir,
                'log_to_file': True
            }
        }
        try:
            wf.inputs.inputnode.in_data = os.path.abspath(data_path)
        except AttributeError:
            pass  # the workflow does not have inputnode.in_data

        wf.run(plugin=plugin, plugin_args=plugin_args)
        # run twice to check if nothing is rerunning
        wf.run(plugin=plugin)


def main():
    parser = argparse.ArgumentParser(description="Run example worklow")
    parser.add_argument('example', type=str, help="name of example workflow")
    parser.add_argument('plugin', type=str, help="execution plugin")
    parser.add_argument('data_path', type=str, help="path to input data")
    parser.add_argument('pipeline', type=str, nargs="+",
                        help="name of pipelines to run")
    opts = parser.parse_args()
    run_examples(opts.example, opts.pipeline, opts.data_path, opts.plugin)
