from dataclasses import dataclass

# Pitch: positive values are pitch up
# Bank: positive values are bank right

class Camper:

    # Default values
    N_RAMPS: int = 2
    N_TYRES: int = 4

    # Calculation tuning
    INITIAL_INCREMENT: float = 1.0
    ITERATIONS: int = 5

    @dataclass
    class Attitude:
        ramps: list[float]
        pitch: float
        bank: float
        total: float

        def __init__(self, ramps: list[float], pitch: float, bank: float):
            self.ramps = ramps
            self.pitch = pitch
            self.bank = bank
            # Total incline as combination of pitch and bank
            self.total: float = (pitch**2 + bank**2)**0.5

    def __init__(self, pitch_per_ramp:float = 0.0, bank_per_ramp: float = 0.0, n_ramps: int = N_RAMPS):
        self.pitch_per_ramp = pitch_per_ramp
        self.bank_per_ramp = bank_per_ramp
        self.n_ramps = n_ramps

        # Save initial attitude
        self._initial_attitude: Camper.Attitude = Camper.Attitude(ramps=[0.0] * Camper.N_TYRES, pitch=0.0, bank=0.0)

    def __str__(self) -> str:
        best_attitude = self.best_attitude
        return "RAMPS:\n" \
               "Front:   {:4.2f} | {:4.2f}\n" \
               "Rear:    {:4.2f} | {:4.2f}\n\n" \
               "\n" \
               "ATTITUDE:\n" \
               "       BEFORE | AFTER\n" \
               "Pitch:  {:+3.1f}° | {:+3.1f}°\n" \
               "Bank:   {:+3.1f}° | {:+3.1f}°\n" \
               "Total:  {:+3.1f}° | {:+3.1f}°\n\n" \
               "\n" \
               "CORRECTION:      {:3d}%".format(
                best_attitude.ramps[0],
                best_attitude.ramps[1],
                best_attitude.ramps[2],
                best_attitude.ramps[3],
                self._initial_attitude.pitch,
                best_attitude.pitch,
                self._initial_attitude.bank,
                best_attitude.bank,
                self._initial_attitude.total,
                best_attitude.total,
                int(self.correction *100)
            )

    @property
    def initial_attitude(self) -> Attitude:
        return self._initial_attitude
    
    @property
    def best_attitude(self) -> Attitude:
        return self._get_best_attitude()
    
    @property
    def correction(self) -> float:
        return self._get_correction()

    @property
    def pitch(self) -> float:
        return self._initial_attitude.pitch
    
    @pitch.setter
    def pitch(self, pitch: float):
        self._initial_attitude = Camper.Attitude(self._initial_attitude.ramps, pitch, self._initial_attitude.bank)
    
    @property
    def bank(self) -> float:
        return self._initial_attitude.bank
    
    @bank.setter
    def bank(self, bank: float):
        self._initial_attitude = Camper.Attitude(self._initial_attitude.ramps, self._initial_attitude.pitch, bank)
    
    def _get_best_attitude(self) -> Attitude:
        # Start from initial attitude
        attitude = self._initial_attitude

        for iteration in range(Camper.ITERATIONS):
            while True:
                # Increment will be 1/10 fi initial increment each following iteration
                increment = Camper.INITIAL_INCREMENT / (10**iteration)

                possible_attitudes = []

                # Find all possible attitudes using the any combination of modification of the ramps
                # Take each tire
                for tire in range(Camper.N_TYRES):

                    # Check for increasing and decreasing the amount of ramp used oh this tire
                    for sign in [1, -1]:
                        new_ramps = attitude.ramps[:]
                        # Modify the amount of ramp used by this tire
                        new_ramps[tire] += increment * sign

                        # Check if only the available number of ramps used
                        if Camper.N_TYRES - new_ramps.count(0.0) <= self.n_ramps:

                            # Check if ramp usage factor is between 0.0 and 1.0
                            if not any(ramp < 0.0 or ramp > 1.0 for ramp in new_ramps):

                                # Calculate resulting pitch and bank and append the resulting attitude to the list
                                # of possible attitudes
                                new_pitch = self.pitch - self.pitch_per_ramp * (
                                    new_ramps[0] + new_ramps[1] - new_ramps[2] - new_ramps[3]
                                )
                                new_bank = self.bank - self.bank_per_ramp * (
                                    -new_ramps[0] + new_ramps[1] - new_ramps[2] + new_ramps[3]
                                )
                                possible_attitudes.append(Camper.Attitude(new_ramps, new_pitch, new_bank))
                
                # Sort all possible attitudes by total incline and take the best of all possible attitudes
                best = sorted(possible_attitudes, key=lambda x: x.total)[0]

                # Use new attitude if the total incline is less than the current or start the next iteration using
                # smaller increments to further refine the best possible attitude
                if best.total < attitude.total:
                    attitude = best
                else:
                    break
        
        # Return the best possible attitude that can be achieved using the available ramps
        return attitude

    def _get_correction(self) -> float:
        try:
            return (1 - (self.best_attitude.total / self.initial_attitude.total))
        except ZeroDivisionError:
            return 1.0


if __name__ == "__main__":
    MY_PITCH_PER_RAMP = 1.5
    MY_BANK_PER_RAMP = 0.75

    camper=Camper(MY_PITCH_PER_RAMP, MY_BANK_PER_RAMP)

    camper.pitch = float(input("Pitch (+ is nose up): "))
    camper.bank = float(input("Bank (+ is right side low): "))
    
    print()
    print(camper)
