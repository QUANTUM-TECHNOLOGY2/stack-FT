from pathlib import Path
pyd = Path('.venv/Lib/site-packages/pydantic_core/_pydantic_core.cp314-win_amd64.pyd')
print('exists', pyd.exists())
print('path', pyd)
try:
    with open(str(pyd) + ':Zone.Identifier', 'rb') as f:
        data = f.read()
        print('Zone-Identifier size', len(data))
        print(data)
except FileNotFoundError:
    print('no zone identifier')
except Exception as e:
    print('error reading ADS', repr(e))
