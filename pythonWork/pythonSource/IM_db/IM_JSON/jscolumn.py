from IM_OBJECTS import Column,Table,OragnisationalUnit,Modelelemtype,Boolean,Externalref,Datatype,Document,Interface,ColAttrMap
from IM_JSON import jsguid,jsguid2id,inssourceref,udpv2js,updvs2sql,JSModel

def columns2js():
    cols = {jsguid(Modelelemtype.COLU,c.colu_id) :
        {'name':c.colu_column_name
         ,'table-name+':Table().getbyid(c.colu_tabl_id).getname()
         ,'table-id':jsguid(Modelelemtype.TABL, Table().getbyid(c.colu_tabl_id).getid())
        , 'interface-name+': Interface().getbyid(Table().getbyid(c.colu_tabl_id).tabl_intf_id).getname()
        , 'interface-id+': jsguid(Modelelemtype.INTF, Interface().getbyid(Table().getbyid(c.colu_tabl_id).tabl_intf_id).getid())
        ,'mandatory' : Boolean.str2bool(c.colu_mandatory)
        ,'basedatatype+' : None if c.colu_daty_id is None else Datatype().getbyid(c.colu_daty_id).daty_name
        ,'datatype+':c.colu_type_string
        ,'datatypeid':c.colu_daty_id
        ,'format':c.colu_format
        ,'domain':jsguid(Modelelemtype.DOMA,c.colu_doma_id)
        ,'descr':c.colu_descr
       ,'interface_col_id':c.colu_ext_system_id
        ,'uc' : c.colu_uc
        ,'dc': c.colu_dc
        ,'um': c.colu_um
        , 'dm': c.colu_dm
        , 'attributes-mapped': [jsguid(Modelelemtype.ATTR, a.attr_id) for a in
                                ColAttrMap.getattrlist(pcoluid=c.colu_id)]
        , 'userdefprops': udpv2js(pmodeid=c.colu_id,pmodelemtype=Modelelemtype.COLU)
            , 'sourceref': Externalref.getsrcinfo(pmodeid=c.colu_id)
        , 'refindocuments+': [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=c.colu_id)]
            ,'refbyorgunits+': [jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=c.colu_id)]
         }
            for c in Column.select()
            }
    return cols

def columns2sql(pmodel:JSModel):
    for jid,jelem in pmodel.jsmodel['columns'].items():
        colu = Column()
        colu.colu_id = jsguid2id(jid)
        colu.colu_column_name = jelem['name']
        colu.colu_tabl_id = jsguid2id(jelem['table-id'])
        colu.colu_mandatory = Boolean.bool2str(jelem['mandatory'])
        colu.colu_type_string = jelem['datatype+']
        colu.colu_daty_id = jelem['datatypeid']
        colu.colu_format = jelem['format']
        colu.colu_doma_id = jsguid2id(jelem['domain'])
        colu.colu_descr = jelem['descr']
        colu.colu_ext_system_id = jelem['interface_col_id']
        colu.colu_uc = jelem['uc']
        colu.colu_dc = jelem['dc']
        colu.colu_um = jelem['um']
        colu.colu_dm = jelem['dm']
        try:
            colu.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=colu.tostring())
            continue

        inssourceref(pmodel = pmodel,pmodeid=jsguid2id(jid), psources=jelem["sourceref"])
    #for
    return


def colattrmaps2sql(pmodel:JSModel, pcoluid, pattrs):
    for jattrid in pattrs:
        coam = ColAttrMap()
        coam.coam_seq = 1
        coam.coam_direction = ColAttrMap.INBOUND
        coam.coam_colu_id = pcoluid
        coam.coam_attr_id = jsguid2id(jattrid)
        try:
            coam.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=coam.tostring())
            continue
    #for
    return

"""transfer references and subtypes"""
def colurefs2sql(pmodel:JSModel):
    for jid,jelem in pmodel.jsmodel['columns'].items():
        colattrmaps2sql(pmodel=pmodel,pcoluid=jsguid2id(jid),pattrs=jelem['attributes-mapped'])
        updvs2sql(pmodel=pmodel,pmodeid=jid, pudps=jelem["userdefprops"])
    return
