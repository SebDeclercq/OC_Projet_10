#!/usr/bin/env python3
from typing import Any, List
import subprocess
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    help: str = 'Run tests and return tests coverage analysis'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--app', type=str, help='The App to test')
        parser.add_argument('--html', action='store_true',
                            help='Turns on the HTML reporting')

    def handle(self, *args: Any, **kwargs: Any) -> None:
        print('Starts the tests coverage compute')
        cmds: List[str] = [
            'coverage erase',
            'coverage run manage.py test',
        ]
        if kwargs['html']:
            cmds.append('coverage html')
        if 'app' in kwargs and kwargs['app'] is not None:
            cmds[1] += ' ' + kwargs['app']
        for cmd in cmds:
            print(cmd)
            subprocess.run(cmd.split())
        uncovered_cmd: str = 'coverage report --skip-covered'
        if 'app' in kwargs and kwargs['app'] is not None:
            print(f'{uncovered_cmd} | grep {kwargs["app"]}')
            uncovered: subprocess.Popen = subprocess.Popen(
                (uncovered_cmd.split()),
                stdout=subprocess.PIPE
            )
            report: str = uncovered.stdout.read().decode('utf8').rstrip()
            max_len = stmts = miss = 0
            cover: List[int] = []
            for line in report.split('\n'):
                if ('Name' in line) or ('----' in line):
                    print(line)
                    if 'Name' in line:
                        max_len = line.find('Stmts')
                    continue
                elif line.startswith(kwargs['app'].strip('/')):
                    print(line)
                else:
                    continue
                parts: List[str] = line.split()
                stmts += int(parts[1])
                miss += int(parts[2])
                cover.append(int(parts[3].strip('%')))
            if len(cover):
                total: str = str(int(sum(cover) / len(cover))) + '%'
            else:
                total = '0%'
            print(f'{"TOTAL": <{max_len}}{stmts: >5}{miss: >7}{total: >7}')
        else:
            print(uncovered_cmd)
            subprocess.run(uncovered_cmd.split())
