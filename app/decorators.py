from fastapi import FastAPI

app=FastAPI()


# Example 1

print('='*20, 'Example 1' ,'='*20)
def fence(log):
    log()


@fence
def log():
    print('decorated')





# Example 2
print('='*20, 'Example 2' ,'='*20)

def fence2(log2):
    def wrapper():
        print('+'*10)
        log2()
        print('+'*10)
    return wrapper
    
@fence2
def log2():
    print('decorated 2')

log2()


# Example 3

print('='*20, 'Example 3' ,'='*20)

def custom_decorator(fence:str="+"):
    def add_fence(func):
        def wrapper(text:str):
            print(fence*len(text))
            func(text)
            print(fence*len(text))
        return wrapper
    return add_fence


@custom_decorator('-')
def log3(text:str):
    print(text)

log3('hello')           
            