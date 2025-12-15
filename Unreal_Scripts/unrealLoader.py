# import modules
from pathlib import Path
import unreal
import json
import os

unreal.log('unrealLoader.py: Scripts & Modules Initialized.')

class UnrealLoader:
    '''
    Class to handle Unreal Engine project paths & asset data. 
    Obtains the directory of the currently running UE Project. 
    '''
    def __init__(self) -> None:
        # get the path directory of the currently running unreal engine project
        self._project_dir = unreal.Paths.project_dir()
        # get the absolute path of the UE path directory
        self._full_path = os.path.abspath(self._project_dir)
        # save the absolute path into a dictionary
        self._ue_dict = {'Current Project' : self._full_path.replace('\\', '/')}
        # find the user's home directory & documents folder 
        self._documents_path = os.path.join(str(Path.home()), 'Documents')
        # create a fixed directory in the user's documents folder
        self._data_path = os.path.join(self._documents_path,'UE','Data')
        # get unreal's Asset Registry singleton
        self._asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

    def get_project_path_data(self) -> dict:
        ''' Returns current UE project path data set. '''
        return self._ue_dict

    def get_documents_path(self) -> str:
        ''' Returns user's documents path from system's home directory. '''
        return self._documents_path

    def save_path_to_json(self) -> None:
        ''' Store current UE project path data set (JSON) into an absolute path in home directory.'''
        # check if the path exists, if it doesn't exists create it
        if not os.path.exists(self._data_path):
            os.makedirs(self._data_path)
        # log the currently running UE project to view it in the output log inside Unreal
        unreal.log(self._ue_dict)
        # store the current UE project path to ue data set
        self.save_data(self._data_path, 'ue_data.json', self._ue_dict)

    def save_skeletons_to_json(self) -> None:
        ''' Store all skeleton assets found in the project into the project's data (JSON) file. '''
        # create a filter to search only within the content directory 
        asset_filter = unreal.ARFilter(class_paths=[unreal.TopLevelAssetPath("/Script/Engine", "Skeleton")], # type: ignore
                                       package_paths=["/Game"], recursive_paths=True) 
        
        # get all skeleton assets in the project
        skeleton_asset_data = self._asset_registry.get_assets(asset_filter)
        
        skeleton_assets = {}
        # get and store skeleton asset names with their full package paths
        for asset_data in skeleton_asset_data:
            asset = asset_data.get_asset()
            asset_full_path = asset_data.package_name
            asset_name = asset.get_name()
            skeleton_assets[asset_name] = str(asset_full_path)      
            
        if skeleton_assets:
            # load ue data set
            data_file = os.path.join(self._data_path, 'ue_data.json')
            with open(data_file, 'r') as file:
                ue_data = json.load(file)
            for skeleton in skeleton_assets:
                unreal.log(f'Saving Skeleton: {skeleton}')
            # assign assets to skeletons data
            ue_data['Skeletons'] = skeleton_assets
            # store skeleton assets into the ue data set
            self.save_data(self._data_path, 'ue_data.json', ue_data)

    def get_folder_assets(self, folder_path:str) -> list:
        ''' Returns a list of asset data inside the provided folder path. '''
        data_list = self._asset_registry.get_assets_by_path(folder_path, recursive=True)
        return data_list

    def save_data(self, path:str, file_name:str, data) -> None:
        ''' Saves data into a json file: must include a path to store data. '''
        if not file_name.endswith('.json'):
            file_name+='.json'

        with open(os.path.join(path, file_name), 'w') as file:
            json.dump(data, file, indent=4, sort_keys=True)

