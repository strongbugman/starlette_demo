from . import extensions as exts


@exts.task.task
def example(x: int):
    print(f"Get {x}")
    x += 1
    print(f"Return {x}")
