#!/usr/bin/env python
import argparse
import os
from datetime import datetime
from datetime import timedelta
from random import randint
from subprocess import Popen
import sys

skip_date_range = [['2015-07-01','2015-07-15']\
                    ,['2015-08-12','2015-09-10']\
                    ,['2015-09-12','2015-10-25']\
                    ,['2015-11-12','2015-12-01']\
                    ,['2015-12-12','2016-03-25']\
                    ,['2016-04-15','2016-06-25']\
                    ,['2016-07-15','2016-09-25']\
                    ,['2016-12-15', '2017-01-23']\
                    ,['2017-04-12', '2017-06-23']\
                    ,['2017-07-03', '2017-07-05']\
                    ,['2017-07-26', '2017-08-23']\
                    ,['2017-10-15', '2017-11-04']\
                    ,['2017-12-23', '2018-01-10']\
                    ,['2018-02-23', '2018-06-10']\
                    ,['2018-07-03', '2018-07-10']\
                    ,['2018-09-14', '2018-10-10']\
                    ,['2018-12-20', '2019-02-10']\
                    ,['2019-03-20', '2019-04-10']\
                    ,['2019-09-20', '2019-10-10']\
                    ,['2019-12-22', '2020-01-30']\
                    ,['2020-04-22', '2020-08-30']\
                    ,['2020-12-22', '2021-03-12']\
                    ,['2021-07-02', '2021-08-12']\
                    ,['2021-12-02', '2022-02-12']\
                    ,['2022-07-02', '2022-07-12']]


def main(def_args=sys.argv[1:]):
    args = arguments(def_args)
    curr_date = datetime.now()
    directory = 'repository-' + curr_date.strftime('%Y-%m-%d-%H-%M-%S')
    repository = args.repository
    user_name = args.user_name
    user_email = args.user_email
    if repository is not None:
        start = repository.rfind('/') + 1
        end = repository.rfind('.')
        directory = repository[start:end]
    no_weekends = args.no_weekends
    frequency = args.frequency
    days_before = args.days_before
    if days_before < 0:
        sys.exit('days_before must not be negative')
    days_after = args.days_after
    if days_after < 0:
        sys.exit('days_after must not be negative')
    os.mkdir(directory)
    os.chdir(directory)
    run(['git', 'init', '-b', 'main'])

    if user_name is not None:
        run(['git', 'config', 'user.name', user_name])

    if user_email is not None:
        run(['git', 'config', 'user.email', user_email])

    start_date = curr_date.replace(hour=20, minute=0) - timedelta(days_before)
    for day in (start_date + timedelta(n) for n
                in range(days_before + days_after)):
        if (not no_weekends or day.weekday() < 5) \
                and randint(0, 100) < frequency:
            for commit_time in (day + timedelta(minutes=m)
                                for m in range(contributions_per_day(args))):
                if not is_skip_date(commit_time):
                    # print(commit_time)
                    contribute(commit_time)

    if repository is not None:
        run(['git', 'remote', 'add', 'origin', repository])
        run(['git', 'branch', '-M', 'main'])
        run(['git', 'push', '-u', 'origin', 'main'])

    print('\nRepository generation ' +
          '\x1b[6;30;42mcompleted successfully\x1b[0m!')


def contribute(date):
    with open(os.path.join(os.getcwd(), 'README.md'), 'a') as file:
        file.write(message(date) + '\n\n')
    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', '"%s"' % message(date),
         '--date', date.strftime('"%Y-%m-%d %H:%M:%S"')])


def run(commands):
    Popen(commands).wait()


def message(date):
    return date.strftime('Contribution: %Y-%m-%d %H:%M')


def contributions_per_day(args):
    max_c = args.max_commits
    if max_c > 20:
        max_c = 20
    if max_c < 1:
        max_c = 1
    return randint(1, max_c)


def arguments(argsval):
    parser = argparse.ArgumentParser()
    parser.add_argument('-nw', '--no_weekends',
                        required=False, action='store_true', default=False,
                        help="""do not commit on weekends""")
    parser.add_argument('-mc', '--max_commits', type=int, default=10,
                        required=False, help="""Defines the maximum amount of
                        commits a day the script can make. Accepts a number
                        from 1 to 20. If N is specified the script commits
                        from 1 to N times a day. The exact number of commits
                        is defined randomly for each day. The default value
                        is 10.""")
    parser.add_argument('-fr', '--frequency', type=int, default=80,
                        required=False, help="""Percentage of days when the
                        script performs commits. If N is specified, the script
                        will commit N%% of days in a year. The default value
                        is 80.""")
    parser.add_argument('-r', '--repository', type=str, required=False,
                        help="""A link on an empty non-initialized remote git
                        repository. If specified, the script pushes the changes
                        to the repository. The link is accepted in SSH or HTTPS
                        format. For example: git@github.com:user/repo.git or
                        https://github.com/user/repo.git""")
    parser.add_argument('-un', '--user_name', type=str, required=False,
                        help="""Overrides user.name git config.
                        If not specified, the global config is used.""")
    parser.add_argument('-ue', '--user_email', type=str, required=False,
                        help="""Overrides user.email git config.
                        If not specified, the global config is used.""")
    parser.add_argument('-db', '--days_before', type=int, default=365,
                        required=False, help="""Specifies the number of days
                        before the current date when the script will start
                        adding commits. For example: if it is set to 30 the
                        first commit date will be the current date minus 30
                        days.""")
    parser.add_argument('-da', '--days_after', type=int, default=0,
                        required=False, help="""Specifies the number of days
                        after the current date until which the script will be
                        adding commits. For example: if it is set to 30 the
                        last commit will be on a future date which is the
                        current date plus 30 days.""")
    return parser.parse_args(argsval)


def is_skip_date(date_time):
    date_time = datetime.strptime(str(date_time)[:10], "%Y-%m-%d")
    for sdr in skip_date_range:
        start_date = datetime.strptime(sdr[0], "%Y-%m-%d")
        end_date = datetime.strptime(sdr[1], "%Y-%m-%d")
        if date_time >= start_date and date_time <= end_date:
            return True
    return False


if __name__ == "__main__":
    main()
