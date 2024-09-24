## Initializations ##

import ipywidgets as w
from ipywidgets import interactive, interact_manual
from IPython.display import display, clear_output

from ipyfilechooser import FileChooser
#from ipyvuetify.extra import FileInput
import hashlib
import datetime as dt
import sys

import modules.run_Mapper as Mapper

## Global Variables ##

platform_global = w.Text(value = "PALSAR-2")
scan_mode_global = w.Text("dsc")
band_global = w.IntText(value = 6)

studyarea_name_global = w.Text(value = 'DosHermanas_TalisayCity')
croptype_global = w.Text(value = 'sugarcane')
sample_shp_global =  w.Text(value = 'shp/DosHermanas_TalisayCity_Negros_SRA_Sugarcane_Parcel_Sample.shp')
studyarea_shp_global =  w.Text(value = 'shp/DosHermanas_TalisayCity_Negros.shp')
# reference_directory_global =  w.Text(value = 'C:\\Users\\Altansarnai\\code\\asti-new\\asti\\alam-cropmapper\\img_data\\palsar2_talisay_test_2018')
# test_directory_global =  w.Text(value = 'C:\\Users\\Altansarnai\\code\\asti-new\\asti\\alam-cropmapper\\img_data\\palsar2_talisay_test_2018')
reference_directory_global =  w.Text(value = 'img_data/palsar2_talisay_test_2018')
test_directory_global =  w.Text(value = 'img_data/palsar2_talisay_test_2018')
crop_reference_startDate_global = w.Text(value = "2018/01/01")
crop_reference_endDate_global = w.Text(value = "2018/12/31")
test_data_startDate_global = w.Text(value = "2018/01/01")
test_data_endDate_global = w.Text(value = "2018/12/31")

dtw_window_size_global = w.IntText(value = 3)
dtw_psi_global = w.IntText(value = 2)
dtw_use_pruning_global = w.Text(value = "True")
dtw_use_C_global = w.Text(value = "False")

#### Function for sending the list for returning these variables to its main module ####
def retrieve_global_var_dict():
    global_var_dict = {'platform' : platform_global.value,
                   'scan_mode' : scan_mode_global.value,
                   'band' : band_global.value,
                   'studyarea_name' : studyarea_name_global.value,
                   'croptype' : croptype_global.value,
                   'sample_shp' : sample_shp_global.value,
                   'studyarea_shp': studyarea_shp_global.value,
                   'reference_directory' : reference_directory_global.value,
                   'test_directory' : test_directory_global.value,
                   'crop_reference_startDate' : crop_reference_startDate_global.value,
                   'crop_reference_endDate' : crop_reference_endDate_global.value,
                   'test_data_startDate' : test_data_startDate_global.value,
                   'test_data_endDate' : test_data_endDate_global.value,
                   'dtw_window_size' : dtw_window_size_global.value,
                   'dtw_psi' : dtw_psi_global.value,
                   'dtw_use_pruning' : dtw_use_pruning_global.value,
                   'dtw_use_C' : dtw_use_C_global.value}
    return global_var_dict

def retrieve_global_var_list():
    global_var_list = [platform_global.value,
                       scan_mode_global.value,
                       band_global.value,
                       studyarea_name_global.value,
                       croptype_global.value,
                       sample_shp_global.value,
                       studyarea_shp_global.value,
                       reference_directory_global.value,
                       test_directory_global.value,
                       crop_reference_startDate_global.value,
                       crop_reference_endDate_global.value,
                       test_data_startDate_global.value,
                       test_data_endDate_global.value,
                       dtw_window_size_global.value,
                       dtw_psi_global.value,
                       dtw_use_pruning_global.value,
                       dtw_use_C_global.value]
    return global_var_list

## Widget development ##

# Loggers to check cross-cell event handling
logger_Widget = w.Output(
    layout={'border': '3px solid black'},
    label='Choices:')

progress_Widget = w.Output(
    layout={'border': '3px solid green'},
    label='Choices:')

def init_logger_Widget():
    with logger_Widget:
        clear_output()
        print("Changes made appear here.")
        
def init_progress_Widget():
    with progress_Widget:
        clear_output()
        print("Run progress appears here.")

def init_status_Widget(w):
    with w:
        clear_output()
        print("Default value loaded.")
        
def call_logger_Widget(fnc, change):
    with logger_Widget:
        clear_output()
        print("%s logged change: %s" % (fnc, change))

def call_progress_Widget(fnc, change):
    with progress_Widget:
        clear_output()
        print("%s logged change: %s" % (fnc, change))

def call_status_Widget(w, change):
    with w:
        clear_output()
        if change == True:
            print("New input recorded!")
        else:
            print("No new input recorded - default value remains.")
        
