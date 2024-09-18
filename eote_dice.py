#!/usr/bin/env python3

import argparse
import sys

import colorama

from dice import DicePool
from dice import Symbol
from plot import DicePlotter


def parse_arguments():
    parser = argparse.ArgumentParser(description='Analyzes or rolls SW EotE dice pools.')
    parser.add_argument('-p',
                        '--pool',
                        type=str,
                        required=True,
                        action='append',
                        help='A string containing the EotE dice pool, annotated using the first '
                             'letter of color of the die (except for black Setback dice, '
                             'which use "k".  Example: "yygbrppk".')

    parser.add_argument('-d',
                        '--debug',
                        action='store_true',
                        help='Print debug information.')

    parser.add_argument('-a',
                        '--above',
                        action='store_true',
                        help='activate probability above threshold mode, default is exact match probability',)

    parser.add_argument('-C',
                        '--compare',
                        action='store_true',
                        help='compare all pool on the same graph instead of multiple graphs',)

    parser.add_argument('-E',
                            '--experimental',
                            action='store_true',
                            help='Use custom adjusted dice',
                            default=False)

    subparsers = parser.add_subparsers(dest='command', help='Subcommands.')
    analysis_parser = subparsers.add_parser('analyze', help='Analysis commands.')
    analysis_parser.add_argument('-t',
                                 '--triumph-cutoff',
                                 type=int,
                                 required=False,
                                 default=None,
                                 help='Return probability of at least this many triumph.')
    analysis_parser.add_argument('-s',
                                 '--success-cutoff',
                                 type=int,
                                 required=False,
                                 default=None,
                                 help='Return probability of at least this many success.')
    analysis_parser.add_argument('-a',
                                 '--advantage-cutoff',
                                 type=int,
                                 required=False,
                                 default=None,
                                 help='Return probability of at least this many advantage.')
    analysis_parser.add_argument('-d',
                                 '--despair-cutoff',
                                 type=int,
                                 required=False,
                                 default=None,
                                 help='Return probability of at least this many despair.')

    plot_parser = subparsers.add_parser('plot', help='Plot statistics.')
    plot_parser.add_argument('--upgrade','-u', type=int, required=False, default=0, help='Number of dice to upgrade, will plot one line per upgrade pool')
    plot_subparser = plot_parser.add_subparsers(dest='plotcommand', help='Subcommands.')
    singe_plot_parser = plot_subparser.add_parser('single', help='Plot single Symbol probability distribution, can specify multiple symbols')
    singe_plot_parser.add_argument('--Symbol',"-s",type=Symbol,action='append',required=False,help='value between T(riumph), s(uccess), a(dvantage), D(espair)')
    plot_subparser.add_parser('combined', help='Plot special cases')
    compare_plot_parser=plot_subparser.add_parser('compare', help='Plot multiple pools, without upgrade')
    compare_plot_parser.add_argument('--Symbol',"-s",type=Symbol,action='append',required=False,help='value between T(riumph), s(uccess), a(dvantage), D(espair)')
    subparsers.add_parser('roll', help='Roll pool of dices.')


    return parser.parse_args()


def main() -> None:
    colorama.init(autoreset=True, strip=False)
    args = parse_arguments()
    DicePool._experimental = args.experimental

    try:
        args.debug and print(args), print(args.command)
        DicePool.is_experimental = args.experimental
        dice_pool = DicePool.from_string(args.pool[0])

        if args.command == 'analyze':
            print(dice_pool.mean())
            if (args.triumph_cutoff is not None or
               args.success_cutoff is not None or
               args.advantage_cutoff is not None or
               args.despair_cutoff is not None):
                probability_above = dice_pool.probability_above(
                    triumph_cutoff=args.triumph_cutoff,
                    success_cutoff=args.success_cutoff,
                    advantage_cutoff=args.advantage_cutoff,
                    despair_cutoff=args.despair_cutoff)
                if probability_above >= 0.5:
                    probability_color = colorama.Fore.GREEN
                else:
                    probability_color = colorama.Fore.RED

                print('{}Probability Above: {}{}%{}'.format(
                    colorama.Style.BRIGHT,
                    probability_color,
                    round(probability_above, 2) * 100,
                    colorama.Style.RESET_ALL))
                if args.triumph_cutoff is not None:
                    print('\tTriumph: {}'.format(args.triumph_cutoff))
                if args.success_cutoff is not None:
                    print('\tSuccess: {}'.format(args.success_cutoff))
                if args.advantage_cutoff is not None:
                    print('\tAdvantage: {}'.format(args.advantage_cutoff))
                if args.despair_cutoff is not None:
                    print('\tDespair: {}'.format(args.despair_cutoff))
        elif args.command == 'roll':
            symbols_ascii, cancelled_symbols_ascii = dice_pool.roll_ascii()
            print('Full Roll: {}'.format(symbols_ascii))
            print('Net Roll:  {}'.format(cancelled_symbols_ascii))
        elif args.command == 'plot':
            DicePlotter.plot(args)
        else:
            print('No command specified, see --help.', file=sys.stderr)
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()
