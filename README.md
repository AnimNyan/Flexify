# TransferShapeKeys

# Discord
First things first, I have a discord server for questions, support and bugs find me here: https://discord.gg/rkkWSH2EMz or message me on my discord account Anime Nyan#5897

# Installation
### To install TransferShapeKeys:
1. Go here: https://github.com/AnimNyan/TransferShapeKeys/releases/latest > Right click on "TransferShapeKeys_v.X.X.X.zip" > Save Link As do NOT unzip it.
2. Open Blender and click Edit > Preferences > Add-Ons > Install > in the file explorer find "TransferShapeKeys_v.X.X.X.zip" and double click to install.
3. In the Add-Ons search, search for transfer and enable the Transfer Shape Keys addon.

## What does TransferShapeKeys do?
TransferShapeKeys is a free Blender Plugin. It is an add on that transfers shape keys via mesh deform modifiers.

The best way to explain this is through an example. So I have a face with many shape keys for different expressions such as angry, sad and happy. I have made a moustache mesh to attach to the face. 

Problem: I need my moustache mesh to follow the shape keys of the face. 
This will help transfer all those shape keys a lot easier. You still do need to set up the solidify and mesh deform modifiers manually first though.

## How to use TransferShapeKeys?
Continuing with the previous example of transferring various facial expression shape keys to a moustache:
### How to prepare a mesh for Shape Key transfer:
1. Select the face mesh > go to Edit Mode > change to face selection mode.
2. Select all of the faces underneath the moustache your selection must be bigger than the moustache > press shift + d to copy those faces and press enter.
3. You should now be selecting the copy of those faces press p to separate the meshes > Selection to separate by selection we will call this new mesh "Skin Under Moustache".
4. Go back to Object Mode > Select the "Skin Under Moustache" Mesh and move it slightly underneath the face.
5. Select the "Skin Under Moustache" Mesh > Object Properties (the orange square in the vertical tabs) > Display as > Change Display to wire.
6. Add a Solidify modifier to "Skin Under Moustache" and increase the size until you are sure that every vertex on the moustache is inside the "Skin Under Moustache" mesh cage.
7. Add a Mesh Deform Modifier > For Object select the face mesh > Press Bind.  

### How to use TransferShapeKeys to transfer all shape keys
1. In the 3D View press n to open the properties panel > Shapekeys.
2. For **From Mesh** select the face mesh as we are transferring shape keys **from** the face to the moustache.
3. For **To Mesh** select the moustache mesh as we are transferring shape keys from the face **to** the moustache.
4. Press Transfer Shape Keys and all of your shape keys should be transferred through the mesh deform modifier.

## Disclaimer: When should this plugin not be used
You must go through the steps in How to prepare a mesh for Shape Key transfer first, otherwise the shape keys will not be transferred.