########################################################################################################################
###The purpose of this script is to download the most recent file from the OSG FTP using FTPES (i.e. FTP over Explicit#
###TLS). The output of the script is the filename downloaded.
########################################################################################################################

from datetime import datetime
import ftp_helpers as fth
import configuration
import csv

class DownloadNationalExtract(configuration.Conf):

    ftpes = fth.ExplicitTLS()

    def __init__(self):

        configuration.Conf.__init__(self)

    def establish_secure_authenticated_connection_to_ftp(self):

        self.ftpes.setup()
        self.ftpes.connect()

        return self.ftpes.login()

    def identify_most_recent_file_available_in_the_ftp_server(self,client):
        """(ftplib object) -> str
        Returns the 'SDTF' file which will be downloaded in the local machine for further processing.
        >>>identify_most_recent_file_available_in_the_ftp_server(obj)
        '9080_20180102_A_01_242.zip'
        >>>identify_most_recent_file_available_in_the_ftp_server(obj)
        None
        """

        #Change working directory to 'DOWNLOAD'. The OSG server includes two folders which the user can access;
        #UPLOAD or DOWNLOAD. In this case a national extract of OSG will be downloaded so the script will change
        #to DOWNLOAD.
        client.cwd('DOWNLOAD')

        #In a list of lists hold the extract datetime and the file name for each file in the FTP server within the DOWNLOAD
        #folder. Each nested list within the list represents the data for each file. An example of the output for the
        #file_dates list is: [[datetime.date(2018, 1, 2), '9080_20180102_A_01_242.zip'], [datetime.date(2018, 1, 9), \
        # '9080_20180109_A_01_242.zip'], [datetime.date(2018, 1, 16), '9080_20180116_A_01_242.zip'], \
        #[datetime.date(2018, 1, 23),'9080_20180123_A_01_242.zip'],[datetime.date(2018, 1, 30),'9080_20180130_A_01_242.zip'],\
        #[datetime.date(2018, 2, 6),'9080_20180206_A_01_242.zip'],[datetime.date(2018, 2, 13),'9080_20180213_A_01_242.zip']]
        #In the list only SDTF extracts are included (i.e. filename must include the substring '242'.
        files_dates = [[datetime.strptime(file_name.split('_')[1], '%Y%m%d').date(), file_name]\
                       for file_name in client.nlst() if '277' in file_name]

        #Identify the file which is the most recent using the files_dates list and return it as an output from this
        #function.
        most_recent_ftp_date = sorted(files_dates, key=lambda x: x[0], reverse=True)[0][0]

        #Collect the most recent date of data load in the metadata.log file which holds all the dates when data
        #were loaded in the database.
        with open(self.metadata_log, 'r', newline='\n', encoding='utf') as f:
            reader = csv.reader(f)
            reader.__next__()
            most_recent_loaded_date = max([datetime.strptime(item[0], '%Y%m%d').date() for item in reader])

        if most_recent_ftp_date > most_recent_loaded_date:
            result = [item[1] for item in files_dates if item[0] == most_recent_ftp_date][0]
        else:
            result = None

        return result

    def download_the_most_recent_file_using_the_ftp(self, client,file_name):

        #An FTP RETR command needs to be used to download the identified file.
        #The FTP RETR command is used to retrieve a copy of the file requested.
        retr_command = 'RETR %s' % file_name

        #This is where the file will be held.
        download_file = self.file_processing_folder + '\\' + file_name

        with open(download_file, 'wb') as f:
            client.retrbinary(retr_command, f.write)

        return file_name

def main():

    df = DownloadNationalExtract()
    client = df.establish_secure_authenticated_connection_to_ftp()
    file_name = df.identify_most_recent_file_available_in_the_ftp_server(client)
    if file_name is not None:
        filename = df.download_the_most_recent_file_using_the_ftp(client, file_name)
    else:
        filename = None

    print(filename)

if __name__ == "__main__":
    main()
