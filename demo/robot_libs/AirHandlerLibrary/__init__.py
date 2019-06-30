from .air_handler_states import AirHandlerStates
from .air_handler_actions import AirHanlderActions


class AirHandlerStatesLibrary(AirHandlerStates):
    ROBOT_LIBRARY_SCOPE = "GLOBAL"


class AirHandlerActionsLibrary(AirHanlderActions):
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
