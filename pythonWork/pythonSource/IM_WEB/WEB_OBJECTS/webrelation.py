from IM_OBJECTS import Relation, Entity, Arc, Keyelement
from .webbaseobject import BaseWebObj
from .webentity import WebEntity


class WebRelation(BaseWebObj):
    def __init__(self, pid=None, pdbobj: Relation = None, plang=None):
        super().__init__(pobjtype=WebRelation, pid=pid, pdbobj=pdbobj)
        self.from_enti = WebEntity(pdbobj=self.dbobject().getfromentity())
        self.from_rela_assoc = self.dbobject().getassocfromto(plang=plang)
        self.from_card = self.minmaxcardinality(pfromto=True)
        self.from_mandatory = self.dbobject().getmandatoryfromto()
        self.to_enti = WebEntity(pdbobj=self.dbobject().gettoentity())
        self.to_rela_assoc = self.dbobject().getassoctofrom(plang=plang)
        self.to_card = self.minmaxcardinality(pfromto=False)
        self.to_mandatory = self.dbobject().getmandatorytofrom()
        self.rela_id = self.dbobject().rela_id
        self.rela_type = self.dbobject().rela_type
        self.rela_name = self.dbobject().rela_name
        arcids = set((self.dbobject().rela_arcs_id_from, self.dbobject().rela_arcs_id_to))
        arcids.discard(None)
        self.arcs_name = ', '.join(Arc().getbyid(arcid).arcs_name for arcid in arcids)
        self.isinkey = Keyelement.isinkey(prelaid=self.dbobject().rela_id)

    def minmaxcardinality(self, pfromto):
        maptype = self.dbobject().rela_maptype_from_to if pfromto else self.dbobject().rela_maptype_to_from
        mandatory = self.dbobject().getmandatoryfromto() if pfromto else self.dbobject().getmandatorytofrom()

        if maptype == Relation.ONE:
            return '1' if mandatory else '0..1'
        elif maptype == Relation.MANY:
            return '1..N' if mandatory else '0..N'
        else:
            raise Exception("invalid Value for Maptype {}".format(maptype))

    # minmaxcartinality

    @staticmethod
    def relalist(pentiid, plang):
        relas = Relation.select(pwhere="rela_enti_id_from = {} or rela_enti_id_to = {}".format(pentiid, pentiid))
        webrelas = [WebRelation(pdbobj=r, plang=plang) for r in relas]
        """
              with sprenti as 
              (select enti_id
                    ,case when ena.lgtx_text is null then enti_name else ena.lgtx_text end enti_name
                    ,lang_id,superenti_id enti_enti_id
                 from entities
                     left join SUPERENTI on subenti_id = ENTI_ID
                  left join langattr ena on ena.lgtx_attrname = 'ENTI_NAME'
                                    and ena.lgtx_mode_id = enti_id
               )
                select von.enti_id as von_enti_id,von.enti_name as von_name
                                    ,case when bvon.lgtx_text is null then  rela_assoc_from_to else bvon.lgtx_text end  rela_assoc_from_to
                                    ,case rela_type
                               when '1:1' then 
                                case rela_mandatory_from_to
                                     when 'TRUE' THEN '1'
                                     else '0..1'
                                   end
                               when 'M:N' then 
                                case rela_mandatory_from_to
                                     when 'TRUE' THEN '1..N'
                                     else '0..N'
                                   end
                               when 'M:1' then 
                                    case rela_mandatory_from_to
                                     when 'TRUE' THEN '1'
                                     else '0..1'
                                   end         
                                end card1
                                ,zu.enti_id as zu_enti_id,zu.enti_name as zu_name
                                ,case when bzu.lgtx_text is null then  rela_assoc_to_from else bzu.lgtx_text end rela_assoc_to_from
                                ,case rela_type
                                   when '1:1' then 
                                      case rela_mandatory_to_from
                                         when 'TRUE' THEN '1'
                                         else '0..1'
                                       end
                                   when 'M:N' then 
                                    case rela_mandatory_to_from
                                         when 'TRUE' THEN '1..N'
                                         else '0..N'
                                       end
                                   when 'M:1' then 
                                        case rela_mandatory_to_from
                                         when 'TRUE' THEN '1..N'
                                         else '0..N'
                                       end         
                                    end card2
                                ,rela_id,rela_type,rela_mandatory_from_to,rela_mandatory_to_from
                                ,arcs_name,extr_source_id,rela_name
                                ,case when (select 1 from key_elements 
                                             join keys on keys_id = kele_keys_id
                                             where kele_rela_id = rela_id
                                             and keys_enti_id = von.enti_id
                                             ) IS NULL 
                                THEN 'FALSE' ELSE 'TRUE' end keys
                            from  sprenti as von
                            join relations on rela_enti_id_from = von.enti_id
                                                and not (rela_type in  ('ISAS','ISAR')) 
                            join languages sp on sp.lang_id = von.lang_id
                            left join langattr bvon on bvon.lgtx_attrname = 'RELA_TEXT_FROM'
                                    and bvon.lgtx_mode_id = rela_id
                                    and bvon.lang_id = sp.lang_id 
                            left join langattr bzu on bzu.lgtx_attrname = 'RELA_TEXT_TO'
                                    and bzu.lgtx_mode_id = rela_id
                                    and bzu.lang_id = sp.lang_id 
                            join sprenti as zu on zu.enti_id = rela_enti_id_to
                                            and zu.lang_id = sp.lang_id
                            left join arcs on arcs_enti_id = von.enti_id
                            left join external_refs on extr_mode_id = arcs_id
                            where  sp.lang_iso_code2 = '{}'
                               and (von.enti_id = {} or zu.enti_id = {})     
                            order by arcs_name 
                            """  # .format(plang, pentiid, pentiid))
        return webrelas
    # relalist
# WebRelation
