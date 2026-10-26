SIM ?= icarus
TOPLEVEL_LANG= verilog
VERILOG_SOURCES += $(PWD)/../rtl/apb_v3_sram.sv
COMPILE_ARGS += -g2012

export PYTHONPATH := $(PWD)/../tb/:$(PYTHONPATH)
apb:
	$(MAKE) sim COCOTB_TEST_MODULES=test_lib.apb_test COCOTB_TOPLEVEL=apb_v3_sram

include $(shell cocotb-config --makefiles)/Makefile.sim
