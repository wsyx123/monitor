def _read_mem_info():
    mem={}
    with open('/proc/meminfo') as f:
        for line in f:
            key=line.split(':')[0] 
            value=line.split(':')[1].split()[0]
            mem[key]=float(value)
    return mem

def memory():
    free = round(_read_mem_info()['MemFree']/1024/1000,2)
    total = round(_read_mem_info()['MemTotal']/1024/1000,2)
    return {'total':total,'free':free}