#### Study metadata ####
def on_studyareanameRetype(change):
    if change['type'] == 'change' and change['name'] == 'value':
        studyarea_name_global.value = change.new
        call_logger_Widget(sys._getframe().f_code.co_name, change['new'])
studyarea_name_global.observe(on_studyareanameRetype)
def on_croptypeRetype(change):
    if change['type'] == 'change' and change['name'] == 'value':
        croptype_global.value = change.new
        call_logger_Widget(sys._getframe().f_code.co_name, change['new'])
croptype_global.observe(on_croptypeRetype)
        
### Platform-specific parameters ###
#### Platform scan mode and band selections ####
def on_scanmodeSelect(change):
    if change['type'] == 'change' and change['name'] == 'value':
        scan_mode_global.value = change.new
        #print("Scan mode: %s" %scan_mode_global)
        call_logger_Widget(sys._getframe().f_code.co_name, change['new'])
              
def on_bandSelect(change):
    if change['type'] == 'change' and change['name'] == 'value':
        band_global.value = change.new
        #print("Band: %s" %band_global)
        call_logger_Widget(sys._getframe().f_code.co_name, change['new'])

# Sentinel-1 parameters

scan_mode_s1 = w.Dropdown(
    description="S1 Scan Mode",
    options=['dsc', 'asc'], #  "dsc" for descending orbit, "asc" for ascending orbit (not recommended - mission is short)
    value='dsc')
scan_mode_s1.observe(on_scanmodeSelect, 'value')

band_s1 = w.Dropdown(
    description="S1 Band",
    options=['1', '2'], # 1 = VV, 2 = VH (recommended)
    value='2')
band_s1.observe(on_bandSelect, 'value')

s1_mode_vBox = w.VBox([
        w.HTML(
            value="<i>S1 scan mode ('dsc' recommended):</i>"
        ),
        scan_mode_s1,
        w.HTML(
            value="<i>S1 band ('2' recommended):</i>"
        ),
        band_s1
        ])

#PALSAR-2 parameters

scan_mode_p2 = w.Dropdown(
    description="P2 Scan Mode",
    options=['dsc', 'asc'], #  "dsc" for descending orbit, "asc" for ascending orbit (not recommended - mission is short)
    value='dsc')
scan_mode_p2.observe(on_scanmodeSelect)

band_p2 = w.Dropdown(
    description="P2 Band",
    options=['5', '6'], # 5 = HH_dB, 6 = HV_dB (recommended)
    value='6')
band_p2.observe(on_bandSelect)

p2_mode_vBox = w.VBox([
        w.HTML(
            value="<i>P2 scan mode ('dsc' recommended):</i>"
        ),
        scan_mode_p2,
        w.HTML(
            value="<i>S1 band ('6' recommended):</i>"
        ),
        band_p2
        ])

# Event handling for selecting platform
platformSelect = w.Dropdown(
    options=['Sentinel-1', 'PALSAR-2'],
    value='PALSAR-2',
    description='Platform:',
)

platformSpecs = w.Output(
    layout={'border': '1px solid black'},
    label='Choices:')

def on_platformSelect(change):
    with platformSpecs:
        if change['type'] == 'change' and change['name'] == 'value':
            newval = "%s" % change['new']
            call_logger_Widget(sys._getframe().f_code.co_name, change['new'])
            # print("Platform: %s" % newval)
            if newval == 'Sentinel-1':
                platform_global.value = newval
                clear_output()
                display(s1_mode_vBox)
            elif newval == 'PALSAR-2':
                platform_global.value = newval
                clear_output()
                display(p2_mode_vBox)
            else:
                clear_output()
                print(newval)

platformSelect.observe(on_platformSelect)

#### Vector choosers ####
sample_shp_chooser = FileChooser('shp')
sample_shp_chooser.sandbox_path='shp'
sample_shp_chooser.filter_pattern = "*.shp"
sample_shp_chooser.default_filename = 'DosHermanas_TalisayCity_Negros_SRA_Sugarcane_Parcel_Sample.shp'

sample_shp_status_Widget = w.Output(
    layout={'border': '3px solid red'},
    label='Default value loaded.')
studyarea_shp_status_Widget = w.Output(
    layout={'border': '3px solid red'},
    label='Default value loaded.')

def getSampleSHP(chooser):
    if chooser != None:
        sample_shp_global.value = chooser
        call_logger_Widget(sys._getframe().f_code.co_name, chooser)
        call_status_Widget(sample_shp_status_Widget, True)
    else:
        call_status_Widget(sample_shp_status_Widget, False)

sample_shp_interactive = interactive(getSampleSHP, {'manual': True, "manual_name": "Get Sample SHP"},
                                chooser = sample_shp_chooser)
sample_shp_chooser
studyarea_shp_chooser = FileChooser('shp')
studyarea_shp_chooser.sandbox_path='shp'
studyarea_shp_chooser.filter_pattern = "*.shp"
studyarea_shp_chooser.default_filename = 'DosHermanas_TalisayCity_Negros.shp'

