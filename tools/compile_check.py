import traceback
path='c:/Users/kpeho/Downloads/Quantum/deepseek_python_20260708_1a153f.py'
try:
    source=open(path,'r',encoding='utf-8').read()
    compile(source,path,'exec')
    print('COMPILE_OK')
except Exception:
    traceback.print_exc()
