# PlatformIO Upload Report

Date: 2024-09-29 00:30:46

## Command: `pio run --target clean`

**Status:** Success

**Execution Time:** 1.08 seconds

**Output:**

```
Processing bluepill_f103c8 (platform: ststm32; board: bluepill_f103c8; framework: arduino)
--------------------------------------------------------------------------------
Verbose mode can be enabled via `-v, --verbose` option
Removing .pio/build/bluepill_f103c8
Done cleaning
========================= [SUCCESS] Took 0.46 seconds =========================

```

---

## Command: `pio run`

**Status:** Success

**Execution Time:** 13.82 seconds

**Output:**

```
Processing bluepill_f103c8 (platform: ststm32; board: bluepill_f103c8; framework: arduino)
--------------------------------------------------------------------------------
Verbose mode can be enabled via `-v, --verbose` option
CONFIGURATION: https://docs.platformio.org/page/boards/ststm32/bluepill_f103c8.html
PLATFORM: ST STM32 (17.5.0) > BluePill F103C8
HARDWARE: STM32F103C8T6 72MHz, 20KB RAM, 64KB Flash
DEBUG: Current (stlink) External (blackmagic, cmsis-dap, jlink, stlink)
PACKAGES: 
 - framework-arduinoststm32 @ 4.20801.240815 (2.8.1) 
 - framework-cmsis @ 2.50900.0 (5.9.0) 
 - toolchain-gccarmnoneeabi @ 1.120301.0 (12.3.1)
LDF: Library Dependency Finder -> https://bit.ly/configure-pio-ldf
LDF Modes: Finder ~ chain, Compatibility ~ soft
Found 15 compatible libraries
Scanning dependencies...
Dependency Graph
|-- RadioHead @ 1.120.0
|-- SPI @ 1.1.0
Building in release mode
Compiling .pio/build/bluepill_f103c8/USBDevice/src/USBSerial.cpp.o
Compiling .pio/build/bluepill_f103c8/USBDevice/src/cdc/cdc_queue.c.o
Compiling .pio/build/bluepill_f103c8/USBDevice/src/cdc/usbd_cdc.c.o
Compiling .pio/build/bluepill_f103c8/USBDevice/src/cdc/usbd_cdc_if.c.o
Compiling .pio/build/bluepill_f103c8/USBDevice/src/hid/usbd_hid_composite.c.o
Compiling .pio/build/bluepill_f103c8/USBDevice/src/hid/usbd_hid_composite_if.c.o
Compiling .pio/build/bluepill_f103c8/USBDevice/src/usb_device_core.c.o
Compiling .pio/build/bluepill_f103c8/USBDevice/src/usb_device_ctlreq.c.o
Compiling .pio/build/bluepill_f103c8/USBDevice/src/usb_device_ioreq.c.o
Compiling .pio/build/bluepill_f103c8/USBDevice/src/usbd_conf.c.o
Compiling .pio/build/bluepill_f103c8/USBDevice/src/usbd_desc.c.o
Compiling .pio/build/bluepill_f103c8/USBDevice/src/usbd_ep_conf.c.o
Compiling .pio/build/bluepill_f103c8/USBDevice/src/usbd_if.c.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduinoVariant/PeripheralPins.c.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduinoVariant/PeripheralPins_MALYANM200_F103CB.c.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduinoVariant/generic_clock.c.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduinoVariant/startup_M200_f103xb.S.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduinoVariant/variant_AFROFLIGHT_F103CB.cpp.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduinoVariant/variant_MALYANM200_F103CB.cpp.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduinoVariant/variant_MAPLEMINI_F103CB.cpp.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduinoVariant/variant_PILL_F103Cx.cpp.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduinoVariant/variant_generic.cpp.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_adc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_adc_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_can.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_cec.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_comp.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_comp_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_cordic.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_cortex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_crc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_crc_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_cryp.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_cryp_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_dac.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_dac_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_dcache.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_dcmi.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_dcmi_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_dfsdm.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_dfsdm_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_dma.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_dma2d.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_dma_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_dsi.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_dts.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_eth.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_eth_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_exti.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_fdcan.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_firewall.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_flash.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_flash_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_flash_ramfunc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_fmac.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_fmpi2c.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_fmpi2c_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_fmpsmbus.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_fmpsmbus_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_gfxmmu.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_gfxtim.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_gpio.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_gpio_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_gpu2d.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_gtzc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_hash.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_hash_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_hcd.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_hrtim.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_hsem.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_i2c.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_i2c_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_i2s.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_i2s_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_i3c.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_icache.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_ipcc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_irda.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_iwdg.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_jpeg.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_lcd.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_lptim.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_ltdc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_ltdc_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_mdf.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_mdios.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_mdma.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_mmc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_mmc_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_nand.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_nor.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_opamp.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_opamp_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_ospi.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_otfdec.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_pccard.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_pcd.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_pcd_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_pka.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_pssi.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_pwr.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_pwr_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_qspi.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_ramcfg.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_ramecc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_rcc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_rcc_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_rng.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_rng_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_rtc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_rtc_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_sai.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_sai_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_sd.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_sd_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_sdadc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_sdram.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_smartcard.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_smartcard_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_smbus.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_smbus_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_spdifrx.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_spi.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_spi_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_sram.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_subghz.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_swpmi.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_tim.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_tim_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_tsc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_uart.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_uart_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_usart.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_usart_ex.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_wwdg.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HAL/stm32yyxx_hal_xspi.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/HardwareTimer.cpp.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_adc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_bdma.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_comp.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_cordic.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_crc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_crs.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_dac.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_delayblock.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_dlyb.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_dma.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_dma2d.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_exti.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_fmac.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_fmc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_fmpi2c.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_fsmc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_gpio.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_hrtim.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_i2c.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_i3c.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_icache.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_lpgpio.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_lptim.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_lpuart.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_mdma.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_opamp.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_pka.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_pwr.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_rcc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_rng.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_rtc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_sdmmc.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_spi.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_swpmi.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_tim.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_ucpd.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_usart.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_usb.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/LL/stm32yyxx_ll_utils.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/new.cpp.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/stm32/PortNames.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/stm32/analog.cpp.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/stm32/bootloader.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/stm32/clock.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/stm32/core_callback.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/stm32/dwt.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/stm32/hw_config.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/stm32/interrupt.cpp.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/stm32/otp.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/stm32/pinmap.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/stm32/stm32_def.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/stm32/system_stm32yyxx.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/stm32/timer.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/stm32/uart.c.o
Compiling .pio/build/bluepill_f103c8/SrcWrapper/src/syscalls.c.o
Compiling .pio/build/bluepill_f103c8/src/main.cpp.o
Compiling .pio/build/bluepill_f103c8/lib6b7/SPI/SPI.cpp.o
Compiling .pio/build/bluepill_f103c8/lib6b7/SPI/utility/spi_com.c.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RHCRC.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RHDatagram.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RHEncryptedDriver.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RHGenericDriver.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RHGenericSPI.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RHHardwareSPI.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RHMesh.cpp.o
Archiving .pio/build/bluepill_f103c8/lib6b7/libSPI.a
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RHNRFSPIDriver.cpp.o
Indexing .pio/build/bluepill_f103c8/lib6b7/libSPI.a
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RHReliableDatagram.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RHRouter.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RHSPIDriver.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RHSoftwareSPI.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RH_ABZ.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RH_ASK.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RH_CC110.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RH_E32.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RH_LoRaFileOps.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RH_MRF89.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RH_NRF24.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RH_NRF51.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RH_NRF905.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RH_RF22.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RH_RF24.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RH_RF69.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RH_RF95.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RH_Serial.cpp.o
Compiling .pio/build/bluepill_f103c8/lib299/RadioHead/RH_TCP.cpp.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/HardwareSerial.cpp.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/IPAddress.cpp.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/Print.cpp.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/RingBuffer.cpp.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/Stream.cpp.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/Tone.cpp.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/WInterrupts.cpp.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/WMath.cpp.o
Archiving .pio/build/bluepill_f103c8/lib299/libRadioHead.a
Indexing .pio/build/bluepill_f103c8/lib299/libRadioHead.a
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/WSerial.cpp.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/WString.cpp.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/abi.cpp.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/avr/dtostrf.c.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/board.c.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/core_debug.c.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/hooks.c.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/itoa.c.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/main.cpp.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/pins_arduino.c.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/stm32/startup_stm32yyxx.S.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/wiring_analog.c.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/wiring_digital.c.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/wiring_pulse.cpp.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/wiring_shift.c.o
Compiling .pio/build/bluepill_f103c8/FrameworkArduino/wiring_time.c.o
Archiving .pio/build/bluepill_f103c8/libFrameworkArduino.a
Indexing .pio/build/bluepill_f103c8/libFrameworkArduino.a
Linking .pio/build/bluepill_f103c8/firmware.elf
Checking size .pio/build/bluepill_f103c8/firmware.elf
Advanced Memory Usage is available via "PlatformIO Home > Project Inspect"
RAM:   [===       ]  25.1% (used 5140 bytes from 20480 bytes)
Flash: [=======   ]  72.6% (used 47592 bytes from 65536 bytes)
Building .pio/build/bluepill_f103c8/firmware.bin
========================= [SUCCESS] Took 13.51 seconds =========================
In file included from .pio/libdeps/bluepill_f103c8/RadioHead/RH_LoRaFileOps.cpp:5:
.pio/libdeps/bluepill_f103c8/RadioHead/RH_LoRaFileOps.h:27:2: warning: #warning RH_LoRaFileOps unfinished [-Wcpp]
   27 | #warning RH_LoRaFileOps unfinished
      |  ^~~~~~~
/home/sam/.platformio/packages/toolchain-gccarmnoneeabi/bin/../lib/gcc/arm-none-eabi/12.3.1/../../../../arm-none-eabi/bin/ld: warning: .pio/build/bluepill_f103c8/firmware.elf has a LOAD segment with RWX permissions

```

