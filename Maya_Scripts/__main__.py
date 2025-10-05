import maya.cmds as mc
from .mtouExporter import mtouExporterUI

def run_mtou(*args):
    ''' Load Maya to Unreal Exporter UI and dependant modules. '''
    print('Run mtou module')
    
    mtouExporterUI()
    
if mc.menu('UExporterMenu', exists = True):
    mc.deleteUI('UExporterMenu', menu = True)

main_menu = mc.menu('UExporterMenu', label = 'Exporter Tools', parent = 'MayaWindow', tearOff = True)

mc.menuItem(label='MayaToUnreal', command = run_mtou, parent = main_menu)

