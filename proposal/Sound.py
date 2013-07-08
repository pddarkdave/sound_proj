
example_sound_function = None
example_sound_width = 4

class Sound(object):
    def __init__(self):
        self.maximum_memory = 40 # maximum degree of FIR filters on this sound
        self.clear_memory()

    def configure(self, duration):
        # May be modified after .configure()
        self.sound_functions = [example_sound_function, ]
        self.mixing_rule = None
        self.duration = duration # doesn't do anything yet but should

        # Not allowed to be modified after .configure()
        self.function_amplitude = example_sound_amplitude
        self.sampling_rate = example_sound_samples_hz

    def restart(self):
        # should there be a global time, or is it helpful
        # to be able to expand or contract individual sounds in time?
        self.time = 0 
        self.clear_memory()

    def clear_memory(self):
        self.previous_samples_buffer = []

    def next_sample(self):
        # These are the args with which to call the sound functions
        s_f_args = (self.time, self.previous_samples_buffer)

        # Default value of sample is zero if there are no sound functions
        # (only possible if configure() initialized .sound_functions to [] )
        next_sample = 0
        samples_to_mix = None

        if len(self.sound_functions) > 0:
            samples_to_mix = [ f(s_f_args*) for f in self.sound_functions ]

        if len(self.samples_to_mix) == 1:
            next_sample = samples_to_mix[0]
        elif self.mixing_rule is None:
            raise NotImplementedError(
                "Default mixing rule only implemented for one sound source")
        else:
            next_sample = self.mixing_rule.mix(
                        self.time,
                        self.previous_samples_buffer,
                        samples_to_mix
                    )
        
        self.previous_samples_buffer.append(next_sample)
        if len(self.previous_samples_buffer) == self.maximum_memory:
            self.previous_samples_buffer.pop(0) # remove oldest sample

        return next_sample

class WaveSoundFile(object):
    def __init__(self, filename):
        self.filename = filename

    def write_sound(self, sound):
        raise NotImplementedError()
        # General idea: 
