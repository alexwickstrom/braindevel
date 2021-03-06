import numpy as np
from braindecode.datasets.fft import amplitude_phase_to_complex

class BandpowerMeaner(object):
    def process(self, inputs, targets):
        inputs = inputs.copy()
        targets= targets.copy()
        row_targets = targets.reshape(inputs.shape[0], -1, targets.shape[1])
        row_targets = np.argmax(row_targets[:,0,:], axis=1)
    
        for i_class in range(targets.shape[1]):
            i_relevant_blocks = np.flatnonzero(row_targets == i_class)
            n_mix = len(i_relevant_blocks) // 2
            n_mix -= n_mix % 2
            if n_mix >= 2:
                i_mix = i_relevant_blocks[:n_mix]
                inputs_to_modify = inputs[i_mix]
                fft_to_modify = np.fft.rfft(inputs_to_modify, axis=2)
                # Compute mean of amplitudes
                # of both mixed halfs
                amp_to_modify = np.abs(fft_to_modify)
                amp_to_modify[:n_mix/2] += amp_to_modify[n_mix/2:]
                amp_to_modify[n_mix/2:] += amp_to_modify[:n_mix/2]
                amp_to_modify /= 2
                phase = np.angle(fft_to_modify)
                fft_to_modify = amplitude_phase_to_complex(amp_to_modify,
                    phase)
                
                modified_input = np.fft.irfft(fft_to_modify, 
                    n=inputs.shape[2], axis=2)
                inputs[i_mix] = modified_input
        return inputs, targets

