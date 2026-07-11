path='c:/Users/kpeho/Downloads/Quantum/deepseek_python_20260708_1a153f.py'
with open(path,'rb') as f:
    b=f.read()
text=b.decode('utf-8',errors='replace')
for i,line in enumerate(text.splitlines(),start=1):
    if '\\U' in line or '\\u' in line:
        print(i, line)
