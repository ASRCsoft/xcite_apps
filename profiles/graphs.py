"""
Functions for generating nice lidar profile graphs
"""

# get matplotlib with agg backend for drawing graphs on servers with
# no display
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['figure.figsize'] = (15, 7)
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# useful stuff
import xml, rasppy
import datetime as dt
import numpy as np
import xarray as xr
from io import BytesIO
# matplotlib tools for calculating tickmark locations -- I'm using
# these to find nice windbarb intervals
from matplotlib.ticker import MaxNLocator
from matplotlib.dates import AutoDateLocator, num2date
# and this is needed to help monkey patch the barbs function
from dateutil.rrule import (rrule, MO, TU, WE, TH, FR, SA, SU, YEARLY,
                            MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY,
                            SECONDLY)
MICROSECONDLY = SECONDLY + 1

# django stuff
from common.models import Scan, Mwr, MwrProfile
from profiles.models import Lidar5m
from django.contrib.postgres.aggregates import ArrayAgg


# variable-specific plot settings
# barb_resample = None
# barb_bins = .1
barb_length = 4.5
barb_lw = .8
barb_heights = 30
# colorbar labels for different datasets
cb_dict = {'cnr': 'CNR (dB)', 'drws': 'DRWS (m/s)',
           'xwind': 'x Wind Speed (m/s)', 'ywind': 'y Wind Speed (m/s)',
           'zwind': 'Vertical Wind Speed (m/s)',
           'hwind': 'Horizontal Wind Speed (m/s)',
           'barbs': None, 'temp': 'Temperature (K)',
           'vapor': 'Vapor Density (g/m³)',
           'liquid': 'Liquid (g/m³)', 'rh': 'Relative Humidity (%)',
           'tke': 'Turbulent Kinetic Energy (m²/s²)'}
centered_dict = {'cnr': False, 'drws': False, 'xwind': True,
                 'ywind': True, 'zwind': True, 'hwind': False,
                 'barbs': None, 'tke': False}
vmin_dict = {'cnr': -30}
vmax_dict = {'cnr': 0}
mwr_vars = ['temp', 'vapor', 'liquid', 'rh']
for v in mwr_vars:
    centered_dict[v] = False


# this is a fake axis class needed to trick autodatelocator to give me
# times without a real axis
class FakeAxis:
    def get_view_interval(self):
        return 0, 0
    def get_data_interval(self):
        return 0, 0
    def set_view_interval(self, vmin, vmax):
        pass
    def set_data_interval(self, vmin, vmax):
        pass
# set up the wind time locator
dummy_ax = FakeAxis()
xloc = AutoDateLocator(minticks=60, maxticks=80)
xloc.intervald = { YEARLY: [1, 2, 4, 5, 10, 20, 40, 50, 100, 200, 400,
                            500, 1000, 2000, 4000, 5000, 10000], MONTHLY: [1, 2, 3, 4, 6],
                   DAILY: [1, 2, 3, 7, 14, 21], HOURLY: [1, 2, 3, 4, 6, 12],
                   MINUTELY: [5, 10, 15, 20, 30], SECONDLY: [1, 5, 10, 15, 30],
                   MICROSECONDLY: [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000,
                                   5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000]}
# this autodatelocator really wants a graph axis even though it
# doesn't use it. So I'm going to give it this useless axis
xloc.set_axis(dummy_ax)


