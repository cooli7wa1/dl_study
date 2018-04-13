#this is platform common Boardconfig

ifneq ($(MTK_GLOBAL_C_INCLUDES)$(MTK_GLOBAL_CFLAGS)$(MTK_GLOBAL_CONLYFLAGS)$(MTK_GLOBAL_CPPFLAGS)$(MTK_GLOBAL_LDFLAGS),)
$(info *** MTK-specific global flags are changed)
$(info *** MTK_GLOBAL_C_INCLUDES: $(MTK_GLOBAL_C_INCLUDES))
$(info *** MTK_GLOBAL_CFLAGS: $(MTK_GLOBAL_CFLAGS))
$(info *** MTK_GLOBAL_CONLYFLAGS: $(MTK_GLOBAL_CONLYFLAGS))
$(info *** MTK_GLOBAL_CPPFLAGS: $(MTK_GLOBAL_CPPFLAGS))
$(info *** MTK_GLOBAL_LDFLAGS: $(MTK_GLOBAL_LDFLAGS))
$(error bailing...)
endif

MTK_GLOBAL_C_INCLUDES:=
MTK_GLOBAL_CFLAGS:=
MTK_GLOBAL_CONLYFLAGS:=
MTK_GLOBAL_CPPFLAGS:=
MTK_GLOBAL_LDFLAGS:=

# Use the non-open-source part, if present
-include vendor/mediatek/common/BoardConfigVendor.mk

# Use the connectivity Boardconfig
include device/mediatek/common/connectivity/BoardConfig.mk

# for flavor build base project assignment
ifeq ($(strip $(MTK_BASE_PROJECT)),)
  MTK_PROJECT_NAME := $(subst full_,,$(TARGET_PRODUCT))
else
  MTK_PROJECT_NAME := $(MTK_BASE_PROJECT)
endif
MTK_PROJECT := $(MTK_PROJECT_NAME)
MTK_PATH_SOURCE := vendor/mediatek/proprietary
MTK_ROOT := vendor/mediatek/proprietary
MTK_PATH_COMMON := vendor/mediatek/proprietary/custom/common
MTK_PATH_CUSTOM := vendor/mediatek/proprietary/custom/$(MTK_PROJECT)
MTK_PATH_CUSTOM_PLATFORM := vendor/mediatek/proprietary/custom/$(MTK_PLATFORM_DIR)
KERNEL_CROSS_COMPILE:= $(abspath $(TOP))/prebuilts/gcc/linux-x86/arm/cit-arm-eabi-4.8/bin/arm-eabi-
TARGET_BOARD_KERNEL_HEADERS :=
ifneq ($(strip $(MTK_PLATFORM)),)
TARGET_BOARD_KERNEL_HEADERS += device/mediatek/$(MTK_PLATFORM_DIR)/kernel-headers
endif
TARGET_BOARD_KERNEL_HEADERS += device/mediatek/common/kernel-headers

MTK_GLOBAL_C_INCLUDES += $(TOPDIR)vendor/mediatek/proprietary/hardware/audio/common/include
MTK_GLOBAL_C_INCLUDES += $(MTK_PATH_CUSTOM)/cgen/cfgdefault $(MTK_PATH_CUSTOM)/cgen/cfgfileinc $(MTK_PATH_CUSTOM)/cgen/inc $(MTK_PATH_CUSTOM)/cgen
ifneq ($(strip $(MTK_PLATFORM)),)
MTK_GLOBAL_C_INCLUDES += $(MTK_PATH_CUSTOM_PLATFORM)/cgen/cfgdefault $(MTK_PATH_CUSTOM_PLATFORM)/cgen/cfgfileinc $(MTK_PATH_CUSTOM_PLATFORM)/cgen/inc $(MTK_PATH_CUSTOM_PLATFORM)/cgen
endif
MTK_GLOBAL_C_INCLUDES += $(MTK_PATH_COMMON)/cgen/cfgdefault $(MTK_PATH_COMMON)/cgen/cfgfileinc $(MTK_PATH_COMMON)/cgen/inc $(MTK_PATH_COMMON)/cgen

