def to_pandas(Tgrid):
    import pandas as pd
    """
    Parse the time grid of a MONTHLY Dataset and replace by a pandas time grid.
    If the time units are days since, this is approximate, but should take care of 
    different calendars (gregorian, noleap, 360).
    """
    # first get the reference year from units
    words = Tgrid.units.split()
    start_date = words[2].split('-')
    ref_year = int(start_date[0])
    # check what happens if time is from otehr than january
        
    # get the first time grid value
    first_time = Tgrid.values[0] 
    if 'months since' in Tgrid.units:
        datetime = enso2date(first_time - 0.5,ref_year)
        return pd.date_range(start = datetime, periods=Tgrid.shape[0], 
                             freq='MS').shift(15, freq='D')
    elif 'days since' in Tgrid.units:
        if 'gregorian' in Tgrid.calendar or 'standard' in Tgrid.calendar:
            days_in_year = 365.25
        elif '365' in Tgrid.calendar or 'noleap' in Tgrid.calendar:
            days_in_year = 365
        elif '360' in Tgrid.calendar: 
            days_in_year = 360
        else:
            days_in_year = 365.25
            print('Unrecognized calendar -- assume gregorian')
        datetime = enso2date((first_time//days_in_year)*12 + 
                        (first_time%days_in_year)//30 - 0.5,ref_year)
        return pd.date_range(start = datetime, periods=Tgrid.shape[0], 
                        freq='MS').shift(15, freq='D')
    else:
        print('Unrecognized time grid')
        return

def enso2date(T0,ryear=1960,leap=True):
    """
    Print the date corresponding to an enso-time (months since 1960). The reference year can be changed.
    """
    norm = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    iy = ryear + int(T0/12)
    if T0 < 0:
        iy = iy - 1
    res = T0 - (iy - ryear)*12
    im = int(res) + 1
    if im == 13:
        im = 1
        iy = iy + 1
    if leap & (im == 2) &  (iy % 4 == 0 ):   
        id = 1 + int(29 * (res - int(res)))
    else:
        id = 1 + int(norm[im-1] * (res - int(res)))
    return str(im)+'/'+str(id)+'/'+str(iy)    
