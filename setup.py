#!/usr/local/bin/python
#
# Copyright (c) 2014-2015 Denis. All rights reserved.
# Copyright (c) 2006-2009 Sip Software, Inc. All rights reserved.
#
# This file is part of SIP TEST FRAMEWORK.
#
# SIP TEST FRAMEWORK is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# For a license to use the SIP TEST FRAMEWORK software under conditions
# other than those described here, or to purchase support for this
# software, please contact Denis by e-mail at the
# following addresses: senid231@gmail.com.
#
# SIP TEST FRAMEWORK is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.
#
# $Id: setup.py,v 1.0.0.0 2015/01/12 00:20:01 senid231 Exp $

from distutils.core import setup

setup(name='sftf',
      version='1.0.3',
      description='SIP TEST FRAMEWORK',
      author='Denis',
      author_email=' senid231@gmail.com',
      url='http://www.example.com/',
      packages=['sftf'],
      scripts=['sftf/b2bua_radius.py', 'sftf/b2bua_simple.py'],
      data_files=[('share/doc/sftf', ['COPYING', 'sippy/Docs'])])
