# one-scotland-gazetteer

#####The code in this repository makes the following assumptions:

**(A)** You have installed python 3.x in your operating system (OS)

**(B)** You have registered with the One Scotland Gazetteer (OSG) and can you are authorised to use the OSG web service
or the OSG FTP. To learn more please visit the [One Scotland Gazetteer](https://osg.scot) website.

#####To use the code, examples, and scripts in this repository please follow the instructions below:

**(A) Edit the ```configuration.py```:** In the root folder of this repository edit and and replace the values 
```"your-user"``` and ```"your-pass"``` with the credentials provided by the One Scotland Gazetteer custodian. 
Your username and password credentials may be different depending on FTP or WebServices access.

**(B)** Use the web services examples: 

```python /examples/web_services.py```

**(C)** Use the FTP functionality by running the following

```python /scripts/download_the_latest_osg_extract.py```

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


###Web services 
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
and raise a request. For example, an authorised user may have access to use the **search** web service 
(```sendNGSearchMessage```) to return the OSG data held in the fields of the ```EST_STANDARD_SEARCH``` dataset but not 
have access to ```ADDRESS_SEARCH```. The following REST example demonstrates an example of the request and response if
a user has access to the ```EST_STANDARD_SEARCH``` dataset and no access to the ```FVGIS_STANDARD_SEARCH``` dataset

Request data

```
{"query":{
    "dataset":"EST_STANDARD_SEARCH",
    "type":"full"
}}

```
Response body - authorised
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

Response body - not authorised

```
{
    "SearchResponseMessage":{
        "NGSearchResponseData":{
            "Header":{
                "ResultCount":0,
                "ReturnCount":0,
                "ErrorCode":3,
                "ErrorMessage":"You do not have permissions to use this service."
            },
            "Result":{
                   "any": 
                        null
                        }
        }
    }
}
```

**Query:** Querying the OSG data includes using the **search** web service and fields or/and geometries. The **search**
web service can receive the following inputs:


 |Input|Description|Values|
 |---|---|---|
 | ```dataset```  | The name of the dataset to be queried by the web service | ```equal to``` (default), ```greater than```, ```greater than or equal to```, ```less than```, ```less than or equal to```, ```not equal to```, ```contains```, ```between```, ```in```, ```not in```|
 | ```attribute``` | One or more attributes of the dataset which can be used for filtering the results to be returned. The attributes specified must be from the fields in the dataset. A matchtype can be specified (see below for list) with ‘equal to’ being the default.  All comparisons are case-insensitive. For the attribute being specified, a name (of the field) and one or more values must be supplied. Multiple attributes are applied in turn to produce smaller sets of results to be returned (i.e. they are logically anded together). ||
 | ```area``` | This takes the name of a pre-loaded polygon which can be used to restrict results to items with a UPRN in a geographical area defined by that polygon.||
 | ```within``` | If this element is supplied then it must contain three sub-elements, an easting, a northing and a distance.  These elements define an area and only items with a UPRN in that area are returned. ||
 | ```sortField``` | This allows the results to be sorted on one of the fields from the dataset.  The value supplied for this must be one of the fields from the dataset. ||
 |```sortOrder```| Applied to the ```sortField``` | ```asc``` (default), ```desc```|

