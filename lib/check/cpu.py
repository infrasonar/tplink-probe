from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from libprobe.check import Check
from libprobe.exceptions import CheckException
from ..snmpclient import get_snmp_client
from ..snmpquery import snmpquery

QUERIES = (
    (MIB_INDEX['TPLINK-SYSMONITOR-MIB']['tpSysMonitorCpuEntry'], True),
)


class CheckCPU(Check):
    key = 'cpu'
    unchanged_eol = 14400

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        snmp = get_snmp_client(asset, local_config, config)
        state = await snmpquery(snmp, QUERIES)

        items = state.get('tpSysMonitorCpuEntry')
        if items is None:  # can be an empty list
            raise CheckException('no data found')

        # 60 is the fallback we use in get_snmp_client
        interval = config.get('_interval', 60)
        for item in items:
            item.pop('tpSysMonitorCpu5Seconds')
            cpu_60 = item.pop('tpSysMonitorCpu1Minute')
            cpu_300 = item.pop('tpSysMonitorCpu5Minutes')
            item['tpSysMonitorCpu'] = cpu_60 if interval < 300 else cpu_300

        return {
            'cpu': items
        }