# Add MTK compile options to wrap MTK's modifications on AOSP.
ifneq ($(strip $(MTK_BASIC_PACKAGE)),yes)
ifneq ($(strip $(MTK_EMULATOR_SUPPORT)),yes)
  MTK_GLOBAL_CFLAGS += -DMTK_AOSP_ENHANCEMENT
endif
endif

# TODO: remove MTK_PATH_PLATFORM
MTK_PATH_PLATFORM := $(MTK_PATH_SOURCE)/platform/$(MTK_PLATFORM_DIR)
GOOGLE_RELEASE_RIL := no
BUILD_NUMBER := $(shell date +%s)
# reduce BUILD_ID length
ifdef BUILD_ID
ifeq (3,$(words $(subst ., ,$(BUILD_ID))))
N := $(shell echo $(word 1,$(subst ., ,$(BUILD_ID))) | cut -b 1)
M1 := $(shell echo $(word 1,$(subst ., ,$(BUILD_ID))) | cut -b 3-)
ifneq ($(filter M%,$(M1)),)
  M1 := $(patsubst M%,%,$(M1))
else
  M1 := 0
endif
YYMMDD := $(shell echo $(word 2,$(subst ., ,$(BUILD_ID))) | cut -b 3-6)
BUILD_ID := $(N)$(M1)$(YYMMDD)
endif
endif

ifeq ($(strip $(CUSTOM_BUILD_VERNO)),)
  CUSTOM_BUILD_VERNO_HDR := $(shell echo $(firstword $(BUILD_NUMBER)) | cut -b 1-15)
else
  CUSTOM_BUILD_VERNO_HDR := $(shell echo $(firstword $(CUSTOM_BUILD_VERNO)) | cut -b 1-15)
endif

#Enable HWUI by default
USE_OPENGL_RENDERER := true

#SELinux Policy File Configuration
ifeq ($(strip $(MTK_BASIC_PACKAGE)), yes)
BOARD_SEPOLICY_DIRS := \
        device/mediatek/sepolicy/basic/non_plat
BOARD_PLAT_PUBLIC_SEPOLICY_DIR := \
        device/mediatek/sepolicy/basic/plat_public
BOARD_PLAT_PRIVATE_SEPOLICY_DIR := \
        device/mediatek/sepolicy/basic/plat_private
endif
ifeq ($(strip $(MTK_BSP_PACKAGE)), yes)
BOARD_SEPOLICY_DIRS := \
        device/mediatek/sepolicy/basic/non_plat \
        device/mediatek/sepolicy/bsp/non_plat
BOARD_PLAT_PUBLIC_SEPOLICY_DIR := \
        device/mediatek/sepolicy/basic/plat_public \
        device/mediatek/sepolicy/bsp/plat_public
BOARD_PLAT_PRIVATE_SEPOLICY_DIR := \
        device/mediatek/sepolicy/basic/plat_private \
        device/mediatek/sepolicy/bsp/plat_private
endif
ifneq ($(strip $(MTK_BASIC_PACKAGE)), yes)
ifneq ($(strip $(MTK_BSP_PACKAGE)), yes)
BOARD_SEPOLICY_DIRS := \
        device/mediatek/sepolicy/basic/non_plat \
        device/mediatek/sepolicy/bsp/non_plat \
        device/mediatek/sepolicy/full/non_plat
BOARD_PLAT_PUBLIC_SEPOLICY_DIR := \
        device/mediatek/sepolicy/basic/plat_public \
        device/mediatek/sepolicy/bsp/plat_public \
        device/mediatek/sepolicy/full/plat_public
BOARD_PLAT_PRIVATE_SEPOLICY_DIR := \
        device/mediatek/sepolicy/basic/plat_private \
        device/mediatek/sepolicy/bsp/plat_private \
        device/mediatek/sepolicy/full/plat_private

endif
endif

BOARD_SEPOLICY_DIRS += $(wildcard device/mediatek/sepolicy/secure)


ifeq ($(strip $(MTK_YIQI_FONTS_FRAMEWORK_SUPPORT)), yes)
BOARD_SEPOLICY_DIRS +=  frameworks/base/lovelyfontsframework/sepolicy
endif

