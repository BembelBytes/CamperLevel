# Copyright (c) 2025 Aljoscha Greim <aljoscha@bembelbytes.com>
# MIT License

from dataclasses import dataclass

# Pitch: positive values are pitch up
# Bank: positive values are bank right

class Camper:
    # Default values
    N_RAMPS: int = 2
    N_TYRES: int = 4

    # Calculation values
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
        
        def __str__(self) -> str:
            return "Ramps:\n" \
                   "  FL: {:3d}%, FR: {:3d}%\n" \
                   "  RL: {:3d}%, RR: {:3d}%\n" \
                   "\n" \
                   "Attitude:\n" \
                   "  Pitch: {:+3.1f}°\n" \
                   "  Bank:  {:+3.1f}°".format(
                    int(self.ramps[0] * 100),
                    int(self.ramps[1] * 100),
                    int(self.ramps[2] * 100),
                    int(self.ramps[3] * 100),
                    self.pitch,
                    self.bank
                )
    
        def __eq__(self, other: object) -> bool:
            return self.ramps == other.ramps and self.pitch == other.pitch and self.bank == other.bank
        
        def __lt__ (self, other: object) -> bool:
            return self.total < other.total
        
        def __gt__ (self, other: object) -> bool:
            return self.total > other.total


    def __init__(self, pitch_per_ramp:float = 0.0, bank_per_ramp: float = 0.0, n_ramps: int = N_RAMPS):
        self._pitch_per_ramp = pitch_per_ramp
        self._bank_per_ramp = bank_per_ramp
        self.n_ramps = n_ramps

        # Save initial attitude
        self._initial_attitude: Camper.Attitude = Camper.Attitude(ramps=[0.0] * Camper.N_TYRES, pitch=0.0, bank=0.0)

    def __str__(self) -> str:
        best_attitude = self.best_attitude
        return "RAMPS:\n" \
               "Front:   {:3d}% | {:3d}%\n" \
               "Rear:    {:3d}% | {:3d}%\n\n" \
               "\n" \
               "ATTITUDE:\n" \
               "       BEFORE | AFTER\n" \
               "Pitch:  {:+3.1f}° | {:+3.1f}°\n" \
               "Bank:   {:+3.1f}° | {:+3.1f}°\n" \
               "Total:  {:+3.1f}° | {:+3.1f}°\n\n" \
               "\n" \
               "CORRECTION:      {:3d}%".format(
                int(best_attitude.ramps[0] * 100),
                int(best_attitude.ramps[1] * 100),
                int(best_attitude.ramps[2] * 100),
                int(best_attitude.ramps[3] * 100),
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
                
                # Get attitude with the smallest total error
                best = min(self._get_possible_attitudes(attitude, increment))

                # Use new attitude if the total incline is less than the current or start the next iteration using
                # smaller increments to further refine the best possible attitude
                if best < attitude:
                    attitude = best
                else:
                    break
        
        # Return the best possible attitude that can be achieved using the available ramps
        return attitude
    
    def _get_possible_attitudes(self, attitude: Attitude, increment: float) -> list[Attitude]:
        # Find all possible attitudes that can be reached from the current attitude using the given increment
        possible_attitudes = []

        # Take each tire
        for tire in range(Camper.N_TYRES):

            # Check for increasing and decreasing the amount of ramp used oh this tire
            for sign in [1, -1]:
                new_ramps = attitude.ramps[:]
                # Modify the amount of ramp used by this tire
                new_ramps[tire] += increment * sign

                # Delete diagonal corrections as they don't have any effect on the attitude
                if new_ramps[0] != 0.0 and new_ramps[3] != 0.0:
                    correction = min(new_ramps[0], new_ramps[3])
                    new_ramps[0] -= correction
                    new_ramps[3] -= correction

                if new_ramps[1] != 0.0 and new_ramps[2] != 0.0:
                    correction = min(new_ramps[1], new_ramps[2])
                    new_ramps[1] -= correction
                    new_ramps[2] -= correction

                # Check if only the available number of ramps used
                if Camper.N_TYRES - new_ramps.count(0.0) > self.n_ramps:
                    break

                # Check if ramp usage factor is between 0.0 and 1.0
                if any(ramp < 0.0 or ramp > 1.0 for ramp in new_ramps):
                    break

                # Calculate resulting pitch and bank and append the resulting attitude to the list
                # of possible attitudes
                new_pitch = self.pitch + self._pitch_per_ramp * (
                    new_ramps[0] + new_ramps[1] - new_ramps[2] - new_ramps[3]
                )
                new_bank = self.bank + self._bank_per_ramp * (
                    new_ramps[0] - new_ramps[1] + new_ramps[2] - new_ramps[3]
                )
                new_attitude = Camper.Attitude(new_ramps, new_pitch, new_bank)
                
                if new_attitude not in possible_attitudes:
                    possible_attitudes.append(new_attitude)
        
        return possible_attitudes

    def _get_correction(self) -> float:
        # Get amount of correction that could be applied using the available ramps
        try:
            return (1 - (self.best_attitude.total / self.initial_attitude.total))
        except ZeroDivisionError:
            return 1.0
        
    def cli_get_ramp_effect(self) -> None:
        # Ask the user via the command line to enter the RVs attitude without ramps and with one ramp at the LF wheel
        print("Enter the attitude of your RV without any ramps below your wheels")
        pitch_initial = Camper.get_float("Pitch (+ is nose up): ")
        bank_initial = Camper.get_float("Bank (+ is right side low): ")

        print("Place your RV's left front wheel at the highest postion of your ramp")
        pitch_ramp_lf = Camper.get_float("Pitch (+ is nose up): ")
        bank_ramp_lf = Camper.get_float("Bank (+ is right side low): ")

        # Save the effect of one ramp
        self._pitch_per_ramp = pitch_ramp_lf - pitch_initial
        self._bank_per_ramp = bank_ramp_lf - bank_initial
        
    def cli_get_ramp_positions(self) -> None:
        # Ask the user via the command line for the current attitude ad provide ramp positions for the best possible
        # attitude correction
        print("Enter the attitude of your RV without any ramps below your wheels")
        self.pitch = Camper.get_float("Pitch (+ is nose up): ")
        self.bank = Camper.get_float("Bank (+ is right side low): ")
        print(self)

    @staticmethod
    def get_float(query="Enter a number: ", error_msg="Invalid Entry!", blank_is_zero=True) -> float:
        # Get a float from the user via the command line
        while True:
            user_input = input(query)
            if user_input == "" and blank_is_zero:
                return 0.0

            try:
                return float(user_input)
            except ValueError:
                print(error_msg)
                pass


if __name__ == "__main__":
    # Preset ramp effect values
    # CHANGE THESE VALUES ACCORDING TO YOUR RV/RAMP COMBINATION
    MY_PITCH_PER_RAMP = 0.8
    MY_BANK_PER_RAMP = 1.5

    camper=Camper(MY_PITCH_PER_RAMP, MY_BANK_PER_RAMP)
    camper.cli_get_ramp_positions()
