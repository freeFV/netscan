#!/usr/bin/python3
import argparse

from utils.process_inputs import process_inputs, str_comma, str_ports
from utils.dispatch import dispatch_targets
from utils.output import Output
from lib.rpcscan.rpcscan import rpcscan_worker

def main():
    parser = argparse.ArgumentParser(description='RPCScan')
    parser.add_argument('targets', type=str)
    parser.add_argument('--timeout', metavar='timeout', nargs='?', type=int, help='Connect timeout', default=5, dest='timeout')
    # Actions
    parser.add_argument('--rpc', action='store_true', help='List RPC entries', dest='rpc')
    parser.add_argument('--mounts', action='store_true', help='List RPC entries', dest='mounts')
    parser.add_argument('--list', action='store_true', help='List RPC entries', dest='list')
    parser.add_argument('--uid', metavar='uid', nargs='?', type=int, help='Connect uid (for NFS)', default=0, dest='uid')
    parser.add_argument('--gid', metavar='gid', nargs='?', type=int, help='Connect gid (for NFS)', default=0, dest='gid')
    parser.add_argument('--recurse', metavar='number of times', nargs='?', type=int, help='Number of recursions during directory listing', default=1, dest='recurse')
    # Dispatcher arguments
    parser.add_argument('-w', metavar='number worker', nargs='?', type=int, help='Number of concurent workers', default=10, dest='workers')
    args = parser.parse_args()

    static_inputs = {}

    actions = {}
    if args.rpc:
        actions['rpc'] = {}
    if args.mounts:
        actions['mounts'] = {}
    if args.list:
        actions['list'] = {'recurse': args.recurse, 'uid': args.uid, 'gid': args.gid}

    Output.setup()

    rpcscan(args.targets, static_inputs, args.workers, actions, args.timeout)

    Output.stop()

def rpcscan(input_targets, static_inputs, workers, actions, timeout):

    args = (actions, timeout)

    dispatch_targets(input_targets, static_inputs, rpcscan_worker, args, workers=workers)

if __name__ == '__main__':
    main()
