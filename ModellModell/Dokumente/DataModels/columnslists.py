"""
NUMERIC\W*\([^\)]+\)    NUMERIC
(CHECK|UNIQUE|FOREIGN KEY)\W*\([^\)]+\)+[^,;]*,		,
(CHECK|UNIQUE|FOREIGN KEY)\W*\([^\)]+\)+[^;]*;  );
,(\W|\n)*CONSTRAINT \W*[^;]*;		);
,(\W|\n)*CONSTRAINT \W*[^,]*,	 
CREATE[^\(]+\W*			_columnlist: list = [
);			]
(\[|,)\W*([A-Za-z0-9_$]+)[^,\]]+		$1'$2' 
"""

_columnlist: list = ['arcs_id' ,'arcs_name','arcs_enti_id','arcs_uc','arcs_dc','arcs_um','arcs_dm']
_columnlist: list = ['attr_id','attr_enti_id','attr_rela_id','attr_doma_id','attr_tech_name','attr_displ_name','attr_displ_seq','attr_tooltip','attr_descr','attr_is_descriptive','attr_is_mandatory','attr_is_historicised','attr_is_repeated','attr_is_translated','attr_is_encrypted','attr_uc','attr_dc','attr_um','attr_dm']
_columnlist: list = ['buru_id','buru_name','buru_rule','buru_descr','buru_errmsg','buru_uc','buru_dc','buru_um','buru_dm']
_columnlist: list = ['bure_id','bure_buru_id','bure_attr_id','bure_enti_id','bure_rela_id','bure_uc','bure_dc','bure_um','bure_dm']



_columnlist: list = ['deva_id','deva_doma_id','deva_value','deva_sort_order','deva_displ','deva_descr','deva_uc','deva_dc','deva_um','deva_dm']
_columnlist: list = ['docu_id','docu_name','docu_format','docu_reference','docu_content','docu_docu_id']


_columnlist: list = ['dgrm_id','dgrm_name','dgrm_descr','drgm_id_mandatory','dgrm_doma_id_group','dgrm_doma_id_member','dgrm_uc','dgrm_dc','dgrm_um','dgrm_dm']
_columnlist: list = ['enti_id','enti_name','enti_short_name','enti_prefix','enti_tooltip','enti_descr','enti_exp_tuplecnt','enti_uc','enti_dc','enti_um','enti_dm']
_columnlist: list = ['extr_id','extr_source_name','extr_source_id','extr_mode_id']

_columnlist: list = ['doma_id','doma_name','doma_descr','doma_type','doma_origin','doma_dat_minvalue','doma_dat_maxvalue','doma_dat_granularity','doma_txt_maxlng','doma_txt_syntaxrule','doma_num_maxvalue','doma_num_minvalue','doma_num_total_digits','doma_num_fract_digits','doma_num_round_value','doma_num_phyu_id','doma_bin_contenttype','doma_bin_stfo_id','doma_uc','doma_dc','doma_um','doma_dm']

_columnlist: list = ['kele_id','kele_keys_id','kele_attr_id','kele_rela_id','kele_uc','kele_dc','kele_um','kele_dm']


_columnlist: list = ['keys_id','keys_name','keys_enti_id','keys_uc','keys_dc','keys_um','keys_dm']
_columnlist: list = ['lgtx_id','lgtx_attrname','lgtx_text','lgtx_lang_id','lgtx_mode_id','lgtx_uc','lgtx_dc','lgtx_um','lgtx_dm']
_columnlist: list = ['lang_id','lang_iso_name','lang_iso_code2','lang_is_base_lang','lang_lang_id','lang_uc','lang_dc','lang_um','lang_dm']
_columnlist: list = ['modo_id','modo_mode_id','modo_docu_id']
_columnlist: list = ['melt_id','melt_shortname','melt_name','melt_uc','melt_dc','melt_um','melt_dm']
_columnlist: list = ['mode_id','mode_type','mode_melt_id']


_columnlist: list = ['metp_id','metp_melt_id','metp_udpr_id','metp_optional']
_columnlist: list = ['phyu_id','phyu_si_unit','phyu_name','phyu_descr','phyu_uc','phyu_dc','phyu_um','phyu_dm']
_columnlist: list = ['rela_id','rela_name','rela_type','rela_enti_id_from','rela_arcs_id_from','rela_assoc_from_to','rela_maptype_from_to','rela_mandatory_from_to','rela_hist_from_to','rela_enti_id_to','rela_arcs_id_to','rela_assoc_to_from','rela_maptype_to_from','rela_mandatory_to_from','rela_hist_to_from','rela_uc','rela_dc','rela_um','rela_dm']
_columnlist: list = ['stfo_id','stfo_name','stfo_descr','stfo_uc','stfo_dc','stfo_um','stfo_dm']
_columnlist: list = ['syno_id','syno_name','syno_enti_id','syno_uc','syno_dc','syno_um','syno_dm']


_columnlist: list = ['udpv_id','udpv_value','udpv_mode_id','udpv_udpr_id','udpv_uc','udpv_dc','udpv_um','udpv_dm']
_columnlist: list = ['udpr_id','udpr_group','udpr_name','udpr_descr','udpr_uc','udpr_dc','udpr_um','udpr_dm']



