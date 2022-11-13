"""
2022/11/12
Make log files (info.csv and img in Dataframe) to html for quick inspection

Reference: https://stackoverflow.com/questions/53468558/adding-image-to-pandas-dataframe?noredirect=1&lq=1
"""
import pandas as pd
from glob import glob


# # from IPython.core.display import display,HTML
#
# df = pd.DataFrame([['A231', 'Book', 5, 3, 150],
#                    ['M441', 'Magic Staff', 10, 7, 200]],
#                   columns=['Code', 'Name', 'Price', 'Net', 'Sales'])
#
# # your images
# # images1 = [
# #     'https://vignette.wikia.nocookie.net/2007scape/images/7/7a/Mage%27s_book_detail.png/revision/latest?cb=20180310083825',
# #     'https://i.pinimg.com/originals/d9/5c/9b/d95c9ba809aa9dd4cb519a225af40f2b.png']
#
# images1 = [
#     'https://vignette.wikia.nocookie.net/2007scape/images/7/7a/Mage%27s_book_detail.png/revision/latest?cb=20180310083825',
#     r'G:\2020_01_17\G\gmycode\unet-BET_pm2.5\code-in-home\BEN-github\utils/C1-rigidaffine_lddm_t2MTONOFF_JZ.mp4']
#
# images2 = [
#     'https://static3.srcdn.com/wordpress/wp-content/uploads/2020/07/Quidditch.jpg?q=50&fit=crop&w=960&h=500&dpr=1.5',
#     'https://specials-images.forbesimg.com/imageserve/5e160edc9318b800069388e8/960x0.jpg?fit=scale']
#
# df['imageUrls'] = images1
# df['otherImageUrls'] = images2


# convert your links to html tags (img)
def path_to_image_html(path):
    return '<img src="' + path + '" width="1000" >'


# convert your links to html tags (video)
def path_to_video_html(path):
    # todo: fix bug, *LOCAL videos* don't load correctly in HTML page.
    return '<video controls > <source src="' + path + '"> </video>'


def make_logs_to_html(log_folder):
    """
    Make log files (info.csv and img in Dataframe) to html for quick inspection
    :param log_folder: contain png img and info.csv
    :return: None. HTML will be saved in logs folder.
    """
    '''
    Decoupling design of modules to avoid over-encapsulation and integration, which are not conducive to reuse
    '''
    ''' 1. Visual report (png) '''
    # Implemented in check_result.py

    ''' 2. Volumetric report (csv) '''
    # Implemented in check_result.py

    ''' 3. Read log files (png) and Volumetric report (csv) in Dataframe to generate html'''
    df = pd.read_csv(log_folder + '/info.csv')

    ''' Add image list to Dataframe '''
    images_list = glob(log_folder + '/*.png')

    df['Visual Result'] = images_list

    ''' Make HTML '''
    pd.set_option('display.max_colwidth', None)

    image_cols = ['Visual Result', ]  # <- define which columns will be used to convert to html

    # Create the dictionary to be passed as formatters
    format_dict = {}
    for image_col in image_cols:
        format_dict[image_col] = path_to_image_html

    ''' Save HTML '''
    # for jupyter notebook:
    # display(HTML(df.to_html(escape=False ,formatters=format_dict)))
    # for pycharm/console:
    df.to_html(log_folder + '/Report.html', escape=False, formatters=format_dict, )

    return None


if __name__ == '__main__':
    log_folder = r'E:\New\Data_repo\doi_10.5061_dryad.1vhhmgqv8__v2\dataset\pred-pipe_30epoch_11090153\logs'

    make_logs_to_html(log_folder)
