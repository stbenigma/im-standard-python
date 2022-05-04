from SSOT_db.SQL_INFRA import dbConnect

def filldb(transferfunction, **kwargs):
    assert dbConnect.isopenDB()
    transferfunction(**kwargs)
    return