def import_asset_type():
    ''' 
    Automates import based on the asset type import data set.
    Task is managed by the active Interchange Manager.
    '''
    # get unreal's Interchange Manager singleton
    interchange_manager=unreal.InterchangeManager.get_interchange_manager_scripted()
    # load Import Asset Parameters; enable automated and headless import
    asset_params=unreal.ImportAssetParameters(is_automated=True)

    # load paths to retrieve external import data set
    ue_loader = UnrealLoader()
    ue_path = ue_loader.get_project_path_data()
    data_file = os.path.join(ue_loader.get_documents_path(),'UE','Data','importSettings.json')

    if os.path.exists(data_file):
        # load import data set
        with open(data_file, 'r') as file:
            import_data = json.load(file)

        # data sorter based on asset type; work in progress
        if import_data.get('OBJ'):
            unreal.log('Importing OBJ')
            importer=import_data.get('OBJ')
            handler='OBJ'
        elif import_data.get('FBX'):
            unreal.log('Importing FBX')
            importer=import_data.get('FBX')
            handler='FBX'
        else:
            unreal.log_error('unrealLoader.py: No valid Importer Type is available.')
        
        for file in importer:
            unreal.log(file)
            # load individual import settings for file
            import_settings=importer.get(file)

            # load generic pipelines for public property overrides
            generic_pipeline=unreal.InterchangeGenericAssetsPipeline()
            generic_common_meshes=generic_pipeline.common_meshes_properties
            generic_anim_pipeline=generic_pipeline.animation_pipeline
            generic_mesh_anim_pipeline=generic_pipeline.common_skeletal_meshes_and_animations_properties
            generic_mesh_pipeline=generic_pipeline.mesh_pipeline
            generic_mat_pipeline=generic_pipeline.material_pipeline
            generic_tex_pipeline=generic_mat_pipeline.texture_pipeline

            # load and store import settings data string values
            folder_path=import_settings.get('Folder Path').replace('\\', '/')
            # store full file path using the current UE project 
            asset_file_path = os.path.join(ue_path['Current Project'], 'Content', folder_path, file)
            # store destination path in unreal's Content Browser
            destination_path = f"/Game/{folder_path}"

            # verify asset file does exists prior to import
            if os.path.exists(asset_file_path):
                # load general import settings data values
                use_source_name=import_settings.get('Use Source Name')
                imp_materials=import_settings.get('Import Materials')
                imp_textures=import_settings.get('Import Textures')
                imp_static_mesh=import_settings.get('Import Static Mesh')
                imp_skeletal_mesh=import_settings.get('Import Skeletal Mesh')
                imp_animations=import_settings.get('Import Animations')
                anim_range=import_settings.get('Animation Range')

                # create source data from stored file path
                source_data=interchange_manager.create_source_data(asset_file_path)

                # evaluate if assets names will be set by file name or source file data name 
                generic_pipeline.use_source_name_for_asset=use_source_name

                # set common mesh properties based on import data
                generic_common_meshes.auto_detect_mesh_type=True

                # set import static and skeletal mesh bool properties based on import data
                generic_mesh_pipeline.import_static_meshes=imp_static_mesh
                generic_mesh_pipeline.import_skeletal_meshes=imp_skeletal_mesh
                # evaluate if the asset's mesh contain pre-built collisions
                generic_mesh_pipeline.collision=True

                # set import materials bool property based on import data set value
                generic_mat_pipeline.import_materials=imp_materials

                # set import textures bool property based on import data set value
                generic_tex_pipeline.import_textures=imp_textures
                generic_tex_pipeline.allow_non_power_of_two=True

                if handler=='FBX':
                    # set import animations bool property based on import data set value
                    generic_anim_pipeline.import_animations=imp_animations

                    if imp_animations:
                        # set animation range or value based on import animation data
                        if anim_range:
                            generic_anim_pipeline.animation_range=unreal.InterchangeAnimationRange.SET_RANGE
                            unreal.log(generic_anim_pipeline.animation_range)
                            start_range=anim_range[0]
                            end_range=anim_range[1]
                            # convert and set animation integer range to unreal Int32Interval
                            unreal_range=unreal.Int32Interval()
                            unreal_range.min=start_range
                            unreal_range.max=end_range
                            generic_anim_pipeline.frame_import_range=unreal_range
                        else:
                            # import entire timeline 
                            generic_anim_pipeline.animation_range=unreal.InterchangeAnimationRange.TIMELINE
                            unreal.log(generic_anim_pipeline.animation_range)
                        # set common skeletal mesh and anim configurations based on import data
                        generic_mesh_anim_pipeline.import_only_animations=import_settings.get('Import Only Animations') 
                    generic_mesh_anim_pipeline.import_meshes_in_bone_hierarchy=import_settings.get('Meshes in Bone Hierarchy')

                    skeleton_data=import_settings.get('Skeleton')
                    if not skeleton_data:
                        # if set, disable importing animations if no skeleton asset is found
                        generic_mesh_anim_pipeline.import_only_animations=False
                        skeleton_asset=None
                    else:
                        skeleton_asset = unreal.load_asset(skeleton_data)
                        # error handling for invalid skeleton asset
                        if not skeleton_asset:
                            unreal.log_warning(f'unrealLoader.py: Skeleton asset {skeleton_data} cannot be loaded, make sure skeleton asset is valid.')
                            skeleton_asset=None
                    # assign existing skeleton asset to newly imported skeletal meshes & animations
                    generic_mesh_anim_pipeline.skeleton=skeleton_asset

                if import_settings.get('Force Mesh Type'):
                    # sort and set force mesh type property based on import data
                    force_mesh_type=import_settings.get('Force Mesh Type')
                    if force_mesh_type==0:
                        generic_common_meshes.force_all_mesh_as_type=unreal.InterchangeForceMeshType.IFMT_NONE
                    elif force_mesh_type==1:
                        generic_common_meshes.force_all_mesh_as_type=unreal.InterchangeForceMeshType.IFMT_STATIC_MESH
                    elif force_mesh_type==2:
                        generic_common_meshes.force_all_mesh_as_type=unreal.InterchangeForceMeshType.IFMT_SKELETAL_MESH

                # apply the same pipeline properties on reimport unless import data changes
                generic_pipeline.reimport_strategy=unreal.ReimportStrategyFlags.APPLY_PIPELINE_PROPERTIES
                unreal.log(generic_pipeline.reimport_strategy)

                # use Interchange Import Data for setting generic and specialized asset pipelines
                asset_import_data=unreal.InterchangeAssetImportData()
                asset_import_data.set_pipelines([generic_pipeline,
                                                 generic_mesh_anim_pipeline,
                                                 generic_common_meshes,
                                                 generic_mat_pipeline,
                                                 generic_tex_pipeline,]) # pyright: ignore[reportArgumentType] 

                # override Interchange default import asset parameters, parsing through loaded pipelines 
                asset_params.override_pipelines=asset_import_data.get_pipelines()

                # execute custom import 
                interchange_manager.import_asset(destination_path, source_data,
                                                asset_params)
            
                ue_loader.save_skeletons_to_json()

            else:
                unreal.log_warning(f'unrealLoader.py: {asset_file_path} cannot be located, make sure asset file path exists or is valid.')

    else:
        unreal.log_warning('unrealLoader.py: Custom Import settings data set has not been generated or cannot be located.')

