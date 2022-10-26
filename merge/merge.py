#!/usr/bin/python
# -*- coding: utf-8 -*-
import maya.cmds as cmds
import pymel.core as pm
from maya import mel

def GetHikList():
    mel.eval("HIKCharacterControlsTool;")
    _HUMAN_IK_SOURCE_MENU = "hikSourceList"
    _HUMAN_IK_SOURCE_MENU_OPTION = _HUMAN_IK_SOURCE_MENU + "|OptionMenu"
    items = cmds.optionMenuGrp(_HUMAN_IK_SOURCE_MENU, q=True, ill=True)

    hikList = []
    for i in xrange(0, len(items)):
        label = cmds.menuItem(items[i], q=True, l=True)
        hikList.append(label)

    return hikList

def GetCurrentHikCharacter():
    """
    ....Get the current active character definition.
    ...."""

    mel.eval("HIKCharacterControlsTool;")
    char = mel.eval("hikGetCurrentCharacter();")
    return char

def hikUpdateTool():
    melCode = """
        if ( hikIsCharacterizationToolUICmdPluginLoaded() )
        {
            hikUpdateCharacterList();
            hikUpdateCurrentCharacterFromUI();
            hikUpdateContextualUI();
            hikControlRigSelectionChangedCallback;
            hikUpdateSourceList();
            hikUpdateCurrentSourceFromUI();
            hikUpdateContextualUI();
            hikControlRigSelectionChangedCallback;
        }
        """
    try:
        mel.eval(melCode)
    except:
        pass

def SetHikChar(targetChar):
    mel.eval("HIKCharacterControlsTool;")
    mel.eval('hikSetCurrentCharacter("{0}")'.format(targetChar))
    hikUpdateTool()

def SetHikSourceChar(source):
    _HUMAN_IK_SOURCE_MENU = "hikSourceList"
    _HUMAN_IK_SOURCE_MENU_OPTION = _HUMAN_IK_SOURCE_MENU + "|OptionMenu"
    items = cmds.optionMenuGrp(_HUMAN_IK_SOURCE_MENU, q=True, ill=True)
    for i in xrange(0, len(items)):
        label = cmds.menuItem(items[i], q=True, l=True)

        # 空白が頭に入っているので除去
        if label.lstrip() == source:
            cmds.optionMenu(_HUMAN_IK_SOURCE_MENU_OPTION, e=True, sl=i + 1)
            mel.eval("hikUpdateCurrentSourceFromUI()")
            mel.eval("hikUpdateContextualUI()")
            mel.eval("hikControlRigSelectionChangedCallback")
            break

def isCharacterDefinition(char):
	# Check Node Exists
	if not cmds.objExists(char): return False
	
	# Check Node Type
	if cmds.objectType(char) != 'HIKCharacterNode': return False
	
	return True

def getCharacterNodes(char):
    # Check Node
    if not isCharacterDefinition(char):
        raise Exception(
            'Invalid character definition node! Object "'
            + char
            + '" does not exist or is not a valid HIKCharacterNode!'
        )

    # Get Character Nodes
    charNodes = mel.eval('hikGetSkeletonNodes "' + char + '"')

    # Return Result
    return charNodes

def bake(char, start, end):
    cmds.playbackOptions(min=start, max=end)

    bones = getCharacterNodes(char)

    # Bake Animation
    cmds.bakeResults(
        bones,
        simulation=True,
        t=(start, end),
        sampleBy=1,
        disableImplicitControl=True,
        preserveOutsideKeys=False,
        sparseAnimCurveBake=False,
        removeBakedAttributeFromLayer=False,
        bakeOnOverrideLayer=False,
        minimizeRotation=False,
        at=["tx", "ty", "tz", "rx", "ry", "rz"],
    )

def main(sourceFile, targetFile):
    cmds.file(new=True, force=True)
    defaultHikList = GetHikList()
    cmds.file(sourceFile, i=True, force=True)
    allTransform = cmds.ls()
    cmds.select(allTransform)
    for i in allTransform:
        try:
            oldName = i.split("|")[-1]
            newName = ":source:{}".format(oldName)
            if ":" in oldName:
                newName = ":source:" + oldName.split(":")[-1]
            new = cmds.rename(oldName, newName)
        except:
            continue

    joints = cmds.ls("*:*", long=True, type="joint")
    cmds.select(joints)
    all_keys = sorted(cmds.keyframe(joints, q=True) or [])
    if all_keys:
        start = int(all_keys[0])
        end = int(all_keys[-1])
    print(start, end)

    sourceChar = GetCurrentHikCharacter()

    cmds.file(targetFile, i=True, force=True)

    hikList = GetHikList()

    targetChar = ""
    for hik in hikList:
        if hik not in defaultHikList:
            if hik != sourceChar:
                targetChar = hik.lstrip()
                break

    SetHikChar(targetChar)

    SetHikSourceChar(sourceChar)

    bake(targetChar, start, end)
