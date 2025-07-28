import numpy as np
import cv2
import pyautogui


from pymodaq_utils.utils import ThreadCommand
from pymodaq_data.data import DataToExport
from pymodaq_gui.parameter import Parameter

from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.data import DataFromPlugins

class PythonWrapperOfYourInstrument:
    #  TODO Replace this fake class with the import of the real python wrapper of your instrument
    pass

# TODO:
# (1) change the name of the following class to DAQ_0DViewer_TheNameOfYourChoice
# (2) change the name of this file to daq_0Dviewer_TheNameOfYourChoice ("TheNameOfYourChoice" should be the SAME
#     for the class name and the file name.)
# (3) this file should then be put into the right folder, namely IN THE FOLDER OF THE PLUGIN YOU ARE DEVELOPING:
#     pymodaq_plugins_my_plugin/daq_viewer_plugins/plugins_0D

class DAQ_0DViewer_Rigi(DAQ_Viewer_base):
    """ Instrument plugin class for a OD viewer.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Viewer module through inheritance via
    DAQ_Viewer_base. It makes a bridge between the DAQ_Viewer module and the Python wrapper of a particular instrument.

    TODO Complete the docstring of your plugin with:
        * The set of instruments that should be compatible with this instrument plugin.
        * With which instrument it has actually been tested.
        * The version of PyMoDAQ during the test.
        * The version of the operating system.
        * Installation instructions: what manufacturer’s drivers should be installed to make it run?

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.
         
    # TODO add your particular attributes here if any

    """
    params = comon_parameters+[
        ## TODO for your custom plugin: elements to be added here as dicts in order to control your custom stage
        ]


    def ini_attributes(self):
        #  TODO declare the type of the wrapper (and assign it to self.controller) you're going to use for easy
        #  autocompletion
        self.controller: PythonWrapperOfYourInstrument = None

        
        # Define region: (left, top, width, height)
        # region = (50, 55, 950, 700)
        self.region = (50, 55, 1260, 960)
        self.background = 10.082550805224868

        pass

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """

        if param.name() == "a_parameter_you've_added_in_self.params":
           self.controller.your_method_to_apply_this_param_change()


    def ini_detector(self, controller=None):
        """Detector communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator/detector by controller
            (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """
        
        initialized = True
        info = "Rigi Initialized (Not really I can't read the .dll)"
        return info, initialized

    def close(self):
        """Terminate the communication protocol"""
        return " "


    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """

        screenshot = pyautogui.screenshot(region=self.region)
        frame = np.array(screenshot)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        pxls = gray.shape[0] * gray.shape[1]
        middle_pixel = gray[int(gray.shape[0]/2)][int(gray.shape[1]/2)]
        intensity = np.sum(gray) / pxls - self.background

        data_tot = intensity
        self.dte_signal.emit(DataToExport(name='RigiPlugin',
                                          data=[DataFromPlugins(name='IntegratedValue', data=data_tot,
                                                                dim='Data0D', labels=['Integrated Value'])]))

        #########################################################



    def callback(self):
        """optional asynchrone method called when the detector has finished its acquisition of data"""
        data_tot = self.controller.your_method_to_get_data_from_buffer()
        self.dte_signal.emit(DataToExport(name='myplugin',
                                          data=[DataFromPlugins(name='Mock1', data=data_tot,
                                                                dim='Data0D', labels=['dat0', 'data1'])]))

    def stop(self):
        """Stop the current grab hardware wise if necessary"""
        self.emit_status(ThreadCommand('Update_Status', ['Stop']))
        # ##############################
        return ''


if __name__ == '__main__':
    main(__file__)
