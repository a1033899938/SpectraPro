from matplotlib.transforms import Bbox


def full_extent(ax, pad=0.0):
    """get boundaries of axes for saving subplot"""
    """Get the full extent of an axes, including axes labels, tick labels, and titles."""
    # For text objects, we need to draw the figure first, otherwise the extents
    try:
        # are undefined.
        ax.figure.canvas.draw()
        # items = [ax]
        items = ax.get_xticklabels()
        items += ax.get_yticklabels()
        items += [ax.title]
        items += [ax.xaxis.label, ax.yaxis.label]
        bbox_items = [item.get_window_extent() for item in items if item.get_visible()]
        bbox_plot = ax.get_window_extent()
        bbox = Bbox.union(bbox_items + [bbox_plot])
        return bbox.expanded(1.0 + pad, 1.0 + pad)
    except Exception as e:
        print(f"Error save_figure.full_extent:\n  |--> {e}")


def save_subfig(fig, ax, save_name_full):
    try:
        bbox = ax.get_tightbbox(fig.canvas.get_renderer()).expanded(1.02, 1.02)
        extent = bbox.transformed(fig.dpi_scale_trans.inverted())
        fig.savefig(save_name_full, bbox_inches=extent)
    except Exception as e:
        print(f"Error save_figure.save_subfig:\n  |--> {e}")