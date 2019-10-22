__author__ = "Mohamed Abouelmagd"
__version__ = "3.8.0"
__email__ = "mohamed.almajd@gmail.com"
__status__ = "Coding Assessment Assignment"

from src.Thermometer import Thermometer
import time


def main():
    path = 'temp.csv'  # Thermometer assumes readings to be loaded from .csv file (see DocString for Thermometer Class)
    # Test 1:
    # Wait 1 second 1.2x(reading rate) and print out the current temperature and unit of measurement and Thermometer
    # alerts us if temperature has gone through both high or low thresholds (threshold_dir= None)

    print('\nStarting Test 1 ->\n')
    thermometer = Thermometer(
        source_path=path,
        low_temp_threshold=0,
        high_temp_threshold=100,
        fluctuation=0.5,
        thermometer_unit='°C',
        threshold_dir=None
    )
    thermometer.start()
    for i in range(19):
        time.sleep(.6)
        print(f'Current Temperature is: {thermometer.get_current_temperature()}{thermometer.get_current_unit()} ')
    thermometer.kill()

    # Test 2:
    # Wait 1 second 1.2x(reading rate) and print out the current temperature and unit of measurement and Thermometer
    # alerts us if temperature has gone through low threshold only (threshold_dir='downwards')

    # print('\nStarting Test 2 ->\n')
    # thermometer = Thermometer(
    #     source_path=path,
    #     low_temp_threshold=0,
    #     high_temp_threshold=100,
    #     fluctuation=0.5,
    #     thermometer_unit='°C',
    #     threshold_dir='downwards'
    # )
    # thermometer.start()
    # for i in range(19):
    #     time.sleep(.6)
    #     print(f'Current Temperature is: {thermometer.get_current_temperature()}{thermometer.get_current_unit()} ')
    # thermometer.kill()

    # Test 3:
    # Wait 1 second 1.2x(reading rate) and print out the current temperature and unit of measurement and Thermometer
    # alerts us if temperature has gone through high threshold only (threshold_dir='upwards')

    # print('\nStarting Test 3 ->\n')
    # thermometer = Thermometer(
    #     source_path=path,
    #     low_temp_threshold=0,
    #     high_temp_threshold=100,
    #     fluctuation=0.5,
    #     thermometer_unit='°C',
    #     threshold_dir='upwards'
    # )
    # thermometer.start()
    # for i in range(19):
    #     time.sleep(.6)
    #     print(f'Current Temperature is: {thermometer.get_current_temperature()}{thermometer.get_current_unit()} ')
    # thermometer.kill()

    # Test 4:
    # We wait only .5 seconds 1x(reading rate) and toggle to switch to different unit on each reading
    # and print out the current Temperature and unit of measurement

    # print('\nStarting Test 4 ->\n')
    # thermometer = Thermometer(
    #     source_path=path,
    #     low_temp_threshold=0,
    #     high_temp_threshold=100,
    #     fluctuation=0.5,
    #     thermometer_unit='°C',
    #     threshold_dir=None
    # )
    # thermometer.start()
    # for i in range(25):
    #     time.sleep(.5)
    #     thermometer.toggle_celsius_fahrenheit()
    #     print(f'Current Temperature is: {thermometer.get_current_temperature()}{thermometer.get_current_unit()} ')
    # thermometer.kill()


if __name__ == "__main__":
    main()
