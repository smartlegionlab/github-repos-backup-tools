# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import shutil


class CenteredTextDecorator:
    @classmethod
    def decorate(cls, text='', symbol=''):
        columns = cls._get_term_width()
        symbol = ' ' if not symbol else symbol
        msg = (f' {text} ' if text else '').center(columns, symbol[0])
        return msg

    @classmethod
    def _get_term_width(cls):
        return shutil.get_terminal_size()[0]


class SmartPrinter:
    @classmethod
    def print_center(cls, text='', symbol='-'):
        print(CenteredTextDecorator.decorate(text, symbol))

    @classmethod
    def show_header(cls, text=''):
        print(CenteredTextDecorator.decorate(symbol='*'))
        print(CenteredTextDecorator.decorate(text=text, symbol='-'))

    @classmethod
    def show_footer(cls, url='', copyright_=''):
        print(CenteredTextDecorator.decorate(symbol='-'))
        print(CenteredTextDecorator.decorate(text=url, symbol='-'))
        print(CenteredTextDecorator.decorate(text=copyright_, symbol='-'))
        print(CenteredTextDecorator.decorate(symbol='*'))
