from django.urls import path
from . import views


urlpatterns = [
    path('MS/', views.load_ms_page, name='MS'),
    path('ms/submit/', views.handle_ms_form, name='ms_submit'),
    path('generate_ms_report/', views.generate_ms_report, name='generate_ms_report'),
    path('modify_ms_dxf/', views.modify_ms_dxf, name='modify_ms_dxf'),
     
    
    path('BC/', views.load_bc_page, name='BC'),
    path('bc/submit/', views.handle_bc_form, name='bc_submit'), 
    path('generate_bc_report/', views.generate_bc_report, name='generate_bc_report'),
    path('modify_bc_dxf/', views.modify_bc_dxf, name='modify_bc_dxf'),
    
    
    path('GR/', views.load_gr_page, name='GR'),
    path('gr/submit/', views.handle_gr_form, name='gr_submit'), 
    path('generate_gr_report/', views.generate_gr_report, name='generate_gr_report'),
    path('modify_gr_dxf/', views.modify_gr_dxf, name='modify_gr_dxf'),
    
    
    path('PS/', views.load_ps_page, name='PS'),
    path('ps/submit/', views.handle_ps_form, name='ps_submit'),
    path('generate_ps_report/', views.generate_ps_report, name='generate_ps_report'),
    path('modify_ps_dxf/', views.modify_ps_dxf, name='modify_ps_dxf'),
     
    
    path('TH/', views.load_th_page, name='TH'),
    path('th/submit/', views.handle_th_form, name='th_submit'), 
    path('generate_th_report/', views.generate_th_report, name='generate_th_report'),
    path('modify_th_dxf/', views.modify_th_dxf, name='modify_th_dxf'),
    
    
    path('MX/', views.load_mx_page, name='MX'),
    path('mx/submit/', views.handle_mx_form, name='mx_submit'), 
    path('generate_mx_report/', views.generate_mx_report, name='generate_mx_report'),
    path('modify_mx_dxf/', views.modify_mx_dxf, name='modify_mx_dxf'),
    
    
    path('RT/', views.load_rt_page, name='RT'),
    path('rt/submit/', views.handle_rt_form, name='rt_submit'), 
    path('generate_rt_report/', views.generate_rt_report, name='generate_rt_report'),
    path('modify_rt_dxf/', views.modify_rt_dxf, name='modify_rt_dxf'),
    
    
    path('CT/', views.load_ct_page, name='CT'),
    path('ct/submit/', views.handle_ct_form, name='ct_submit'),
    path('generate_ct_report/', views.generate_ct_report, name='generate_ct_report'),
    path('modify_ct_dxf/', views.modify_ct_dxf, name='modify_ct_dxf'),
     
    
    path('SC/', views.load_sc_page, name='SC'),
    path('sc/submit/', views.handle_sc_form, name='sc_submit'), 
    path('generate_sc_report/', views.generate_sc_report, name='generate_sc_report'),
    path('modify_sc_dxf/', views.modify_sc_dxf, name='modify_sc_dxf'),
     
    
    path('BS/', views.load_bs_page, name='BS'),
    path('bs/submit/', views.handle_bs_form, name='bs_submit'), 
    path('generate_bs_report/', views.generate_bs_report, name='generate_bs_report'),
    path('modify_bs_dxf/', views.modify_bs_dxf, name='modify_bs_dxf'),
     
    
    path('NS/',                 views.load_ns_page, name='NS'),
    path('ns/submit/',          views.handle_ns_form, name='ns_submit'), 
    path('generate_ns_report/', views.generate_ns_report, name='generate_ns_report'),
    path('modify_ns_dxf/',      views.modify_ns_dxf, name='modify_ns_dxf'),
     
    
    path('PNch/',                 views.load_pnch_page, name='PNch'),
    path('PNch/submit/',          views.handle_pnch_form, name='PNch_submit'), 
    path('generate_pnch_report/', views.generate_pnch_report, name='generate_pnch_report'),
    path('modify_pnch_dxf/',      views.modify_pnch_dxf, name='modify_pnch_dxf'),
     
    
    path('PNwa/',                 views.load_pnwa_page, name='PNwa'),
    path('PNwa/submit/',          views.handle_pnwa_form, name='PNwa_submit'), 
    path('generate_pnwa_report/', views.generate_pnwa_report, name='generate_pnwa_report'),
    path('modify_pnwa_dxf/',      views.modify_pnwa_dxf, name='modify_pnwa_dxf'),
    
    
    path('formdata/', views.list_configs, name='list_configs'),
    path('add/', views.add_config, name='add_config'),
    path('edit/<int:config_id>/', views.edit_config, name='edit_config'),
    path('delete/<int:config_id>/', views.delete_config, name='delete_config'),
    
    
    
    path('projects/', views.project_list, name='project_list'),
    path('editprojects/<int:project_id>/', views.edit_project, name='edit_project'),
    path('deleteprojects/<int:project_id>/', views.delete_project, name='delete_project'),
    
    
    path('DataSheetNS/',       views.load_DataSheetNS, name='load_DataSheetNS'),
    path('DataSheetNS/Save/',  views.Save_DataSheetNS, name='Save_DataSheetNS'), 
    
    path('DataSheetNSdelete/<int:machine_id>/', views.Delete_DataSheetNS, name='Delete_DataSheetNS'),
    path('editDS/<int:id>/', views.edit_datasheet, name='Edit_DataSheetNS'),
    path('DataSheetNSget_data/<int:machine_id>/', views.get_datasheet_data, name='get_datasheet_data'),

    path('get_machines/<int:project_id>/', views.get_machines, name='get_machines'),
    
    path('generate_report/<int:project_id>/', views.generate_report, name='generate_report'),
    

]