def getStudyareaSHP(chooser):
    if chooser != None:
        studyarea_shp_global.value = chooser
        call_logger_Widget(sys._getframe().f_code.co_name, chooser)
        call_status_Widget(studyarea_shp_status_Widget, True)
    else:
        call_status_Widget(studyarea_shp_status_Widget, False)

studyarea_shp_interactive = interactive(getStudyareaSHP, {'manual': True, "manual_name": "Get Study Area SHP"},
                                chooser = studyarea_shp_chooser)

vectorChooser_vBox = w.VBox([
    w.HTML(
            value="<b>Sample Parcel Browser</b>"
        ),
    w.HTML(
            value="<i>Find sample shapefile for reference temporal signature generation</i>"
        ),
    sample_shp_status_Widget,
    sample_shp_interactive,

        
    w.HTML(
            value="<b>Study Area Browser</b>"
        ),
    w.HTML(
            value="<i>Find study area boundary shapefile</i>"
        ),
    studyarea_shp_status_Widget,
    studyarea_shp_interactive
])

#### Platform vBox assembly
platform_vBox = w.VBox([
        w.HTML(
            value="<b>Platform Selection</b>"
        ),
        w.HTML(
            value="<i>Choose between Sentinel-1 and PALSAR-2</i>"
        ),
        platformSelect,
        w.HTML(
            value="<b>Platform Specifications (Pops After Above Selection)</b>"
        ),
        platformSpecs,
        vectorChooser_vBox,
        ])

### Time-series Catalog Parameters ###
#### Raster directory choosers ####
reference_path_status_Widget = w.Output(
    layout={'border': '3px solid red'},
    label='Default value loaded.')
test_path_status_Widget = w.Output(
    layout={'border': '3px solid red'},
    label='Default value loaded.')

### Reference directory chooser ###
reference_directory_chooser = FileChooser('img_data')
reference_directory_chooser.sandbox_path='img_data'
reference_directory_chooser.show_only_dirs = True
reference_directory_chooser.default_path=r'img_data/palsar2_talisay_test_2018'

def getReferencePath(chooser):
    if chooser != None:
        reference_directory_global.value = chooser
        call_logger_Widget(sys._getframe().f_code.co_name, chooser)
        call_status_Widget(reference_path_status_Widget, True)
    else:
        call_status_Widget(reference_path_status_Widget, False)

reference_directory_interactive = interactive(getReferencePath, {'manual': True, "manual_name": "Get Reference Directory"},
                                chooser = reference_directory_chooser)

### Test directory chooser ###
test_directory_chooser = FileChooser('img_data')
test_directory_chooser.sandbox_path='img_data'
test_directory_chooser.show_only_dirs = True
test_directory_chooser.default_path=r"img_data/palsar2_talisay_test_2018"

def getTestPath(chooser):
    if chooser != None:
        test_directory_global.value = chooser
        call_logger_Widget(sys._getframe().f_code.co_name, chooser)
        call_status_Widget(test_path_status_Widget, True)
    else:
        call_status_Widget(test_path_status_Widget, False)

test_directory_interactive = interactive(getTestPath, {'manual': True, "manual_name": "Get Test Directory"},
                                chooser = test_directory_chooser)

#### Date configuration pickers ####
crop_reference_startDate = w.DatePicker(
    description='Start Date:',
    value = dt.date(2018,1,1)
    )

def on_referencestartDateSelect(change):
    if change['type'] == 'change' and change['name'] == 'value':
        crop_reference_startDate_global.value = "%s" % change.new
        call_logger_Widget(sys._getframe().f_code.co_name, change['new'])
        
crop_reference_startDate.observe(on_referencestartDateSelect)


crop_reference_endDate = w.DatePicker(
    description='End Date:',
    value = dt.date(2018,12,31)
    )

def on_referenceendDateSelect(change):
    if change['type'] == 'change' and change['name'] == 'value':
        crop_reference_endDate_global.value = "%s" % change.new
        call_logger_Widget(sys._getframe().f_code.co_name, change['new'])
        
crop_reference_endDate.observe(on_referenceendDateSelect)

ref_vBox = w.VBox([crop_reference_startDate,
                   crop_reference_endDate,
                   w.HTML(
                       value="<b>Browse for reference dataset directory:</b>"
                   ),
                   reference_path_status_Widget,
                   reference_directory_interactive])

test_data_startDate = w.DatePicker(
    description='Start Date:',
    value = dt.date(2018,1,1)
    )

def on_teststartDateSelect(change):
    if change['type'] == 'change' and change['name'] == 'value':
        test_data_startDate_global.value = "%s" % change.new
        call_logger_Widget(sys._getframe().f_code.co_name, change['new'])

