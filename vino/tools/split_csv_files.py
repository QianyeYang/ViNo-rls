from vino.logic import utils
from icecream import ic
import vino, os

csv_root = os.path.join(
    vino.DIR_PROJECT, 
    'projects/coche/backup'
    )

csv_path = os.path.join(csv_root, 'R_single_window_2ndTrim_scans_with_view_annotation.csv')


if __name__ == '__main__':
    df = utils.load_csv(csv_path)
    
    # ['4CH']-X under component_00002
    df_4ch = df[df['component_00002'] == "['4CH']-X"]
    df_lvot = df[df['component_00002'] == "['LVOT']-X"]
    df_3vv = df[df['component_00002'] == "['3VV']-X"]
    df_3vt = df[df['component_00002'] == "['3VT']-X"]
    
    ic(df_4ch.shape, df_lvot.shape, df_3vv.shape, df_3vt.shape)
    

    participants_4ch = df_4ch['participantFull'].unique().tolist()
    break_point = len(participants_4ch) // 2

    participants_4ch_1 = participants_4ch[:break_point]
    participants_4ch_2 = participants_4ch[break_point:]

    df_4ch_1 = df_4ch[df_4ch['participantFull'].isin(participants_4ch_1)]
    df_4ch_2 = df_4ch[df_4ch['participantFull'].isin(participants_4ch_2)]

    # df_4ch.to_csv(os.path.join(csv_root, 'R_single_window_2ndTrim_scans_with_view_annotation_4ch.csv'), index=False)
    df_4ch_1.to_csv(os.path.join(csv_root, 'R_single_window_2ndTrim_scans_with_view_annotation_4ch_part1.csv'), index=False)
    df_4ch_2.to_csv(os.path.join(csv_root, 'R_single_window_2ndTrim_scans_with_view_annotation_4ch_part2.csv'), index=False)
    # df_lvot.to_csv(os.path.join(csv_root, 'R_single_window_2ndTrim_scans_with_view_annotation_lvot.csv'), index=False)
    # df_3vv.to_csv(os.path.join(csv_root, 'R_single_window_2ndTrim_scans_with_view_annotation_3vv.csv'), index=False)
    # df_3vt.to_csv(os.path.join(csv_root, 'R_single_window_2ndTrim_scans_with_view_annotation_3vt.csv'), index=False)