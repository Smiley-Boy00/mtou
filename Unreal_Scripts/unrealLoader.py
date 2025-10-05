# import modules
from pathlib import Path
import unreal
import json
import os

unreal.log('MtoULoader module')

class UnrealLoader:
    ''' Obtain and store the directory of the currently running UE Project. '''
    def __init__(self) -> None:
        # get the path directory of the currently running unreal engine project
        self._project_dir = unreal.Paths.project_dir()
        # get the absolute path of the UE path directory
        self._full_path = os.path.abspath(self._project_dir)
        # save the absolute path into a dictionary
        self._ue_dict = {'Current Project' : self._full_path.replace('\\', '/')}
        # find the user's home directory & documents folder 
        self._documents_path = os.path.join(str(Path.home()), 'Documents')

    def get_project_path_data(self) -> dict:
        ''' Return current UE project path data set. '''
        return self._ue_dict

    def get_documents_path(self) -> str:
        ''' Return User document path string from home directory. '''
        return self._documents_path

    def save_path_to_json(self) -> None:
        ''' Store current UE project path data set (JSON) into an absolute path in home directory.'''
        # create a fixed directory in the user's documents folder
        stored_data_dir = os.path.join(self._documents_path,'UE','Data')
        # check if the path exists, if it doesn't exists create it
        if not os.path.exists(stored_data_dir):
            os.makedirs(stored_data_dir)
        # log the currently running UE project to view it in the output log inside Unreal
        unreal.log(self._ue_dict)
        directory = os.path.join(f'{stored_data_dir}', 'ue_path.json')
        # save the UE path dictionary data into a JSON in the specified directory
        with open(os.path.join(directory), 'w') as file:
            json.dump(self._ue_dict, file, indent=4, sort_keys=True)
        unreal.log(f'Project Path Directory stored in: {directory}')

# add comments to function
def import_asset_type():
    ''' 
    Automate import based on the asset type import data set.
    Task is managed by the active Interchange Manager.
    '''
    # get unreal's Interchange Manager singleton
    interchange_manager=unreal.InterchangeManager.get_interchange_manager_scripted()
    asset_params=unreal.ImportAssetParameters(is_automated=True)

    # load paths to retrieve external import data set
    ue_loader = UnrealLoader()
    ue_path = ue_loader.get_project_path_data()
    ue_data = os.path.join(ue_loader.get_documents_path(),'UE','Data','importSettings.json')

    if os.path.exists(ue_data):
        # load import data set
        with open(ue_data, 'r') as file:
            import_data = json.load(file)

        # load generic pipelines for public property overrides
        generic_pipeline=unreal.InterchangeGenericAssetsPipeline()
        generic_mat_pipeline=generic_pipeline.material_pipeline
        generic_tex_pipeline=generic_mat_pipeline.texture_pipeline

        # dynamic data sorter and handler based on asset type # work in progress
        for importer in import_data:
            if importer=='OBJ':
                import_settings=import_data['OBJ']
                
            elif importer=='FBX':
                import_settings=import_data['FBX']

        # load and store import settings data values
        folder_path=import_settings['Folder Path'].replace('\\', '/')
        file_name=import_settings['File Name']
        imp_materials=import_settings['Import Materials']
        imp_textures=import_settings['Import Textures']
        use_source_name=import_settings['Use Source Name']

        # store full file path using the current UE project 
        asset_file_path = os.path.join(ue_path['Current Project'], 'Content', folder_path, file_name)
        # store destination path in unreal's Content Browser
        destination_path = f"/Game/{folder_path}"

        # create source data from stored file path
        source_data=interchange_manager.create_source_data(asset_file_path)

        # evaluate if assets names will be set by file name or source file data name 
        generic_pipeline.use_source_name_for_asset=use_source_name
        # set import materials bool property based on import data set value
        generic_mat_pipeline.import_materials=imp_materials
        # set import textures bool property based on import data set value
        generic_tex_pipeline.import_textures=imp_textures
        generic_tex_pipeline.allow_non_power_of_two=True

        # use Interchange Import Data for setting generic and specialized asset pipelines
        asset_import_data=unreal.InterchangeAssetImportData()
        asset_import_data.set_pipelines([generic_pipeline,
                                        generic_mat_pipeline,
                                        generic_tex_pipeline]) # pyright: ignore[reportArgumentType] 

        # override Interchange default import asset parameters, parsing through loaded pipelines 
        asset_params.override_pipelines=asset_import_data.get_pipelines()

        # execute custom import 
        interchange_manager.import_asset(destination_path, source_data,
                                        asset_params)
    
    else:
        unreal.log_warning('unrealLoader.py: Custom Import Settings data set has not been generated or cannot be located.')

def run_loader():
    ue_loader = UnrealLoader()
    ue_loader.save_path_to_json()

def create_loader_toolbar():

    # Create a new toolbar section
    toolbar_name = "Unreal Import"
    section_name = "UnrealImportSection"

    # Register the toolbar
    menus = unreal.ToolMenus.get()
    toolbar = menus.find_menu("LevelEditor.LevelEditorToolBar.User")

    if toolbar:
        toolbar.add_section(section_name, label=toolbar_name)

        # Add import asset button entry
        entryImport = unreal.ToolMenuEntry(
            name="ImportAssetsWithSettings",
            type=unreal.MultiBlockType.TOOL_BAR_BUTTON
        )
        entryImport.set_label("Import Assets")
        entryImport.set_tool_tip("Imports Assets using external settings")
        entryImport.set_icon("EditorStyle", "Profiler.Tab.FiltersAndPresets") # Use any existing icon

        # Set the action
        entryImport.set_string_command(
            type=unreal.ToolMenuStringCommandType.PYTHON,
            custom_type="",
            string="import unrealLoader; unrealLoader.import_asset_type()"  # Python function
        )
        
        toolbar.add_menu_entry("ImportAssetsWithSettings", entryImport)

        # Add reload button entry
        entryStore = unreal.ToolMenuEntry(
            name="StoreCurrentProjectPath",
            type=unreal.MultiBlockType.TOOL_BAR_BUTTON
        )
        entryStore.set_label("Store Project Path")
        entryStore.set_tool_tip("Save current project path for MtoU Exporter")
        entryStore.set_icon("EditorStyle", "GenericCommands.Redo")  # Use any existing icon
    
        # Set the action
        entryStore.set_string_command(
            type=unreal.ToolMenuStringCommandType.PYTHON,
            custom_type="",
            string="import unrealLoader; unrealLoader.run_loader()"  # Python function
        )
        
        toolbar.add_menu_entry("StoreCurrentProjectPath", entryStore)

        # Refresh the toolbar
        menus.refresh_all_widgets()

if __name__=="__main__":
    run_loader()

create_loader_toolbar()

