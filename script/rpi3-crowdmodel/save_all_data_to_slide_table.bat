python save_all_data_to_slide_table.py

call ck prepare table @save_all_model_data_tmp_table_full.json --record_html=save_all_model_data_tmp_table_full.html --record_tex=save_all_model_data_tmp_table_full.tex
call ck prepare table @save_all_model_data_tmp_table_milepost.json --record_html=save_all_model_data_tmp_table_milepost.html --record_tex=save_all_model_data_tmp_table_milepost.tex
call ck prepare table @save_all_model_data_tmp_table_short.json --record_html=save_all_model_data_tmp_table_short.html --record_tex=save_all_model_data_tmp_table_short.tex

call ck copy_file slide:rpi3-crowdmodeling-all-apps --file=save_all_model_data_tmp_table_milepost.html --new_name=08ac094d04acd157-table.html
call ck copy_file slide:rpi3-crowdmodeling-all-apps --file=save_all_model_data_tmp_table_milepost.tex --new_name=08ac094d04acd157-table.tex

call ck copy_file slide:rpi3-crowdmodeling-all-apps --file=save_all_model_data_tmp_table_full.html --new_name=74089e922ca45f99-table.html
call ck copy_file slide:rpi3-crowdmodeling-all-apps --file=save_all_model_data_tmp_table_full.tex --new_name=74089e922ca45f99-table.tex

call ck copy_file slide:rpi3-crowdmodeling-all-apps --file=save_all_model_data_tmp_table_short.html --new_name=142fbaf8c4fb48b8-table.html
call ck copy_file slide:rpi3-crowdmodeling-all-apps --file=save_all_model_data_tmp_table_short.tex --new_name=142fbaf8c4fb48b8-table.tex

