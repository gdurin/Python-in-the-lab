"""
Script to load info
of students from a cvs database
"""
import os
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import webbrowser

def cds_polito(fname):
    """
    get the Names of the Departments at Politecnico
    given as short name, long name
    """
    cds = dict()
    with open(fname) as f:
        data = f.readlines()
    for row in data:
        # Split only using the first comma
        s, l = row.split(",", 1)
        # Populate the dict
        cds[s] = l.strip() # Clean the spaces
    return cds

class Classroom:
    """
    class to load a csv file
    containing a table of students
    
    It is a combination of semi-private methods like
    _get_student_info_by_*
    and a public one 
        get_student_info(tag)
    which accepts a tag as a number (id_code, matricola)
    and as a string (surname)
    """
    def __init__(self, csv_filename, cds_filename, cols=6):
        self.students = pd.read_csv(csv_filename, index_col=0, usecols=range(cols))
        self.surnames = list(self.students.COGNOME)
        self._id_codes = list(self.students.index)
        self._cds_polito = cds_polito(cds_filename)
        
    def _get_student_info_by_surname(self, surname):
        """
        returns a pandas dataframe
        with the students' infos
        based on the surname
        """
        # Surname are saves as Capital, so let's transform
        surname = surname.upper()
        if surname in self.surnames:
            # extract the student as a dataframe of pandas
            df = self.students[self.students.COGNOME == surname]
            return df
        else:
            print("Surname %s not in the list" % surname)
            return None
        # Can be done with try ... except ...

    def _get_student_info_by_id(self, id_code):
        """
        returns a pandas dataframe
        with the student' info
        based on id_code (Matricola)
        """
        return self.students.loc[id_code]

    def _get_student_info(self, tag=None):
        if not tag:
            print("Please give a id code or his/her surname")
            return
        else:
            return self._get_df_from_tag(tag)

    def get_student_info(self, tag=None):
        """
        Why two methods with the same name
        just one private?
        If we return a dataframe,
        pandas will plot it, 
        and this is what we do not want to
        """
        df = self._get_student_info(tag)
        if df is not None:
            print(df.to_string())
        return

    def _get_df_from_tag(self, tag):
        """
        get the pandas dataframe
        corresponding a tag (id_code or surname)

        tag: int or string (also as 'ALL')
        """
        if type(tag) == int and tag in self._id_codes:
            df = self._get_student_info_by_id(tag)
        elif type(tag) == str:
            tag = tag.upper() 
            if tag in self.surnames:
                df = self._get_student_info_by_surname(tag)
            elif tag == 'ALL':
                df = self.students
            else:
                df = None
                print("%s surname does not exist" % tag)
        else:
            print("There is a problem, check your input")
            df = None
        return df


    def get_students_cds(self, cds):
        cds_short = cds[:3]
        cds_long = self._cds_polito[cds_short]
        locations = self.students['CDS STUDENTE'] == cds
        st = sum(locations)
        # Can we adjust plural and singular?
        if st == 1:
            verb, stud = "is", ""
        else:
            verb, stud = "are", "s"
        print("There %s %i student%s from %s" % (verb, st, stud, cds_long))
        return st

    def get_student_photo(self, tag=None):
        """
        This method unfortunately works
        only if connected to the polito network
        """
        if not tag:
            print("Please provide some info")
            return
        df = self._get_student_info(tag)
        url = "https://didattica.polito.it/pls/portal30/sviluppo.foto_studente?p_matricola=%s" % df.name
        webbrowser.open(url)
        print("Browser opened")
        
    @property
    def cds(self):
        return set(self.students['CDS STUDENTE'])

class WinterClassroom(Classroom):
    """
    this is a subclass of Classroom
    where only the students attendind the winter edition
    are selected
    """
    def __init__(self, csv_filename, cds_filename, cols=6):
        Classroom.__init__(self, csv_filename, cds_filename, cols=cols)
        # Need to add mr.Botta to the database of the winter students
        #
        # Need selecting only the winter students
        is_winter = self.students.FREQUENZA == 'Winter'
        self.students = self.students[is_winter] 

    def get_student_photo(self, tag=None):
        print("Nothing this time")

    def plot_pie(self):
        """
        plot the distribution of CDS students in a pie
        see matplotlib documentation
        """
        pass

    def plot_bar(self):
        """
        plot the distribution of CDS students in a bar
        see matplotlib documentation
        """
        pass

    def write_emails(self):
        """
        write a students_emails.txt file with as
        <Surname Name> email;
        etc
        """
        pass

    def write_cds_id_sorted(self):
        """
        write a students_ids.txt file with as
        ***** cds1 ******
        id1 Surname1 Name1
        id2 Surname2 Name2
        .... 
        ***** cds2 ******
        idx Surnamex Namex
        etc
        with cds and Surnames sorted
        """
        pass

    def write_cds_surnames_sorted(self):
        """
        write a students_surnames.txt file with as
        ***** cds1 ******
        Surname1 Name1 id1
        Surname2 Name2 id2
        .... 
        ***** cds2 ******
        Surnamex Namex idx
        etc
        with cds and Surnames sorted
        """
        pass

    def my_group(self):
        """
        returns a df with the students of the group
        """

if __name__ == "__main__":
    csv_file = "01RONKG_2019.csv"
    cds_file ='phds.txt'
    cl = WinterClassroom(csv_file, cds_file)
    for c in sorted(cl.cds):
        cl.get_students_cds(c)

