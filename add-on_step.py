#add-on to add a step fcurve modifier to all fcurves selected objects

bl_info = {
    'name' : 'Step',
    'author' : 'Hans Willem Gijzel',
    'version' : (1, 0),
    'blender' : (2, 80, 1  ),
    'location' : 'View 3D > Tools > Step',
    'description' : 'Adds a step modifier to every fcurve',
    'warning' : '',
    'wiki_url' : '',
    'category' : 'Step'
    }

#imports
import bpy

#setup some global scene properties
class MyPropertyGroup(bpy.types.PropertyGroup):
    bpy.types.Scene.prop_step_value = bpy.props.IntProperty(min=1, name='Steps', default=2)

#add step modifier or remove all modifiers (if n = -1)
def main_step(n):
    a = bpy.context.area.type
    #get selected object
    obs = bpy.context.selected_objects
    for ob in obs:
    #get curves and add step modifier
        fc = ob.animation_data.action.fcurves
        for i in fc:
            #remove ALL modifiers
            for j in i.modifiers:
                i.modifiers.remove(j)
            #add step modifier
            if n != -1:
                mod = i.modifiers.new(type='STEPPED')
                mod.frame_step = n
            
            #update modifiers otherwise you have to touch the fcruves with the mouse first for it to work
            i.modifiers.update()

#panel class
class STEPPANEL_PT_Panel(bpy.types.Panel):
    #panel attributes
    """Tooltip"""
    bl_label = 'Step'
    bl_idname = 'STEP_PT_Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Step'
    
    #draw loop
    def draw(self, context):
        layout = self.layout
        col = layout.column(align = True)
        col.prop(context.scene, 'prop_step_value', slider=False)
        col.operator('script.add_step_modifier', text='Add')
        col.operator('script.remove_all_modifiers', text='Remove')
        
#operator class
class ADDSTEPMODIFIER_OT_Operator(bpy.types.Operator):
    #operator attributes
    """Tooltip"""
    bl_label = 'Add Modifier'
    bl_idname = 'script.add_step_modifier'
    
    #poll - if the poll function returns False, the button will be greyed out
    @classmethod
    def poll(cls, context):
        return len(bpy.context.selected_objects) > 0
    
    #execute
    def execute(self, context):
        main_step(bpy.context.scene.prop_step_value)
        return {'FINISHED'}
    
#operator class
class REMOVEALLMODIFIERS_OT_Operator(bpy.types.Operator):
    #operator attributes
    """Tooltip"""
    bl_label = 'Remove All Modifiers'
    bl_idname = 'script.remove_all_modifiers'
    
    #poll - if the poll function returns False, the button will be greyed out
    @classmethod
    def poll(cls, context):
        return len(bpy.context.selected_objects) > 0
    
    #execute
    def execute(self, context):
        main_step(-1)
        return {'FINISHED'}
      
#registration
classes = (
    STEPPANEL_PT_Panel,
    ADDSTEPMODIFIER_OT_Operator,
    REMOVEALLMODIFIERS_OT_Operator,
    MyPropertyGroup
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


#enable to test the addon by running this script
if __name__ == '__main__':
    register()
