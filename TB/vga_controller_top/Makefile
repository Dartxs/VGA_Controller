TOPLEVEL_LANG = verilog
SIM = verilator

VERILOG_SOURCES = \
	../../RTL/*.sv \
	../../package/vga_controller_pkg.sv

TOPLEVEL = vga_controller_top
COCOTB_TEST_MODULES = test_vga_controller_top

EXTRA_ARGS += --trace --trace-structs
EXTRA_ARGS += -I../../package

export PYTHONPATH := ..:$(PYTHONPATH)

include $(shell cocotb-config --makefiles)/Makefile.sim