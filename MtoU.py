import maya.cmds as mc
import maya.api.OpenMaya as om
import importlib
import sys
from os import path

LOADER=importlib.abc.Loader()
SCRIPTS_DIR=None

def maya_useNewAPI():
    """
    Internal function: tells Maya that the plugin produces and
    objects are created using the Maya Python API 2.0.
    """
    pass

# provide specific plugin functions to run internal mel commands 
def initializePlugin(pluginObject):
    ''' Initializes OpenMaya.MFnPlugin and passes a MObject(pluginObject) created at run time. '''
    plugin_data=om.MFnPlugin(pluginObject, 'Smiley', '0.1.0' , 'Any')
    
    # load the plugin path, find and append the 'Maya_Scripts' as active scripts directory
    plugin_path=plugin_data.loadPath()
    SCRIPTS_DIR = path.join(plugin_path, 'Maya_Scripts')
    if SCRIPTS_DIR not in sys.path:
        sys.path.append(SCRIPTS_DIR)

    print(f'Running MtoU from: {plugin_path}')
    print(SCRIPTS_DIR)
    create_menu()


def create_menu():
    ''' Creates Plugin Menu parented to the main Maya Window (Top Section). '''
    if mc.menu('UExporterMenu', exists = True):
        mc.deleteUI('UExporterMenu', menu = True)

    main_menu = mc.menu('UExporterMenu', label = 'Exporter Tools', parent = 'MayaWindow', tearOff = True)

    mc.menuItem(label='MayaToUnreal', command = run_mtou, parent = main_menu)

def run_mtou(*args):
    ''' Load Maya to Unreal Exporter UI and dependant modules. '''
    print('Run mtou module')
    # exporter module can only be loaded after obtaining active scripts directory 
    import mtouExporter # noqa: E402 
    
    importlib.reload(mtouExporter)
    mtouExporter.mtouExporterUI()

def uninitializePlugin(pluginObject):
    ''' 
    Removes the MObject(pluginObject) created in the initialization. 
    Deletes Plugin Menu created in the main Maya Window.
    '''
    plugin_data=om.MFnPlugin(pluginObject)

    # load the plugin path to remove the 'Maya_Scripts' from active scripts directory
    plugin_path=plugin_data.loadPath()
    scripts_dir = path.join(plugin_path, 'Maya_Scripts')
    if scripts_dir not in sys.path:
        sys.path.remove(scripts_dir)

    if mc.menu('SmileyMenu', exists = True):
        mc.deleteUI('SmileyMenu', menu = True)
