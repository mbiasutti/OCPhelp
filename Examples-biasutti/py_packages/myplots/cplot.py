def my_contourf(X, subplot=111, vmin=None, vmax=None, levels=None, 
        clon=180, cmap='jet', title=False, grid=False):
    """ quick global plot with coasts, labels and gridlines """
    from matplotlib import pyplot as plt
    import numpy as np
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature 
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
    
    proj = ccrs.PlateCarree(central_longitude=clon)
    trans = ccrs.PlateCarree()
    ax = plt.subplot(subplot,projection=proj)
    im = X.plot.contourf(vmin=vmin, vmax=vmax, levels=levels, add_colorbar =False, 
            transform=trans,cmap=plt.get_cmap(cmap))
    #cb = plt.colorbar(im, orientation='horizontal', shrink = 0.8, pad=0.15, extend='none')
    cb = plt.colorbar(im, extend='both', shrink = 0.75)
    cb.set_label(X.name+' in '+X.units)
    if grid: 
        ax.coastlines(linewidth=1.5,color="grey")
        ax.set_xticks(np.arange(0, 361, 90), crs=trans)
        ax.set_yticks(np.arange(-90,91,30), crs=trans)
        lon_formatter = LongitudeFormatter(zero_direction_label=True)
        lat_formatter = LatitudeFormatter()
        ax.xaxis.set_major_formatter(lon_formatter)
        ax.yaxis.set_major_formatter(lat_formatter)
        ax.gridlines(xlocs=np.arange(0, 361, 90),ylocs = np.arange(-90,91,30))
    if title: 
        ax.set_title(title,fontsize=16)

