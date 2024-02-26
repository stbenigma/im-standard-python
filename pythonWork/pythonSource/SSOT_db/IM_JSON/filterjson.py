# -*- coding: latin-1 -*-
import argparse
from pathlib import Path

from SSOT_db.IM_JSON import JSModel, FILTEREDJSModel
from SSOT_db.IM_OBJECTS import Modelelement


def filterjson(pjsmodel, pstatus = None, pdiagrams=None):

    jsmodel = FILTEREDJSModel(pmodel=pjsmodel.jsmodel, ppublstatus=pstatus, pimdiagrams=pdiagrams)

    return jsmodel

def filterjsonfile(pjsonfile, pdestination, pstatus = None, pdiagrams=None):
    """ reads a jsonfile, applies the filters and creates a new file in pdestination

        return pdestination
    """
    jsonfile = pjsonfile if type(pjsonfile) is str else str(pjsonfile)
    jsmodel = JSModel.readfromfile(pfilename=jsonfile)

    filteredmodel=filterjson(pjsmodel=jsmodel, pstatus=pstatus, pdiagrams=pdiagrams)
    filteredmodel.write_json(pdestination)

    return str(pdestination)


def main():
    """
    parses sysargs, read json file and creates a filtered copy of it

    :param argv:

    :return:
    """
    parser = argparse.ArgumentParser(description='Create filtered json-file.')
    parser.add_argument('jsonfilepath', nargs=1,
                        help=f"Path of the jsonfile to load.")
    parser.add_argument('--destination', '-d', dest="destination",
                        help=f"Filepath of created file. Default ./<filename of inputfile>_filtered.xlsx")
    parser.add_argument('--status', '-s', dest='status',
                        help=f"Filter: publication status (DRAFT, GTOP, PUBL). Default: None")
    parser.add_argument('--diagrams', '-diag', dest='diagrams',
                        help=f"Filter: list of comma seperated diagram names to be published. Default: None")
    argparse.Namespace()
    arguments = parser.parse_args()

    jsonfile = Path(arguments.jsonfilepath[0])
    destination = arguments.destination
    if destination is None:
        destination = jsonfile.with_name(jsonfile.stem+"_filtered").with_suffix(".json")

    status = arguments.status
    stati = [Modelelement.GTOP, Modelelement.DRAFT, Modelelement.PUBL]
    assert status is None or status.upper() in stati, f"Publication status must be in {stati}"
    diags = arguments.diagrams
    diagrams = None if diags is None else [dia.strip(" '\"") for dia in diags.split(',')]

    dest=filterjsonfile(pjsonfile=jsonfile, pdestination=destination,
                        pstatus=status, pdiagrams=diagrams)
    print (f"filtered json file {dest} created")

if __name__ == '__main__':
    main()
