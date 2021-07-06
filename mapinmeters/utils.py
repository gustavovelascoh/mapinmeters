import pandas as pd
import pynmea2


def nmea2df(data_src):

    file = open(data_src)    
    llh_data = []
    
    for line in file.readlines():
        try:
            msg = pynmea2.parse(line)
            if type(msg) == pynmea2.types.talker.GGA:                
                llh_entry = {}
                llh_entry["latitude"] = msg.latitude
                llh_entry["longitude"] = msg.longitude
                llh_entry["q"] = msg.gps_qual
                llh_entry["age"] = msg.age_gps_data
                llh_entry["ns"] = msg.num_sats
                
                llh_data.append(llh_entry)

        except pynmea2.ParseError as e:
            print('Parse error: {}'.format(e))
            continue
        
    position_df = pd.DataFrame(llh_data)
    position_df["age"] = pd.to_numeric(position_df["age"])
    position_df["ns"] = pd.to_numeric(position_df["ns"])

    return position_df