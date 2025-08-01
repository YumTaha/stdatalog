#!/usr/bin/env python
# coding: utf-8 
# *****************************************************************************
#  * @file    stdatalog_TUI.py
#  * @author  SRA
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

"""
This script, `stdatalog_TUI.py`, is a Text-based User Interface designed to manage data logging
for devices using STMicroelectronics' HSDatalog tool. It supports various options for configuring
the data logging process, including setting acquisition parameters, uploading configuration files, 
labeling acquired data and more.
It uses click for command-line interface options and logs information and errors during execution.
The script can be run from the command line with various options to tailor the data logging
to the user's needs.

Key Features:
- Manage data logging for specific sensors or all active components.
- Set acquisition parameters such as name, description, and duration.
- Specify the output folder for logged data.
- Upload and use custom configuration files (JSON, UCF).
- Enable interactive mode for device selection and acquisition management.
- Save ISPU output format description JSON in the acquisition folder.
"""

import sys
import os
import time

# Add the STDatalog SDK root directory to the sys.path to access the SDK packages
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

import subprocess
import click
import shutil
import stdatalog_core.HSD_utils.logger as logger
log = logger.setup_applevel_logger(is_debug = False, file_name= "app_debug.log")

log.info("Checking additional required packages...")

# required package
required_package = "asciimatics"

# Check for missing packages
missing_asciimatics = False
try:
    __import__(required_package)
except ImportError:
    if required_package == "asciimatics":
        missing_asciimatics = True

# Notify user of missing packages
if missing_asciimatics:
    log.warning("The following required packages are missing:")
    log.warning(f" - (asciimatics) asciimatics")
    log.info("This package is required for the TUI (Textual-based User Interface) and it will be now automatically installed.")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "asciimatics"])
    # Close the script execution
    print("Installation complete!")
    time.sleep(2)
else:
    log.info("All required packages are installed.")

from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError

