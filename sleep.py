import time


def sleep(duration: int, tracer):
    with tracer.start_as_current_span("sleep_sleep"):
        time.sleep(addition(duration,tracer))


def addition(duration: int, tracer):
    with tracer.start_as_current_span("sleep_addition"):
        return duration + 1
