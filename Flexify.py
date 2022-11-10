import bpy

#property group to store options that the user can
#make true or false
class transfer_shape_keys_properties(bpy.types.PropertyGroup):
    is_add_modifiers_if_not_there: bpy.props.BoolProperty(name="Add Solidify + Mesh Deform if not exist", default = True)
    solidify_thickness_float: bpy.props.FloatProperty(name="Solidify Thickness", default = -0.1)
  



#this is panel 2 as it is the second panel in the psk/psa panel
class TRANSFERSHAPEKEYS_PT_main_panel(bpy.types.Panel):
    bl_label = "Transfer Shape Keys"
    bl_idname = "TRANSFERSHAPEKEYS_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Shapekeys"

    def draw(self, context):
        layout = self.layout
        #store active/selected scene to variable
        scene = context.scene
        #allow access to user inputted properties through pointer
        #to properties
        transfershapekeystool = scene.transfershapekeys_tool

        layout.prop(scene, "mesh_source")
        layout.prop(scene, "mesh_target")

        layout.separator()

        layout.prop(transfershapekeystool, "is_add_modifiers_if_not_there")
        layout.prop(transfershapekeystool, "solidify_thickness_float")
        
        layout.separator()

        layout.operator("transfershapekeys.transfer_shapekeys_operator")
        
        
        

#---------------fix the active action (only one) for killer and survivor 
class TRANSFERSHAPEKEYS_OT_transfer_shapekeys(bpy.types.Operator):
    bl_label = "Transfer Shape Keys"
    bl_description = "Transfer Shape Keys from first mesh to second mesh"
    bl_idname = "transfershapekeys.transfer_shapekeys_operator"

    def execute(self, context):
        transfer_all_shape_keys()
        
        return {'FINISHED'}



def transfer_all_shape_keys():
    #store active scene to variable
    scene = bpy.context.scene
    #allow access to user inputted properties through pointer
    #to properties
    mesh_source = scene.mesh_source
    mesh_target = scene.mesh_target


    

    #-----------------------iterate over all shape keys in mesh_source and add them to mesh_target

    #----------------Check if Transfer Shape Keys can be done
    #store active scene to variable
    scene = bpy.context.scene
    #allow access to user inputted properties through pointer
    #to properties
    transfershapekeystool = scene.transfershapekeys_tool

    is_add_modifiers_if_not_there = transfershapekeystool.is_add_modifiers_if_not_there


    #find the first mesh deform modifier for mesh_target
    isFoundSolidify = False
    isFoundMeshDeform = False

    for modifier in mesh_target.modifiers:
        
        #we use the (and not isFoundMeshDeform) because we want to use
        #the first mesh deform modifier in case of 2 or more
        if (modifier.type == "MESH_DEFORM" and not isFoundMeshDeform):
            mesh_deform_modifier = modifier
            isFoundMeshDeform = True

        #we use the (and not isFoundSolidify) because we want to use
        #the first solidify modifier in case of 2 or more
        elif(modifier.type == "SOLIDIFY" and not isFoundSolidify):
            solidify_modifier = modifier
            isFoundSolidify = True
    
    

    #-----------------Check the Mesh Deform Modifier
    #if there is no mesh deform modifier add it or show error depending on option user has chosen
    if (isFoundMeshDeform == False):

        #----------if setting to add modifiers is activated
        #add the MeshDeform
        if(is_add_modifiers_if_not_there):
            mesh_deform_modifier = mesh_target.modifiers.new(type="MESH_DEFORM")
        

        #else show the error instead
        else:
            #show user feedback error message so they know what to do
            #also print to console so they can check error message from console
            error_message = "Error: To Mesh \'" + mesh_target.name + "\' does not have a Mesh Deform modifier, so the shape key transfer cannot be done!"
            bpy.ops.transfershapekeys.show_message_operator(message = error_message)
            log(error_message)

            #return will stop the rest of this function executing
            #and return prematurely as there is no mesh deform modifier to apply
            #so the transfer shape keys cannot work
            return
    
    #if the mesh deform is found we also need to check if the modifier targets an object
    #this means the mesh deform modifier is valid to be applied as a shape key
    #AND we also need to check if the mesh deform modifier is bound to an object
    elif (isFoundMeshDeform == True):

        #if there is no target Object show an error
        if (mesh_deform_modifier.object is None):
            #show user feedback error message so they know what to do
            #also print to console so they can check error message from console
            error_message = "Error: Mesh Deform modifier on \'" + mesh_target.name + "\' does not have an target Object, so the shape key transfer cannot be done!"
            bpy.ops.transfershapekeys.show_message_operator(message = error_message)
            log(error_message)

            #return will stop the rest of this function executing
            #and return prematurely as the mesh deform modifier 
            #cannot be applied as there is no target Object
            #so the transfer shape keys cannot work
            return

        elif (mesh_deform_modifier.is_bound == False):
            #show user feedback error message so they know what to do
            #also print to console so they can check error message from console
            error_message = "Error: Mesh Deform modifier on \'" + mesh_target.name + "\' is not bound, so the shape key transfer cannot be done!"
            bpy.ops.transfershapekeys.show_message_operator(message = error_message)
            log(error_message)

            #return will stop the rest of this function executing
            #and return prematurely as the mesh deform modifier 
            #is not bound so the shape keys will not transfer over properly
            return

    #-----------------Check the Solidify Modifier
    if (isFoundSolidify == False):

        #----------if setting to add modifiers is activated
        #add the Solidify Modifier
        if(is_add_modifiers_if_not_there):
            solidify_modifier = mesh_target.modifiers.new(type="SOLIDIFY")

            #change the Thickness of the newly created Solidfy modifier to the user setting
            solidify_modifier.thickness = transfershapekeystool.solidify_thickness_float
        

        #else show the error instead
        else:
            #show user feedback error message so they know what to do
            #also print to console so they can check error message from console
            error_message = "Error: To Mesh \'" + mesh_target.name + "\' does not have a Solidify modifier, so the shape key transfer cannot be done!"
            bpy.ops.transfershapekeys.show_message_operator(message = error_message)
            log(error_message)

            #return will stop the rest of this function executing
            #and return prematurely as there is no mesh deform modifier to apply
            #so the transfer shape keys cannot work
            return


    #------------------------------Do Transfer Shape Keys now that the checks for valid shape key transfer is done

    #turn off shape key lock for both meshes to not cause problems
    mesh_source.show_only_shape_key = False
    mesh_target.show_only_shape_key = False

    #reset all shape keys to value 0
    #we need to do this so when we apply the mesh deform modifier
    #it applies it with the effect of only one shape key at a time
    for shapekey_keyblock in mesh_source.data.shape_keys.key_blocks:
        shapekey_keyblock.value = 0




    #get the basis shape key which will be the first one 
    #so we can skip transferring it because we don't need it
    basis_shape_key = mesh_source.data.shape_keys.key_blocks[0]


    # if there is no shape keys, meaning there is no basis shape key on mesh_target
    # create a basis shape key on mesh_target
    if (mesh_target.data.shape_keys is None):
        mesh_target.shape_key_add(name = 'Basis')
    
    #for each shape key we need to
    #1: Adjust the current shapekey value to 1 on mesh_source
    #2: Apply the Mesh Deform Modifier as shape key keeping the modifier on mesh_target (i.e Same as manually going Save as Shape Key)
    #3: Get the new shape key that was created on mesh_target
    #4: Change the name of the new shape key on mesh_target to be same as the name of the shape key on mesh_source
    #5: Adjust the current shapekey value to 0
    #and we will iterate through all shape keys on mesh_source
    for keyblock_source in mesh_source.data.shape_keys.key_blocks:
        #skip the basis shape key because we don't need to copy it
        if keyblock_source == basis_shape_key:
            continue

        shapekey_from = keyblock_source

        #1: Adjust the current shapekey value to 1 on mesh_source
        shapekey_from.value = 1

        #2: Apply the Mesh Deform Modifier as shape key keeping the modifier on mesh_target (i.e Same as manually going Save as Shape Key)
        bpy.ops.object.modifier_apply_as_shapekey( keep_modifier=True, modifier = mesh_deform_modifier.name)

        #3: Get the new shape key that was created on mesh_target
        #we do the -1 index as that will always be the last item, which will be the newly created shape key
        new_shape_key_to = mesh_target.data.shape_keys.key_blocks[-1]

        #4: Change the name of the new shape key on mesh_target to be same as the name of the shape key on mesh_source
        new_shape_key_to.name = shapekey_from.name

        #5: Adjust the current shapekey value to 0
        shapekey_from.value = 0



    #at the end reset shape key lock for both meshes so the shape keys can be previewed
    mesh_source.show_only_shape_key = True
    mesh_target.show_only_shape_key = True
    