from stdatalog_pnpl.DTDL.device_template_manager import DeviceTemplateManager, DeviceCatalogManager
from stdatalog_core.HSD_link.HSDLink import HSDLink
from stdatalog_examples.gui_applications.stdatalog.TUI.Views.tui_views import HSDMainView, HSDLoggingView
class HSDInfo():

    class TUIFlags():
        
        def __init__(self, output_folder, sub_datetime_folder, acq_name, acq_desc, file_config, ucf_file, ispu_out_fmt, time_sec, interactive_mode):
            self.output_folder = output_folder
            self.sub_datetime_folder = sub_datetime_folder
            self.acq_name = acq_name
            self.acq_desc = acq_desc
            self.file_config = file_config
            self.ucf_file = ucf_file if ucf_file != "" else None
            self.ispu_out_fmt = ispu_out_fmt if ispu_out_fmt != "" else None
            self.time_sec = time_sec
            self.interactive_mode = interactive_mode
    
    tui_flags = None
    version = None
    device_list = None
    sensor_list = None
    sensor_count = None
    tag_list = []
    highlighted_device_id = None
    selected_device_id = None
    selected_fw_info = None
    mlc_sensor_list = None
    ispu_sensor_list = None
    selected_mlc_id = None
    selected_ispu_id = None
    is_log_started = False
    is_log_manually_stopped = False
    is_shutting_down = False
    output_acquisition_path = None
    threads_stop_flags = []
    tag_status_list = []
    start_time = None

    def __init__(self, tui_flags):
        self.tui_flags = tui_flags

        #Initialize the HSD_PythonSDK HSD_link module
        self.hsd_link_factory = HSDLink()
        self.hsd_link = self.hsd_link_factory.create_hsd_link(acquisition_folder = tui_flags.output_folder)

        #Get the connected device list
        self.device_list = HSDLink.get_devices(self.hsd_link)

        if len(self.device_list) == 0:
            quit()

        #Updates the output folder field
        if self.tui_flags.output_folder is None:
            self.tui_flags.output_folder = HSDLink.get_acquisition_folder(self.hsd_link)
                
        #Multiple connected devices management
        if self.device_list is None or len(self.device_list) > 1:
            self.selected_device_id = None
        else:
            self.selected_device_id = 0
            pres_res = HSDLink.get_device_presentation_string(self.hsd_link, self.selected_device_id)
            if pres_res is not None:
                board_id = hex(pres_res["board_id"])
                fw_id = hex(pres_res["fw_id"])
                self.load_device_template(board_id,fw_id)
    
    def is_hsd_link_v2(self):
        if self.hsd_link is not None:
            return HSDLink.is_v2(self.hsd_link)
        return False
    
    def load_device_template(self, board_id, fw_id):
        dev_template_json = DeviceCatalogManager.query_dtdl_model(board_id, fw_id)
        if isinstance(dev_template_json,dict):
            fw_name = self.hsd_link.get_firmware_info(self.selected_device_id).get("firmware_info").get("fw_name")
            if fw_name is not None:
                splitted_fw_name = fw_name.lower().split("-")
                reformatted_fw_name = "".join([splitted_fw_name[0]] + [f.capitalize() for f in splitted_fw_name[1:]])
            for dt in dev_template_json:
                if reformatted_fw_name.lower() in dev_template_json[dt][0].get("@id").lower():
                    dev_template_json = dev_template_json[dt]
                    break
        HSDLink.set_device_template(self.hsd_link, dev_template_json)
    
    def update_fw_info(self):
        self.selected_fw_info = HSDLink.get_firmware_info(self.hsd_link, self.selected_device_id)

    def check_output_folder(self):
        if self.output_acquisition_path is None:
            if self.tui_flags.output_folder is not None:
                if not os.path.exists(self.tui_flags.output_folder):
                    os.makedirs(self.tui_flags.output_folder)
                self.output_acquisition_path = self.tui_flags.output_folder
            else:
                self.output_acquisition_path = HSDLink.get_acquisition_folder(self.hsd_link)

    def save_device_in_output_folder(self):
        return HSDLink.save_json_device_file(self.hsd_link, self.selected_device_id, self.output_acquisition_path)

    def update_acq_params(self):
        # Set acquisition name and description parameters to the device
        if self.tui_flags.acq_name is None:
            self.tui_flags.acq_name = "STWIN_Acq"
        if self.tui_flags.acq_desc is None:
            self.tui_flags.acq_desc = ""

        HSDLink.set_acquisition_info(self.hsd_link, self.selected_device_id, self.tui_flags.acq_name, self.tui_flags.acq_desc)

    def upload_device_conf_file(self):
        # Device configuration file [DeviceConfig.json]
        if self.tui_flags.file_config != '' and os.path.exists(self.tui_flags.file_config):
            res = HSDLink.update_device(self.hsd_link, self.selected_device_id, self.tui_flags.file_config)
            if not res:
                log.warning("Error in Device configuration update. The default configuration will be used!")
            else:
                shutil.copy(self.tui_flags.file_config, self.output_acquisition_path)
    
    def update_sensor_list(self):
        if self.is_shutting_down or self.selected_device_id is None:
            return
        try:
            self.sensor_list = HSDLink.get_sensor_list(self.hsd_link, self.selected_device_id, only_active=True)
        except Exception as e:
            log.warning(f"Could not update sensor list: {e}")
            # Keep the existing sensor list if update fails
            if self.sensor_list is None:
                self.sensor_list = []
    
    def init_sensor_data_counters(self):
        all_sensor_list = HSDLink.get_sensor_list(self.hsd_link, self.selected_device_id, only_active=False)
        HSDLink.init_sensors_data_counters(self.hsd_link, all_sensor_list)

    def update_ai_sensor_list(self):
        self.mlc_sensor_list = HSDLink.get_updated_mlc_sensor_list(self.hsd_link, self.selected_device_id, self.mlc_sensor_list)
        self.ispu_sensor_list = HSDLink.get_updated_ispu_sensor_list(self.hsd_link, self.selected_device_id, self.ispu_sensor_list)
        if self.mlc_sensor_list is not None and len(self.mlc_sensor_list) > 0:
            self.selected_mlc_id = HSDLink.get_mlc_id(self.hsd_link, self.selected_device_id)
        if self.ispu_sensor_list is not None and len(self.ispu_sensor_list) > 0:
            self.selected_ispu_id = HSDLink.get_ispu_id(self.hsd_link, self.selected_device_id)

    def upload_ai_ucf_file(self):
        if self.selected_mlc_id is not None:
            HSDLink.upload_mlc_ucf_file(self.hsd_link, self.selected_device_id, self.tui_flags.ucf_file)
            self.update_sensor_list()
        if self.selected_ispu_id is not None:
            HSDLink.upload_ispu_ucf_file(self.hsd_link, self.selected_device_id, self.tui_flags.ucf_file)
            self.update_sensor_list()

    def save_ai_ucf_file(self):
        self.output_acquisition_path = HSDLink.get_acquisition_folder(self.hsd_link)
        if self.tui_flags.ucf_file is not None:
            ucf_filename = os.path.basename(self.tui_flags.ucf_file)
            shutil.copyfile(self.tui_flags.ucf_file, os.path.join(self.output_acquisition_path, ucf_filename))
            log.info("{} File correctly saved".format(ucf_filename))
    
    def save_ispu_out_fmt_file(self):
        self.output_acquisition_path = HSDLink.get_acquisition_folder(self.hsd_link)
        if self.tui_flags.ispu_out_fmt is not None:
            shutil.copyfile(self.tui_flags.ispu_out_fmt, os.path.join(self.output_acquisition_path,"ispu_output_format.json"))
            log.info("ispu_output_format.json File correctly saved")

    def update_tag_list(self):
        if self.selected_device_id is not None:
            self.tag_list = HSDLink.get_sw_tag_classes(self.hsd_link, self.selected_device_id)

    def set_rtc(self):
        HSDLink.set_RTC(self.hsd_link, self.selected_device_id)
    
    def init_tag_status_list(self):
        self.tag_status_list = [False] * len(self.tag_list)

    def do_tag(self, t_id):
        self.tag_status_list[t_id] = not self.tag_status_list[t_id]
        HSDLink.set_sw_tag_on_off(self.hsd_link, self.selected_device_id, t_id, self.tag_status_list[t_id])

    def start_log(self):
        self.is_log_started = HSDLink.start_log(self.hsd_link, self.selected_device_id, self.tui_flags.sub_datetime_folder)
        self.threads_stop_flags = []
        self.sensor_data_files = []

        for s in self.sensor_list:
            HSDLink.start_sensor_acquisition_thread(self.hsd_link, self.selected_device_id, s, self.threads_stop_flags, self.sensor_data_files)
        self.output_acquisition_path = HSDLink.get_acquisition_folder(self.hsd_link)

    def stop_log(self):
        for sf in self.threads_stop_flags:
            sf.set()
        for f in self.sensor_data_files:
            f.close()
        HSDLink.stop_log(self.hsd_link, self.selected_device_id)
        self.is_log_started = False
        
        # Try to save device JSON file with error handling and retry
        import time
        for attempt in range(3):  # Try up to 3 times
            try:
                if attempt > 0:
                    time.sleep(0.5)  # Wait 500ms between attempts
                HSDLink.save_json_device_file(self.hsd_link, self.selected_device_id, self.output_acquisition_path)
                log.info("Device Config json File correctly saved")
                break  # Success, exit the retry loop
            except Exception as e:
                if attempt == 2:  # Last attempt
                    log.warning(f"Could not save device config JSON file after {attempt + 1} attempts: {e}")
                else:
                    log.debug(f"Attempt {attempt + 1} to save device config failed, retrying...")
        
        # Try to save acquisition info file with error handling
        try:
            HSDLink.save_json_acq_info_file(self.hsd_link, self.selected_device_id, self.output_acquisition_path)
            log.info("Acquisition Info json File correctly saved")
        except Exception as e:
            log.warning(f"Could not save acquisition info JSON file: {e}")
            
        #Save ISPU output format json file if passed as CLI parameter
        self.save_ai_ucf_file()
        self.save_ispu_out_fmt_file()
        HSDLink.refresh_hsd_link(self.hsd_link) #Needed by HSDLink_v1


