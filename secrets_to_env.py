# secrets_to_env.py
import os
import sys
from typing import Dict
from config_sm import Config, ConfigBuilder

arn = "arn:aws:secretsmanager:eu-west-1:330652100360:secret:techops_automation"
secrets_arns: Dict[str, str] = {
    "supply_growth_sheets": f"{arn}/supply_growth_sheets-QgzjWO",
    "supply_growth_liveDB": f"{arn}/supply_growth_liveDB-Dkw8NS",
    "supply_growth_dwh": f"{arn}/supply_growth_dwh-l2mnwI",
    "supply_growth_slack": f"{arn}/supply_growth_slack-bk7e0S",
    "supply_growth_pacodb": f"{arn}/supply_growth_pacodb-jgYaHP",
}
cb: ConfigBuilder = ConfigBuilder()
for name, arn in secrets_arns.items():
    cb.add_parameter(name, sm=arn)
config: Config = cb.build()
for secret_name in secrets_arns.keys():
    os.environ[secret_name] = config.get_value(secret_name)

failure = os.system(sys.argv[1])
if failure:
    print('Execution of "%s" failed!\n' % sys.argv[1])
    sys.exit(1)