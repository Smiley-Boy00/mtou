![Alt text](https://github.com/Smiley-Boy00/Smiley-Boy00/blob/main/Resources/MtoU_Banner.png?raw=true)
![Python](https://img.shields.io/badge/python-ffdd54?logo=python&logoColor=white) ![Autodesk Maya 2024+](https://img.shields.io/badge/Autodesk%20Maya%202024+-00AEEF?logo=autodesk&logoColor=white) ![Unreal Engine 5.5 | 5.6](https://img.shields.io/badge/Unreal%20Engine%205.5%20|%205.6-0E1128?logo=unrealengine&logoColor=white) ![Latest Commit](https://img.shields.io/github/last-commit/Smiley-Boy00/mtou) [![Latest Release](https://img.shields.io/github/v/release/Smiley-Boy00/mtou?label=Download&color=37A5CC)](https://github.com/Smiley-Boy00/mtou/releases/latest) ![Windows](https://img.shields.io/badge/Windows-0078D6?logo=windows&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)
 ![Free for Commercial Use](https://img.shields.io/badge/Free%20for%20Commercial%20Use-✔-brightgreen) ![No Resale](https://img.shields.io/badge/Do%20Not%20Resale-✖-red)

## Table of Contents
- [About](#fax-about)
- [Tool Source Code and Details](#bulb-tool-source-code-and-details)
- [How to Install](#bookmark_tabs-sparkles-how-to-install)
- [Download Latest Release](#inbox_tray-download-latest-release)
- [Feedback](#speech_balloon-feedback)
- [Contacts](#-contacts)

## :fax: About
MtoU (Maya to Unreal) is a Python-based tool package that enables seamless export from Autodesk Maya to Unreal Engine. Originally developed as part of the Smiley Tools Plugin, this package has now been isolated for independent development. This new version has been fully refactored, optimized for better performance and now includes an automatic importer script for Unreal Engine to streamline the workflow.

**Important**: As of the latest release, manual installation/linking is required for Unreal Engine integration (unrealLoader.py).

## ✨ Features

*   Direct export from Maya to Unreal Engine
*   Import settings generation based on Maya's export configuration
*   Custom folder path support within UE project's Content folder
*   **New:** Handles animation data for export and import, including animation clips.
*   **New:** Supports joint chains and hierarchy preservation.
*   **New:** Allows selection of existing skeletons within the scene for animation export.

### ⚠️ Experimental | WIP
*   **New Experimental Module:** Exporter now includes 'Bind Unused Joints', a new module function that finds and binds any unused joints within the selected joint chain to an existing skin cluster. This aims to ensure all joints in a hierarchy are included in the skinning data, even if they initially have no weights (e.g. **End_Joints**).
  
*   **Experimental Module:** 'unrealLoader.py' contains fix_name_import_handling() which tries to handle naming conventions annoyance; Unreal (Interchange Manager) imports skeleletal assets and dependencies with source file name even if directly specifies. The module is functioning but inactive from the current import process.
  
*   **Experimental Module:**  'unrealLoader.py' contains create_imported_asset_data() which stores string data from every imported asset to UE Project. The module is functioning but inactive due to no practical use for the current import process.

## :bulb: Tool Source Code and Details
### Current Release: v0.3.0
### Maya Tools Source Code:
**Maya to Unreal Exporter (Maya_Scripts/mtouExporter.py): ver. 0.3.0**  
**Compatibility**: Maya 2024 and above

**Details**: Generates Exporter UI that allows you to directly export assets to your currently loaded UE project, input or generate a folder path anywhere inside the UE project's Content folder to import your assets. The tool now automatically generates import settings for Unreal based on your Maya configuration inside the Exporter UI. 'unrealLoader.py' Requires to be run inside a compatible Unreal Engine 5 project in order for the Exporter to execute.  

### Unreal Engine Source Code:
**Maya to Unreal Importer (Unreal_Scripts/unrealLoader.py): ver. 0.2.0**  
**Compatibility**: Unreal Engine 5.5 and Unreal Engine 5.6  

**Details**: Saves and stores the currently active Unreal project path, required to be run inside a compatible Unreal Engine 5 project in order for the Maya Exporter to execute, but Unreal Importer can be executed indepentently as long as import settings data exists (detailed inside 'unrealLoader.py'). The Reload Button functionality has been merged into this script, allowing it to re-save the active Unreal project path. Additionally, a new import button icon has been added next to the reload button, which runs an automatic importer script using the import settings data created from the Maya tool.  


## :bookmark_tabs: :sparkles: How to Install
[![Installation Video](https://img.shields.io/badge/Installation%20Video-FF0000?logo=youtube&logoColor=white)](https://youtu.be/eiXnYpwpQRU)

### Maya Side:
> - Extract **mtou** and place the folder contents into your Maya directory folder and inside your plug-ins folder, if no plug-ins folder exists create one:
**/maya/plug-ins** (this directory is usually found in the Documents folder).
> - Inside Maya, go to **Windows -> Settings/Preferences -> Plug-in Manager**.
> - In the **Plug-in Manager** enable the **MtoU.py** plugin, a tab named "Exporter Tools" should appear where you can start utilizing the MtoU exporter.
### Unreal Side:
> - Launch the Unreal Engine project where you would like the import capability enabled and linked.
> - Go to **Edit -> Plugins**, search for **Python Editor Script Plugin** and make sure is enabled.
> - Once enabled, go to **Edit -> Project Settings -> Plugins -> Python**:
> - In **Additional Paths**, add the folder directory where the unrealLoader.py is saved in your system.
> - In **Startup Scripts**, add a section and write "unrealLoader.py" in order to load the file into the project.
> - Restart your Unreal Engine Project. <br>
>**Note**: This process has to be set for every project you would like to enable the loader module.

## :inbox_tray: Download Latest Release

:rocket: **Grab the Latest Build Here:**  

[![Download Release](https://img.shields.io/github/v/release/Smiley-Boy00/mtou?label=Download&color=blue)](https://github.com/Smiley-Boy00/mtou/releases/latest)  

> 🛠 This tool is in **Alpha**: Expect changes and possible bugs as I add new features and improve workflows.  
> ✅ **Free for Commercial Use**: This tool can be used for both personal and professional projects without restrictions.  
> ⚠️ **No Resale or Redistribution**: This tool cannot be resold or redistributed for commercial intent.  

**Download Notes:**  
- Alpha builds may have partial or experimental features.  
- Manual setup is required for Unreal Engine linkage (see [How to Install](#-how-to-install)).  
- Feedback and bug reports are encouraged to help improve stability.  

## :speech_balloon: Feedback  

If you encounter a problem or have an idea for improvement:  
1. Open an **[Issue](https://github.com/Smiley-Boy00/mtou/issues)** describing your problem, suggestion, or request.  
2. Include as much detail as possible: logs, screenshots, reproduction steps.  

💡 Your feedback will influence future releases!  

## 📇 Contacts  

Want to connect, ask a question, or collaborate? Here's how to reach me:  

- 📧 **Email:** david.e.margon@hotmail.com  
- 💬 **Discord:** `smiley_boy`  
- 🌐 **Portfolio / Website:** [Artstation](https://www.artstation.com/david_martinez)  
