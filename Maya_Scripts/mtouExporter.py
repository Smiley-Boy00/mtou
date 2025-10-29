import maya.cmds as mc
import os
import sys
# import package dependent modules
from .library import modules as md
from .library import exporter

class mtouExporterUI():
    '''
    Class to handle UI display for exporter types.
    Executes modules once a project path data is instantiated.
    Generates import data after execution.
    '''
    def __init__(self):
        ''' Initializes the tool's UI layout, elements and class dependencies. '''
        print('Running MtoU Exporter Version: 0.1.0 ')

        # locate the user's home\Documents  path 
        # place data under: c:\Users\[user]\Documents\UE\Data
        self.folder_path = os.path.join(md.get_documents_folder(), 'UE', 'Data')
        
        # check if a UE project path data has been generated
        self.ue_data_exists = md.path_exists(os.path.join(self.folder_path, 
                                                          'ue_path.json'))
        
        # check if import data has been generated prior
        self.import_data_exists = md.path_exists(os.path.join(self.folder_path, 
                                                              'importSettings.json'))

        # import exporter classes
        self.fbx = exporter.fbx()
        self.obj = exporter.obj()

        self.window_ID = "EXPORTER"
        self.title = "Maya to Unreal Exporter"
        self.size = (500, 500)
        
        # dictionaries to store and handle UI elements (check boxes and option menus)
        self.checkerSettings = {}
        self.menuSettings = {}
        # list to store and handle separator elements 
        self.separators = []

        if mc.window(self.window_ID, exists=True):
            mc.deleteUI(self.window_ID, window=True)

        self.windowDisplay = mc.window(self.window_ID, 
                                       title=self.title, 
                                       widthHeight=self.size, sizeable=True)

        # form layout to allow precision in handling UI elements 
        self.main_layout = mc.formLayout(parent=self.windowDisplay)

        # create tab option menu to contain exporter types as menu item elements
        self.exportType_tab = mc.optionMenu(label='Export:', 
                                            changeCommand=self.change_export_type)
        mc.menuItem(label="FBX")
        mc.menuItem(label="OBJ")

        # create fields to input the file and folder name of the exported asset  
        self.filename_field = mc.textFieldGrp(label='File Name:', 
                                              placeholderText = 'Name your .fbx file',
                                              adjustableColumn=2,
                                              columnAlign=[1, 'left'],
                                              columnWidth=[1, 55])
        self.foldername_field = mc.textFieldGrp(label='Folder Name:', 
                                                placeholderText = 'Name the Contents Folder', 
                                                text = 'MayaImports',
                                                adjustableColumn=2,
                                                columnAlign=[1, 'left'],
                                                columnWidth=[1, 70])

        self.batchButton = mc.checkBox('batch_export', label='Export Selected into Separate Files',
                                       onc=lambda args:self.switch_bool_state('batch_export', state=True),
                                       ofc=lambda args:self.switch_bool_state('batch_export'))
        
        # connect checker identifier to it's boolean value for precise handling and callback
        self.checkerSettings['batch_export'] = False

        # create list comprehension of all the available FBX Maya export versions
        self.fbx_versions=[version for version in self.fbx.get_fbx_versions()]
        
        # build Maya export option settings frame grid layout
        self.maya_frame = mc.frameLayout(label='Maya Export Settings', 
                                         collapsable = True,
                                         backgroundColor=(0.25,0.46,0.88),
                                         highlightColor=(0.25,0.46,0.88),
                                         marginWidth=10,
                                         parent=self.main_layout)

        self.maya_column = mc.columnLayout(adjustableColumn=True)
        self.maya_checker_row = mc.rowLayout(numberOfColumns=4, generalSpacing=25,
                                           adjustableColumn=2, columnAlign=(4, 'right'))

        # columns parented to row layout create grid layout for check box element placement 
        self.left_maya_column = mc.columnLayout(adjustableColumn=True, 
                                                parent=self.maya_checker_row)
        self.centerLeft_maya_column = mc.columnLayout(adjustableColumn=True, 
                                                      parent=self.maya_checker_row)
        self.centerRight_maya_column = mc.columnLayout(adjustableColumn=True, 
                                                       parent=self.maya_checker_row)
        self.right_maya_column = mc.columnLayout(adjustableColumn=True, 
                                                 parent=self.maya_checker_row)

        # build Unreal import option settings frame grid layout
        self.unreal_frame = mc.frameLayout(label='Unreal Import Settings', 
                                           collapsable = True,
                                           backgroundColor=(0.15,0.18,0.20),
                                           highlightColor=(0.15,0.18,0.20),
                                           marginWidth=10,
                                           parent=self.main_layout)

        self.unreal_column = mc.columnLayout(adjustableColumn = True)
        self.unreal_checker_row = mc.rowLayout(numberOfColumns=4, generalSpacing=25, 
                                    adjustableColumn=2, columnAlign=(4, 'right'))

        self.left_unreal_column = mc.columnLayout(adjustableColumn=True, 
                                                  parent=self.unreal_checker_row)
        self.centerLeft_unreal_column = mc.columnLayout(adjustableColumn=True, 
                                                        parent=self.unreal_checker_row)
        self.centerRight_unreal_column = mc.columnLayout(adjustableColumn=True, 
                                                         parent=self.unreal_checker_row)
        self.right_unreal_column = mc.columnLayout(adjustableColumn=True, 
                                                   parent=self.unreal_checker_row)

        # display default settings UI when initializing
        # priority to FBX settings 
        self.fbx_ui_settings()

        # build utility button elements
        self.check_current_button = mc.button(label='Current UE Project', 
                                              command=self.print_UE_project_path, parent=self.main_layout)
        self.export_button = mc.button(label='Export To Unreal', 
                                       command=self.do_FBX_export, parent=self.main_layout)

        # align and place the layout's frames and elements in the display window    
        mc.formLayout(self.main_layout, edit=True, attachForm = [(self.maya_frame, 'left', 5), (self.maya_frame, 'right', 5),
                                                                 (self.unreal_frame, 'left', 5), (self.unreal_frame, 'right', 5),
                                                                (self.exportType_tab, 'left', 5), (self.exportType_tab, 'top', 10),
                                                                (self.filename_field, 'left', 5), (self.filename_field, 'right', 5),
                                                                (self.foldername_field, 'left', 5), (self.foldername_field, 'right', 5),
                                                                (self.batchButton, 'left', 200), (self.batchButton, 'right', 5)],
                                                    attachControl = [(self.filename_field, 'top', 10, self.exportType_tab),
                                                                     (self.foldername_field, 'top', 5, self.filename_field),
                                                                     (self.batchButton, 'top', 5, self.foldername_field),
                                                                     (self.maya_frame, 'top', 10, self.batchButton),
                                                                     (self.unreal_frame, 'top', 10, self.maya_frame),])
        
        mc.formLayout(self.main_layout, edit=True, attachForm = [(self.export_button, 'left', 5), (self.export_button, 'right', 5),
                                                                (self.export_button, 'bottom', 5),
                                                                (self.check_current_button, 'left', 5), (self.check_current_button, 'right', 5),
                                                                (self.check_current_button, 'bottom', 5)],
                                                    attachControl = [(self.check_current_button, 'bottom', 8, self.export_button)])

        mc.showWindow()

    def fbx_ui_settings(self):
        ''' Handles the UI elements of the FBX export and import settings. '''
        # build check box elements for export settings 
        self.create_or_show_checkbox('smooth_groups', 'maya', label='Smoothing Groups', position='left', checkerValue=True)
        self.create_or_show_checkbox('smooth_mesh', 'maya', label='Smooth Mesh', position='left', checkerValue=False)
        self.create_or_show_checkbox('tangents', 'maya', label='Tangents and Binormals', position='centerLeft', checkerValue=True)
        self.create_or_show_checkbox('triangulate', 'maya', label='Triangulate', position='centerLeft', checkerValue=False)
        self.create_or_show_checkbox('move_to_origin', 'maya', label='Move to Origin', position='centerRight', checkerValue=True)
        self.create_or_show_checkbox('embed_media', 'maya', label='Embed Textures', position='centerRight', checkerValue=True)
        self.create_or_show_checkbox('skins', 'maya', label='Skinning', position='right', checkerValue=True)
        self.create_or_show_checkbox('blnd_shapes', 'maya', label='Blend Shapes', position='right', checkerValue=True)

        if mc.control('middle_separator_01', exists=True):
            mc.control('middle_separator_01', edit=True, visible=True)
        else:
            middle_separator = mc.separator('middle_separator_01', style='none', 
                                            height=7.5, 
                                            parent=self.maya_column)
            self.separators.append(middle_separator)
        
        # build option menu elements export settings
        self.create_or_show_menu('axis', 'maya', label='Up Axis:', 
                                 items=['Y-Up', 'Z-Up'])
        self.create_or_show_menu('fileType', 'maya', label='FBX File Type:', 
                                 items=['Binary', 'Ascii'])
        self.create_or_show_menu('version', 'maya', label='FBX Version:', 
                                 items=self.fbx_versions)

        # build check box elements for import settings 
        self.create_or_show_checkbox('imp_materials', 'unreal', label='Include Materials', position='left', checkerValue=True)
        self.create_or_show_checkbox('imp_textures', 'unreal', label='Include Textures', position='centerLeft', checkerValue=True)
        self.create_or_show_checkbox('use_source_name', 'unreal', label='Import Asset with File Name', position='right', checkerValue=False)

        for id in self.checkerSettings:
            print(mc.control(id, query=True, fpn=True))
        print(self.separators)

    def obj_ui_settings(self):
        ''' Handles the UI elements of the FBX export and import settings. '''
        # build export settings checker objects
        self.create_or_show_checkbox('move_to_origin', 'maya', label='Move to Origin', position='left', checkerValue=True)
        self.create_or_show_checkbox('groups', 'maya', label='Groups', position='centerLeft', checkerValue=True)
        self.create_or_show_checkbox('pt_groups', 'maya', label='Point Groups', position='centerLeft', checkerValue=True)
        self.create_or_show_checkbox('materials', 'maya', label='Materials', position='centerRight', checkerValue=True)
        self.create_or_show_checkbox('smoothing', 'maya', label='Smoothing', position='right', checkerValue=True)
        self.create_or_show_checkbox('normals', 'maya', label='Normals', position='right', checkerValue=True)

        # build import settings checker objects
        self.create_or_show_checkbox('imp_materials', 'unreal', label='Include Materials', position='left', checkerValue=True)
        self.create_or_show_checkbox('imp_textures', 'unreal', label='Include Textures', position='centerLeft', checkerValue=False)
        self.create_or_show_checkbox('use_source_name', 'unreal', label='Import Asset with File Name', position='right', checkerValue=True)

        print(self.checkerSettings)

    def create_or_show_checkbox(self, checkerID:str, frame:str, label="checkerName", position="left", checkerValue=False):
        '''
        Builds a check box element. Requires ID string for element callback. 
        If the check box already exists, unhide and enable it alongside its separator.
        Frame args: ['maya', 'unreal'] 
        '''
        # decide which frame and column inside the grid layout the check box will be placed
        if frame=='maya':
            if position == 'centerLeft':
                parentUI = self.centerLeft_maya_column
            elif position == 'centerRight':
                parentUI = self.centerRight_maya_column
            elif position == 'right':
                parentUI = self.right_maya_column
            else:
                parentUI = self.left_maya_column # default to left

        elif frame=='unreal':
            if position == 'centerLeft':
                parentUI = self.centerLeft_unreal_column
            elif position == 'centerRight':
                parentUI = self.centerRight_unreal_column
            elif position == 'right':
                parentUI = self.right_unreal_column
            else:
                parentUI = self.left_unreal_column # default to left
        
        else:
            raise ValueError(f"{frame} is not a frame entity.")

        if mc.control(checkerID, exists=True):
            # enable visibility of check box and separator if it has already been created
            mc.control(checkerID, edit=True, visible=True, enable=True, parent=parentUI)

            mc.control(f'{checkerID}_separator', edit=True, visible=True, parent=parentUI)

        else:
            # create the check box element
            mc.checkBox(checkerID, label=label,
                        parent=parentUI,
                        value=checkerValue,
                        onc=lambda arg:self.switch_bool_state(checkerID, state=True),
                        ofc=lambda arg:self.switch_bool_state(checkerID))
        
            # connect checker identifier to it's boolean value for precise handling and callback
            self.checkerSettings[checkerID] = checkerValue

            # add vertical separator attached to checker column
            checker_separator = mc.separator(f'{checkerID}_separator', style='none', 
                                                height=5, 
                                                parent=parentUI)
            # store separator element information
            self.separators.append(checker_separator)
    
    def create_or_show_menu(self, menuID:str, frame:str, label="menuName", items:list=['firstItem']):
        '''
        Builds an option menu containing menu item elements. Requires ID string for element callback. 
        If the option menu already exists, unhide and enable it alongside its separator.
        Frame args: ['maya', 'unreal'] 
        '''
        # decide which column the option menu will be placed
        if frame=='maya':
            parentUI=self.maya_column
        elif frame=='unreal':
            parentUI=self.unreal_column
        else:
            raise ValueError(f"{frame} is not a frame entity.")
        
        if mc.control(menuID, exists=True):
            # enable visibility of option menu and separator if it has already been created
            mc.control(menuID, edit=True, visible=True, enable=True, parent=parentUI)

            mc.control(f'{menuID}_separator', edit=True, visible=True)

        else:
            menuElement=mc.optionMenu(menuID, label=label,parent=parentUI)
            # create items for menu
            for item in items:
                mc.menuItem(label=item)

            # connect menu string identifier to it's UI element for precise callback
            self.menuSettings[menuID] = menuElement

            # add vertical separator attached to column
            menu_separator = mc.separator(f'{menuID}_separator', style='none',
                                             height=2.5,
                                             parent=self.maya_column)
            # store separator element information
            self.separators.append(menu_separator)

    def switch_bool_state(self, id:str, state=False):
        ''' Changes boolean state of check box element: requires string identifier. '''
        self.checkerSettings[id]=state
        print(f"{id} set to: {self.checkerSettings[id]}")

    def disable_ui_elements(self):
        ''' Turns visibility and functionality off for stored UI elements.'''
        for checkerID in self.checkerSettings:
            if checkerID=='batch_export':
                continue
            mc.control(checkerID, 
                       edit=True, visible=False, enable=False)
        for menuElement in self.menuSettings:
            mc.control(menuElement,
                       edit=True, visible=False, enable=False)
        for separator in self.separators:
            mc.control(separator,
                       edit=True, visible=False)
        
    def change_export_type(self, *args):
        ''' Handles switching UI elements depending on the requested exporter type. '''
        export_type = mc.optionMenu(self.exportType_tab, query=True, value=True)
        if export_type=='OBJ':
            mc.textFieldGrp(self.filename_field, edit=True, placeholderText='Name your .obj file')
            self.disable_ui_elements()
            
            self.obj_ui_settings()
            
            mc.button(self.export_button, edit=True, command=self.do_OBJ_export)
        
        elif export_type=='FBX':
            mc.textFieldGrp(self.filename_field, edit=True, placeholderText='Name your .fbx file')
            self.disable_ui_elements()

            self.fbx_ui_settings()
            
            mc.button(self.export_button, edit=True, command=self.do_FBX_export)

    def print_UE_project_path(self, *args):
        ''' Logs the currently active UE project path. '''
        # verify UE project path data exists
        if not self.ue_data_exists:
            mc.warning('No UE project has been loaded! Make sure to load "unrealLoader.py" on UE project.')
            return
        
        if self.ue_data_exists:
            # load project path data, store active UE project path
            ue_path=md.load_data(self.folder_path, 'ue_path.json')
            ue_proj=ue_path.get("Current Project")
            # print and write path to script editor and command line 
            sys.stdout.write(f"Current UE Project: {ue_proj}\n")

    def do_FBX_export(self, *args):
        '''
        Handles the FBX export procedure. 
        Ensures no input error before executing exporter type methods.
        '''
        # create a list of the selected mesh/es
        mesh_selection = mc.ls(selection = True)

        if not self.ue_data_exists:
            mc.warning('No UE project has been loaded for export!')
            return

        if not mesh_selection:
            mc.warning("Please select a mesh to export.")
            return
        
        # query the user's file & folder name
        mesh_file = mc.textFieldGrp(self.filename_field, query=True, text=True)
        folder_name = mc.textFieldGrp(self.foldername_field, query=True, text=True)

        if not mesh_file:
            mc.warning('Please name for your file for export.')
            return

        # load project path data, store active UE project path
        ue_dict = md.load_data(self.folder_path, 'ue_path.json')
        ue_project_path = ue_dict.get('Current Project')

        if folder_name:
            folder_name=folder_name.replace('\\', '/')
            # create a path inside the UE's project contents folder where the mesh will be exported to
            self.fbx.set_UE_project_path(ue_project_path, folder_name)
        else:
            mc.warning('Please provide a folder name to export.')
            return

        move_mesh = self.checkerSettings['move_to_origin']

        # evaluate user's fbx settings before exporting mesh 
        # evaluate if the mesh will be exported with Smoothing Groups information data
        self.fbx.export_smoothing_groups(self.checkerSettings['smooth_groups'])

        # evaluate if the mesh will be Subdivided once exported
        self.fbx.export_smooth_mesh(self.checkerSettings['smooth_mesh'])

        # evaluate if the mesh will contain Tangents & Binormals information data 
        self.fbx.export_tangents_binormals(self.checkerSettings['tangents'])

        # evaluate if the mesh will get Triangulated before exporting
        self.fbx.triangulate(self.checkerSettings['triangulate'])

        # evaluate if the mesh will be exported with Skin Deformation data
        self.fbx.export_skinWeights(self.checkerSettings['skins'])

        # evaluate if the mesh will contain geometry Blend Shapes from the current scene
        self.fbx.export_blendShapes(self.checkerSettings['blnd_shapes'])

        # evaluate if the mesh will be exported with Embedded Media (textures)
        self.fbx.export_embedded_textures(self.checkerSettings['embed_media'])

        # evaluate the primary axis the mesh will be exported with (Y-Up or Z-Up)
        axisValue = mc.optionMenu(self.menuSettings['axis'], query=True, value=True)
        if axisValue == 'Y-Up':
            self.fbx.up_axis(True)
        else:
            self.fbx.up_axis()

        # evaluate if the file will be exported as Ascii or Binary
        fbxFileType=mc.optionMenu(self.menuSettings['fileType'], query=True, value=True)
        if fbxFileType == "Ascii":
            self.fbx.file_type(True)
        else:
            self.fbx.file_type()

        # evaluate which FBX maya version will the mesh be exported in    
        fbxVersion = mc.optionMenu(self.menuSettings['version'], query=True, value=True)
        print(fbxVersion)
        self.fbx.file_version(fbxVersion)

        if self.import_data_exists:
            # load and store import settings data set
            import_data = md.load_data(self.folder_path, 'importSettings.json')
        else:
            # create empty import settings data set
            import_data = {}

        # clear data set; avoids conflict with latest version of importer script
        import_data.clear()
        # create fbx import settings data set
        fbx_import = {}
        import_data['FBX'] = fbx_import
        import_settings={}

        batch_export=self.checkerSettings['batch_export']

        if batch_export:
            iter_val=0
            for mesh in mesh_selection:
                iter_val+=1
                print(mesh)
                mc.select(mesh)
                if move_mesh:
                    # move mesh selection to world origin [0,0,0]
                    self.fbx.move_sel_to_origin(mesh)

                if '.fbx' in mesh_file:
                    mesh_file=mesh_file.split('.fbx')[0]

                iter_file_name = mesh_file + f"_{iter_val}.fbx"
                self.fbx.set_file_name(iter_file_name)
                # change & store file name and folder path values 
                fbx_import[iter_file_name]=import_settings
                import_settings['Folder Path']=folder_name

                # overwrite values with check box selection (user settings)
                import_settings['Import Materials']=self.checkerSettings['imp_materials']
                import_settings['Import Textures']=self.checkerSettings['imp_textures']
                import_settings['Use Source Name']=self.checkerSettings['use_source_name']
        
                # save the user import settings for unreal importer
                md.save_data(self.folder_path, 'importSettings.json', import_data)

                print(import_settings)

                self.fbx.export()

                if move_mesh:
                    # move mesh selection back to the original location prior placing it at world origin
                    self.fbx.place_sel_to_original_pos(mesh)

        else:
            if move_mesh:
                # move mesh selection to world origin [0,0,0]
                for mesh in mesh_selection:
                    self.fbx.move_sel_to_origin(mesh)

            # if the user didn't add '.fbx' at the end of the file name, add it
            if not mesh_file.endswith('.fbx'):
                mesh_file += ".fbx"
            self.fbx.set_file_name(mesh_file)

            # change & store file name and folder path values 
            fbx_import[mesh_file]=import_settings
            import_settings['Folder Path']=folder_name

            # overwrite values with check box selection (user settings)
            import_settings['Import Materials']=self.checkerSettings['imp_materials']
            import_settings['Import Textures']=self.checkerSettings['imp_textures']
            import_settings['Use Source Name']=self.checkerSettings['use_source_name']

            # save the user import settings for unreal importer
            md.save_data(self.folder_path, 'importSettings.json', import_data)

            print(import_settings)

            self.fbx.export()

            if move_mesh:
                # move mesh selection back to the original location prior placing it at world origin
                for mesh in mesh_selection:
                    self.fbx.place_sel_to_original_pos(mesh)

        # clear selection
        mc.select(cl=True)

    def do_OBJ_export(self, *args):
        '''
        Handles the OBJ export procedure. 
        Ensures no input error before executing exporter type methods.
        '''
        if not self.ue_data_exists:
            mc.warning('No UE project has been loaded for export!')
            return

        # create a list of the selected mesh/es
        mesh_selection = mc.ls(selection = True)

        if not mesh_selection:
            mc.warning("Please select a mesh to export.")
            return
        
        # query the user's file & folder name
        mesh_file = mc.textFieldGrp(self.filename_field, query=True, text=True)
        folder_name = mc.textFieldGrp(self.foldername_field, query=True, text=True)

        if not mesh_file:
            mc.warning('Please name for your file for export.')
            return
        
         # load project path data, store active UE project path
        ue_dict = md.load_data(self.folder_path, 'ue_path.json')
        ue_project_path = ue_dict.get('Current Project')

        if folder_name:
            folder_name=folder_name.replace('\\', '/')
            # create a path inside the UE's project contents folder where the mesh will be exported to
            self.obj.set_UE_project_path(ue_project_path, folder_name)
        else:
            mc.warning('Please provide a folder name to export.')
            return     

        move_mesh = self.checkerSettings['move_to_origin']

        # evaluate if mesh will contain group information data
        if self.checkerSettings['groups']:
            obj_groups=1
        
        # evaluate if mesh will contain point groups information data
        if self.checkerSettings['pt_groups']:
            obj_ptgroups=1

        # evaluate if mesh will contain material information data
        if self.checkerSettings['materials']:            
            obj_materials=1

        # evaluate if mesh will contain smoothing groups information data
        if self.checkerSettings['smoothing']:
            obj_smoothing=1

        # evaluate if mesh will contain normals information data
        if self.checkerSettings['normals']:
            obj_normals=1

        if self.import_data_exists:
            # load and store import settings data set
            import_data = md.load_data(self.folder_path, 'importSettings.json')
        else:
            # create empty import settings data set
            import_data = {}

        
        # clear data set; avoids conflict with latest version of importer script
        import_data.clear()
        # create obj import settings data set
        obj_import = {}
        import_data['OBJ'] = obj_import
        import_settings={}

        batch_export=self.checkerSettings['batch_export']

        if batch_export:
            iter_val=0
            for mesh in mesh_selection:
                iter_val+=1
                print(mesh)
                mc.select(mesh)
                # create temporary transform node 
                tempGRP=mc.group(empty=True)
                # parent mesh to transform node and rotate the node 90 degrees
                mc.parent(mesh, tempGRP)
                mc.rotate(90,0,0, tempGRP)

                if move_mesh:
                    # move mesh selection to world origin [0,0,0]
                    self.obj.move_sel_to_origin(mesh)

                if '.obj' in mesh_file:
                    mesh_file = mesh_file.split('.obj')[0]

                iter_file_name = mesh_file + f"_{iter_val}.obj"
                self.obj.set_file_name(iter_file_name)
                # change & store file name and folder path values 
                obj_import[iter_file_name]=import_settings
                import_settings['Folder Path']=folder_name

                # overwrite values with check box selection (user settings)
                import_settings['Import Materials']=self.checkerSettings['imp_materials']
                import_settings['Import Textures']=self.checkerSettings['imp_textures']
                import_settings['Use Source Name']=self.checkerSettings['use_source_name']
        
                # save the user import settings for unreal importer
                md.save_data(self.folder_path, 'importSettings.json', import_data)

                print(import_settings)

                # evaluate the user's settings and store them in a tuple for exporting
                self.obj.export(obj_groups, obj_ptgroups, obj_materials, 
                                obj_smoothing, obj_normals, 
                                include_textures=self.checkerSettings['imp_textures'])

                # undo rotation of temporary transform node
                mc.rotate(0,0,0, tempGRP)
                # unparent mesh to transform node and delete the node 
                mc.parent(mesh, world=True)
                mc.delete(tempGRP)

                if move_mesh:
                    # move mesh selection back to the original location prior placing it at world origin
                    self.obj.place_sel_to_original_pos(mesh)

        else: 
            # create temporary transform node 
            tempGRP=mc.group(empty=True)
            for obj in mesh_selection:
                # parent mesh to transform node and rotate the node 90 degrees
                mc.parent(obj, tempGRP)
            mc.rotate(90,0,0, tempGRP)

            if move_mesh:
            # move mesh selection to world origin [0,0,0]
                for mesh in mesh_selection:
                    self.obj.move_sel_to_origin(mesh)
            # if the user didn't add '.obj' at the end of the file name, add it
            if not mesh_file.endswith('.obj'):
                mesh_file += ".obj"
            self.obj.set_file_name(mesh_file)

            # change & store file name and folder path values 
            obj_import[mesh_file]=import_settings
            import_settings['Folder Path']=folder_name

            # overwrite values with check box selection (user settings)
            import_settings['Import Materials']=self.checkerSettings['imp_materials']
            import_settings['Import Textures']=self.checkerSettings['imp_textures']
            import_settings['Use Source Name']=self.checkerSettings['use_source_name']

            # save the user import settings for unreal importer
            md.save_data(self.folder_path, 'importSettings.json', import_data)

            print(import_settings)

            # evaluate the user's settings and store them in a tuple for exporting
            self.obj.export(obj_groups, obj_ptgroups, obj_materials, 
                            obj_smoothing, obj_normals, 
                            include_textures=self.checkerSettings['imp_textures'])
        
            # undo rotation of temporary transform node
            mc.rotate(0,0,0, tempGRP)
            for obj in mesh_selection:
                # unparent mesh to transform node and delete the node 
                mc.parent(obj, world=True)
            mc.delete(tempGRP)

            # move mesh selection back to the original location prior placing it at world origin
            if move_mesh:
                for mesh in mesh_selection:
                    self.obj.place_sel_to_original_pos(mesh)

        # clear selection
        mc.select(cl=True)

        

        

