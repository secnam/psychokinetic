# -*- coding: utf-8 -*-
# Copyright (c) 2018 Christiaan Frans Rademan.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
from luxon import g
from psychokinetic.client import Client as APIClient

class Client(object):
    __slots__ = ( 'restapi', 'region', 'interface' )

    def __init__(self):
        self.restapi = g.config.get('restapi', 'uri')
        self.region = g.config.get('restapi', 'region')
        self.interface = g.config.get('restapi', 'interface')

    def pre(self, req, resp):
        req.context.client = g.client = APIClient(self.restapi,
                                                 default_region=self.region,
                                                 default_interface=self.interface)
        if req.get_header('X-Auth-Token'):
            token = req.get_header('token')
        else:
            token = req.session.get('token')

        if req.get_header('X-Region'):
            region = req.get_header('X-Region')
        else:
            region = req.session.get('region')

        scoped = req.session.get('scoped')

        if req.get_header('X-Domain'):
            domain = req.get_header('X-Domain')
        else:
            domain = req.session.get('domain')

        if req.get_header('X-Tenant-Id'):
            tenant_id = req.get_header('X-Tenant-Id')
        else:
            tenant_id = req.session.get('tenant_id')

        if region is None:
            region = g.config.get('restapi', 'region')

        if token is not None:
            g.client.set_context(token,
                                 scoped,
                                 domain,
                                 tenant_id,
                                 region,
                                 g.config.get('restapi', 'interface'))
