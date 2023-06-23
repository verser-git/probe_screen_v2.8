#!/usr/bin/env python
#
# Touchy is Copyright (c) 2009  Chris Radek <chris@timeguy.com>
# Probe Screen is Copyright (c) 2015 Serguei Glavatski ( verser  from forum.linuxcnc.org and cnc-club.ru )
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; If not, see <http://www.gnu.org/licenses/>.

import os
import ConfigParser

ps_cp = ConfigParser.RawConfigParser
class ProbeScreenPreferences(ps_cp):
    types = {
        bool: ps_cp.getboolean,
        float: ps_cp.getfloat,
        int: ps_cp.getint,
        str: ps_cp.get,
        repr: lambda self, section, option: eval(ps_cp.get(self, section, option)),
    }

    def __init__(self, path=None):
        ps_cp.__init__(self)

        if not path:
            path = "~/.toolch_preferences"

        self.fn = os.path.expanduser(path)
        self.read(self.fn)

    def getpref(self, option, default=False, type=bool):
        m = self.types.get(type)
        try:
            o = m(self, "DEFAULT", option)
        except Exception as detail:
            print(detail)
            self.set("DEFAULT", option, default)
            self.write(open(self.fn, "w"))
            if type in (bool, float, int):
                o = type(default)
            else:
                o = default
        return o

    def putpref(self, option, value, type=bool):
        self.set("DEFAULT", option, type(value))
        self.write(open(self.fn, "w"))