# so w.r.t. unwanted circles instead of barbs at low speeds-- it looks
# like I could get rid of the circles by overwriting _make_barbs in
# matplotlib.quiver.Barbs to replace circles with lines
class BarbsWithoutCircles(matplotlib.quiver.Barbs):
    def _make_barbs(self, u, v, nflags, nbarbs, half_barb, empty_flag, length,
                    pivot, sizes, fill_empty, flip):
        '''
        This function actually creates the wind barbs.  *u* and *v*
        are components of the vector in the *x* and *y* directions,
        respectively.

        *nflags*, *nbarbs*, and *half_barb*, empty_flag* are,
        *respectively, the number of flags, number of barbs, flag for
        *half a barb, and flag for empty barb, ostensibly obtained
        *from :meth:`_find_tails`.

        *length* is the length of the barb staff in points.

        *pivot* specifies the point on the barb around which the
        entire barb should be rotated.  Right now, valid options are
        'tip' and 'middle'. Can also be a number, which shifts the start
        of the barb that many points from the origin.

        *sizes* is a dictionary of coefficients specifying the ratio
        of a given feature to the length of the barb. These features
        include:

            - *spacing*: space between features (flags, full/half
               barbs)

            - *height*: distance from shaft of top of a flag or full
               barb

            - *width* - width of a flag, twice the width of a full barb

            - *emptybarb* - radius of the circle used for low
               magnitudes

        *fill_empty* specifies whether the circle representing an
        empty barb should be filled or not (this changes the drawing
        of the polygon).

        *flip* is a flag indicating whether the features should be flipped to
        the other side of the barb (useful for winds in the southern
        hemisphere).

        This function returns list of arrays of vertices, defining a polygon
        for each of the wind barbs.  These polygons have been rotated to
        properly align with the vector direction.
        '''

        # These control the spacing and size of barb elements relative to the
        # length of the shaft
        spacing = length * sizes.get('spacing', 0.125)
        full_height = length * sizes.get('height', 0.4)
        full_width = length * sizes.get('width', 0.25)
        empty_rad = length * sizes.get('emptybarb', 0.15)

        # Controls y point where to pivot the barb.
        pivot_points = dict(tip=0.0, middle=-length / 2.)

        # Check for flip
        if flip:
            full_height = -full_height

        endx = 0.0
        try:
            endy = float(pivot)
        except ValueError:
            endy = pivot_points[pivot.lower()]

        # Get the appropriate angle for the vector components.  The offset is
        # due to the way the barb is initially drawn, going down the y-axis.
        # This makes sense in a meteorological mode of thinking since there 0
        # degrees corresponds to north (the y-axis traditionally)
        angles = -(np.ma.arctan2(v, u) + np.pi / 2)

        # Used for low magnitude.  We just get the vertices, so if we make it
        # out here, it can be reused.
        empty_barb = [(endx, endy), (endx, endy + length)]

        barb_list = []
        for index, angle in np.ndenumerate(angles):
            
            # If the vector magnitude is too weak to draw flags
            if empty_flag[index]:
                poly_verts = empty_barb
            else:
                poly_verts = [(endx, endy)]
                offset = length
                
            # Add vertices for each flag
            for i in range(nflags[index]):
                # The spacing that works for the barbs is a little to much for
                # the flags, but this only occurs when we have more than 1
                # flag.
                if offset != length:
                    offset += spacing / 2.
                    poly_verts.extend(
                        [[endx, endy + offset],
                         [endx + full_height, endy - full_width / 2 + offset],
                         [endx, endy - full_width + offset]])

                offset -= full_width + spacing

            # Add vertices for each barb.  These really are lines, but works
            # great adding 3 vertices that basically pull the polygon out and
            # back down the line
            for i in range(nbarbs[index]):
                poly_verts.extend(
                    [(endx, endy + offset),
                     (endx + full_height, endy + offset + full_width / 2),
                     (endx, endy + offset)])

                offset -= spacing

            # Add the vertices for half a barb, if needed
            if half_barb[index]:
                # If the half barb is the first on the staff, traditionally it
                # is offset from the end to make it easy to distinguish from a
                # barb with a full one
                if offset == length:
                    poly_verts.append((endx, endy + offset))
                    offset -= 1.5 * spacing
                    poly_verts.extend(
                        [(endx, endy + offset),
                         (endx + full_height / 2, endy + offset + full_width / 4),
                         (endx, endy + offset)])

            # Rotate the barb according the angle. Making the barb first and
            # then rotating it made the math for drawing the barb really easy.
            # Also, the transform framework makes doing the rotation simple.
            poly_verts = matplotlib.transforms.Affine2D().rotate(-angle).transform(
                poly_verts)
            barb_list.append(poly_verts)

        return barb_list
matplotlib.quiver.Barbs = BarbsWithoutCircles


def xrlist_from_profiles(profiles, columns, time_min, time_max, minutes=5):
    # organize the xarray datasets
    datasets = []
    for profile in profiles:
        ranges = Scan.get_ranges(profile['xml']) / 1000
        coords = {'Time': profile['time'], 'Range': ranges}
        data_vars = {}
        for column in columns:
            data_vars[column] = (['Time', 'Range'], profile[column])
            attrs = {'lidar': profile['lidar__name'],
                     'scan': profile['name']}
            ds = xr.Dataset(data_vars=data_vars, coords=coords,
                            attrs=attrs)
            # fill in missing time values if needed
        if minutes is not None:
            t1 = np.datetime64(time_min); t2 = np.datetime64(time_max)
            time_index = np.arange(t1, t2, np.timedelta64(minutes, 'm'))
            ds = ds.reindex({'Time': time_index}, copy=False)
        datasets.append(ds)

    return datasets

