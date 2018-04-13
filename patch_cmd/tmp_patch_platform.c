--- ./tmp_file	2018-04-13 21:21:39.199138659 +0800
+++ /home/cooli7wa/ost1/official_release/2018_4_13_6763_o_v01_stable_2.7.0/Android/alps/./vendor/mediatek/proprietary/bootable/bootloader/preloader/platform/mt6763/src/drivers/platform.c	2018-04-13 09:13:59.065139524 +0800
@@ -1206,20 +1206,26 @@
 	if ( 0x0 == ver )
 		sw_ver = CHIP_SW_VER_01;
 	else
 		sw_ver = CHIP_SW_VER_02;
 #ifdef SLT
         print("chip uid: 0x%x 0x%x\n", get_chip_uid(), get_chip_uid2());
 #endif
 	return sw_ver;
 }
 
+#if CFG_MICROTRUST_TEE_SUPPORT
+u32 platform_chip_hw_code(void)
+{
+    return DRV_Reg32(APHW_CODE);
+}
+#endif
 
 // ------------------------------------------------
 // detect download mode
 // ------------------------------------------------
 
 bool platform_com_wait_forever_check(void)
 {
 #ifdef USBDL_DETECT_VIA_KEY
     /* check download key */
     if (TRUE == mtk_detect_key(COM_WAIT_KEY)) {
