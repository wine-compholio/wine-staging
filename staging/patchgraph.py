#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# Plot dependency graph for Staging patches.
#
# Copyright (C) 2017 Sebastian Lackner
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
#

from patchupdate import load_patchsets
from graphviz import Digraph
import os

if __name__ == '__main__':
    tools_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(os.path.join(tools_directory, "./.."))

    all_patches = load_patchsets()
    graph = Digraph(comment='Patch dependencies')

    for i, patch in all_patches.iteritems():
        if patch.disabled: continue
        for j in patch.depends:
            graph.edge(patch.name, all_patches[j].name)

    graph.render(view=True)
