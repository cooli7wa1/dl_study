--- ./tmp_file	2018-04-13 21:21:39.247137734 +0800
+++ /home/cooli7wa/ost1/official_release/2018_4_13_6763_o_v01_stable_2.7.0/Android/alps/./vendor/mediatek/proprietary/bootable/bootloader/preloader/platform/mt6763/src/security/trustzone/tz_init.c	2018-04-13 09:13:59.065139524 +0800
@@ -45,20 +45,23 @@
 #include "tz_mem.h"
 #include "sec_devinfo.h"
 #include "cust_sec_ctrl.h"
 #include "sec.h"
 #if CFG_TRUSTONIC_TEE_SUPPORT
 #include "tz_tbase.h"
 #endif
 #if CFG_GOOGLE_TRUSTY_SUPPORT
 #include "tz_trusty.h"
 #endif
+#if CFG_MICROTRUST_TEE_SUPPORT
+#include "tz_teei.h"
+#endif
 #include "sec_devinfo.h"
 #include "key_derive.h"
 #include "rpmb_key.h"
 #include <emi_mpu_mt.h>
 #include "log_store_pl.h"
 
 /**************************************************************************
  *  DEBUG FUNCTIONS
  **************************************************************************/
 #define MOD "[TZ_INIT]"
@@ -303,20 +306,23 @@
             DBG_ERR("%s Fail to allocate atf log buffer: 0x%x, 0x%x\n", MOD,
                 ATF_LOG_BUFFER_SIZE, TEE_MEM_ALIGNMENT);
             teearg->atf_log_buf_size = 0;
         }
         save_atf_log_buf_to_log_store();
     }
 #endif
 #endif
 }
 
+#if CFG_MICROTRUST_TEE_SUPPORT
+extern void teei_rtctime_param_prepare(u32 param_addr);
+#endif
 
 void trustzone_post_init(void)
 {
     atf_arg_t_ptr teearg = (atf_arg_t_ptr)trustzone_get_atf_boot_param_addr();
     u32 i;
     u8 rpmb_key[RPMB_KEY_SIZE] = {0};
     u8 fde_key[FDE_KEY_SIZE] = {0};
     int ret = 0;
 
     teearg->atf_magic = ATF_BOOTCFG_MAGIC;
@@ -407,31 +413,38 @@
     teearg->atf_log_buf_size = 0;
     teearg->atf_aee_debug_buf_start = 0;
     teearg->atf_aee_debug_buf_size = 0;
 #endif
     DBG_MSG("%s ATF log buffer start : 0x%x\n", MOD, teearg->atf_log_buf_start);
     DBG_MSG("%s ATF log buffer size : 0x%x\n", MOD, teearg->atf_log_buf_size);
     DBG_MSG("%s ATF aee buffer start : 0x%x\n", MOD, teearg->atf_aee_debug_buf_start);
     DBG_MSG("%s ATF aee buffer size : 0x%x\n", MOD, teearg->atf_aee_debug_buf_size);
 
 #if CFG_TEE_SUPPORT
+#if CFG_MICROTRUST_TEE_SUPPORT
+    teei_key_param_prepare(TEE_PARAMETER_KEY, (u8 *)teearg->hwuid, sizeof(teearg->hwuid), (u8 *)teearg->HRID,
+					sizeof(u32) * teearg->atf_hrid_size, rpmb_key);
+#endif
 
 #if CFG_RPMB_SET_KEY
 #if (CFG_BOOT_DEV == BOOTDEV_SDMMC) // For eMMC project with TEEs
     teearg->tee_rpmb_size = mmc_rpmb_get_size();
 #elif (CFG_BOOT_DEV == BOOTDEV_UFS)
 	teearg->tee_rpmb_size = ufs_rpmb_get_lu_size();
 #endif
 	DBG_MSG("%s TEE RPMB Size : 0x%x\n", MOD, teearg->tee_rpmb_size);
 #endif /* CFG_RPMB_SET_KEY */
 #endif /* CFG_TEE_SUPPORT */
 
+#if CFG_MICROTRUST_TEE_SUPPORT
+    teei_rtctime_param_prepare(TEE_BOOT_ARG_ADDR);
+#endif
     tz_dapc_sec_postinit();
 }
 
 void trustzone_jump(u32 addr, u32 arg1, u32 arg2)
 {
 #if !CFG_BYPASS_EMI
     u32 bl31_reserve = 0; /* Reserved for future in ATF */
 #else
     u32 bl31_reserve = 0;
 #endif
