--- ./tmp_file	2018-04-13 21:21:39.323136270 +0800
+++ /home/cooli7wa/ost1/official_release/2018_4_13_6763_o_v01_stable_2.7.0/Android/alps/./device/mediatek/common/device.mk	2018-04-13 09:13:59.065139524 +0800
@@ -2065,20 +2065,28 @@
   PRODUCT_PACKAGES += gatekeeper.trusty
   PRODUCT_PACKAGES += keystore.trusty
   PRODUCT_PACKAGES += storageproxyd
   PRODUCT_PACKAGES += libtrusty
   PRODUCT_PACKAGES += kmsetkey.trusty
   PRODUCT_PROPERTY_OVERRIDES += ro.hardware.gatekeeper=trusty
   PRODUCT_PROPERTY_OVERRIDES += ro.hardware.keystore=trusty
   PRODUCT_PROPERTY_OVERRIDES += ro.hardware.kmsetkey=trusty
 endif
 
+ifeq ($(strip $(MICROTRUST_TEE_SUPPORT)), yes)
+  PRODUCT_PACKAGES += teei_daemon
+  PRODUCT_PACKAGES += init_thh
+#  PRODUCT_PACKAGES += libteei_fp
+#  PRODUCT_PACKAGES += libfingerprint_tac
+  PRODUCT_PROPERTY_OVERRIDES += ro.mtk_microtrust_tee_support=1
+  include device/mediatek/common/microtrust/device.microtrust.mk
+endif
 
 ifeq ($(strip $(MTK_SEC_VIDEO_PATH_SUPPORT)), yes)
   PRODUCT_PROPERTY_OVERRIDES += ro.mtk_sec_video_path_support=1
   ifeq ($(filter $(MTK_IN_HOUSE_TEE_SUPPORT) $(MTK_GOOGLE_TRUSTY_SUPPORT),yes),yes)
   PRODUCT_PACKAGES += lib_uree_mtk_video_secure_al
   endif
 endif
 
 #################################################
 #DRM part
