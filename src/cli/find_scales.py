
def find_subscales(scale, priorities_function, length):
    subscales = []
    for subscale in all_subscales(scale, length):
        subscales.append((subscale, *priorities_function(subscale)))

    subscales.sort(key=lambda x: x[1:])
    print(len(subscales))
    for subscale_stats in subscales:
        this_scale_names = []
        for scale_name, named_scale in SCALES_31EDO.items():
            if tuple(find_canon_rotation(named_scale)) == subscale_stats[0]:
                this_scale_names.append(scale_name)
        print(*subscale_stats, *this_scale_names)



def print_family(parent_scale_name, lengths=(6, 7, 8, 9, 10,)):
    parent_scale = SCALES_31EDO[parent_scale_name]
    subscales = {}
    for length in lengths:
        subscales[length] = all_subscales(parent_scale, length)

    named_subscales = []
    for name, scale in SCALES_31EDO.items():
        if find_canon_rotation(tuple(scale)) in subscales.get(len(scale), []):
            named_subscales.append((name, scale))
    named_subscales.sort(key=lambda x: len(x[1]))

    for name, scale in named_subscales:
        scale_info(name, [f"Keys: {' '.join(list(find_keys(scale, parent_scale)))}"])

    scale_info(parent_scale_name)