def xrlist_from_mwrprofiles(profiles, columns, time_min, time_max, minutes=5):
    # organize the xarray datasets
    datasets = []
    for profile in profiles:
        ranges = Mwr.ranges
        coords = {'Time': profile['time'], 'Range': ranges}
        data_vars = {}
        for column in columns:
            data_vars[column] = (['Time', 'Range'], profile[column])
        attrs = {'lidar': profile['name'],
                 'scan': 'Microwave Radiometer'}
        ds = xr.Dataset(data_vars=data_vars, coords=coords,
                        attrs=attrs)

        # ideally I would get the profiles in chronological order from
        # the database. But. Django doesn't support that in version
        # 1.11. So. Instead I'm roerdering it here.
        ds = ds.reindex({'Time': np.sort(ds.coords['Time'])}, copy=False)
        ds = ds.resample('5T', 'Time')
        # fill in missing time values if needed
        t1 = np.datetime64(time_min); t2 = np.datetime64(time_max)
        time_index = np.arange(t1, t2, np.timedelta64(minutes, 'm'))
        ds = ds.reindex({'Time': time_index}, copy=False)
        ds.attrs = attrs
        datasets.append(ds)

    return datasets
    

# return a list of xarray objects
def xrlist_from_lidar5m(scan_ids, columns, time_min, time_max):
    # fields_dict = {'times': ArrayAgg('lidar5m__time')}
    fields_dict = {}
    for column in columns + ['time']:
        fields_dict[column] = ArrayAgg('lidar5m__' + column, )

    # get the data -- yes all the data at once -- yes really
    profiles = Scan.objects \
                   .filter(id__in=scan_ids,
                           lidar5m__time__range=(time_min, time_max)) \
                   .extra({'name': "(xpath('//lidar_scan/@name', xml)::varchar[])[1]"}) \
                   .values('id', 'lidar__name', 'name', 'xml') \
                   .annotate(**fields_dict)
    return xrlist_from_profiles(profiles, columns, time_min, time_max)

def xrlist_from_mwr(mwr_ids, columns, time_min, time_max):
    fields_dict = {}
    for column in columns + ['time']:
        fields_dict[column] = ArrayAgg('mwrprofile__' + column)

    # get the data -- yes all the data at once -- yes really
    profiles = Mwr.objects \
                  .filter(id__in=mwr_ids,
                          mwrprofile__time__range=(time_min, time_max),
                          mwrprofile__processor='Zenith') \
                  .values('id', 'name') \
                  .annotate(**fields_dict)
    return xrlist_from_mwrprofiles(profiles, columns, time_min, time_max)


def get_lidar_data(params):
    time_min = dt.datetime.strptime(params['time_min'],
                                    '%Y-%m-%dT%H:%M:00.000Z')
    time_max = dt.datetime.strptime(params['time_max'],
                                    '%Y-%m-%dT%H:%M:00.000Z')
    scan_ids = np.fromstring(params['scan_id'], sep=',')
    var = params['var']
    # figure out which columns we need to get
    if var == 'hwind':
        columns = ['xwind', 'ywind']
    else:
        columns = [var]

    # get the data
    if var in Mwr.mwr_vars:
        lidars = xrlist_from_mwr(scan_ids, columns, time_min,
                                 time_max)
    else:
        lidars = xrlist_from_lidar5m(scan_ids, columns, time_min,
                                     time_max)
    # calculate wind speeds if needed
    if var == 'hwind':
        for l0 in lidars:
            l0['hwind'] = np.sqrt(l0['xwind'] ** 2 + l0['ywind'] ** 2)
    return lidars

def get_barb_data(params):
    time_min = dt.datetime.strptime(params['time_min'],
                                    '%Y-%m-%dT%H:%M:00.000Z')
    time_max = dt.datetime.strptime(params['time_max'],
                                    '%Y-%m-%dT%H:%M:00.000Z')
    scan_ids = np.fromstring(params['scan_id'], sep=',')

    # get nice time intervals
    times = [ num2date(n) for n in xloc.tick_values(time_min, time_max) ]

    fields_dict = {}
    for column in ['xwind', 'ywind', 'time']:
        fields_dict[column] = ArrayAgg('lidar5m__' + column)
        
    # profiles = Scan.objects \
    #                .filter(id__in=scan_ids,
    #                        lidar5m__time__range=(time_min, time_max)) \
    #                .extra({'name': "(xpath('//lidar_scan/@name', xml)::varchar[])[1]"},
    #                       where=["(date_part('minute', time)::int %% 20)=0"]) \
    #                .values('id', 'lidar__name', 'name', 'xml') \
    #                .annotate(**fields_dict)
    profiles = Scan.objects \
                   .filter(id__in=scan_ids,
                           lidar5m__time__in=times) \
                   .extra({'name': "(xpath('//lidar_scan/@name', xml)::varchar[])[1]"}) \
                   .values('id', 'lidar__name', 'name', 'xml') \
                   .annotate(**fields_dict)

    dss = xrlist_from_profiles(profiles, ['xwind', 'ywind'], time_min, time_max,
                               minutes=None)
    for ds in dss:
        ds['windspeed'] = xr.concat([ds['xwind'], ds['ywind']], dim='Component')
        ds.coords['Component'] = ['x', 'y']
    return dss


