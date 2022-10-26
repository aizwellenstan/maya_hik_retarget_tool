# Maya Human Retarget

### Without UI
```
import sys
sys.path.append(r"I:\script\bin\td\maya\scripts\mocapConvert\merge")
import merge
reload(merge)
sourceFile = "T:/xrs_mocap/work/prod/ani/PartyOnRollup_cut001_v01_t002/tests/PartyOnRollup_cut001_Kai_v01.fbx"
targetFile = "T:/xrs_mocap/work/prod/ani/PartyOnRollup_cut001_v01_t002/tests/P_M_H_E01_01_mocap.fbx"
merge.main(sourceFile, targetFile)
```

### UI
```
import sys
sys.path.append(r"I:\script\bin\td\maya\scripts\mocapConvert\merge")
import merge_ui
reload(merge_ui)
merge_ui.run()
```

## Script Flow
1. Open New Scene
2. Get Default Hik List
3. Import Source Fbx
4. Rename Fbx with 'source:' namespace
5. Save source hik to list
6. Import Target Fbx
7. Get Target Hik from diff between cuurent hik list and default+source hik list
8. Retarget target Hik to source
9. bake
