from .nmea0183_sentences import NMEA0183_GEN

class NMEA0183_GEN_TEST:
    '''
    This class is used to test the NMEA0183_GEN class.
    All the functions in this class return a NMEA0183 sentence.
    Some functions require the latitude and longitude to be passed in.
    Some parameters are set to default values.
    '''
    def __init__(self):
        pass

    def test_hdt(*, latitude: float | None, longitude: float | None, print_sentence = False) -> str:
        '''
        This function tests the hdt() function in NMEA0183_GEN class.
        '''
        hdt_sentence = NMEA0183_GEN.hdt(heading_degrees_true = 45)
        if print_sentence:
            print(hdt_sentence)
        return hdt_sentence
    
    def test_hdm(*, latitude: float | None, longitude: float | None, print_sentence = False) -> str:
        '''
        This function tests the hdm() function in NMEA0183_GEN class.
        '''
        hdm_sentence = NMEA0183_GEN.hdm(heading_degrees_magnetic = 45)
        if print_sentence:
            print(hdm_sentence)
        return hdm_sentence
    
    def test_hdg(*, latitude: float | None, longitude: float | None, print_sentence = False) -> str:
        '''
        This function tests the hdg() function in NMEA0183_GEN class.
        '''
        hdg_sentence = NMEA0183_GEN.hdg(heading_degrees_true = 45, 
                                heading_degrees_magnetic = 45, 
                                deviation_degrees = 45, 
                                deviation_direction = "E", 
                                variation_degrees = 45, 
                                variation_direction = "E")
        if print_sentence:
            print(hdg_sentence)
        return hdg_sentence
    
    def test_rmb(*, latitude: float | None, longitude: float | None, print_sentence = False) -> str:
        '''
        This function tests the rmb() function in NMEA0183_GEN class.
        '''
        rmb_sentence = NMEA0183_GEN.rmb(cross_track_error_nautical_miles = 0.0, #0.1
                                direction_to_steer = "R", 
                                origin_waypoint_id = "0000", 
                                destination_waypoint_id = "0001", 
                                destination_latitude = latitude, 
                                destination_longitude = longitude, 
                                range_to_destination_nautical_miles = 0.0, #0.1
                                bearing_to_destination_true = 0.0, #45
                                destination_closing_velocity_knots = 0.0, #0.1
                                arrival_status = "A")
        if print_sentence:
            print(rmb_sentence)
        return rmb_sentence
    
    def test_rmc(*, latitude: float | None, longitude: float | None, print_sentence = False) -> str:
        '''
        This function tests the rmc() function in NMEA0183_GEN class.
        '''
        rmc_sentence = NMEA0183_GEN.rmc(time_data = None, 
                                status = "A", 
                                lat = latitude, 
                                long = longitude, 
                                speed_over_ground_knots = 0.0, #0.1
                                course_over_ground_true = 0.0, #45
                                date = None, 
                                magnetic_variation = 0.0, #0.1
                                magnetic_variation_direction = "E")
        if print_sentence:
            print(rmc_sentence)
        return rmc_sentence
    
    def test_gga(*, latitude: float | None, longitude: float | None, print_sentence = False) -> str:
        '''
        This function tests the gga() function in NMEA0183_GEN class.
        '''
        gga_sentence = NMEA0183_GEN.gga(lat = latitude, 
                                long = longitude, 
                                fix_quality = 1, 
                                satellites = 10, 
                                horizontal_dilution_of_precision = 0.1, 
                                elevation_above_sea_level = 255.747, 
                                elevation_unit = "M", 
                                geoid = -32.00, 
                                geoid_unit = "M", 
                                age_of_correction_data_seconds = "01", 
                                correction_station_id = "0000")
        if print_sentence:
            print(gga_sentence)
        return gga_sentence
    
    def test_gsv(*, latitude: float | None, longitude: float | None, print_sentence = False) -> str:
        '''
        This function tests the gsv() function in NMEA0183_GEN class.
        '''
        gsv_sentence = NMEA0183_GEN.gsv(number_of_sentences_in_cycle = 1, 
                                sentence_number = 1, 
                                total_satellites_in_view = 10, 
                                satellite_prn_number_1 = 1, 
                                elevation_degrees_1 = 45, 
                                azimuth_true_degrees_1 = 45, 
                                snr_1 = 45, 
                                satellite_prn_number_2 = 2, 
                                elevation_degrees_2 = 45, 
                                azimuth_true_degrees_2 = 45, 
                                snr_2 = 45, 
                                satellite_prn_number_3 = 3, 
                                elevation_degrees_3 = 45, 
                                azimuth_true_degrees_3 = 45, 
                                snr_3 = 45, 
                                satellite_prn_number_4 = 4, 
                                elevation_degrees_4 = 45, 
                                azimuth_true_degrees_4 = 45, 
                                snr_4 = 45)
        if print_sentence:
            print(gsv_sentence)
        return gsv_sentence
    
    def test_gll(*, latitude: float | None, longitude: float | None, print_sentence = False) -> str:
        '''
        This function tests the gll() function in NMEA0183_GEN class.
        '''
        gll_sentence = NMEA0183_GEN.gll(lat = latitude, 
                                long = longitude, 
                                time_data = None, 
                                status = "A", 
                                mode_indicator = "A")
        if print_sentence:
            print(gll_sentence)
        return gll_sentence
    
    def test_vtg(*, latitude: float | None, longitude: float | None, print_sentence = False) -> str:
        '''
        This function tests the vtg() function in NMEA0183_GEN class.
        '''
        vtg_sentence = NMEA0183_GEN.vtg(course_over_ground_true = 45, 
                                course_over_ground_magnetic = 45, 
                                speed_over_ground_knots = 0.0, #0.1
                                speed_over_ground_kilometers_per_hour = 0.0, #0.1
                                mode_indicator = "A")
        if print_sentence:
            print(vtg_sentence)
        return vtg_sentence
    
    def test_zda(*, latitude: float | None, longitude: float | None, print_sentence = False) -> str:
        '''
        This function tests the zda() function in NMEA0183_GEN class.
        '''
        zda_sentence = NMEA0183_GEN.zda(time_data = None, 
                                day = None, 
                                month = None, 
                                year = None, 
                                local_zone_hours = None, 
                                local_zone_minutes = None)
        if print_sentence:
            print(zda_sentence)
        return zda_sentence
