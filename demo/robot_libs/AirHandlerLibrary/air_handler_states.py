from robot.api.deco import keyword


class AirHandlerStates(object):
    @keyword('Idle')
    def idle:
        print(r'Checking "Idle" state...')

    @keyword('Cooling Down')
    def cooling_down:
        print(r'Checking "Cooling Down" state...')

    @keyword('Warming Up')
    def warming_up:
        print(r'Checking "Warming Up" state...')

    @keyword('Off')
    def off:
        print(r'Checking "Off" state...')
