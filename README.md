# The toolsuite around Information Modeling and the Information Cadastre

[![Build status](https://github.com/foryouandyourcustomers/fyyccim-tools/actions/workflows/Quality.yaml/badge.svg)](https://github.com/foryouandyourcustomers/fyyccim-tools/actions) ![cod cov](https://img.shields.io/badge/coverage-82%25-seagreen)

The tools provided by
<a href="https://foryouandyourcustomers.com" style="color: #F79724; text-decoration: underline;text-decoration-style: dotted;">
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

The <span style="font-family:FreeSet">Information Cadastre</span> organises the organisation around the Information
Model.

- It supports the method 'information modeling' and publishing its results with various tools.
- It provides guidance in how to set up the work and governance around the Information Model.

# Tooling
[invoke](https://www.pyinvoke.org/) is the tool to bootstrap and execute various tasks.
See `invoke --help` for a list of tasks.

## Bootstrapping and installation
Bootstrap your Anaconda environment:

```conda env update --file conda-base-environment.yaml```

```invoke translate```