# one-scotland-gazetteer

#### How to use this repository 

This repository includes two things:

(A) Python 3.x code, examples, and scripts to test the One Scotland Gazetteer (OSG) web services and FTP download.

(B) General documentation for the OSG web services and FTP.

#### Assumptions to use the python code

**(A)** You have installed python 3.x in your operating system (OS)

**(B)** You have registered with the One Scotland Gazetteer (OSG) and can you are authorised to use the OSG web service
or the OSG FTP. To learn more please visit the [One Scotland Gazetteer](https://osg.scot) website.

#### Instructions to use the python code

**(A) Edit the ```development.ini```:**

In the root folder of this repository edit the development.ini file and add your username and password for the OSG FTP and
the OSG web services. These credentials are provided by the One Scotland Gazetteer Custodian and you may have different for
the FTP and the Web services.

**(B)** Use the web services examples: 

```python rest.py```

**(C)** Use the FTP functionality by running the following

```python download_osg_using_ftp.py```

# Documentation

**Overview:** 
This documentation provides information on how to use programmatically two of the "One Scotland Gazetteer" (OSG) 
services:

**(1)** Web service; The web service communicates directly with the OSG database and allows you to access the gazetteer 
in real time, providing the most up to date information. OSG supports two types of services; the "Representational 
state transfer" (REST) and the "Simple Object Access Protocol" (SOAP). 

**(2)**  Export files; An export may be provided in the Scottish Data Transfer Format (SDTF) as a CSV file. Exports, 
will be scheduled to be run at a predetermined frequency.  A subset of data may also be supplied to match your 
requirements.

For additional information please visit the [One Scotland Gazetteer](https://osg.scot) website.

### Web services 
The OSG web services are structured around **datasets**, which contain **fields** which in turn contain the actual 
**data**. Each web service dataset returns different fields & data and may also support different functionality. The 
OSG has two web services ```sendNGListDataSetsMessage``` (henceforth **list**) which returns the datasets available for 
querying, and ```sendNGSearchMessage``` (henceforth **search**) which allows queries to be performed on those datasets. 
The maximum count of records returned by the OSG web services cannot exceed **250**. The OSG services descriptions can 
be found at [REST](https://osg.scot/services/NGSearchServiceRest?_wadl) and 
[SOAP](https://osg.scot/services/NGSearchService?wsdl) respectively.

**Authentication:** All OSG web services require authentication using a ```username``` and a ```password```. Both 
```username``` and a ```password``` should be provided in the ```HTTP request headers``` for every request sent to the 
web service. An example of the authentication request headers for both REST and SOAP using fake credentials can be found 
below:

**REST**
```
Content-Type:application/json
Accept:application/json
username:Alice
password:secret
```

**SOAP**
```
<soapenv:Header>
 <v0:HeaderLogin>
  <username>Alice</username>
  <password>secret</password>
 </v0:HeaderLogin>
</soapenv:Header>
```

**Authorisation:** Authenticating with the OSG web service using your ```username``` and ```password``` does not mean 
that you have access to all available OSG datasets. Access to datasets is administrated by the OSG custodian and if 
access is needed for additional datasets the users need to visit the [One Scotland Gazetteer](https://osg.scot) website 
and raise a request. For example, a successfully authenticated user may be authorised to access the **search** web 
service (```sendNGSearchMessage```) only with the ```EST_STANDARD_SEARCH``` dataset but not  the ```ADDRESS_SEARCH``` 
dataset.


**Datasets:** The **list** web service can return all available OSG datasets. The OSG datasets list can be dynamic 
since the OSG custodian can easily create new ones if there is value to them. To get a list of all the available 
**datasets** including the **fields** for each dataset which can be queried the following request can be used:

**REST**

Request body
```
{"listdatasets":{}}
```

Response body

```{
    "ListDataSetsResponseMessage":{
        "Header":{
            "ResultCount":8,
            "ReturnCount":8,
            "ErrorCode":0,
            "ErrorMessage":"Success"
            },
            
        "NGListDataSetsResponseData":[
            {"DataSet":"EST_STANDARD_SEARCH","Col":["Address_One_Line","Custodian","Easting","Northing","Parent_UPRN","Postcode","Search_Building_Name","Search_Building_No","Search_Postcode_No_Space","Search_Street_Name","Search_Town","Status","UPRN","USRN"]},
            {"DataSet":"FVGIS_STANDARD_SEARCH","Col":["Address_One_Line","address_one_line_custom","County_Name","Custodian","Easting","Locality_Name","Northing","paon","PAO_NO","Postcode","Post_Town","p_text","record_type_id","saon","SAO_NO","search_building","search_building_name","search_building_no","search_street_name","search_town","Status","s_text","Street_Descriptor","Town","uprn","usrn","x_coordinate","y_coordinate"]},
            {"DataSet":"FVGIS_STREET_SEARCH","Col":["Custodian","End_Easting","End_Northing","Local_Authority","Locality","search_street_name","search_street_town","Start_Easting","Start_Northing","Street_Name","street_one_line","Town","usrn"]},
            {"DataSet":"GLASGOW_ACCESS_SAP","Col":["ADDRESS_ONE_LINE","ADR03","ADR04","FLOOR","LAND1","LOCALITY","ORT01","ORT02","PAO_NO","PSTLZ","P_TEXT","SAO_NO","search_line_one","search_postcode_no_space","STATE","S_TEXT","STREET_DESCRIPTOR","UPRN"]},
            {"DataSet":"STANDARD_SEARCH","Col":["ADDRESS_ONE_LINE","Custodian","Easting","Northing","Postcode","search_building_name","search_building_no","search_street_name","search_town","Status","UPRN"]},
            {"DataSet":"STANDARD_SEARCH_OLDP","Col":["address_one_line","Custodian","Easting","Northing","Postcode","search_building_name","search_building_no","search_postcode_no_space","search_street_name","search_town","Status","uprn"]},
            {"DataSet":"STD_ADDRESS_SEARCH","Col":["ADD_LINE_1","ADD_LINE_2","ADD_LINE_3","address_string","la_code","POST_CODE","start_date","TOWN","UPRN","USRN","x_coord","y_coord"]},
            {"DataSet":"WLC_SEARCH","Col":["Address_One_Line","address_one_line_custom","County_Name","Custodian","Easting","Locality_Name","Northing","paon","PAO_NO","Postcode","Post_Town","p_text","record_type_id","saon","SAO_NO","search_building","search_building_name","search_building_no","search_street_name","search_town","Status","s_text","Street_Descriptor","Town","uprn","usrn","x_coordinate","y_coordinate"]}
            ]
        }
    }
```


**Query:** Querying the OSG data includes using the **search** web service and fields or/and geometries. The **search**
web service can receive the following inputs:

**REST Examples**

(1) Return OSG records from the ```EST_STANDARD_SEARCH``` dataset.

Request body

```
{"query":{
    "dataset":"EST_STANDARD_SEARCH",
    "type":"full"
}}

```
Response body
```
{
    "SearchResponseMessage": {
        "NGSearchResponseData": {
            "Header": {
                "ResultCount": 3296208,
                "ReturnCount": 250,
                "ErrorCode": 0,
                "ErrorMessage": "Success"
            },
            "Result": {
                  "any": [ 
                      [CONTENT OMITTED DUE TO DATA LENGTH]
                         ]         
                      }
        }
    }
}
```

# Appendices

**Table 1.** HTTP request data which can be included within the query posted to the web service.

 |Value|Description|Mandatory|Type|
 |---|---|---|---|
 | ```dataset```  | The name of the dataset to be queried by the web service |Yes|```string```|
 | ```attribute``` | One or more attributes of the dataset which can be used for filtering the results to be returned. The attributes specified must be from the fields in the dataset. A matchtype can also be specified. All comparisons are case-insensitive. For the attribute being specified, a name (of the field) and one or more values must be supplied. Multiple attributes are applied in turn to produce smaller sets of results to be returned (i.e. they are logically branded together). |No| ```AttributeType```|
 | ```area``` | This takes the name of a pre-loaded polygon which can be used to restrict results to items with a UPRN in a geographical area defined by that polygon.|No| ```string``` |
 | ```within``` | If this element is supplied then it must contain three sub-elements, an easting, a northing and a distance.  These elements define an area and only items with a UPRN in that area are returned.|No| ```WithinType``` |
 | ```sortField``` | This allows the results to be sorted on one of the fields from the dataset.  The value supplied for this must be one of the fields from the dataset.|No| ```string``` |
 |```sortOrder```| Applied to the ```sortField``` |No| ```SortOrderType``` |
 
 
**Table 2.** Definition of the ```AttributeType```

|Value|Type|Options|
|---|---|---|
| ```matchtype``` | ```string``` |```equal to (default)``` ```greater than``` ```greater than or equal to``` ```less than``` ```less than or equal to``` ```not equal to``` ```contains``` ```between``` ```in``` ```not in```|
| ```name``` | ```string``` ||
| ```value```| ```string``` ||


**Table 3.** Definition of the ```WithinType```

|Value|Type|Options|
|---|---|---|
|```easting``` | ```unsignedLong``` | ```0 - 500000``` |
|```northing``` | ```unsignedLong``` | ```500000 - 1300000``` |
|```distance``` | ```decimal``` ||

 
**Table 4.** Definition of the ```SortOrderType```

|Value|Type|Options|
|---|---|---|
| ```asc``` | ```string```||
| ```desc``` | ```string```||
 
 
**Table 5. HTTP response body:** Includes the data which are returned in the server's response body.

|Value|Description|Options|
|---|---|---|
|```ResultCount```|The number of data items found which match the query||
|```ReturnCount```|The number of data items returned by the web service (the minimum of ResultCount and 250)||
|```ErrorCode```|Zero for success or non-zero for failure (see later)| See "Error codes" table|
|```ErrorMessage```|A message describing an error which occurred (see later)| See "Error codes" table|
|```Result```|The data items matching the query.  The actual format will depend on the dataset being queried, but it will consist of a set of elements named the same as the dataset, each element containing an element for each field in the dataset (named the same as that field).||


**Table 6. HTTP response error codes:** Includes all the possible error codes returned by the server in the response body

The web service can return four possible error codes which are the following:

|Code|Explanation|Message(s)|
|---|---|---|
|```0```| Successful submission to the web service||
|```1```| Error with the data posted to the web service| ```Invalid Value - Schema validation error : <error msg>```|
|```2```| Issue was encountered during request processing (for example requesting a dataset which does not exist)| ```Invalid dataset [<dataset>]``` ```Invalid attribute name for dataset <dataset> [<attr_name>]``` ```<attr_name>: Invalid Date [<value>] expected format YYYY-MM-DD``` ```<attr_name>: Invalid Number [<value>]``` ```Invalid area [<area>]``` ```The dataset <dataset> does not support filtering on area``` ```polygon (<area>) awaiting initial index build - please try again later``` ```Invalid sort_field for dataset <dataset> [<sort_field>]```|
|```3```| Authentication/authorisation error|```Invalid Username/Password``` ```The address your computer is accessing this site from (xxx.xxx.xxx.xxx) has been blocked due to excessive failed login attempts. To have this block removed, please contact <contact email>. Alternatively, the block will be automatically removed in two hours time``` ```An unknown login failure occurred. The administrators have been notified of the event``` ```You do not have permission to use this service``` ```Missing authentication header in soap request```|