def get_is_problem_jaw_bone_var():
    #store active scene to variable
    scene = bpy.context.scene
    #allow access to user inputted properties through pointer
    #to properties
    fixdbdanimtool = scene.fixdbdanim_tool

    return fixdbdanimtool.is_problem_jaw_bone


#--------------------------------Show feedback to user class and function

#class that is shown when a message needs to 
#pop up for the user as feedback
class TRANSFERSHAPEKEYS_OT_show_message(bpy.types.Operator):
    bl_idname = "transfershapekeys.show_message_operator"
    bl_label = ""
    bl_description = "Show Message for PSK PSA importer"
    bl_options = {'REGISTER'}
    message: bpy.props.StringProperty(default="Message Dummy")
    called: bpy.props.BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=700)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text=self.message)

    def execute(self, context):
        if not self.called:
            wm = context.window_manager
            self.called = True
            return wm.invoke_props_dialog(self, width=700)
        return {'FINISHED'}

#function used to log to console success and error messages
def log(msg):
    print("[Transfer Shape Keys]:", msg)


#------------------------------function to allow user object selection dropdown box to work properly
#filter the callback function to only show meshes
def filter_callback_only_meshes(self, object):
    return object.type == 'MESH'




classes = [transfer_shape_keys_properties, TRANSFERSHAPEKEYS_PT_main_panel,

TRANSFERSHAPEKEYS_OT_transfer_shapekeys,

TRANSFERSHAPEKEYS_OT_show_message]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    #register transfershapekeys_tool as a type which has all
    #the user input properties from the properties class
    #use a unique name so you don't stop other add ons
    #working which also register pointer properties
    bpy.types.Scene.transfershapekeys_tool = bpy.props.PointerProperty(type = transfer_shape_keys_properties)

    #create a pointer property to select an object
    #this will create a dropdown so a user can select objects
    #we use the poll to filter so you can only select meshes
    bpy.types.Scene.mesh_source = bpy.props.PointerProperty(
        name="Source Mesh",
        type=bpy.types.Object,
        poll=filter_callback_only_meshes)

    #create a pointer property to select an object
    #this will create a dropdown so a user can select objects
    #we use the poll to filter so you can only select meshes
    bpy.types.Scene.mesh_target = bpy.props.PointerProperty(
        name="Target Mesh",
        type=bpy.types.Object,
        poll=filter_callback_only_meshes)
 
def unregister():
    #unregister in reverse order to registered so classes relying on other classes
    #will not lead to an error
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
    #unregister transfershapekeys_tool as a type
    del bpy.types.Scene.transfershapekeys_tool
    del bpy.types.Scene.mesh_source
    del bpy.types.Scene.mesh_target
 
 
if __name__ == "__main__":
    register()