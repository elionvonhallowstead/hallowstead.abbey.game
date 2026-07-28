from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

def clear():
    print("\033c", end="")

def multiThread(maxThreads:int, *tasks:tuple[object, tuple], prefix:str="") -> dict:
    out = {}
    with ThreadPoolExecutor(max_workers=maxThreads, thread_name_prefix=prefix) as threads:
        for task in tasks:
            out[task[1:]] = threads.submit(task[0], *task[1:]).result()
        return out

def isEmpty(input_list:list) -> bool:
    if None in input_list:
        input_list.remove(None)
    for item in input_list:
        if not isinstance(item, list) or not isEmpty(item):
             return False
    return True
