# SPDX-License-Identifier: MIT OR GPL-3.0-or-later
from types import SimpleNamespace
from typing import cast
from unittest import main

import bpy
from bpy.types import Armature, Context

from io_scene_vrm.common import ops
from io_scene_vrm.editor.extension import get_armature_extension
from io_scene_vrm.editor.vrm1.property_group import Vrm1LookAtPropertyGroup
from tests.util import AddonTestCase


class RenderContextTests(AddonTestCase):
    def test_restricted_render_context_updates_only_visible_armatures(self) -> None:
        ops.icyp.make_basic_armature()
        armature = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
        self.assertIsInstance(armature.data, Armature)
        vrm1 = get_armature_extension(armature.data).vrm1
        head = next(b for b in armature.pose.bones if b.parent)
        vrm1.humanoid.human_bones.head.node.bone_name = head.name
        target = bpy.data.objects.new("LookAt target", None)
        bpy.context.scene.collection.objects.link(target)
        target.location = (1, -3, 2)
        bpy.context.view_layer.update()
        look_at = vrm1.look_at
        look_at.enable_preview = True
        look_at.preview_target_bpy_object = target
        look_at.previous_preview_matrix = [0.0] * 16
        context = cast("Context", SimpleNamespace(view_layer=bpy.context.view_layer))
        Vrm1LookAtPropertyGroup.update_all_previews(context)
        self.assertNotEqual(list(look_at.previous_preview_matrix), [0.0] * 16)
        armature.hide_set(True)
        look_at.previous_preview_matrix = [0.0] * 16
        Vrm1LookAtPropertyGroup.update_all_previews(context)
        self.assertEqual(list(look_at.previous_preview_matrix), [0.0] * 16)

    def test_no_view_layer_is_safe(self) -> None:
        Vrm1LookAtPropertyGroup.update_all_previews(cast("Context", SimpleNamespace()))

    def test_viewport_visibility_remains_authoritative(self) -> None:
        context = cast(
            "Context",
            SimpleNamespace(visible_objects=[], view_layer=bpy.context.view_layer),
        )
        Vrm1LookAtPropertyGroup.update_all_previews(context)


if __name__ == "__main__":
    main()
