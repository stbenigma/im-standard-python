from IM_OBJECTS import Column,Table,OragnisationalUnit,Modelelemtype,Boolean,Userdefpropvalue,Userdefprop,Externalref,Datatype,Document,Interface,AttrTransf
from IM_JSON import jsguid

def columns2js():
    cols = {jsguid(Modelelemtype.COLU,c.colu_id) :
        {'name':c.colu_column_name
         ,'table-name':Table().getbyid(c.colu_tabl_id).getname()
         ,'table-id':jsguid(Modelelemtype.TABL, Table().getbyid(c.colu_tabl_id).getid())
        , 'interface-name': Interface().getbyid(Table().getbyid(c.colu_tabl_id).tabl_intf_id).getname()
        , 'interface-id': jsguid(Modelelemtype.INTF, Interface().getbyid(Table().getbyid(c.colu_tabl_id).tabl_intf_id).getid())
        ,'mandatory' : Boolean.str2bool(c.colu_mandatory)
        ,'basedatatype' : None if c.colu_daty_id is None else Datatype().getbyid(c.colu_daty_id).daty_name
        ,'datatype':c.colu_type_string
        ,'format':c.colu_format
        ,'domain':jsguid(Modelelemtype.DOMA,c.colu_doma_id)
        ,'descr':c.colu_descr
       ,'interface_col_id':c.colu_ext_system_id
            , 'uc': c.colu_uc
            , 'dc': c.colu_dc
            , 'um': c.colu_um
            , 'dm': c.colu_dm
        , 'attributes-mapped': [jsguid(Modelelemtype.ATTR, a.attr_id) for a in
                             AttrTransf.getattrlist(pcoluid=c.colu_id)]
        , 'userdefprop': {
            th[0]: {gr[1]: {u.udpr_name: Userdefpropvalue.udpvalue(pudprid=u.udpr_id, pmodeid=c.colu_id)
                            for u in Userdefprop.getudps(ptheme=th[0], pgroup=gr[1], pmeltname=Modelelemtype.COLU)}
                    for gr in Userdefprop.grouplist(pudptheme=th[0], pmelttype=Modelelemtype.COLU)}
            for th in Userdefprop.themelist(pmelttype=Modelelemtype.COLU)
        }
            , 'sourceref': {s: Externalref.getsrcid(psrcname=s, pmodeid=c.colu_id)
                        for s in Externalref.getsources()}
        , 'refindocuments': [jsguid(Modelelemtype.DOCU, d[0]) for d in Document.getrefdoculist(pid=c.colu_id)]
            ,'refbyorgunits': [jsguid(Modelelemtype.ORGU, d[0]) for d in OragnisationalUnit.getreforgulist(pid=c.colu_id)]
         }
            for c in Column.select()
            }
    return cols