script_version = "1.0.0"
def show_help(ctx, param, value):
    if value and not ctx.resilient_parsing:
        click.secho(ctx.get_help(), color=ctx.color)
        click.secho("\n-> Script execution examples:")
        click.secho("   python stdatalog_TUI.py", fg='cyan')
        click.secho("   python stdatalog_TUI.py -o .\\your_out_folder", fg='cyan')
        click.secho("   python stdatalog_TUI.py -t 10", fg='cyan')
        click.secho("   python stdatalog_TUI.py -i", fg='cyan')
        click.secho("   python stdatalog_TUI.py -t 20 -an your_acq_name -ad your_acq_descr", fg='cyan')
        click.secho("   python stdatalog_TUI.py -f ..\\STWIN_config_examples\\DeviceConfig.json -u ..\\STWIN_config_examples\\UCF_examples\\ism330dhcx_six_d_position.ucf", fg='cyan')
        ctx.exit()

def validate_duration(ctx, param, value):
    if value < -1 or value == 0:
        raise click.BadParameter('\'{d}\'. Please retry'.format(d=value))
    return value

@click.command()
@click.option('-o', '--output_folder', help="Output folder (this will be created if it doesn't exist)")
@click.option('-s', '--sub_datetime_folder', help="Put automatic datetime sub-folder in Output folder [HighSpeedDatalogv2 Only] (this will be created if it doesn't exist)", type=bool, default=True)
@click.option('-an','--acq_name', help="Acquisition name", type=str)
@click.option('-ad','--acq_desc', help="Acquisition description", type=str)
@click.option('-f', '--file_config', help="Device configuration file (JSON)", default='')
@click.option('-u', '--ucf_file', help="UCF Configuration file for MLC or ISPU", default='')
@click.option('-iof', '--ispu_out_fmt', help="ISPU output format descrition json. If passed, this json will be saved in acquisition folder", default='')
@click.option('-t', '--time_sec', help="Duration of the current acquisition [seconds]", callback=validate_duration, type=int, default=-1)
@click.option('-i', '--interactive_mode', help="Interactive mode. It allows to select a connected device, get info and start the acquisition process",  is_flag=True, default=False)
@click.version_option(script_version, '-v', '--version', prog_name="stdatalog_TUI", is_flag=True, help="stdatalog_TUI tool version number")
@click.option("-h", "--help", is_flag=True, is_eager=True, expose_value=False, callback=show_help, help="Show this message and exit.",)

def hsd_TUI(output_folder, sub_datetime_folder, acq_name, acq_desc, file_config, ucf_file, ispu_out_fmt, time_sec, interactive_mode):
    last_scene = None

    tui_flags = HSDInfo.TUIFlags(output_folder, sub_datetime_folder, acq_name, acq_desc, file_config, ucf_file, ispu_out_fmt, time_sec, interactive_mode)
    hsd_info = HSDInfo(tui_flags)

    while True:
        try:
            Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene, hsd_info])
            
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene

def demo(screen, scene, hsd_info):    
    if hsd_info.tui_flags.interactive_mode or len(hsd_info.device_list) == 0:
        scenes = [
            Scene([HSDMainView(screen, hsd_info)], -1, name="Main"),
            Scene([HSDLoggingView(screen, hsd_info)], -1, name="Logger")
        ]
    else:
        hsd_info.selected_device_id = 0
        scenes = [      
            Scene([HSDLoggingView(screen, hsd_info)], -1, name="Logger")
        ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

if __name__ == '__main__':
    hsd_TUI()