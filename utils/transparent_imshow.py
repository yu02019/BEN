"""
This is a simple wrapper along matplotlib's `imshow` function, which 
allows to produce images with pixel-dependent transparency.
"""
import matplotlib
import matplotlib.pyplot as plt

def transp_imshow( data, tvmin=None, tvmax=None, tmax=1.,
                    gam=1., cmap='Blues', **kwargs ) :
    """
    Displays the 2d array `data` with pixel-dependent transparency.
    Parameters
    ----------
    data: 2d numpy array of floats or ints
        Contains the data to be plotted as a 2d map
    tvmin, tvmax: floats or None, optional
        The values (for the elements of `data`) that will be plotted
        with minimum opacity and maximum opacity, respectively.
        If no value is provided, this uses by default the arguments
        `vmin` and `vmax` of `imshow`, or the min and max of `data`.
    tmax: float, optional
        Value between 0 and 1. Maximum opacity, which is reached
        for pixel that have a value greater or equal to `tvmax`.
        Default: 1.
    gam: float, optional
        Distortion of the opacity with pixel-value.
        For `gam` = 1, the opacity varies linearly with pixel-value
        For `gam` < 1, low values have higher-than-linear opacity
        For `gam` > 1, low values have lower-than-linear opacity
    cmap: a string or a maplotlib.colors.Colormap object
        Colormap to be used
    kwargs: dict
        Optional arguments, which are passed to matplotlib's `imshow`.
    """
    # Determine the values between which the transparency will be scaled
    if 'vmax' in kwargs :
        vmax = kwargs['vmax']
    else :
        vmax = data.max()
    if 'vmin' in kwargs :
        vmin = kwargs['vmin']
    else :
        vmin = data.min()
    if tvmax is None:
        tvmax = vmax
    if tvmin is None:
        tvmin = vmin

    # Rescale the data to get the transparency and color
    color = (data-vmin)/(vmax-vmin)
    color[color > 1.] = 1.
    color[color < 0.] = 0.
    transparency = tmax*(data-tvmin)/(tvmax-tvmin)
    transparency[transparency > 1.] = 1
    transparency[transparency < 0.] = 0.
    # Application of a gamma distortion
    transparency = tmax * transparency**gam

    # Get the colormap
    if isinstance( cmap, matplotlib.colors.Colormap ):
        colormap = cmap
    elif type(cmap) == str:
        colormap = getattr( plt.cm, cmap )
    else:
        raise ValueError('Invalid type for argument `cmap`.')
    
    # Create an rgba stack of the data, using the colormap 
    rgba_data = colormap( color )
    # Modify the transparency
    rgba_data[:,:,3] = transparency

    sc = plt.imshow( rgba_data, **kwargs )

    # test
    # plt.colorbar(sc)
    return sc

# 2021/06/30 添加，便于绘图
def plot_no_margin(img=None, fig=None,save_path=None):
    '''
    去除白边
    :param img:
    :param save_path:
    :return:
    '''
    # fig, ax = plt.subplots()
    # # plt.imshow(rawimg, cmap='gray')
    # ax.imshow(rawimg, cmap='gray',
    #           # aspect="equal"
    #           )
    plt.xticks([]), plt.yticks([])
    plt.axis("off")
    # 去除图像周围的白边
    height, width = img.shape
    # 如果dpi=300，那么图像大小=height*width
    fig.set_size_inches(width / 100.0, height / 100.0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
    plt.margins(0, 0)
    # plt.savefig('{}_output/'.format(patientID) + name_id + '_' + str(slice_id) + '_Raw.png')
    # plt.savefig(save_path)