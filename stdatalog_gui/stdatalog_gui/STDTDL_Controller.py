
# ******************************************************************************
# * @attention
# *
# * Copyright (c) 2022 STMicroelectronics.
# * All rights reserved.
# *
# * This software is licensed under terms that can be found in the LICENSE file
# * in the root directory of this software component.
# * If no LICENSE file comes with this software, it is provided AS-IS.
# *
# *
# ******************************************************************************
#

from abc import abstractmethod
from enum import Enum

from PySide6.QtCore import QObject, Signal

from stdatalog_dtk.HSD_DataToolkit_Pipeline import HSD_DataToolkit_Pipeline
from stdatalog_pnpl.DTDL.device_template_manager import DeviceTemplateManager
from stdatalog_pnpl.DTDL.device_template_model import InterfaceElement
from stdatalog_gui.Utils.PlotParams import SensorPlotParams, AlgorithmPlotParams, ActuatorPlotParams
from stdatalog_pnpl.DTDL.dtdl_utils import DTDL_ACTUATORS_ID_COMP_KEY, DTDL_ALGORITHMS_ID_COMP_KEY, DTDL_SENSORS_ID_COMP_KEY


class ComponentType(Enum):
    SENSOR = 0
    ALGORITHM = 1
    OTHER = 2
    ACTUATOR = 3
    NONE = -1

