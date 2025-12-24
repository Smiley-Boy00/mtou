import maya.cmds as mc
import maya.api.OpenMaya as om
import importlib
import runpy
import sys
import os 

def maya_useNewAPI():
    """
    Internal function: tells Maya that the plugin data and
    objects are created using the Maya Python API 2.0.
    """
    pass

# provide specific plugin functions to run internal mel commands 
def initializePlugin(pluginObject):
    ''' Initializes OpenMaya.MFnPlugin and passes a MObject(pluginObject) created at run time. '''
    plugin_data=om.MFnPlugin(pluginObject, 'Smiley', '0.3.0 ALPHA' , 'Any')
    
    # load the plugin path, find and append the 'Maya_Scripts' as active scripts directory
    plugin_path=plugin_data.loadPath()

    if plugin_path not in sys.path:
        sys.path.append(plugin_path)

    print(f'Running MtoU from: {plugin_path}')
    runpy.run_module('Maya_Scripts', run_name="__main__")

def uninitializePlugin(pluginObject):
    ''' 
    Removes the MObject(pluginObject) created in the initialization. 
    Deletes Plugin Menu created in the main Maya Window.
    '''
    plugin_data=om.MFnPlugin(pluginObject)

    # load the plugin path to remove the 'Maya_Scripts' from active scripts directory
    plugin_path=plugin_data.loadPath()
    scripts_path = os.path.join(plugin_path, 'Maya_Scripts')
    if plugin_path not in sys.path:
        sys.path.remove(plugin_path)

    if mc.menu('UExporterMenu', exists = True):
        mc.deleteUI('UExporterMenu', menu = True)
