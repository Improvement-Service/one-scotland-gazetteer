# one-scotland-gazetteer

***The code in this repository has been fully tested using Python 3.6***

**Before using the examples and the scripts:** Edit the ```configuration.py``` found in the root folder of this 
repository and replace the values ```"your-user"``` and ```"your-pass"``` with the credentials provided by the One 
Scotland Gazetteer custodian. Your username and password credentials may be different depending on FTP or WebServices 
access.

**Explore Web Services functionality:** Run the web services examples: ```python /examples/web_services.py```

**Explore FTP functionality** Run the FTP script ```python /scripts/download_the_latest_osg_extract.py```

For additional information relating to the web services and the FTP usage visit [One Scotland Gazetteer](https://osg.scot)

# Documentation

**Overview:** 
This documentation provides information on the following "One Scotland Gazetteer" (OSG) functions:

**(1)** Web services; which allow access to the most recent data held in OSG through "Representational state transfer"
(REST) and "Simple Object Access Protocol" (SOAP). 

**(2)**  File Transfer Protocol Secure (FTPS); which allows uploading files to the OSG and downloading files from the 
OSG using the Scottish Data Trasfer Format (SDTF).


###Web services 
The OSG web services are structured around **datasets**, which contain **fields** which in turn contain the actual 
**data**. OSG has two web services ```sendNGListDataSetsMessage``` (henceforth **list**) which returns the datasets 
available for querying, and ```sendNGSearchMessage``` (henceforth **search**) which allows queries to be performed on 
those datasets. The maximum count of records returned by the OSG web services cannot exceed **250**. The services 
descriptions can be found at [REST](https://osg.scot/services/NGSearchServiceRest?_wadl) and 
[SOAP](https://osg.scot/services/NGSearchService?wsdl) respectively.

**Authentication:** All OSG web services require authentication. The authentication parameters should be provided in the
HTTP request headers for every request sent to the web service. An example of the authentication request headers for both 
REST and SOAP can be found below:

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

**Authorisation:** Authenticating with the OSG web service does not mean that you have access to all available datasets.
Access to datasets is administrated by the OSG custodian and if access is needed to additional datasets the users need
to contact the OSG custodian. For example, an authorised user may have access to use the **search** web service 
(```sendNGSearchMessage```) to return the OSG data held in the fields of the ```EST_STANDARD_SEARCH``` dataset as the 
following REST example:

```
Content-Type:application/json
Accept:application/json
username:Alice
password:secret
```
```
{"query":{
    "dataset":"EST_STANDARD_SEARCH",
    "type":"full"
}}
```

which will result in a ```200``` http status response code returning 250 records. The same user may not be able to 
return the OSG data held in the fields of the ```ADDRESS_SEARCH``` dataset if they are not authorised resulting to a 
```403``` http status response code.

**Query a dataset:** The OSG can be queried using the search web service either using **attributes queries** or 
**Spatial queries**. Attributes and spatial queries can also be combined in one web service query.



