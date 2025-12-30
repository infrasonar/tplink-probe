from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from libprobe.check import Check
from libprobe.exceptions import CheckException
from ..snmpclient import get_snmp_client
from ..snmpquery import snmpquery

QUERIES = (
    (MIB_INDEX['TPLINK-SYSMONITOR-MIB']['tpSysMonitorMemoryEntry'], True),
)


class CheckMemory(Check):
    key = 'memory'
    unchanged_eol = 14400

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        snmp = get_snmp_client(asset, local_config, config)
        state = await snmpquery(snmp, QUERIES)

        items = state.get('tpSysMonitorMemoryEntry')
        if items is None:  # can be an empty list
            raise CheckException('no data found')

        return {
            'memory': items
        }
