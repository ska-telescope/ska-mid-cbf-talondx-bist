RAW_PKGS_TO_PUBLISH ?= ska-mid-cbf-talondx-bist

# include RAW packages support
include .make/raw.mk

# include docs support
include .make/docs.mk

# include make support
include .make/make.mk

# include help support
include .make/help.mk

# include core release support
include .make/release.mk
