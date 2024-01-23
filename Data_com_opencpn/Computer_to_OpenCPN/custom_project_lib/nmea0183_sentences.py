import pynmea2
import time
from datetime import datetime
from typing import Optional
from .converter_location_format import CONVERTER

class NMEA0183_GEN:
    @staticmethod
    def __getDirection(direction, value):
        valid_lat_str = ["latitude", "lat"]
        valid_long_str = ["longitude", "long", "lon"]
        if (direction not in valid_lat_str) and (direction not in valid_long_str):
            return "NONE"
        elif direction in valid_lat_str:
            if float(value) < 0:
                return "S"
            else:
                return "N"
        elif direction in valid_long_str:
            if float(value) < 0:
                return "W"
            else:
                return "E"
    
    # RMB SENTENCE >>> $GPRMB,A,x.x,a,c--c,d--d,llll.ll,e,yyyyy.yy,f,g.g,h.h,i.i
    # Recommended Minimum Navigation Information B
    @staticmethod
    def rmb(*,
            status = "V", # A = Data Valid, V = Data Invalid
            cross_track_error_nautical_miles: Optional[float] = None, # Cross-track error in nautical miles to the nearest 0.01 nautical miles
            direction_to_steer = '', # Direction to steer, L or R
            origin_waypoint_id = '', # Origin waypoint ID
            destination_waypoint_id = '', # Destination waypoint ID
            destination_latitude: Optional[float] = None, # Destination waypoint latitude
            destination_latitude_direction = '', # Destination waypoint latitude direction, N or S
            destination_longitude: Optional[float] = None, # Destination waypoint longitude
            destination_longitude_direction = '', # Destination waypoint longitude direction, E or W
            range_to_destination_nautical_miles: Optional[float] = None, # Range to destination in nautical miles to the nearest 0.1 nautical miles
            bearing_to_destination_true: Optional[float] = None, # Bearing to destination in degrees True to the nearest 0.1 degree
            destination_closing_velocity_knots: Optional[float] = None, # Destination closing velocity in knots to the nearest 0.1 knot
            arrival_status = '' # Arrival status, A = Arrival circle entered, V = Not entered
            ) -> str:
        return pynmea2.RMB('GP', 'RMB', (
            str(status),
            str(cross_track_error_nautical_miles) or '',
            str(direction_to_steer),
            str(origin_waypoint_id),
            str(destination_waypoint_id),
            CONVERTER.DD_DM("lat", destination_latitude) or '',
            str(destination_latitude_direction) or '',
            CONVERTER.DD_DM("long", destination_longitude) or '',
            str(destination_longitude_direction) or '',
            str(range_to_destination_nautical_miles) or '',
            str(bearing_to_destination_true) or '',
            str(destination_closing_velocity_knots) or '',
            str(arrival_status)
        )).render() + '\r\n'

    # RMC SENTENCE >>> $GPRMC,hhmmss.ss,A,llll.ll,a,yyyyy.yy,a,x.x,x.x,ddmmyy,x.x,a
    # Recommended Minimum Navigation Information C
    @staticmethod
    def rmc(*, 
            time_data = str((float(time.strftime("%H%M%S")) - 10000.0)) +"00", # Time - hhmmss.ss
            status = "V", # A = Data Valid, V = Data Invalid
            lat: Optional[float] = None,
            long: Optional[float] = None,
            speed_over_ground_knots: Optional[float] = None, # Speed over ground in knots 0.1
            track_angle_degree_true: Optional[float] = None, # Track angle in degrees True 45
            date_ddmmyy = str((float(time.strftime("%d%m%y")) - 10000.0)) +"00", # Date - ddmmyy
            magnetic_variation_degrees: Optional[float] = None, # Magnetic variation degrees (Easterly var. subtracts from true course) 0.1
            magnetic_direction = '', # E = East, W = West
            navigation_status = '' # A = Data Valid, V = Data Invalid
            ) -> str:
        return pynmea2.RMC('GP', 'RMC', (
            time_data,
            str(status),
            CONVERTER.DD_DM("lat", lat) or '',
            NMEA0183_GEN.__getDirection("latitude", lat) if lat is not None else '',
            CONVERTER.DD_DM("long", long) or '',
            NMEA0183_GEN.__getDirection("longitude", long) if long is not None else '',
            str(speed_over_ground_knots) or '',
            str(track_angle_degree_true) or '',
            date_ddmmyy or str(datetime.now().strftime("%d%m%y")),
            str(magnetic_variation_degrees) or '',
            str(magnetic_direction),
            str(navigation_status)
        )).render() + '\r\n'
        
    # GGA SENTENCE >>> $GPGGA,hhmmss.ss,llll.ll,a,yyyyy.yy,a,x,xx,x.x,x.x,M,x.x,M,x.x,xxxx
    # Global Positioning System Fix Data
    @staticmethod
    def gga(*,
            time_data = str((float(time.strftime("%H%M%S")) - 10000.0)) +"00", 
            lat: Optional[float] = None, 
            long: Optional[float] = None, #lat and long in degree minutes format(DM)
            fix_quality: Optional[int] = None, # 0 = Invalid, 1 = GPS fix, 2 = DGPS fix, 3 = PPS fix, 4 = Real Time Kinematic, 5 = Float RTK, 6 = Estimated (dead reckoning), 7 = Manual input mode, 8 = Simulation mode
            satellites: Optional[int] = None, #number of satellites being tracked
            horizontal_dilution_of_precision: Optional[float] = None, #horizontal dilution of precision
            elevation_above_sea_level: Optional[float] = None, #elevation above sea level
            elevation_unit = '', 
            geoid: Optional[float] = None, #geoid separation
            geoid_unit = '', 
            age_of_correction_data_seconds = '',  #age of correction data in seconds
            correction_station_id = '' #correction station ID 0000-1023
            ) -> str:

        return pynmea2.GGA('GP', 'GGA', (
            time_data, # hhmmss.ss
            CONVERTER.DD_DM("lat", lat) or '',
            NMEA0183_GEN.__getDirection("latitude", lat) if lat is not None else '',
            CONVERTER.DD_DM("long", long) or '',
            NMEA0183_GEN.__getDirection("longitude", long) if long is not None else '',
            str(fix_quality) or '',
            str(satellites) or '',
            str(horizontal_dilution_of_precision) or '',
            str(elevation_above_sea_level) or '',
            str(elevation_unit),
            str(geoid) or '',
            str(geoid_unit),
            str(age_of_correction_data_seconds),
            str(correction_station_id)
        )).render() + '\r\n'

    # GSV SENTENCE >>> $GPGSV
    # GPS Satellites in view
    @staticmethod
    def gsv(*, 
            number_of_sentences: Optional[int] = None, #total number of GSV sentences in this cycle
            sentence_number: Optional[int] = None, #sentence number
            number_of_satellites_in_view: Optional[int] = None, #total number of satellites in view
            satellite_prn_number_1: Optional[int] = None, #satellite PRN number 1
            elevation_degrees_1: Optional[int] = None, #elevation in degrees 1
            azimuth_degrees_1: Optional[int] = None, #azimuth in degrees 1
            snr_1: Optional[int] = None, #SNR 1
            satellite_prn_number_2: Optional[int] = None, #satellite PRN number 2
            elevation_degrees_2: Optional[int] = None, #elevation in degrees 2
            azimuth_degrees_2: Optional[int] = None, #azimuth in degrees 2
            snr_2: Optional[int] = None, #SNR 2
            satellite_prn_number_3: Optional[int] = None, #satellite PRN number 3
            elevation_degrees_3: Optional[int] = None, #elevation in degrees 3
            azimuth_degrees_3: Optional[int] = None, #azimuth in degrees 3
            snr_3: Optional[int] = None, #SNR 3
            satellite_prn_number_4: Optional[int] = None, #satellite PRN number 4
            elevation_degrees_4: Optional[int] = None, #elevation in degrees 4
            azimuth_degrees_4: Optional[int] = None, #azimuth in degrees 4
            snr_4: Optional[int] = None #SNR 4
            ) -> str:
        return pynmea2.GSV('GP', 'GSV', (
            str(number_of_sentences) or '1',
            str(sentence_number) or '1 ',
            str(number_of_satellites_in_view) or '',
            str(satellite_prn_number_1) or '',
            str(elevation_degrees_1) or '',
            str(azimuth_degrees_1) or '',
            str(snr_1) or '',
            str(satellite_prn_number_2) or '',
            str(elevation_degrees_2) or '',
            str(azimuth_degrees_2) or '',
            str(snr_2) or '',
            str(satellite_prn_number_3) or '',
            str(elevation_degrees_3) or '',
            str(azimuth_degrees_3) or '',
            str(snr_3) or '',
            str(satellite_prn_number_4) or '',
            str(elevation_degrees_4) or '',
            str(azimuth_degrees_4) or '',
            str(snr_4) or ''
        )).render() + '\r\n'
    
    # GGL SENTENCE >>> $GPGLL,llll.ll,a,yyyyy.yy,a,hhmmss.ss,A
    # Geographic Position - Latitude/Longitude
    @staticmethod
    def gll(*, 
            lat: Optional[float] = None, 
            long: Optional[float] = None, #lat and long in degree minutes format(DM)
            time_data = str((float(time.strftime("%H%M%S")) - 10000.0)) +"00", 
            status = "V" # A = Data Valid, V = Data Invalid
            ) -> str:
        return pynmea2.GLL('GP', 'GLL', (
            CONVERTER.DD_DM("lat", lat) or '',
            NMEA0183_GEN.__getDirection("latitude", lat) if lat is not None else '',
            CONVERTER.DD_DM("long", long) or '',
            NMEA0183_GEN.__getDirection("longitude", long) if long is not None else '',
            time_data,
            str(status)
        )).render() + '\r\n'
    
    # VTG SENTENCE >>> $GPVTG,x.x,T,x.x,M,x.x,N,x.x,K
    # Course Over Ground and Ground Speed
    @staticmethod
    def vtg(*,
            track_degrees_true: Optional[float] = None, #track degrees true
            true = 'T', #T true
            track_degrees_magnetic: Optional[float] = None, #track degrees magnetic
            magnetic = 'M', #M magnetic
            speed_knots: Optional[float] = None, #speed over ground knots
            knots = 'N', #N knots
            speed_kph: Optional[int] = None, #speed over ground km/h
            kmh = 'K' #K km/h
            ) -> str:
        return pynmea2.VTG('GP', 'VTG', (
            str(track_degrees_true) or '',
            str(true),
            str(track_degrees_magnetic) or '',
            str(magnetic),
            str(speed_knots) or '',
            str(knots),
            str(speed_kph) or '',
            str(kmh)
        )).render() + '\r\n'
    
    # ZDA SENTENCE >>> $GPZDA,hhmmss.ss,dd,mm,yyyy,xx,yy
    # Time & Date - UTC, day, month, year and local time zone
    @staticmethod
    def zda(*,
            time_data = str((float(time.strftime("%H%M%S")) - 10000.0)) +"00",
            day = str(datetime.now().strftime("%d")),
            month = str(datetime.now().strftime("%m")),
            year = str(datetime.now().strftime("%Y")),
            local_zone_hours = '00',
            local_zone_minutes = '00',
            ) -> str: 
        return pynmea2.ZDA('GP', 'ZDA', (
            time_data,
            day,
            month,
            year,
            local_zone_hours,
            local_zone_minutes
        )).render() + '\r\n'
     