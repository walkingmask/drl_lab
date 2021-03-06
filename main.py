#!/usr/bin/env python
# encoding: utf-8

from argparse import ArgumentParser
from datetime import datetime, timedelta, timezone
import importlib
import os
from pprint import pprint
import sys

from drl_lab.expt import Experiment

# Default hyper parameters

env_hparams = {
    'env_id': 'Breakout_pygame-v0',
    'observation': {
        'normalize': False,
        'rescaled_shape': [],
        'opt_flow': False,
    },
    'action': {
        'excluded_actions': [],
    },
}

run_hparams = {
    'verbose': False,
    'save_at': None,  # None, int, list of float or int
    'max_steps': 1000,
    'num_runs': 1,
}

nn_hparams = {
    'layers': [
        ['conv', 30, 8, 4],
        ['conv', 40, 4, 3],
        ['conv', 60, 3, 1],
        ['gap'],
        ['fc', 512]],
    'learn_rate': 0.00005,
    'optimizer': 'RMSprop',
    'saved_model': None,
}

agent_hparams = {
    'reward_decay': 0.99,
    'initial_epsilon': 1.0,
    'final_epsilon': 0.1,
    'batch_size': 32,
    'target_q_network_update_freq': 10,
}

# Overwrite hprams with arguments

parser = ArgumentParser()
parser.add_argument('--name', default='expt', help='Experiment name.')
parser.add_argument('--hparams', help='Path to hparams.py.')
parser.add_argument('--env-id',  help='Environemt id of gym or gym-ple.')
parser.add_argument('--obs-normailize', action='store_true',
                    help="Enable observation normalization.")
parser.add_argument('--obs-opt-flow', action='store_true',
                    help="Enable observation opt-flow.")
parser.add_argument('--max-steps', type=int,
                    help="Specify max_steps.")
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Enable verbose.")
parser.add_argument('--num-runs', type=int,
                    help="Specify num_runs.")
parser.add_argument('-s', '--save',  action='store_true',
                    help='Save something.')
parser.add_argument('--saved-model',  help='Path to saved model.')
parser.add_argument('--learn-rate', type=int,
                    help="Specify learn_rate.")
parser.add_argument('--optimizer',  help='Specify optimizer (RMSProp, Adam).')
parser.add_argument('-n', '--dry-run', action='store_true',
                    help="Dry run.")
args = parser.parse_args()

if args.hparams is not None:
    if not os.path.exists(args.hparams):
        raise FileNotFoundError(args.hparams)
    sys.path.append(args.hparams)
    hparams = importlib.import_module('hparams')
    for k in hparams.env_hparams.keys():
        env_hparams[k] = hparams.env_hparams[k]
    for k in hparams.run_hparams.keys():
        run_hparams[k] = hparams.run_hparams[k]
    for k in hparams.nn_hparams.keys():
        nn_hparams[k] = hparams.nn_hparams[k]
    for k in hparams.agent_hparams.keys():
        agent_hparams[k] = hparams.agent_hparams[k]
if args.env_id is not None:
    env_hparams['env_id'] = args.env_id
if args.obs_opt_flow:
    env_hparams['observation']['opt_flow'] = True
if args.max_steps is not None:
    run_hparams['max_steps'] = args.max_steps
if args.verbose:
    run_hparams['verbose'] = True
if args.save:
    run_hparams['save_at'] = [0.0, 1.0]
if args.num_runs is not None:
    run_hparams['num_runs'] = args.num_runs
if args.saved_model is not None:
    nn_hparams['saved_model'] = args.saved_model
if args.learn_rate is not None:
    nn_hparams['learn_rate'] = args.learn_rate
if args.optimizer is not None:
    nn_hparams['optimizer'] = args.optimizer

# Run

if args.verbose:
    JST = timezone(timedelta(hours=+9), 'JST')
    print("Start runnning at {}.".format(str(datetime.now(JST))))
    print("Hyper parameters are below.")
    pprint({
        'env_hparams': env_hparams,
        'run_hparams': run_hparams,
        'nn_hparams': nn_hparams,
        'agent_hparams': agent_hparams,
    })

if not args.dry_run:
    expt = Experiment(args.name)
    expt.init(env_hparams, run_hparams, nn_hparams, agent_hparams)
    expt.run()
