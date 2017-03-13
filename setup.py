# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 McKinsey Academy
#
# Authors:
#          Jonathan Piacenti <jonathan@opencraft.com>
#
# This software's license gives you freedom; you can copy, convey,
# propagate, redistribute and/or modify this program under the terms of
# the GNU Affero General Public License (AGPL) as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version of the AGPL published by the FSF.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program in a file in the toplevel directory called
# "AGPLv3".  If not, see <http://www.gnu.org/licenses/>.
#
"""Setup for poll XBlock."""

import os
import subprocess
from setuptools import setup
from setuptools.command.install import install as _install


class XBlockInstall(_install):
    """Custom XBlock install command."""

    def run(self):
        _install.run(self)
        self.compile_translations()

    def compile_translations(self):
        """
        Compiles textual translations files(.po) to binary(.mo) files.
        """
        self.announce('Compiling translations')
        try:
            for dirname, _, files in os.walk(os.path.join('poll', 'translations')):
                for fname in files:
                    if os.path.splitext(fname)[1] == '.po':
                        po_path = os.path.join(dirname, fname)
                        mo_path = os.path.splitext(po_path)[0] + '.mo'
                        self.announce('Compiling translation at %s' % po_path)
                        subprocess.check_call(['msgfmt', po_path, '-o', mo_path], cwd=self.install_lib)
        except Exception as ex:
            self.announce('Translations compilation failed: %s' % ex.message)


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='xblock-poll',
    version='1.2.6',
    description='An XBlock for polling users.',
    packages=[
        'poll',
    ],
    install_requires=[
        'markdown',
        'ddt',
        'mock',
    ],
    dependency_links=['http://github.com/edx/xblock-utils/tarball/master#egg=xblock-utils'],
    entry_points={
        'xblock.v1': [
            'poll = poll:PollBlock',
            'survey = poll:SurveyBlock',
        ]
    },
    package_data=package_data("poll", ["static", "public", "translations"]),
    cmdclass={
        'install': XBlockInstall,
    },
)
