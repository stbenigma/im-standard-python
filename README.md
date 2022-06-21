# The toolsuite around Information Modeling and the Information Cadastre

[![Build status](https://github.com/foryouandyourcustomers/fyyccim-tools/actions/workflows/Quality.yaml/badge.svg)](https://github.com/foryouandyourcustomers/fyyccim-tools/actions) ![cod cov](https://img.shields.io/badge/coverage-85%25-seagreen)

The tools provided by
<a href="https://foryouandyourcustomers.com" style="color: #F79724; text-decoration: underline;text-decoration-style: dotted; font-family: Roboto; font-size: 24">
foryouandyourcustomers</a>
to work with the [Information Model](https://www.informationsmodellierung.ch/)
and to operate the <span style="font-family:FreeSet">Information Cadastre</span>.

### The Information Model

The methodology created by
<a href="mailto:stb@foryouandyourcustomers.com">Stefan Berner</a>
to precisely describe business semantics, terms and relations.

The information model encompasses the [business glossary](https://www.dataversity.net/what-is-a-business-glossary/#) and
[ontology](https://en.wikipedia.org/wiki/Ontology_(information_science))
of your domain of work.

### The Information Cadastre

The <span style="font-family:FreeSet">Information Cadastre</span> encompasses tools and processes around the Information
Model to support maintenance and publication of content.

# Tooling
[invoke](https://www.pyinvoke.org/) is the tool to bootstrap and execute various tasks.
Use `invoke --list` for a list of tasks or consult the source `./tasks.py`.

To generate or update the single source of definition (SSOD) including the whole documentation, run
<br>
`inv gen -m [PathToYourModelDirectory]\IM --all`

## Bootstrapping and installation
Bootstrap your Anaconda environment:

```conda env update --file conda-base-environment.yaml```

```invoke bootstrap```