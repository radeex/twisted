
from twisted.spread import pb
from twisted.internet import main
from twisted.python import defer
import time

class PBBenchClient:
    hostname = 'localhost'
    portno = pb.portno
    calledThisSecond = 0

    def callLoop(self, ignored):
        d1 = self.persp.callRemote("simple")
        d2 = self.persp.callRemote("complexTypes")
        defer.DeferredList([d1, d2]).addCallback(self.callLoop).arm()
        self.calledThisSecond += 1
        thisSecond = int(time.time())
        if thisSecond != self.lastSecond:
            if thisSecond - self.lastSecond > 1:
                print "WARNING it took more than one second"
            print 'cps:', self.calledThisSecond
            self.calledThisSecond = 0
            self.lastSecond = thisSecond

    def _cbPerspective(self, persp):
        self.persp = persp
        self.lastSecond = int(time.time())
        self.callLoop(None)

    def runTest(self):
        pb.connect(self.hostname, self.portno,
                   "benchmark", "benchmark", "benchmark").addCallback(self._cbPerspective)

PBBenchClient().runTest()
main.run()
