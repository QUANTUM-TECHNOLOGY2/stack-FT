import shutil
import pathlib

base = pathlib.Path(__file__).resolve().parent
out = base.parent / 'Quantum_app_20260709.zip'
if out.exists():
    out.unlink()
shutil.make_archive(str(out.with_suffix('')), 'zip', root_dir=str(base))
print('Created', out)
