from libprobe.probe import Probe
from lib.check.cpu import CheckCPU
from lib.check.memory import CheckMemory
from lib.check.system import CheckSystem
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = (
        CheckCPU,
        CheckMemory,
        CheckSystem,
    )

    probe = Probe("tplink", version, checks)

    probe.start()
