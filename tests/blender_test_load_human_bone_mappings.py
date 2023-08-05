import json
import tempfile

import bpy


def test() -> None:
    bpy.ops.icyp.make_basic_armature()

    new_head_name = "root"
    with tempfile.NamedTemporaryFile(delete=False) as file:
        file.write(json.dumps({"head": new_head_name}).encode())
        file.close()
        bpy.ops.vrm.load_human_bone_mappings(filepath=file.name)

    data = bpy.context.active_object.data
    if not isinstance(data, bpy.types.Armature):
        raise AssertionError

    b = [
        human_bone
        for human_bone in data.vrm_addon_extension.vrm0.humanoid.human_bones
        if human_bone.bone == "head"
    ][0]
    assert (
        b.node.bone_name == new_head_name
    ), f"head is expected to {new_head_name} but {b.node.bone_name}"


if __name__ == "__main__":
    test()
