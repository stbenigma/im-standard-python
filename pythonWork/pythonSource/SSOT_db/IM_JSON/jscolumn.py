from SSOT_db.IM_JSON import *


def columns2js(pemptymodel):
    model = ['name',
             'table-name+',
             'table-id',
             'interface-name+',
             'interface-id+',
             'mandatory',
             'basedatatype+',
             'datatype',
             'datatypeid+',
             'format',
             'domain',
             'descr',
             'interface_col_id',
             'uc', 'dc', 'um', 'dm',
             'minzoomlevel', 'maxzoomlevel', 'publstatus',
             'R/W',
             'attributesmapped','businessrules+',
             'userdefprops',
             'sourceref','raci+',
             'referencedby'
             ]
    if pemptymodel:
        retval = {jsguid(Modelelemtype.COLU, '0000'): fillmodel(pmodel=model, pentries=['' for i in range(17)]
                                                                                       + [0, 4, 'DRAFT', rwstr(),
                                                                                          reflist(plist=[
                                                                                              Modelelemtype.ATTR + "0000"]),
                                                                                          buruinelements(None),
                                                                                          userdefprops(),
                                                                                          sourceref(), jsentity.racilist(),reflist()
                                                                                          ])}
    else:
        retval = {jsguid(Modelelemtype.COLU, c.colu_id): fillmodel(pmodel=model, pentries=[
            c.colu_column_name,
            Table().getbyid(c.colu_tabl_id).getname(),
            jsguid(Modelelemtype.TABL, Table().getbyid(c.colu_tabl_id).getid()),
            Interface().getbyid(Table().getbyid(c.colu_tabl_id).tabl_intf_id).getname(),
            jsguid(Modelelemtype.INTF, Interface().getbyid(Table().getbyid(c.colu_tabl_id).tabl_intf_id).getid()),
            Boolean.str2bool(c.colu_mandatory),
            Domain().getbyid(c.colu_doma_id).basedatatype(),
            c.colu_type_string,
            jsguid(Modelelemtype.DATY, Domain().getbyid(c.colu_doma_id).doma_daty_id),
            c.colu_format,
            jsguid(Modelelemtype.DOMA, c.colu_doma_id),
            c.colu_descr,
            c.colu_ext_system_id,
            c.colu_uc, c.colu_dc, c.colu_um, c.colu_dm,
            c.getminzoomlevel(), c.getmaxzoomlevel(), c.getpublstatus(),
            rwstr(pread=c.colu_read, pwrite=c.colu_update),
            reflist(plist=[jsguid(Modelelemtype.ATTR, a.attr_id) for a in
                           ColAttrMap.getattrlist(pcoluid=c.colu_id)]),
            buruinelements(c.colu_id),
            udpv2js(pmodeid=c.colu_id, pmodelemtype=Modelelemtype.COLU),
            Externalref.getsrcinfo(pmodeid=c.colu_id),jsentity.racilist(c.colu_id),
            [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=c.colu_id)] \
            + [jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=c.colu_id)]
        ])
                  for c in Column.select()
                  }
    # fi
    return retval


def js2colu(pkey, pelem, psrcname=None, psrcid=None, pmodellang=None):
    colu = Column(psrcname=psrcname, psrcid=psrcid)
    colu.colu_id = jsguid2id(pkey)
    colu.colu_column_name = pelem['name']
    colu.colu_tabl_id = jsguid2id(pelem['table-id'])
    colu.colu_mandatory = Boolean.bool2str(pelem['mandatory'])
    colu.colu_type_string = pelem['datatype']
    colu.colu_format = pelem['format']
    colu.colu_doma_id = jsguid2id(pelem['domain'])
    colu.colu_descr = pelem['descr']
    colu.colu_ext_system_id = pelem['interface_col_id']
    colu.colu_uc = pelem['uc']
    colu.colu_dc = pelem['dc']
    colu.colu_um = pelem['um']
    colu.colu_dm = pelem['dm']
    return colu


def columns2sql(presult: Mergeresult, podmjson: JSModel, pwithextsrcref):
    fromodm2db(presult=presult, podmjson=podmjson, pelemtype=Modelelemtype.COLU, pjs2obj=js2colu,
               pwithextsrcref=pwithextsrcref)

    for jid, jelem in podmjson.getelements(pelemtype=Modelelemtype.COLU).items():
        newcoluid = keytransl(jid)
        if newcoluid is None:
            logging.debug(f"Element {jid} not merged as it is new")
            continue

        minzoomlevel = jelem['minzoomlevel']
        maxzoomlevel = jelem['maxzoomlevel']
        publstatus = jelem['publstatus']
        Modelelement.upddisplelements(pmodeid=newcoluid, pminzl=minzoomlevel, pmaxzl=maxzoomlevel, ppublstat=publstatus)

        colattrmaps2sql(presult=presult, pcoluid=newcoluid, pattrs=jelem['attributesmapped'])
        insreferences(presult=presult, pmodeid=newcoluid, prefs=jelem['referencedby'])
        inssourceref(presult=presult, pmodeid=newcoluid, psources=jelem["sourceref"])
        udpvs2sql(presult=presult, pmodeid=newcoluid, pudps=jelem["userdefprops"])
    # for
    return


def colattrmaps2sql(presult: Mergeresult, pcoluid, pattrs):
    inscnt = 0
    delcnt = ColAttrMap.delete(pwhere=("coam_colu_id = ?", pcoluid))
    for idx, jattrid in enumerate(pattrs, start=1):
        coam = ColAttrMap()
        coam.coam_seq = idx
        coam.coam_direction = ColAttrMap.INBOUND
        coam.coam_colu_id = pcoluid
        coam.coam_attr_id = keytransl(jattrid)
        try:
            coam.insert()
            inscnt += 1
        except Exception as err:
            presult.markdberror(perr=err, pelem=coam.tostring())
            continue
        # try
    # for
    presult.addinscnt(max(0, (inscnt - delcnt)),f"Column Maps for column {pcoluid} ")
    presult.adddelcnt(max(0, (delcnt - inscnt)),f"Column Maps for column {pcoluid} ")
    return