---

## Command: `pio run --target upload`

**Status:** Success

**Execution Time:** 8.49 seconds

**Output:**

```
Processing bluepill_f103c8 (platform: ststm32; board: bluepill_f103c8; framework: arduino)
--------------------------------------------------------------------------------
Verbose mode can be enabled via `-v, --verbose` option
CONFIGURATION: https://docs.platformio.org/page/boards/ststm32/bluepill_f103c8.html
PLATFORM: ST STM32 (17.5.0) > BluePill F103C8
HARDWARE: STM32F103C8T6 72MHz, 20KB RAM, 64KB Flash
DEBUG: Current (stlink) External (blackmagic, cmsis-dap, jlink, stlink)
PACKAGES: 
 - framework-arduinoststm32 @ 4.20801.240815 (2.8.1) 
 - framework-cmsis @ 2.50900.0 (5.9.0) 
 - tool-dfuutil @ 1.11.0 
 - tool-dfuutil-arduino @ 1.11.0 
 - tool-openocd @ 3.1200.0 (12.0) 
 - tool-stm32duino @ 1.0.1 
 - toolchain-gccarmnoneeabi @ 1.120301.0 (12.3.1)
LDF: Library Dependency Finder -> https://bit.ly/configure-pio-ldf
LDF Modes: Finder ~ chain, Compatibility ~ soft
Found 15 compatible libraries
Scanning dependencies...
Dependency Graph
|-- RadioHead @ 1.120.0
|-- SPI @ 1.1.0
Building in release mode
Checking size .pio/build/bluepill_f103c8/firmware.elf
Advanced Memory Usage is available via "PlatformIO Home > Project Inspect"
RAM:   [===       ]  25.1% (used 5140 bytes from 20480 bytes)
Flash: [=======   ]  72.6% (used 47592 bytes from 65536 bytes)
Configuring upload protocol...
AVAILABLE: blackmagic, cmsis-dap, dfu, jlink, mbed, stlink
CURRENT: upload_protocol = stlink
Uploading .pio/build/bluepill_f103c8/firmware.elf
========================= [SUCCESS] Took 7.94 seconds =========================
xPack Open On-Chip Debugger 0.12.0-01004-g9ea7f3d64-dirty (2023-01-30-15:03)
Licensed under GNU GPL v2
For bug reports, read
	http://openocd.org/doc/doxygen/bugs.html
debug_level: 1

hla_swd
none separate

[stm32f1x.cpu] halted due to debug-request, current mode: Thread 
xPSR: 0x01000000 pc: 0x080025e0 msp: 0x20005000
** Programming Started **
Warn : Adding extra erase range, 0x0800bb24 .. 0x0800bbff
** Programming Finished **
** Verify Started **
** Verified OK **
** Resetting Target **
shutdown command invoked

```

---