class STDTDL_Controller(QObject):
    
    # Signals
    sig_device_connected = Signal(bool)
    sig_com_init_error = Signal()
    
    sig_dtm_loading_started = Signal()
    sig_dtm_loading_completed = Signal()
    
    sig_component_found = Signal(str, InterfaceElement)
    sig_sensor_component_found = Signal(str, InterfaceElement)
    sig_actuator_component_found = Signal(str, InterfaceElement)
    sig_algorithm_component_found = Signal(str, InterfaceElement)

    sig_component_updated = Signal(str, dict)
    sig_sensor_component_updated = Signal(str, SensorPlotParams)
    sig_algorithm_component_updated = Signal(str, AlgorithmPlotParams)
    sig_actuator_component_updated = Signal(str, ActuatorPlotParams)
    
    sig_component_removed = Signal(str)
    
    sig_telemetry_received = Signal(str)
    
    sig_component_config_widget_width_updated = Signal(int)
    
    sig_plot_window_time_updated = Signal(float)
    
    sig_ispu_ucf_loaded = Signal(str, str)
    sig_wav_conversion_completed = Signal(str, str)
    sig_offline_plots_completed = Signal()

    sig_tmos_presence_detected = Signal(bool,str,str)
    sig_tmos_motion_detected = Signal(bool,str,str)

    sig_tof_presence_detected = Signal(bool,str)
    sig_tof_presence_detected_in_roi = Signal(bool,int,str)
    
    sig_autologging_is_stopping = Signal(bool)
    sig_logging = Signal(bool, int)
    sig_detecting = Signal(bool)

    sig_pnpl_response_received = Signal(str, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.device_id = 0 #default device id
        self.plots_layout = None
        self.components_dtdl = dict() #From DTDL DeviceModel 
        self.components_status = dict() #From FW
        self.cconfig_widgets = dict() #{comp_name:CConfigWidget}
        self.plot_widgets = dict()
        # self.plugin_plot_widgets = dict()
        self.plugin_plot_widgets = []
        self.__dt_manager = None
        self.log_msg = ""
        self.detect_msg = ""
        self.data_pipeline = None
        self.qt_app = None

    def set_Qt_app(self, qt_app):
        self.qt_app = qt_app

    def set_plots_layout(self, plots_layout):
        self.plots_layout = plots_layout
        
    def load_local_device_template(self, dev_template_json):  
        self.__dt_manager = DeviceTemplateManager(dev_template_json)
        self.components_dtdl = self.__dt_manager.get_components()
        for comp_name in self.components_dtdl.keys():
            if ":"+DTDL_SENSORS_ID_COMP_KEY+":" in self.components_dtdl[comp_name].id:
                self.sig_sensor_component_found.emit(comp_name, self.components_dtdl[comp_name])
            elif ":"+DTDL_ALGORITHMS_ID_COMP_KEY+":" in self.components_dtdl[comp_name].id:
                self.sig_algorithm_component_found.emit(comp_name, self.components_dtdl[comp_name])
            elif ":"+DTDL_ACTUATORS_ID_COMP_KEY+":" in self.components_dtdl[comp_name].id:
                self.sig_actuator_component_found.emit(comp_name, self.components_dtdl[comp_name])
            else:
                self.sig_component_found.emit(comp_name, self.components_dtdl[comp_name])
        if self.data_pipeline is not None:
            self.data_pipeline.update_components_status(self.components_status)
                
    def get_component_config_widget(self, comp_name):
        if comp_name in self.cconfig_widgets:
            return self.cconfig_widgets[comp_name]
        else:
            return None
    
    def add_component_config_widget(self, cconfig_widget):
        self.cconfig_widgets[cconfig_widget.comp_name] = (cconfig_widget)
        self.cconfig_widgets[cconfig_widget.comp_name].setVisible(True)

    def remove_component_config_widget(self, comp_name):
        self.cconfig_widgets[comp_name].setVisible(False)
        self.cconfig_widgets[comp_name].deleteLater()
        self.cconfig_widgets.pop(comp_name)

    def hide_plot_widget(self, comp_name):
        self.plot_widgets[comp_name].setVisible(False)

    def show_plot_widget(self, comp_name):
        self.plot_widgets[comp_name].setVisible(True)

    def add_plugin_plot_widget(self, plot_widget):
        self.plots_layout.addWidget(plot_widget)
        self.plugin_plot_widgets.append(plot_widget)

    def remove_plugin_plot_widget(self, plot_widget):
        plot_widget.setVisible(False)
        plot_widget.deleteLater()
        self.plugin_plot_widgets.remove(plot_widget)
        self.plots_layout.removeWidget(plot_widget)

    def clear_all_plugin_plot_widgets(self):
        for plot_widget in self.plugin_plot_widgets:
            plot_widget.setVisible(False)
            plot_widget.deleteLater()
            self.plots_layout.removeWidget(plot_widget)
        self.plugin_plot_widgets.clear()
        
    def set_log_msg(self, log_msg):
        self.log_msg = log_msg
        
    def set_detect_msg(self, detect_msg):
        self.detect_msg = detect_msg
        
    def set_component_config_width(self, width):
        self.sig_component_config_widget_width_updated.emit(width)

    def create_data_pipeline(self):
        self.data_pipeline = HSD_DataToolkit_Pipeline(self)
    
    def destroy_data_pipeline(self):
        self.data_pipeline = None
    
    def get_log_msg(self):
        return self.log_msg
    
    def get_detect_msg(self):
        return self.detect_msg
        
    @abstractmethod
    def refresh(self):
        pass
    
    @abstractmethod
    def is_com_ok(self):
        pass
    
    @abstractmethod
    def get_device_formatted_name(self):
        pass
    
    @abstractmethod
    def get_device_list(self):
        pass
    
    @abstractmethod
    def get_device_presentation_string(self, d_id = 0):
        pass

    @abstractmethod
    def get_device_info(self, d_id = 0):
        pass

    @abstractmethod
    def is_sensor_enabled(self, comp_name, d_id = 0):
        pass
    
    @abstractmethod
    def fill_component_status(self, comp_name):
        pass
    
    @abstractmethod
    def get_component_status(self, comp_name):
        pass
    
    @abstractmethod
    def update_component_status(self, comp_name, comp_type = "other"):
        pass
    
    @abstractmethod
    def update_device_status(self):
        pass
        
    @abstractmethod
    def connect_to(self, d_id, d_text = None, com_speed = None):  
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def send_command(self, json_command):
        pass

    @abstractmethod
    def get_device_status(self):
        pass
    
    @abstractmethod
    def save_config(self, on_pc, on_sd):
        pass

    @abstractmethod
    def is_hsd_link_serial(self):
        pass
