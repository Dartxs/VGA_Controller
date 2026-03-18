TOPLEVEL_LANG = verilog
SIM = verilator

VERILOG_SOURCES = \
	../../../RTL/vga_timing.sv \
	../../../package/vga_controller_pkg.sv

TOPLEVEL = vga_timing
COCOTB_TEST_MODULES = test_vga_timing

EXTRA_ARGS += --trace --trace-structs
EXTRA_ARGS += -I../../../package

export PYTHONPATH := ..:$(PYTHONPATH)

include $(shell cocotb-config --makefiles)/Makefile.sim