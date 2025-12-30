from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from libprobe.check import Check
from libprobe.exceptions import IgnoreCheckException
from ..snmpclient import get_snmp_client
from ..snmpquery import snmpquery

QUERIES = (
    (MIB_INDEX['TPLINK-SYSMONITOR-MIB']['tpSysMonitorCpuEntry'], True),
)


class CheckCPU(Check):
    key = 'cpu'

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        snmp = get_snmp_client(asset, local_config, config)
        state = await snmpquery(snmp, QUERIES)

        items = state.get('tpSysMonitorCpuEntry')
        if not items:
            raise IgnoreCheckException

        return {
            'cpu': items
        }
