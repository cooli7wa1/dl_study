--- ./tmp_file	2018-04-13 21:21:39.171139199 +0800
+++ /home/cooli7wa/ost1/official_release/2018_4_13_6763_o_v01_stable_2.7.0/Android/alps/./vendor/mediatek/proprietary/bootable/bootloader/preloader/platform/mt6763/feature.mak	2018-04-13 09:13:59.065139524 +0800
@@ -582,24 +582,43 @@
 
 ifdef CFG_TEE_VIRTUAL_RPMB_SUPPORT
 C_OPTION += -DCFG_TEE_VIRTUAL_RPMB_SUPPORT="$(CFG_TEE_VIRTUAL_RPMB_SUPPORT)"
 export CFG_TEE_VIRTUAL_RPMB_SUPPORT
 endif
 ifdef CFG_TRUSTONIC_TEE_SUPPORT
 C_OPTION += -DCFG_TRUSTONIC_TEE_SUPPORT="$(CFG_TRUSTONIC_TEE_SUPPORT)"
 export CFG_TRUSTONIC_TEE_SUPPORT
 endif
 
+ifdef CFG_MICROTRUST_TEE_SUPPORT
+C_OPTION += -DCFG_MICROTRUST_TEE_SUPPORT="$(CFG_MICROTRUST_TEE_SUPPORT)"
+export CFG_MICROTRUST_TEE_SUPPORT
+endif
 
+ifdef CFG_MICROTRUST_TEE_MIN_MEM_SUPPORT
+C_OPTION += -DCFG_MICROTRUST_TEE_MIN_MEM_SUPPORT="$(CFG_MICROTRUST_TEE_MIN_MEM_SUPPORT)"
+export CFG_MICROTRUST_TEE_MIN_MEM_SUPPORT
+endif
 
+ifeq ("$(CFG_MICROTRUST_SVP_SUPPORT)","1")
+C_OPTION += -DMTK_SEC_VIDEO_PATH_SUPPORT
+endif
 
+ifdef CFG_MICROTRUST_TUI_SUPPORT
+C_OPTION += -DCFG_MICROTRUST_TUI_SUPPORT="$(CFG_MICROTRUST_TUI_SUPPORT)"
+export CFG_MICROTRUST_TUI_SUPPORT
+endif
 
+ifdef CFG_MICROTRUST_GP_SUPPORT
+C_OPTION += -DCFG_MICROTRUST_GP_SUPPORT="$(CFG_MICROTRUST_GP_SUPPORT)"
+export CFG_MICROTRUST_GP_SUPPORT
+endif
 ifdef CFG_TEE_SECURE_MEM_PROTECTED
 C_OPTION += -DCFG_TEE_SECURE_MEM_PROTECTED="$(CFG_TEE_SECURE_MEM_PROTECTED)"
 export CFG_TEE_SECURE_MEM_PROTECTED
 endif
 
 ifdef CFG_TEE_TRUSTED_APP_HEAP_SIZE
 C_OPTION += -DCFG_TEE_TRUSTED_APP_HEAP_SIZE="$(CFG_TEE_TRUSTED_APP_HEAP_SIZE)"
 export CFG_TEE_TRUSTED_APP_HEAP_SIZE
 endif
 
