class CONVERTER:
    '''
    This class is used to convert the location format from one to another
    Currently, it supports the following conversions:
    - DD to DM
    '''
    @staticmethod
    def DD_DM(geographic_coordinate_system: str, decimal_degrees: str): #decimal degree -> degrees minutes
        '''
        This function converts the location format from decimal degree to degrees minutes.
        - geographic_coordinate_system: "lat" or "long" or "latitude" or "longitude"
        - decimal_degrees: decimal degree
        \n
        Return: degrees minutes format
        \n
        Example:
        - Input: DD_DM("lat", 53.679746945954754)
        - Output: 5339.19
        '''
        try: #Check for correct format of decimal_degree (any number format)
            float(decimal_degrees)
        except ValueError:
            return "[DD to DM conversion unsuccessful]"
        
        #Must be lat or long
        valid_lat_str = ["lat", "latitude"]
        valid_long_str = ["long", "longitude", "lon"]
        if (geographic_coordinate_system.lower() not in valid_lat_str) and (geographic_coordinate_system.lower() not in valid_long_str):
            return "[DD to DM conversion unsuccessful]"
        else:
            degree = str(int(decimal_degrees))
            minutes = str(abs((decimal_degrees - int(decimal_degrees)) * 60.0))

        #Lat must have 4 digits, in which 2 are for degree and 2 are for minutes
        if geographic_coordinate_system.lower() in valid_lat_str:
            # print("Config lat")
            negative = False
            if decimal_degrees < 0:
                negative = True
                degree = degree.replace("-", '', 1)
            if len(degree) < 2:
                i = 2 - len(degree)
                for j in range(0, i):
                    degree = "0" + degree
                if negative == True: #return the minus
                    degree = "-" + degree

        #Long must have 5 digits, in which 3 are for degree and 2 are for minutes
        else:
            # print("Config long")
            negative = False
            if decimal_degrees < 0:
                negative = True
                degree = degree.replace("-", '', 1)
            if len(degree) < 3:
                i = 3 - len(degree)
                for j in range(0, i+1):
                    degree = "0" + degree
                if negative == True: #return the minus
                    degree = "-" + degree
        
        return degree + minutes