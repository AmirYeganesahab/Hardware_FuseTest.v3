import cython
import logging
from ximea import xiapi
import numpy as np


class camera():
    def __init__(self,exposure_time:cython.int = int(10000),trigger_source:str='hardware') -> None:
        self.logger = logging.getLogger('camera logs')
        self.trigger_source = trigger_source
        self.exposure_time = exposure_time
        self.open_device()

    def open_device(self):
        try:
            self.logger.info(f'trigger sou;rce: {self.trigger_source}')
            self.device:xiapi.Camera = xiapi.Camera()
            self.settings()
            try:
                self.device.close_device()
            except:
                pass
            self.logger.info('device is openning ...')
            self.device.open_device()
            self.logger.info('device is up')
            self.device.stop_acquisition()
            self.apply_settings()
            
            self.img = self.device,xiapi.Image()
            return True
        except Exception as e:
            self.logger.error(f'Error: {e}')
            return False

    def apply_settings(self):
        try:
            # trigger_source
            self.device.set_param( 'trigger_source',self.trigger['source'])
            self.logger.info(f'trigger_source set to: {self.trigger["source"]}')
            # Trigger Selector
            self.device.set_param('trigger_selector',self.trigger['selector'])
            self.logger.info(f'trigger_selector set to: {self.trigger["selector"]}') 
            # GPI Mode
            self.device.set_param( 'gpi_mode',self.gpi['mode'])
            self.logger.info(f'gpi_mode set to: {self.gpi["mode"]}') 
            # GPI Selector
            self.device.set_param( 'gpi_selector',self.gpi['selector'])
            self.logger.info(f'gpi_selector set to: {self.gpi["selector"]}')
            # GPO Mode
            self.device.set_param( 'gpo_mode',self.gpo['mode'])
            self.logger.info(f'gpo_mode set to: {self.gpo["mode"]}') 
            # Auto Exposure
            self.device.set_param('aeag',self.general['auto_exposure'])# or 1 AutoExposure
            self.logger.info(f'Auto exposure set to: {"on" if self.general["auto_exposure"] else "off"}')
            # Exposure Time
            if not self.general['auto_exposure']:
                self.device.set_param('exposure',self.general['exposure_time'])
                self.logger.info(f'exposure_time set to: {self.general["exposure_time"]}')
            else:
                # Maximum limit of gain in AEAG procedure.
                self.device.set_param( 'ag_max_limit',self.general['ag_max_limit'])#db
                self.logger.info(f'ag_max_limit set to: {self.general["ag_max_limit"]}')
                # Maximum limit of exposure (in uSec) in AEAG procedure.
                self.device.set_param( 'ae_max_limit',self.general['ae_max_limit'])#us
                self.logger.info(f'ae_max_limit set to: {self.general["ae_max_limit"]}')
                # Exposure priority for Auto Exposure / Auto Gain function.
                self.device.set_param( 'exp_priority',self.general['exp_priority'])# maximum 1
                self.logger.info(f'exp_priority set to: {self.general["exp_priority"]}')
                # Average intensity of output signal AEAG should achieve(in %).
                self.device.set_param( 'aeag_level',self.general['aeag_level'])
                self.logger.info(f'aeag_level set to: {self.general["aeag_level"]}')
            # Description: Activates Look-Up-Table (LUT).
            # Note1: Possible value: 0 - sensor pixels are transferred directly
            # Note2: Possible value: 1 - sensor pixels are mapped through LUT
            self.device.set_param( 'LUTEnable',self.general['LUTEnable'])
            self.logger.info(f'LUTEnable set to: {self.general["LUTEnable"]}')
            
            #self.device.set_param('acq_frame_burst_count',1)
            #self.device.set_exposure_burst_count(self.general['exposure_burst_count'])
            return True
        except Exception as e:
            self.logger.error(f'Error: {e}')
            return False

    def settings(self):
        try:
            self.trigger = {
                            'source':"XI_TRG_SOFTWARE" if self.trigger_source=='software'\
                                                        else "XI_TRG_EDGE_RISING",
                            'selector':"XI_TRG_SEL_FRAME_START",
                            }
            self.gpi = {'selector':"XI_GPI_PORT1",
                        'mode':"XI_GPI_TRIGGER"
                        }
            
            self.gpo = {'lsector':"XI_GPO_PORT1",
                        'mode':"XI_GPO_BUSY_NEG",
                        'mode_':"XI_GPO_EXPOSURE_ACTIVE_NEG"
                        }
            # ag_max_limit: Maximum limit of gain in AEAG procedure.(db)
            # ae_max_limit: Maximum limit of exposure (in uSec) in AEAG procedure.
            self.general = {'auto_exposure':0,
                            'exposure_time':self.exposure_time,
                            'ag_max_limit':10,
                            'ae_max_limit':10000,
                            'exp_priority':0.5,
                            'aeag_level':50,
                            'LUTEnable':0,
                            'exposure_burst_count':1,
                            }
            return True
        except Exception as e:
            self.logger.error(f'Error: {e}')
            return False
        
    def get_image(self):
        
        try:
            self.device.get_image(self.img[1])
            image2:np.ndarray= self.img[1].get_image_data_numpy()
            return image2
        except Exception as e:
            self.logger.error(f'Error: {e}')
            return None
            
    def close_device(self):
        try:
            self.device.stop_acquisition()
            self.device.close_device()
            return True
        except Exception as e:
            self.logger.error(f'Error: {e}')
            return False