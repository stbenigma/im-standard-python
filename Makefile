
MSGFMT = @MSGFMT@

LOCALES = pythonWork/pythonSource/SSOT_infra/locales/*/*
POFILES = $(wildcard $(LOCALES)/*.po)
MOFILES = $(patsubst %.po,%.mo,$(POFILES))

.DEFAULT_GOAL := package

$(MOFILES): $(POFILES)
	echo "msgfmt -c $< -o $@"
	msgfmt -c $< -o $@

package: $(MOFILES)
