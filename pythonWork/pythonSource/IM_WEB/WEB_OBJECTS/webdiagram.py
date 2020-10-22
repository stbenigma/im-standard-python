from .webbaseobject import Webanker,BaseWebObj,Objlist
from IM_OBJECTS import  Diagram,Diagramtype


class WebDiagram(BaseWebObj):
    def __init__(self, pid=None, pdbobj: Diagram = None):
        super().__init__(pobjtype=WebDiagram, pid=pid, pdbobj=pdbobj)

    def getname(self, plang=None):
        return self.dbobject().diag_name

    """Diagramname (entry type) """
    def getqualifiedname(self, plang=None):
            return '{} ({})'.format(self.dbobject().diag_name, Diagramtype().getbyid(pid=self.dbobject().diag_diat_id).diat_name)

    @staticmethod
    def contentlist(pentiid=None,plang=None):
        if pentiid is None:
            lsql = """  
            select diag_name,diag_id,diag_legendx,diag_legendy,breite,hoehe,diag_uc,diag_dc,diag_um
               from diagrams
               left join  (select diag_id size_diag_id,max(xpos + breite) breite,max(ypos + hoehe) hoehe
                    FROM (select eler_diag_id diag_id,eler_position_x xpos,eler_width breite
                         ,eler_position_y ypos, eler_height hoehe
                         from elementreps
                         union all 
                         select relr_diag_id, relr_endtext_x xpos, relr_endtext_breite breite
                         ,relr_endtext_y ypos, relr_endtext_hoehe hoehe
                         from relationreps
                         union all 
                         select relr_diag_id, lise_x xpos, 3 breite
                         ,lise_y ypos, 3 hoehe
                         from relationreps
                         join linesegments on lise_relr_id = relr_id
                        )
                        group by size_diag_id
                    ) on size_diag_id = diag_id
                order by upper(diag_name)"""
            data = dbDML.select(lsql)
        else:
            diags = Diagram.select(pwhere="diag_id in (select eler_diag_id from elementreps where eler_mode_id = {})".format(pentiid)
                                   ,porderby="upper(diag_name)")
        # fi
        return [WebDiagram(pdbobj=diag.diag_id) for diag in diags]
    # diaglist
    @staticmethod
    def indexlist(pentiid=None,plang=None):
        #order by in indexlist not yet resolved (diagramtype -> diagramnbame)
        #    porderby='(select diat_name from diagramtypes where diat_id = diag_diat_id),diag_name'
        members = WebDiagram.contentlist(pentiid=pentiid,plang=plang)
        return Objlist(pmembers=members).indexlist()
    # indexlist
#WebDiagram
