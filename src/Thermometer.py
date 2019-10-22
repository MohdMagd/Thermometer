__author__ = "Mohamed Abouelmagd"
__version__ = "3.8.0"
__email__ = "mohamed.almajd@gmail.com"
__status__ = "Coding Assessment Assignment"

import pandas
import threading
from time import sleep


class Thermometer(threading.Thread):
    """
    This class implements a Thermometer that provides temperature readings in both Fahrenheit and Celsius.
    The thermometer can be configured to alert users if it has surpassed a pre-set low or high temperature threshold.
    NOTE: The thermometer reads in temperature readings from a .csv extension file, that MUST be inputted in °C unit.
    Thermometer can then be toggled by a caller between Fahrenheit and Celsius (See DocString for read_temperatures()
     and toggle_celsius_fahrenheit() for more information).
    This implementation utilizes multi-threading enabling a user to read-in temperature readings in a new thread
    and leaving the caller or main thread free to perform other processes.
    To start reading in temperature data, user must use start() method, after creating thermometer object
    -> i.e.: thermometer.start()
    """
    def __init__(
            self,
            source_path,
            low_temp_threshold=0,
            high_temp_threshold=100,
            fluctuation=0.5,
            thermometer_unit='°C',
            threshold_dir=None
    ):
        """
        :param source_path: file path for .csv extension file
        :param low_temp_threshold: User-defined low temperature threshold
        :param high_temp_threshold: User-defined high temperature threshold
        :param fluctuation: User-defined margin to ignore alerts for temperature changes +/- fluctuation ° of off
                            low and high temperature thresholds
        :param thermometer_unit: Unit of measurement for temperature (°C or °F only!)
        :param threshold_dir: Used to define if user requires alerts in temperature changes in one and only one
                              direction ('upward' or 'downward')
        """
        super(Thermometer, self).__init__()
        self.source_path: str = source_path
        self.low_threshold: float = low_temp_threshold
        self.high_threshold: float = high_temp_threshold
        self.fluctuation: float = fluctuation
        self.__unit: str = thermometer_unit
        self.__direction: str = threshold_dir
        self.current_temperature = None
        self.__exit: bool = False
        self.__pause = False
        self.pause_cond = threading.Condition(threading.Lock())

    def run(self):
        """
        Method is called by super.start() to start reading in temperature data
        """
        self.__exit = False
        self.monitor_temp()

    def kill(self):
        """
        Method to terminate reading temperature data from source
        """
        if self.is_alive():
            self.__exit = True
        else:
            print('Thermometer is already switched OFF!')

    def monitor_temp(self):
        """
        Informs caller that a specific threshold has been reached in a specific direction, if specified
        """
        last_temp = (self.high_threshold - self.low_threshold)/2
        downwards = self.__direction in (None, 'downwards')
        upwards = self.__direction in (None, 'upwards')
        below, above = False, False

        for temp in self.read_temperatures():
            within_fluc_range = (-1 * self.fluctuation <= abs(temp) - abs(last_temp) <= self.fluctuation)
            # check if thermometer has been stopped
            if self.__exit:
                print('Thermometer OFF! ')
                break
            # check if below low threshold
            if downwards and not below and temp < self.low_threshold and not within_fluc_range:
                print(f'Thermometer: Temperature is below {self.low_threshold}{self.__unit} ')
                below = True
                last_temp = temp
            # check if above high threshold
            elif upwards and not above and temp > self.high_threshold and not within_fluc_range:
                print(f'Thermometer: Temperature is higher than high threshold = {self.high_threshold}{self.__unit} ')
                above = True
                last_temp = temp
            # check if temperature moved to be in range(low_threshold + fluctuation, high_threshold-fluctuation)
            elif below != above and downwards == upwards and not within_fluc_range and self.low_threshold < temp < self.high_threshold:
                print('Back between low & high thresholds ')
                below, above = False, False

    def read_temperatures(self):
        """
        Loads temperature readings from .csv file in the specified path, self.source_path.
        .csv file must include a column with head title 'temperature_readings' and the temperature data must be inputted
        in °C
        :return: yields next temperature reading in 'temperature_readings' column
        """
        df = pandas.read_csv(self.source_path)
        if "temperature_readings" not in df:
            raise ValueError(f'Temperature Readings in {self.source_path} missing temperature_readings column')

        for temp in df["temperature_readings"]:
            sleep(.5)  # Read temperatures at a rate of 2 readings/sec

            with self.pause_cond:  # check if thread has been requested to pause itself by another method()
                while self.__pause:
                    self.pause_cond.wait()

            # Convert temperature to Fahrenheit if thermometer in Fahrenheit
            if self.__unit == '°F':
                temp = self.convert_celsius_to_fahrenheit(temp)

            self.current_temperature = temp  # update current thermometer temperature
            yield float(temp)

    def toggle_celsius_fahrenheit(self):
        """
        This method converts thermometer between (°C -> °F, or vice versa) before resuming temperature reading thread.
        If thermometer is reading temperatures at the time of calling this method, the reading thread is
        paused first before conversion, and resumed again post-unit conversion.
        """
        if self.is_alive():
            self.pause_read_thread()

        if self.__unit == '°C':
            self.__unit = '°F'
            self._convert_thermometer_to_fahrenheit()
        elif self.__unit == '°F':
            self.__unit = '°C'
            self._convert_thermometer_to_celsius()

        if self.is_alive():
            self.resume_read_thread()

    def _convert_thermometer_to_fahrenheit(self):
        """
        Converts the pre-set low, high and fluctuation temperature thresholds as well as current temperature to
        Fahrenheit
        """
        self.__unit = '°F'
        self.low_threshold = self.convert_celsius_to_fahrenheit(self.low_threshold)
        self.high_threshold = self.convert_celsius_to_fahrenheit(self.high_threshold)
        self.fluctuation = self.convert_celsius_to_fahrenheit(self.fluctuation)

        if self.current_temperature:
            self.current_temperature = self.convert_celsius_to_fahrenheit(self.current_temperature)

    def _convert_thermometer_to_celsius(self):
        """
        Converts the pre-set low, high and fluctuation temperature thresholds as well as current temperature to
        Celsius
        """
        self.__unit = '°C'
        self.low_threshold = self.convert_fahrenheit_to_celsius(self.low_threshold)
        self.high_threshold = self.convert_fahrenheit_to_celsius(self.high_threshold)
        self.fluctuation = self.convert_fahrenheit_to_celsius(self.fluctuation)

        if self.current_temperature:
            self.current_temperature = self.convert_fahrenheit_to_celsius(self.current_temperature)

    def get_current_temperature(self):
        """
        :return: Current Thermometer Temperature reading rounded to 2 decimal places
        """
        if self.is_alive():
            while not self.current_temperature:
                continue
            self.pause_read_thread()
            temp = round(self.current_temperature, 2)
            self.resume_read_thread()
            return temp
        else:
            print('Thermometer not enabled! Please enable thermometer first using the run() method')

    def get_current_unit(self):
        """
        :return: Current Thermometer Unit
        """
        self.pause_read_thread()
        current_unit = self.__unit
        self.resume_read_thread()

        return current_unit

    def pause_read_thread(self):
        """
        Sets internal pause flag and waits to acquire thread lock to allow calling method to safely modify class
        variables
        """
        self.__pause = True
        self.pause_cond.acquire()

    def resume_read_thread(self):
        """
        Removes pause flag and releases thread to continue reading temperatures from .csv source file
        :return:
        """
        self.__pause = False
        # Notify so thread will wake after lock released
        self.pause_cond.notify()
        # Now release the lock
        self.pause_cond.release()

    @staticmethod
    def convert_fahrenheit_to_celsius(temp):
        """
        Takes in a Fahrenheit temperature reading and returns the temperature in degrees Celsius
        :param temp: Fahrenheit Temperature Reading
        :return: Celsius Temperature Reading
        """
        return (temp - 32) * 5/9

    @staticmethod
    def convert_celsius_to_fahrenheit(temp):
        """
        Takes in a Celsius temperature reading and returns the temperature in degrees Fahrenheit
        :param temp: Celsius Temperature Reading
        :return: Fahrenheit Temperature Reading
        """
        return (temp * 9/5) + 32