def create_imported_asset_data(ue_loader:UnrealLoader, folder_path:str):
    ''' 
    Creates a list of imported asset names from the provided folder path.
    Requires an instance of UnrealLoader class. 
    '''
    data_list = ue_loader.get_folder_assets(folder_path)

    imported_assets = []

    for asset_data in data_list:
        asset = asset_data.get_asset()
        asset_name = asset.get_name()
        imported_assets.append(asset_name)

    return imported_assets

def fix_name_import_handling(ue_loader:UnrealLoader, folder_path:str, substring:str):
    '''
    Fixes imported asset names by removing a specific substring from the asset names.
    Requires an instance of UnrealLoader class. 
    '''
    asset_tool=unreal.AssetToolsHelpers.get_asset_tools()
    data_list = ue_loader.get_folder_assets(folder_path)

    rename_data = []

    for asset_data in data_list:
        asset = asset_data.get_asset()
        asset_name = asset.get_name()

        if substring not in asset_name:
            continue
        new_asset_name = asset_name.replace(substring, "")

        package_path = str(asset_data.package_path)
        unreal.log(new_asset_name)
        unreal.log(package_path)

        rename_data.append(unreal.AssetRenameData(asset, package_path, new_asset_name))

    if rename_data:
        asset_tool.rename_assets(rename_data)

def run_loader():
    ''' Runs the main UnrealLoader functions to store project data: path and skeletons. '''
    ue_loader = UnrealLoader()
    ue_loader.save_path_to_json()
    ue_loader.save_skeletons_to_json()

def create_loader_toolbar():
    ''' Creates a custom toolbar in the Level Editor for the main UnrealLoader functions. '''
    # create new toolbar section inside Level Editor toolbar
    toolbar_name = "Unreal Import"
    section_name = "UnrealImportSection"

    # find Level Editor toolbar menu
    menus = unreal.ToolMenus.get()
    toolbar = menus.find_menu("LevelEditor.LevelEditorToolBar.User")

    if toolbar:
        # register new toolbar section
        toolbar.add_section(section_name, label=toolbar_name)

        # add import asset button entry
        entryImport = unreal.ToolMenuEntry(name="ImportAssetsWithSettings",
                                           type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
        entryImport.set_label("Import Assets")
        entryImport.set_tool_tip("Imports Assets using external settings")
        entryImport.set_icon("EditorStyle", "Profiler.Tab.FiltersAndPresets") # load import icon

        # set import asset command 
        entryImport.set_string_command(type=unreal.ToolMenuStringCommandType.PYTHON, custom_type="",
                                       string="import unrealLoader; unrealLoader.import_asset_type()")
        
        toolbar.add_menu_entry("ImportAssetsWithSettings", entryImport)

        # add reload button entry
        entryStore = unreal.ToolMenuEntry(name="StoreCurrentProjectData",
                                          type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
        entryStore.set_label("Store Project Data")
        entryStore.set_tool_tip("Save current project data (path and skeletons) for MtoU Exporter.")
        entryStore.set_icon("EditorStyle", "GenericCommands.Redo")  # load reloader icon
    
        # set unreal loader command 
        entryStore.set_string_command(type=unreal.ToolMenuStringCommandType.PYTHON, custom_type="",
                                      string="import unrealLoader; unrealLoader.run_loader()")
        
        toolbar.add_menu_entry("StoreCurrentProjectData", entryStore)

        # refresh the toolbar
        menus.refresh_all_widgets()

if __name__=="__main__":
    run_loader()

create_loader_toolbar()

