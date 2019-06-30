from robot.api.deco import keyword


class AirHanlderActions(object):
    @keyword('Turn AC ON')
    def turn_ac_on:
        print(r'Setting "Turn AC ON" state...')

    @keyword('Turn Heat ON')
    def turn_heat_on:
        print(r'Setting "Turn Heat ON" state...')

    @keyword('Reach Desired Temperature')
    def reach_desired_temp:
        print(r'Setting "Reach Desired Temperature" state...')

    @keyword('Switch OFF')
    def switch_off:
        print(r'Setting "Switch OFF" state...')

    @keyword('Switch ON')
    def switch_on:
        print(r'Setting "Switch ON" state...')
