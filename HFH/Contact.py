#
# Copyright (C) 2004 SIPfoundry Inc.
# Licensed by SIPfoundry under the GPL license.
#
# Copyright (C) 2004 SIP Forum
# Licensed to SIPfoundry under a Contributor Agreement.
#
#
# This file is part of SIP Forum Test Framework.
#
# SIP Forum Test Framework is free software; you can redistribute it 
# and/or modify it under the terms of the GNU General Public License as 
# published by the Free Software Foundation; either version 2 of the 
# License, or (at your option) any later version.
#
# SIP Forum Test Framework is distributed in the hope that it will 
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SIP Forum Test Framework; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# $Id: Contact.py,v 1.15 2004/03/19 18:38:44 lando Exp $
#
from HeaderFieldHandler import HeaderFieldHandler
import name_addr
import sip_uri
from SCException import SCNotImplemented


class Contact(HeaderFieldHandler):
    def __init__(self, value=None):
        HeaderFieldHandler.__init__(self)
        self.star = False
        self.displayname = None
        self.uri = sip_uri.sip_uri()
        self.q = None
        self.expires = None
        self.params = []
        self.next = None
        if value is not None:
            self.parse(value)

    def __str__(self):
        return '[star:\'' + str(self.star) + '\', ' \
               + 'displayname:\'' + str(self.displayname) + '\', ' \
               + 'uri:\'' + str(self.uri) + '\', ' \
               + 'q:\'' + str(self.q) + '\', ' \
               + 'expires:\'' + str(self.expires) + '\', ' \
               + 'params:\'' + str(self.params) + '\', ' \
               + 'next:\'' + str(self.__next__) + '\']'

    def parse(self, value):
        v = value.replace("\r", "").replace("\t", "").strip()
        if v == '*':
            self.star = True
        else:
            self.displayname, uristr, self.params, brackets = name_addr.parse(v)
            self.uri.parse(uristr)
            if (not brackets) and (len(self.uri.params) > 0) and (len(self.uri.headers) == 0) and (
                        len(self.params) == 0):
                self.params = self.uri.params
                self.uri.params = []
            prmlen = list(range(0, len(self.params)))
            if len(self.params):
                prmlen.reverse()
                for i in prmlen:
                    if self.params[i].startswith(","):
                        self.next = Contact(self.params[i][1:])
                        self.params[i:i + 1] = []
                    elif self.params[i].lower().startswith("q="):
                        self.q = self.params[i][2:]
                        self.params[i:i + 1] = []
                    elif self.params[i].lower().startswith("expires="):
                        self.expires = self.params[i][8:]
                        self.params[i:i + 1] = []

    def sub_create(self):
        ret = ""
        if self.star:
            ret = "*"
        else:
            if self.displayname is not None:
                ret = "\"" + str(self.displayname) + "\" "
            if self.uri is not None:
                ret = ret + "<" + self.uri.create() + ">"
            if self.q is not None:
                ret = ret + ";q=" + self.q
            if self.expires is not None:
                ret = ret + ";expires=" + str(self.expires)
            p = ""
            for i in self.params:
                p = p + ';' + i
            if len(p) > 0:
                ret = ret + p
        return ret

    def create(self):
        ret = self.sub_create()
        cur = self.__next__
        while cur is not None:
            ret = ret + ", " + cur.sub_create()
            cur = cur.__next__
        return ret + '\r\n'

    def verify(self):
        raise SCNotImplemented("Contact", "verify", "not implemented")
