from scales import SCALE_REFS, DEGREE_REFS, DEGREES_31EDO, TETRACHORDS_31EDO
from find_scales import interval_diversity, count_interval, count18s, count_chord_richness, count_total_chords, proper, consonances, count_dissonances, count_extensions
from midi_numbers import get_12_edo_name



def scale_info(scale_name, extra_lines=None):
    print(scale_name)
    print_scales(scale_name, 31)
    print_cents(scale_name, 31)
    scale = SCALE_REFS[31][scale_name]
    print(f"Consonant interval diversity: {interval_diversity(scale, consonances)}/{len(consonances)}")
    print("Total dissonances:", count_dissonances(scale, consonances))
    print("Total interval diversity: %d/31" % interval_diversity(scale))
    print(*[(DEGREES_31EDO[i], count_interval(scale, i)) for i in range(32)])
    print("Total chords:", *[count_total_chords(scale, [third]) for third in [7, 8, 9, 10, 11]])
    print("Total tetrachords:")
    for name, degrees in TETRACHORDS_31EDO.items():
        if count_extensions(scale, degrees) > 0:
            print(f"  {name}: {count_extensions(scale, degrees)}")
    print("Proper:", proper(scale))
    print("MIDI notes:", ", ".join(map(get_12_edo_name, get_midi_numbers(scale_name, 31))))
    for line in extra_lines or []:
        print(line)
    print()


if __name__ == "__main__":
    for scale in ("septimal playground octatonic 1", "fairly consonant many-chorded octatonic", "consonant octatonic A", "consonant octatonic B",):
        scale_info(scale)
