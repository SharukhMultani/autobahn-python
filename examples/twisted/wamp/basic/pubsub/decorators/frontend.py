###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from __future__ import print_function

from os import environ
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.python.failure import Failure

from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):

    """
    An application component that subscribes and receives events,
    and stop after having received 5 events.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        # subscribe all methods on this object decorated with "@wamp.subscribe"
        # as PubSub event handlers
        results = yield self.subscribe(self)

        # check we didn't have any errors
        for sub in results:
            if isinstance(sub, Failure):
                print("subscribe failed:", sub.getErrorMessage())

    @wamp.subscribe(u'com.myapp.topic1')
    def onEvent1(self, i):
        print("Got event on topic1: {}".format(i))

    @wamp.subscribe(u'com.myapp.topic2')
    def onEvent2(self, msg):
        print("Got event on topic2: {}".format(msg))

    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


if __name__ == '__main__':
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", "ws://localhost:8080/ws"),
        u"crossbardemo",
        debug_wamp=False,  # optional; log many WAMP details
        debug=False,  # optional; log even more details
    )
    runner.run(Component)