test_data_startDate.observe(on_teststartDateSelect)

test_data_endDate = w.DatePicker(
    description='End Date:',
    value = dt.date(2018,12,31)
    )

def on_testendDateSelect(change):
    if change['type'] == 'change' and change['name'] == 'value':
        test_data_endDate_global.value = "%s" % change.new
        call_logger_Widget(sys._getframe().f_code.co_name, change['new'])

test_data_endDate.observe(on_testendDateSelect)

test_vBox = w.VBox([test_data_startDate,
                    test_data_endDate,
                    w.HTML(
                       value="<b>Browse for test dataset directory:</b>"
                    ),
                    test_path_status_Widget,
                    test_directory_interactive])

#### Time-series catalog tab assembly ####
reftest_tab_contents = [ref_vBox, test_vBox] 

reftest_tab = w.Tab()
reftest_tab.children = reftest_tab_contents
reftest_tab.titles = ["Reference Dataset", "Test Dataset"]

### DTW parameter configurations ###

# dtw_window_size_global = ""
# dtw_psi_global = ""
# dtw_use_pruning_global = True
# dtw_use_C_global = False


dtw_label = w.HTML(
    value="<b>DTW Parameter Configurations</b>"
    )

dtw_window_size = w.Text(
    clearable=False,
    description="Window Size ('3' recommended):",
    value='3')

def on_dtwwindowsizeSelect(change):
    if change['type'] == 'change' and change['name'] == 'value':
        dtw_window_size_global.value = "%s" % change.new
        call_logger_Widget(sys._getframe().f_code.co_name, change['new'])

dtw_window_size.observe(on_dtwwindowsizeSelect)        
        
dtw_psi = w.Text(
    clearable=False,
    description="Psi ('2' recommended):",
    value='2')

def on_dtwpsiSelect(change):
    if change['type'] == 'change' and change['name'] == 'value':
        dtw_psi_global.value = "%s" % change.new
        call_logger_Widget(sys._getframe().f_code.co_name, change['new'])

dtw_psi.observe(on_dtwpsiSelect)        

dtw_use_pruning = w.Checkbox(
    clearable=False,
    description="Use Pruning ('Checked' recommended):",
    value=True)

def on_dtwusepruningSelect(change):
    if change['type'] == 'change' and change['name'] == 'value':
        dtw_use_pruning_global.value = "%s" % change.new
        call_logger_Widget(sys._getframe().f_code.co_name, change['new'])

dtw_use_pruning.observe(on_dtwusepruningSelect)

dtw_use_C = w.Checkbox(
    clearable=False,
    description="Use DTAIdistance C-based functions ('Unchecked' recommended):",
    value=False)

def on_dtwuseCSelect(change):
    if change['type'] == 'change' and change['name'] == 'value':
        dtw_use_C_global.value = "%s" % change.new
        call_logger_Widget(sys._getframe().f_code.co_name, change['new'])

dtw_use_C.observe(on_dtwuseCSelect)

dtw_vBox = w.VBox([dtw_label, dtw_window_size, dtw_psi, dtw_use_pruning, dtw_use_C])

### The Run! button widget ###
def on_runButtonWidgetClick(b):
    global_var_dict = retrieve_global_var_dict()
    with progress_Widget:
        clear_output()
        mapper = Mapper
        mapper.get_global_var_dict(global_var_dict)
        mapper.run_Mapper()    

run_button_Widget = w.Button(
    description = "Run Mapper!",
    tooltip = "Runs the mapper code after everything is configured"
    )

run_button_Widget.on_click(on_runButtonWidgetClick)

### The BIG assembly part ###
init_logger_Widget()
init_progress_Widget()
init_status_Widget(sample_shp_status_Widget)
init_status_Widget(studyarea_shp_status_Widget)
init_status_Widget(reference_path_status_Widget)
init_status_Widget(test_path_status_Widget)

inputParams_leftvBox = w.VBox([
        w.HBox([
            w.HTML(
            value="<b>Study Area Name For Filename Appending: </b>"
            ),
        studyarea_name_global,
        ]),
        w.HBox([
            w.HTML(
            value="<b>Crop Type For Filename Appending: </b>"
            ),
        croptype_global,
        ]),
        platform_vBox,
        dtw_vBox
    ])
inputParams_rightvBox = w.VBox([
        reftest_tab
    ])
inputParams_hBox = w.HBox([
        inputParams_leftvBox,
        inputParams_rightvBox,
    ])

inputParams_logger = w.VBox([
        inputParams_hBox,
        w.HTML(
            value="<b>Interactivity Logger</b>"
        ),
        logger_Widget,
        w.HTML(
            value="<b>Run Mapper</b>"
        ),
        run_button_Widget,
        progress_Widget
    ])


#### Function to call the inputParams_logger UI ####
def callUI():
    display(inputParams_logger)