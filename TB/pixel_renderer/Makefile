TOPLEVEL_LANG = verilog
SIM = verilator

VERILOG_SOURCES = \
	../../RTL/pixel_renderer.sv \
	../../package/vga_controller_pkg.sv

TOPLEVEL = pixel_renderer
COCOTB_TEST_MODULES = test_pixel_renderer

EXTRA_ARGS += --trace --trace-structs
EXTRA_ARGS += -I../../package

export PYTHONPATH := ..:$(PYTHONPATH)

include $(shell cocotb-config --makefiles)/Makefile.sim