def get_plot(params):
    time_min = dt.datetime.strptime(params['time_min'],
                                    '%Y-%m-%dT%H:%M:00.000Z')
    time_max = dt.datetime.strptime(params['time_max'],
                                    '%Y-%m-%dT%H:%M:00.000Z')
    barbs = 'barbs' in params.keys() and params['barbs'] == 'True'
    var = params['var']
    lgd = None
    has_barbs = var == 'barbs' or barbs
    if var == 'barbs':
        lidars = get_barb_data(params)
    else:
        lidars = get_lidar_data(params)
    if barbs:
        ds_barbs = get_barb_data(params)
    nds = len(lidars)
    figsize = (10, 3.5 * nds)
    sharey = False
    f, axarr = plt.subplots(nds, #sharex=True,
                            sharey=sharey,
                            squeeze=False,
                            figsize=figsize)
    cbar_kwargs = {'label': cb_dict[var]}
    is_centered = centered_dict[var]
    graph_center = 0 if is_centered else False
    cmap = 'coolwarm' if is_centered else 'jet'

    for i, ds in enumerate(lidars):
        ax = axarr[i][0]
        title = ds.attrs['lidar'] + ' (' + ds.attrs['scan'] + ')'
        if has_barbs: # get nice range intervals
            # find the scan range_res
            ranges = ds.coords['Range'].values
            ydelta = ranges[1] - ranges[0]
            # get the desired average barb height locations
            ysteps = np.arange(1, 10)
            yloc = MaxNLocator(nbins=barb_heights, steps=ysteps)
            heights = yloc._raw_ticks(0, len(ranges))
            dheight = (heights[1] - heights[0]) * ydelta
            
        if var == 'barbs':
            ds['windspeed'].rasp.plot_barbs(x='Time', y='Range',
                                            components=['x', 'y'],
                                            # resample=barb_resample,
                                            # resampley=barb_bins,
                                            resampley=dheight,
                                            ax=ax,
                                            length=barb_length)
            ax.set_title(title)
            ax.set_xlim([time_min, time_max])
            ax.set_xlabel('Time (UTC)')
            ax.set_ylabel('Range (km)')
        else:
            vmin = vmin_dict[var] if var in vmin_dict.keys() else None
            vmax = vmax_dict[var] if var in vmax_dict.keys() else None
            try:
                da = ds[var]
                da.plot.pcolormesh(x='Time', y='Range', center=graph_center,
                                   robust=True, cmap=cmap, ax=ax,
                                   vmin=vmin, vmax=vmax,
                                   cbar_kwargs=cbar_kwargs)
            except:
                # this happens occasionally when all data is NA, or
                # there's only one profile of data
                Z = np.zeros((ds.dims['Time'], ds.dims['Range'])).transpose()
                # Z = da.values.transpose()
                Zm = np.ma.masked_where(np.isnan(Z), Z)
                ax.pcolormesh(ds.coords['Time'].values,
                              ds.coords['Range'].values, Zm)
            ax.set_title(title)
            ax.set_xlim([time_min, time_max])
            ax.set_xlabel('Time (UTC)')
            ax.set_ylabel('Range (km)')
            if barbs:
                ds = ds_barbs[i]
                ds['windspeed'].rasp.plot_barbs(x='Time', y='Range',
                                                components=['x', 'y'],
                                                # resample=barb_resample,
                                                # resampley=barb_bins,
                                                resampley=dheight,
                                                ax=ax,
                                                length=barb_length,
                                                lw=barb_lw)
    png_output = BytesIO()
    if lgd is None:
        plt.tight_layout()
        canvas = FigureCanvas(plt.gcf())
        canvas.print_png(png_output)
    else:
        plt.savefig(png_output, format='png',
                    bbox_extra_artists=(lgd,),
                    bbox_inches='tight')
    response = png_output.getvalue()
    # have to make sure to close things duh
    plt.close()
    png_output.close()
    return response
