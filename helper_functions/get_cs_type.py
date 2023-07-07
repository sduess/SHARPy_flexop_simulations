       
def get_cs_type(closed_loop, dynamic_cs_input, free_flight=False):
    if closed_loop:
        ailerons_type = 2
    elif dynamic_cs_input:
        ailerons_type = 1
    else:
        ailerons_type = 0
    return ailerons_type