ifdef CUSTOM_MODEM
  ifeq ($(strip $(TARGET_BUILD_VARIANT)),eng)
    MTK_MODEM_MODULE_MAKEFILES := $(foreach item,$(CUSTOM_MODEM),$(firstword $(wildcard vendor/mediatek/proprietary/modem/$(patsubst %_prod,%,$(item))/Android.mk vendor/mediatek/proprietary/modem/$(item)/Android.mk)))
  else
    MTK_MODEM_MODULE_MAKEFILES := $(foreach item,$(CUSTOM_MODEM),$(firstword $(wildcard vendor/mediatek/proprietary/modem/$(patsubst %_prod,%,$(item))_prod/Android.mk vendor/mediatek/proprietary/modem/$(item)/Android.mk)))
  endif
  BOARD_SEPOLICY_DIRS += $(wildcard $(patsubst %/Android.mk,%/sepolicy/o0,$(firstword $(MTK_MODEM_MODULE_MAKEFILES))))
endif

# Include an expanded selection of fonts
EXTENDED_FONT_FOOTPRINT := true

# ptgen
# Add MTK's MTK_PTGEN_OUT definitions
ifeq (,$(strip $(OUT_DIR)))
  ifeq (,$(strip $(OUT_DIR_COMMON_BASE)))
    MTK_PTGEN_OUT_DIR := $(TOPDIR)out
  else
    MTK_PTGEN_OUT_DIR := $(OUT_DIR_COMMON_BASE)/$(notdir $(PWD))
  endif
else
    MTK_PTGEN_OUT_DIR := $(strip $(OUT_DIR))
endif
ifneq ($(strip $(MTK_TARGET_PROJECT)), $(strip $(MTK_BASE_PROJECT)))
MTK_PTGEN_PRODUCT_OUT := $(MTK_PTGEN_OUT_DIR)/target/product/$(MTK_TARGET_PROJECT)
else
MTK_PTGEN_PRODUCT_OUT := $(MTK_PTGEN_OUT_DIR)/target/product/$(TARGET_DEVICE)
endif
MTK_PTGEN_OUT := $(MTK_PTGEN_PRODUCT_OUT)/obj/PTGEN
MTK_PTGEN_MK_OUT := $(MTK_PTGEN_PRODUCT_OUT)/obj/PTGEN
MTK_PTGEN_TMP_OUT := $(MTK_PTGEN_PRODUCT_OUT)/obj/PTGEN_TMP

TARGET_CUSTOM_OUT := $(MTK_PTGEN_PRODUCT_OUT)/custom

#Add MTK's Recovery fstab definitions
TARGET_RECOVERY_FSTAB := $(MTK_PTGEN_PRODUCT_OUT)/system/vendor/etc/fstab.$(MTK_PLATFORM_DIR)

# Define MTK's Recovery UI resolution
MTK_RECOVERY_MEDIUM_RES := yes

ifeq ($(BUILD_GMS),yes)
  ifeq ($(strip $(MTK_AB_OTA_UPDATER)), yes)
    DONT_DEXPREOPT_PREBUILTS := false
  else
    DONT_DEXPREOPT_PREBUILTS := true
  endif
else
  ifeq ($(TARGET_BUILD_VARIANT),userdebug)
    DEX_PREOPT_DEFAULT := nostripping
  endif
endif

ifeq (yes,$(BUILD_MTK_LDVT))
MTK_RELEASE_GATEKEEPER := no
endif

ALLOW_MISSING_DEPENDENCIES ?= true

DEVICE_MANIFEST_FILE += device/mediatek/$(MTK_PLATFORM_DIR)/manifest.xml
DEVICE_MATRIX_FILE := device/mediatek/$(MTK_PLATFORM_DIR)/compatibility_matrix.xml

#Add MTK's hook
-include vendor/mediatek/build/core/base_rule_hook.mk
-include vendor/mediatek/build/core/base_rule_jack.mk
-include vendor/mediatek/build/core/rpgen.mk
-include device/mediatek/build/core/soong_config.mk
