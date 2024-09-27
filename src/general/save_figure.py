from matplotlib.transforms import Bbox
import matplotlib.pyplot as plt
import os


def full_extent(ax, pad=0.0):
    """get boundaries of axes for saving subplot"""
    """Get the full extent of an axes, including axes labels, tick labels, and titles."""
    # For text objects, we need to draw the figure first, otherwise the extents
    try:
        # are undefined.
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.3, wspace=0.3)
        ax.figure.canvas.draw()

        items = []
        items += ax.get_xticklabels()[1:-1]
        items += ax.get_yticklabels()[1:-1]
        items += [ax.title]
        items += [ax.xaxis.label, ax.yaxis.label]

        bbox_items = [item.get_window_extent() for item in items if item.get_text() != '']
        bbox_plot = ax.get_window_extent()

        if bbox_items:
            bbox = Bbox.union(bbox_items + [bbox_plot])
        else:
            bbox = bbox_plot
        return bbox.expanded(1.0 + pad, 1.0 + pad)
    except Exception as e:
        print(f"Error save_figure.full_extent:\n  |--> {e}")


def save_subfig(fig, save_fullpath, mode='all', dpi=100):
    try:
        dir_path = os.path.dirname(save_fullpath)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        pad = 0.1
        if mode == 'all':
            bboxs = []
            for ax in fig.get_axes():
                bbox_now = full_extent(ax)
                bboxs.append(bbox_now)

            bbox = Bbox.union(bboxs)
            extent = bbox.expanded(1.0 + pad, 1.0 + pad).transformed(fig.dpi_scale_trans.inverted())
            fig.savefig(f'{save_fullpath}.png', bbox_inches=extent, dpi=dpi)
        elif mode == 'single':
            for i, ax in enumerate(fig.get_axes()):
                extent = full_extent(ax).transformed(fig.dpi_scale_trans.inverted())
                fig.savefig(f'{save_fullpath}_{i}.png', bbox_inches=extent, dpi=dpi)
        elif mode == 'both':
            save_subfig(fig, save_fullpath, 'all', dpi)
            save_subfig(fig, save_fullpath, 'single', dpi)
        else:
            print("Error mode.")
    except Exception as e:
        print(f"Error save_figure.save_subfig:\n  |--> {e}")


def get_subplots_number_of_rows_and_cols(fig):
    axes = fig.get_axes()

    if axes:
        first_ax = axes[0]
        geometry = first_ax.get_subplotspec().get_geometry()
        n_rows, n_cols = geometry[:2]
    return n_rows, n_cols


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    from src.general import set_figure

    data = np.random.rand(5, 5)
    fig = plt.figure()
    ax = {}
    for i in range(4):
        ax[i] = fig.add_subplot(2, 2, i + 1)
        ax[i].imshow(data)
        set_figure.set_label_and_title(ax[i])
        set_figure.set_legend(ax[i], legend_labels='123')
        set_figure.set_spines(ax[i])
        set_figure.set_tick(ax[i])

    save_subfig(fig, '111', mode='single')
    plt.show()
