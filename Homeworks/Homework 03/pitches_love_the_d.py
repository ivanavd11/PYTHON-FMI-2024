TONE_NAMES  = (
    "C", 
    "C#", 
    "D", 
    "D#", 
    "E", 
    "F", 
    "F#", 
    "G", 
    "G#", 
    "A", 
    "A#", 
    "B"
    )
 
TONES_IN_OCTAVE = 12
 
INTERVAL_NAMES = (
        "unison", 
        "minor 2nd", 
        "major 2nd", 
        "minor 3rd", 
        "major 3rd",
        "perfect 4th",
        "diminished 5th", 
        "perfect 5th", 
        "minor 6th",
        "major 6th", 
        "minor 7th", 
        "major 7th"
        )
 
 
class Tone:
    def __init__(self, name):
        self.name = name
 
    def __str__(self):
        return self.name
 
    def __add__(self, other):
        if isinstance(other, Tone):
            return Chord(self, other)
        elif isinstance(other, Interval):
            return self._add_interval(other)
        else:
            raise TypeError("Invalid operation")
 
    def _add_interval(self, interval):
        """Collects a tone and an interval and returns a new tone."""

        tone_index = TONE_NAMES.index(self.name)
        new_index = (tone_index + interval.halftone) % len(TONE_NAMES)
        return Tone(TONE_NAMES[new_index])
 
    def __sub__(self, other):
        if isinstance(other, Interval): 
            return self._sub_interval(other)
        if isinstance(other, Tone): 
            return self._sub_tone(other)
        else:
            raise TypeError("Invalid operation")
 
    def _sub_interval(self, interval):
        """Subtracts an interval from a tone and returns a new tone with a changed pitch."""

        tone_index = TONE_NAMES.index(self.name)
        new_index = (tone_index - interval.halftone) % len(TONE_NAMES)
        return Tone(TONE_NAMES[new_index])
 
    def _sub_tone(self, other_tone):
        """Subtracts a tone from a tone and returns a space."""

        tone_index = TONE_NAMES.index(self.name)
        other_tone_index = TONE_NAMES.index(other_tone.name)
        distance = (tone_index - other_tone_index) % len(TONE_NAMES)

        return Interval(distance)
 
 
class Interval:
    def __init__(self, halftone):
        self.halftone = halftone % TONES_IN_OCTAVE
 
    def __add__(self, other):
        if isinstance(other, Interval):
            new_halftone = (self.halftone + other.halftone) % TONES_IN_OCTAVE
            return Interval(new_halftone)
 
    def __str__(self):
        return INTERVAL_NAMES[self.halftone]
 
    def __neg__(self):
        """Returns a new Interval object with a negative semitone value."""
        return Interval(-self.halftone)
 
 
class Chord:
    def __init__(self, base_tone, *other_tones):
        unique_tones = [base_tone.name] 
 
        for tone in other_tones:
            if tone.name not in unique_tones:
                unique_tones.append(tone.name)
 
        if len(unique_tones) < 2:
            raise TypeError("Cannot have a chord made of only 1 unique tone")
 
        self.base_tone = base_tone
        self.tones = unique_tones 
 
    def get_tone_index(self, tone_name):
        return TONE_NAMES.index(tone_name)
 
    def __str__(self):
        root_index = self.get_tone_index(self.base_tone.name)
        self.tones.sort(key = lambda current_tone: (TONE_NAMES.index(current_tone) - root_index) % TONES_IN_OCTAVE)
        return "-".join(self.tones)
 
    def is_minor(self):
        MINOR_INTERVAL = 3
        root_index = self.get_tone_index(self.base_tone.name)
        for tone_name in self.tones:
            if (self.get_tone_index(tone_name) - root_index) % TONES_IN_OCTAVE == MINOR_INTERVAL:
                return True
        return False
 
    def is_major(self):
        MAJOR_INTERVAL = 4 
        root_index = self.get_tone_index(self.base_tone.name)
        for tone_name in self.tones:
            if (self.get_tone_index(tone_name) - root_index) % TONES_IN_OCTAVE == MAJOR_INTERVAL:
                return True
        return False
 
    def is_power_chord(self):
        if self.is_minor() or self.is_major():
            return False  
        return True  
 
    def __add__(self, other):
        """Matching a chord with a tone or with another chord."""
 
        if isinstance(other, Tone):
            new_tones = self.tones + [other.name]
            sorted_tones = sorted(set(new_tones), key=lambda t: TONE_NAMES.index(t))
            return Chord(Tone(sorted_tones[0]), *[Tone(t) for t in sorted_tones[1:]])
 
        elif isinstance(other, Chord):
            combined_tones = self.tones + other.tones
            unique_tones = []
            for tone in combined_tones:
                if tone not in unique_tones:
                    unique_tones.append(tone)
            return Chord(Tone(unique_tones[0]), *[Tone(t) for t in unique_tones[1:]])
 
        else:
            raise TypeError("Invalid operation") 
 
    def __sub__(self, tone):
        if tone.name not in self.tones:
            raise TypeError(f"Cannot remove tone {tone} from chord {self}")
        
        new_tones = [t for t in self.tones if t != tone.name]
        if len(new_tones) < 2:
            raise TypeError("Cannot have a chord made of only 1 unique tone")
 
        return Chord(self.base_tone, *[Tone(t) for t in new_tones])
 
    def transposed(self, interval):
        """Transposes the chord by the given interval."""
 
        if not isinstance(interval, Interval):
            raise TypeError("Expected an Interval object for transposition")
 
        transposed_tones = []
        for tone_name in self.tones:
            tone = Tone(tone_name)
            if interval.halftone > 0:
                transposed_tone = tone + interval
            else:
                transposed_tone = tone - Interval(abs(interval.halftone))
            transposed_tones.append(transposed_tone)
 
        return Chord(*transposed_tones)

