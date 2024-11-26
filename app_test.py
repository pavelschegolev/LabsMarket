from functools import wraps

def decor(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print('я wrapper')
        # Делаeт что-то, что меняет поведение func
        return func(*args,**kwargs)
    return wrapper

@decor

def my_func(name:str,value:int):
    print(name,'=',value)
    return value

if __name__ == '__main__':
   # f=decor(my_func)('a',100)
   # print(type(f))
   f= my_func('a',100)
   print(type(f))



















