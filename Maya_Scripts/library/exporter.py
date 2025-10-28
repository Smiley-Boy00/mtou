from ..library import modules as md
from abc import ABC
import maya.cmds as mc
import maya.mel as mel
import sys
import os

class exporterType(ABC):
    ''' Base Class for building exporter type interfaces and its setting dependencies. '''
    def __init__(self):
        ''' Initialize methods and private dependencies. '''
        self._export_path = None
        self._file_name = None

        # create empty data set to store any incoming mesh's translation data values 
        self._mesh_placement = {}

    def set_file_name(self, file_name: str):
        ''' Create unique file name. '''
        self._file_name=file_name

    def set_UE_project_path(self, ue_path:str, folder_name='MayaImports'):
        ''' Build export project path: 
            'c:/Unreal Engine/Active Project/Content/[folder_name]'. '''
        # create a path inside the UE's project contents folder where the mesh will be exported to
        self._export_path = os.path.join(ue_path, 'Content', folder_name)

        if not os.path.exists(self._export_path):
            os.makedirs(self._export_path)

    def move_sel_to_origin(self, mesh_selection):
        ''' Move a mesh to world origin: [0,0,0]. ''' 
            # store every mesh with their initial translation data values (location)
        self._mesh_placement[mesh_selection] = mc.xform(mesh_selection, worldSpace=True, query=True, translation=True)
        md.move_to_origin(mesh_selection)

    def place_sel_to_original_pos(self, mesh_selection):
        ''' Move a mesh to initial translation data values (location). ''' 
        md.place_mesh_back(self._mesh_placement[mesh_selection], mesh_selection)

    def export(self):
        ''' Perform the type dependant export. '''
        if not self._export_path:
            self._export_path = md.get_documents_folder()


class fbx(exporterType):
    ''' 
    FBX exporter interface. 
    Enable mel.eval settings prior to executing export.
    '''
    def __init__(self):
        super().__init__()
        
        self._file_name='mayaExport.fbx'

        self._fbx_ver_dict = {"FBX 2020": "FBX202000", "FBX 2019": "FBX201900",
                             "FBX 2018": "FBX201800", "FBX 2016/2017": "FBX201600",
                             "FBX 2014/2015": "FBX201400", "FBX 2013": "FBX201300",
                             "FBX 2012": "FBX201200", "FBX 2011": "FBX201100",
                             "FBX 2010": "FBX201000", "FBX 2009": "FBX200900"}

    def get_fbx_versions(self) -> dict:
        ''' Return FBX version (key) values data set. '''
        return self._fbx_ver_dict

    def export_smoothing_groups(self, mel_value: bool=False):
        ''' Enable or disable mel.eval 'FBXExportSmoothingGroups' export bool value. '''
        mel.eval('FBXExportSmoothingGroups -v {}'.format(str(mel_value).lower()))

    def export_smooth_mesh(self, mel_value: bool=False):
        ''' Enable or disable mel.eval 'FBXExportSmoothMesh' export bool value. '''
        mel.eval('FBXExportSmoothMesh -v {}'.format(str(mel_value).lower()))

    def export_tangents_binormals(self, mel_value: bool=False):
        ''' Enable or disable mel.eval 'FBXExportTangents' export bool value. '''
        mel.eval('FBXExportTangents -v {}'.format(str(mel_value).lower()))

    def export_skinWeights(self, mel_value: bool=False):
        ''' Enable or disable mel.eval 'FBXExportSkins' export bool value. '''
        mel.eval('FBXExportSkins -v {}'.format(str(mel_value).lower()))

    def export_blendShapes(self, mel_value: bool=False):
        ''' Enable or disable mel.eval 'FBXExportShapes' export bool value. '''
        mel.eval('FBXExportShapes -v {}'.format(str(mel_value).lower()))

    def export_embedded_textures(self, mel_value: bool=False):
        ''' Enable or disable mel.eval 'FBXExportTextures' export bool value. '''
        mel.eval('FBXExportEmbeddedTextures -v {}'.format(str(mel_value).lower()))

    def triangulate(self, mel_value: bool=False):
        ''' Enable or disable mel.eval 'FBXExportTriangulate' export bool value. '''
        mel.eval('FBXExportTriangulate -v {}'.format(str(mel_value).lower()))

    def file_type(self, mel_value: bool=False):
        ''' Enable or disable mel.eval 'FBXExportInAscii' export bool value. '''
        mel.eval('FBXExportInAscii -v {}'.format(str(mel_value).lower()))

    def up_axis(self, value: bool=False):
        ''' Set mel.eval 'FBXExportUpAxis' export value to 'y' or 'z'. '''
        if value:
            mel.eval('FBXExportUpAxis y')
        else:
            mel.eval('FBXExportUpAxis z')
    
    def file_version(self, version: str="FBX 2018"):
        ''' Set mel.eval 'FBXExportFileVersion' export value to an existing FBX version.\n
            Versions:\n["FBX 2020", "FBX 2019", "FBX 2018", "FBX 2016/2017", 
                        "FBX 2014/2015", "FBX 2013", "FBX 2012", "FBX 2011", 
                        "FBX 2010", "FBX 2009"]. '''
        if version not in self._fbx_ver_dict:
            raise ValueError(f'FBX version [{version}] not found or non-existent')
        
        # find the export value based on the version data set
        export_value=self._fbx_ver_dict[version]
        print(f'Exported: {version} - {export_value}')
        mel.eval('FBXExportFileVersion -v {}'.format(export_value))

    def export(self):

        export_file = os.path.join(self._export_path, self._file_name)

        try:
            #'-f' stands for "File" & '-s' for "Selected"; export the selected mesh into a .fbx file
            mel.eval('FBXExport -f "{}" -s'.format(export_file.replace('\\', '/')))

            # log execution
            sys.stdout.write("Export Successful: Open Unreal Project to Initialize Import\n")
        except Exception as e:
            sys.stderr.write(f"Export completed with warnings: {e}")

class obj(exporterType):
    ''' 
    OBJ exporter interface. 
    Set export bool flag values prior to executing export.
    '''
    def __init__(self):
        super().__init__()

        self._file_name='mayaExport.obj'
        
    def export(self,
               groups=0,
               pt_groups=0,
               materials=0,
               smoothing=0,
               normals=0,
               include_textures: bool=False):
        '''OBJ export values are interpreted as bool integers: 0 (False) or 1 (True)'''
        
        export_file = os.path.join(self._export_path, self._file_name)

        # store tuple values corresponding to each OBJ setting
        export_settings=(f'groups={groups};ptgroups={pt_groups};materials={materials};smoothing={smoothing};normals={normals}')

        # force export file
        # ignore non-crucial errors
        try:
            mc.file(export_file, force=True, options=export_settings, typ="OBJexport", 
                    preserveReferences=include_textures, exportSelected=True)
            
            # log execution
            sys.stdout.write("Export Successful: Open Unreal Project to Initialize Import\n")
        except Exception as e:
            sys.stderr.write(f"Export completed with warnings: {e}")
            
    